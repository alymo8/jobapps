"""Find new postings with career-ops' scanner and write them as a /batch target list.

Usage:
  python tools/discover.py [--career-ops PATH] [--since N] [--exclude FILE ...] [--no-scan]
                           [--location KEYWORD ...] [--root PATH]

Runs `node scan.mjs --quiet` in the career-ops checkout (--career-ops, else CAREER_OPS_DIR),
then reads its data/scan-history.tsv: rows with status `added` first seen on or after the
cut-off (--since N days, else the date in discovered/.last-run, else 7 days). Drops URLs
already in applications.md, dlq.md, postings/*/posting.md, earlier discovered/*.csv and every
--exclude file (compared with normalize_url). --location keeps rows whose location contains
one of the keywords (case-insensitive) or is empty. The history file is
CAREER_OPS_SCAN_HISTORY when set, else <career-ops>/data/scan-history.tsv. Writes discovered/<date>.csv
(Rank,Company,Title,Location,URL) for `/batch <mode> <csv>`. --root points at another
jobapps folder (tests, or running from a worktree).
"""

import argparse
import csv
import datetime as dt
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from read_postings import POSTING_URL, dlq_rows, normalize_url, read_source  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
HEADER = ["Rank", "Company", "Title", "Location", "URL"]
# career-ops stores a cell matching ^'*[=+\-@] with one extra leading "'" (lib/tsv-formula-escape.mjs).
FORMULA = re.compile(r"^'(?='*[=+\-@])")
URL_RE = re.compile(r"https?://[^\s|<>()\[\]]+")


def history_rows(path: Path) -> list[dict]:
    """scan-history.tsv rows by position (first 7 columns), formula escaping undone."""
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        cells = [FORMULA.sub("", c, count=1).strip() for c in line.split("\t")]
        if len(cells) < 7 or not cells[0].startswith("http"):
            continue
        try:
            day = dt.date.fromisoformat(cells[1])
        except ValueError:
            continue
        out.append(dict(url=cells[0], first_seen=day, title=cells[3], company=cells[4],
                        status=cells[5], location=cells[6]))  # fmt: skip
    return out


def cutoff(root: Path, since: int | None, today: dt.date) -> dt.date:
    if since is not None:
        return today - dt.timedelta(days=since)
    stamp = root / "discovered" / ".last-run"
    if stamp.exists():
        try:
            return dt.date.fromisoformat(stamp.read_text(encoding="utf-8").strip())
        except ValueError:
            pass
    return today - dt.timedelta(days=7)


def known_urls(root: Path, excludes: list[Path]) -> set[str]:
    """Normalized URLs that are already tracked, listed or excluded."""
    urls: set[str] = set()
    log = root / "applications.md"
    if log.exists():
        urls.update(u.rstrip(".,;:") for u in URL_RE.findall(log.read_text(encoding="utf-8")))
    urls.update(r["url"] for r in dlq_rows(root / "dlq.md"))
    for f in (root / "postings").glob("*/posting.md"):
        urls.update(POSTING_URL.findall(f.read_text(encoding="utf-8")))
    for f in (root / "discovered").glob("*.csv"):
        urls.update(x["url"] for x in read_source(f))
    for f in excludes:
        if f.name.lower() == "dlq.md":
            urls.update(r["url"] for r in dlq_rows(f))
        else:
            urls.update(x["url"] for x in read_source(f))
    return {normalize_url(u) for u in urls}


def select(rows: list[dict], since_day: dt.date, known: set[str]) -> list[dict]:
    """`added` (or empty-status) rows collapsed to the earliest per normalized URL, then kept when
    that earliest first_seen is on or after since_day and the URL isn't known; oldest first."""
    earliest: dict[str, dict] = {}
    for r in sorted(rows, key=lambda r: r["first_seen"]):
        if r["status"] in ("added", ""):
            earliest.setdefault(normalize_url(r["url"]), r)
    return [r for key, r in earliest.items() if r["first_seen"] >= since_day and key not in known]


def out_path(root: Path, today: dt.date) -> Path:
    path, n = root / "discovered" / f"{today.isoformat()}.csv", 2
    while path.exists():
        path, n = root / "discovered" / f"{today.isoformat()}-{n}.csv", n + 1
    return path


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, quoting=csv.QUOTE_ALL)
        w.writerow(HEADER)
        for i, r in enumerate(rows, start=1):
            w.writerow([i, r["company"], r["title"], r["location"], r["url"]])


def run_scan(career_ops: Path) -> None:
    node = shutil.which("node")
    if not node:
        raise SystemExit("discover: node not found on PATH")
    try:
        done = subprocess.run([node, "scan.mjs", "--quiet"], cwd=career_ops, timeout=600)
    except subprocess.TimeoutExpired:
        raise SystemExit("discover: scan.mjs timed out after 10 minutes") from None
    if done.returncode != 0:
        raise SystemExit(f"discover: scan.mjs exited {done.returncode}")


def main(argv: list[str] | None = None, today: dt.date | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--career-ops")
    ap.add_argument("--since", type=int)
    ap.add_argument("--exclude", action="extend", nargs="+", default=[])
    ap.add_argument("--no-scan", action="store_true")
    ap.add_argument("--location", action="extend", nargs="+", default=[])
    ap.add_argument("--root")
    args = ap.parse_args(argv)
    root = Path(args.root).resolve() if args.root else ROOT
    career_ops = args.career_ops or os.environ.get("CAREER_OPS_DIR")
    if not career_ops:
        raise SystemExit("discover: pass --career-ops PATH or set CAREER_OPS_DIR")
    career_ops = Path(career_ops)
    if not career_ops.is_dir():
        raise SystemExit(f"discover: career-ops folder not found: {career_ops}")
    excludes = [Path(x) for x in args.exclude]
    for f in excludes:
        if not f.is_file():
            raise SystemExit(f"discover: --exclude file not found: {f}")
    if not args.no_scan:
        run_scan(career_ops)
    history = Path(os.environ.get("CAREER_OPS_SCAN_HISTORY") or career_ops / "data" / "scan-history.tsv")
    if not history.exists():
        raise SystemExit(f"discover: no scan history at {history}")
    today = today or dt.date.today()
    rows = select(history_rows(history), cutoff(root, args.since, today), known_urls(root, excludes))
    if args.location:
        keys = [k.lower() for k in args.location]
        rows = [r for r in rows if not r["location"] or any(k in r["location"].lower() for k in keys)]
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if not rows:
        print("no new postings")
        return 0
    path = out_path(root, today)
    write_csv(path, rows)
    (root / "discovered" / ".last-run").write_text(today.isoformat() + "\n", encoding="utf-8")
    print(f"{len(rows)} new postings -> {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
