"""List postings for /batch from an Excel target list, a text file, or URLs.

Usage:
  python tools/read_postings.py <file.xlsx|file.csv|file.txt|dlq.md|url> [url ...] [--rows 1-20,25]
                                [--new] [--all] [--reason BLOCKED]

Prints JSON: [{"rank", "company", "title", "location", "url", "eligibility", "flag",
"status", "dlq"}], where status is the posting's current row status in applications.md
("" if never seen) and dlq is its dead-letter reason ("" if none). By default postings
already `applied` or later, and postings in dlq.md (open, or closed/ineligible/dropped),
are skipped; --all keeps them. --rows filters by the sheet's Rank; --new keeps
"New This Week" = Yes. Excel: the "Postings" sheet (or the first sheet), header row with
a URL column; ranks listed on a "Flags & Exclusions" sheet get their reason in "flag".
CSV/TSV: same header names (delimiter and UTF-8/BOM/cp1252 detected); "flag" is empty.
Passing dlq.md as the source retries its `open` rows except CLOSED/INELIGIBLE/LOW-SCORE
(--reason selects exactly one reason, including those three).
"""

import csv
import io
import json
import re
import sys
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parent.parent
DONE = {"applied", "outreach-ready", "outreach-sent"}
DLQ = ROOT / "dlq.md"
DLQ_COLS = ["date", "batch", "rank", "company", "title", "url", "stage", "reason", "detail",
            "needs", "status"]  # fmt: skip
NEVER_RETRY = {"CLOSED", "INELIGIBLE", "LOW-SCORE"}
ALWAYS_HELD = {"CLOSED", "INELIGIBLE"}
# posting.md URL lines: "- URL: u" (current), "apply_url: u", "posting_url: u", "**Apply URL:** u".
POSTING_URL = re.compile(
    r"^(?:- URL:|apply_url:|posting_url:|\*\*Apply URL:\*\*)\s*(https?://\S+)", re.M | re.I
)


def dlq_rows(path: Path | None = None) -> list[dict]:
    path = path or DLQ
    if not path.exists():
        return []
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        cells = [x.strip() for x in line.strip().strip("|").split("|")]
        if len(cells) == len(DLQ_COLS) and cells[5].startswith("http"):
            out.append(dict(zip(DLQ_COLS, cells)))
    return out


def dlq_skip(row: dict) -> bool:
    """A DLQ row keeps its URL out of normal runs until resolved."""
    return row["status"] in ("open", "dropped") or row["reason"] in ALWAYS_HELD


def parse_rows(spec: str) -> set[int]:
    out: set[int] = set()
    for part in spec.split(","):
        a, _, b = part.partition("-")
        out.update(range(int(a), int(b or a) + 1))
    return out


def normalize_url(url: str) -> str:
    """Comparison key for a posting URL: https, lowercase host without `www.`, no fragment, no
    trailing slash, and no query string except `gh_jid` (Greenhouse job ids on career pages)."""
    parts = urlsplit(url.strip())
    host = parts.netloc.lower().removeprefix("www.")
    query = urlencode([(k, v) for k, v in parse_qsl(parts.query) if k == "gh_jid"])
    return urlunsplit(("https", host, parts.path.rstrip("/"), query, ""))


COLS = {
    "rank": ("rank", "#"),
    "company": ("company",),
    "title": ("title", "role"),
    "location": ("location",),
    "url": ("url", "link", "posting url"),
    "eligibility": ("canada eligibility", "eligibility"),
    "new": ("new this week",),
}


def from_table(rows: list, flags: dict[int, str] | None = None) -> list[dict]:
    """Postings from a header row + data rows (Excel and CSV readers)."""
    head = [str(h or "").strip().lower() for h in rows[0]]
    c = {k: next((head.index(n) for n in v if n in head), None) for k, v in COLS.items()}

    def cell(r, k):
        v = r[c[k]] if c[k] is not None and c[k] < len(r) else None
        return str(v).strip() if v not in (None, "") else ""

    out = []
    for i, r in enumerate(rows[1:], start=1):
        url = cell(r, "url")
        if not url:
            continue
        rank = int(float(cell(r, "rank"))) if cell(r, "rank") else i
        out.append(
            dict(
                rank=rank,
                company=cell(r, "company"),
                title=cell(r, "title"),
                location=cell(r, "location"),
                url=url,
                eligibility=cell(r, "eligibility"),
                new=cell(r, "new").lower() == "yes",
                flag=(flags or {}).get(rank, ""),
            )
        )
    return out


def from_xlsx(path: Path) -> list[dict]:
    import openpyxl

    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    ws = wb["Postings"] if "Postings" in wb.sheetnames else wb.worksheets[0]
    flags: dict[int, str] = {}
    for name in wb.sheetnames:
        if name.lower().startswith("flag"):
            section = ""
            for r in wb[name].iter_rows(values_only=True):
                first = r[0] if r else None
                if isinstance(first, str) and re.match(r"^\d+\.", first.strip()):
                    section = first.strip()
                # Only "unverified eligibility" rows flag a current rank; other
                # sections (e.g. last week's dropped ranks) reuse rank numbers.
                elif isinstance(first, (int, float)) and "unverified" in section.lower():
                    reason = " | ".join(str(x) for x in r[3:] if x)
                    flags[int(first)] = f"{section}: {reason}".strip(": ")
    return from_table(list(ws.iter_rows(values_only=True)), flags)


def from_csv(path: Path) -> list[dict]:
    """CSV/TSV target list: same header names as the Excel sheet, no flags."""
    raw = path.read_bytes()
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        text = raw.decode("cp1252")
    try:
        dialect = csv.Sniffer().sniff(text[:4096], delimiters=",;\t")
    except csv.Error:
        dialect = csv.excel_tab if path.suffix.lower() == ".tsv" else csv.excel
    rows = list(csv.reader(io.StringIO(text), dialect))
    return from_table(rows) if rows else []


def read_source(path: Path, start_rank: int = 1) -> list[dict]:
    """Postings of an xlsx, csv/tsv or txt target list; txt ranks count up from start_rank.
    dlq.md and bare URLs are handled in main()."""
    suffix = path.suffix.lower()
    if suffix in (".xlsx", ".xlsm"):
        return from_xlsx(path)
    if suffix in (".csv", ".tsv"):
        return from_csv(path)
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip().startswith("http"):
            out.append(dict(rank=start_rank + len(out), url=line.strip()))
    return out


def statuses() -> dict[str, str]:
    log = ROOT / "applications.md"
    if not log.exists():
        return {}
    out = {}
    for line in log.read_text(encoding="utf-8").splitlines():
        cells = [x.strip() for x in line.strip().strip("|").split("|")]
        if len(cells) >= 7 and cells[4].startswith("postings/"):
            out[cells[4]] = cells[5]
            url_m = re.search(r"https?://\S+", cells[6])
            if url_m:
                out[url_m.group(0)] = cells[5]
    return out


def main(argv: list[str]) -> None:
    args, rows, new_only, keep_all, reason = [], None, False, False, None
    it = iter(argv)
    for a in it:
        if a == "--rows":
            rows = parse_rows(next(it))
        elif a == "--reason":
            reason = next(it).upper()
        elif a == "--new":
            new_only = True
        elif a == "--all":
            keep_all = True
        else:
            args.append(a)
    postings: list[dict] = []
    from_dlq = False
    for a in args:
        p = Path(a)
        if p.name.lower() == "dlq.md":
            from_dlq = True
            for r in dlq_rows():
                wanted = r["reason"] == reason if reason else r["reason"] not in NEVER_RETRY
                if r["status"] == "open" and wanted:
                    rank = int(r["rank"]) if r["rank"].isdigit() else len(postings) + 1
                    postings.append(dict(rank=rank, company=r["company"], title=r["title"],
                                         url=r["url"], flag=""))  # fmt: skip
        elif a.startswith("http"):
            postings.append(dict(rank=len(postings) + 1, url=a))
        else:
            postings += read_source(p, start_rank=len(postings) + 1)
    if rows:
        postings = [x for x in postings if x["rank"] in rows]
    if new_only:
        postings = [x for x in postings if x.get("new")]
    # Posting dirs record their URL in posting.md; map URL -> status through them.
    st = statuses()
    for d in (ROOT / "postings").glob("*/posting.md"):
        rel = f"postings/{d.parent.name}"
        if rel in st:
            for u in POSTING_URL.findall(d.read_text(encoding="utf-8")):
                st[u] = st[rel]
    dlq = {r["url"]: r for r in dlq_rows()}
    for x in postings:
        x["status"] = st.get(x["url"], "")
        x["dlq"] = dlq[x["url"]]["reason"] if x["url"] in dlq else ""
    if not keep_all:
        postings = [x for x in postings if x["status"] not in DONE]
        if not from_dlq:
            postings = [x for x in postings if not (x["url"] in dlq and dlq_skip(dlq[x["url"]]))]
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(postings, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main(sys.argv[1:])
