"""Dedupe a JSON list of job postings and write the new ones as a /batch target list.

Usage:
  python tools/discover.py --input <json> [--exclude FILE ...] [--location KEYWORD ...] [--root PATH]

--input is a JSON list of postings, each an object with `company`, `title`, `url` and an
optional `location` (read as UTF-8, a BOM allowed). A row is kept when `company`, `title` and
`url` are strings and `url` is non-empty after stripping; `location` may be missing or null.
Any other row (not an object, a required key missing or not a string, a blank url) is skipped
and counted. Drops URLs already in applications.md, dlq.md, postings/*/posting.md, earlier
discovered/*.csv and every --exclude file, and repeats within the input (the first one is kept),
all compared with normalize_url. --location keeps rows whose location contains one of the
keywords (case-insensitive) or is empty. Rank is the input order after dedupe. Writes
discovered/<date>.csv (Rank,Company,Title,Location,URL) for `/batch <mode> <csv>`; with no new
rows, prints `no new postings` and writes nothing. --root points at another jobapps folder
(tests, or running from a worktree).
"""

import argparse
import csv
import datetime as dt
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from read_postings import POSTING_URL, dlq_rows, normalize_url, read_source  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
HEADER = ["Rank", "Company", "Title", "Location", "URL"]
URL_RE = re.compile(r"https?://[^\s|<>()\[\]]+")


def load_rows(path: Path) -> tuple[list[dict], int]:
    """Valid posting rows from the --input JSON list (values stripped) and the skipped count."""
    if not path.is_file():
        raise SystemExit(f"discover: --input file not found: {path}")
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        raise SystemExit(f"discover: {path} is not valid JSON: {e}") from None
    if not isinstance(data, list):
        raise SystemExit(f"discover: {path} must hold a JSON list of postings")
    rows, skipped = [], 0
    for item in data:
        if not isinstance(item, dict) or not all(
            isinstance(item.get(k), str) for k in ("company", "title", "url")
        ) or not item["url"].strip():
            skipped += 1
            continue
        loc = item.get("location")
        rows.append(dict(company=item["company"].strip(), title=item["title"].strip(),
                         location=loc.strip() if isinstance(loc, str) else "",
                         url=item["url"].strip()))  # fmt: skip
    return rows, skipped


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


def select(rows: list[dict], known: set[str]) -> list[dict]:
    """The first row per normalized URL, minus URLs in known; input order kept."""
    seen: dict[str, dict] = {}
    for r in rows:
        seen.setdefault(normalize_url(r["url"]), r)
    return [r for key, r in seen.items() if key not in known]


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


def main(argv: list[str] | None = None, today: dt.date | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--input", required=True)
    ap.add_argument("--exclude", action="extend", nargs="+", default=[])
    ap.add_argument("--location", action="extend", nargs="+", default=[])
    ap.add_argument("--root")
    args = ap.parse_args(argv)
    root = Path(args.root).resolve() if args.root else ROOT
    excludes = [Path(x) for x in args.exclude]
    for f in excludes:
        if not f.is_file():
            raise SystemExit(f"discover: --exclude file not found: {f}")
    rows, skipped = load_rows(Path(args.input))
    today = today or dt.date.today()
    rows = select(rows, known_urls(root, excludes))
    if args.location:
        keys = [k.lower() for k in args.location]
        rows = [r for r in rows if not r["location"] or any(k in r["location"].lower() for k in keys)]
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if skipped:
        print(f"skipped {skipped} rows (missing company, title or url)")
    if not rows:
        print("no new postings")
        return 0
    path = out_path(root, today)
    write_csv(path, rows)
    print(f"{len(rows)} new postings -> {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
