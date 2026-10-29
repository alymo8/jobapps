"""Helper for the job-shortlist skill: the user's weekly shortlist artifact and its `decisions`.

Usage: python -I tools/shortlist.py <command> --keys <decision_keys.py> ...

Every key (norm_url, norm_text, norm_company, match_key, doc_id) comes from the artifact's
published data/decision_keys.py, downloaded by the skill and loaded here by path; this file
never computes keys another way. Inputs are files the skill saved with the Artifact and
ArtifactData tools; nothing here talks to the network. Output is JSON on stdout (`list --table`
prints Markdown). Errors print {"ok": false, "error": "..."} and exit 1.

Files ArtifactData saves with `out_dir` hold only the document body; its version appears only in
the tool's result text ("version N"). Writes to an existing document need that version, so `doc`
and `pending-plan` take it as `--version` and refuse to emit `if_version: null` for one.

Commands (see .claude/skills/job-shortlist/SKILL.md and the spec
docs/superpowers/specs/2026-10-18-job-shortlist-design.md):
  list            rows of one week, decided ones left out, deadlines in the next 7 days first
  find            rows matching a URL, a rank, or a company (+ title), newest week first
  doc             a decision document per the data contract, with its doc_id
  decisions       decision documents, newest first, filtered
  pending-add     append a decision to the pending file (used when the tools are unavailable)
  pending-plan    which pending decisions still need writing
  pending-clear   empty the pending file
"""

import argparse
import csv
import importlib.util
import json
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

KEY_FUNCTIONS = ("norm_url", "norm_text", "norm_company", "match_key", "doc_id")
DEFAULT_PENDING = Path.home() / ".job-shortlist" / "pending-decisions.jsonl"
ROW_FIELDS = ("rank", "tab", "company", "title", "location", "work_mode", "company_type",
              "priority", "canada", "new", "status", "deadline", "fit_notes", "url", "score")


class KeysError(Exception):
    pass


def load_keys(path):
    """Import the downloaded decision_keys.py by path and check it has the five key functions."""
    path = Path(path)
    if not path.is_file():
        raise KeysError(f"keys file not found: {path}")
    spec = importlib.util.spec_from_file_location("decision_keys", path)
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except KeyboardInterrupt:
        raise
    except BaseException as e:  # downloaded code: SyntaxError, ImportError, SystemExit, ...
        raise KeysError(f"{path} failed to load: {type(e).__name__}: {e}") from e
    missing = [name for name in KEY_FUNCTIONS if not callable(getattr(module, name, None))]
    if missing:
        raise KeysError(f"{path} lacks key function(s): {', '.join(missing)}")
    return module


def load_rows(path):
    """(week, rows) from a week .json (its `week` and `rows`) or a week .csv (week = file stem)."""
    path = Path(path)
    if path.suffix.lower() == ".csv":
        with path.open(encoding="utf-8", newline="") as f:
            rows = [dict(r) for r in csv.DictReader(f)]
        week = path.stem
    else:
        data = json.loads(path.read_text(encoding="utf-8"))
        week, rows = data.get("week") or path.stem, data.get("rows") or []
    out = []
    for r in rows:
        r = {k: r.get(k, "") if r.get(k) is not None else "" for k in set(ROW_FIELDS) | set(r)}
        if isinstance(r["rank"], str) and r["rank"].strip().isdigit():
            r["rank"] = int(r["rank"])
        out.append(r)
    return week, out


def load_decision_file(path):
    """{doc_id, version, body} from one saved decision, or None if it isn't a JSON object."""
    path = Path(path)
    try:
        obj = json.loads(path.read_text(encoding="utf-8"))
    except ValueError as e:
        print(f"warning: skipped unreadable decision file {path}: {e}", file=sys.stderr)
        return None
    if not isinstance(obj, dict):
        return None
    if isinstance(obj.get("data"), dict):
        return {"doc_id": obj.get("id") or path.stem, "version": obj.get("version"), "body": obj["data"]}
    return {"doc_id": path.stem, "version": obj.get("version"), "body": obj}


def load_decisions(directory):
    """Every decision file under `directory`: {doc_id, version, body}.

    A file holding {"data": {...}, "version": n, "id": ...} is unwrapped; any other object is the
    body itself and its doc_id is the file stem.
    """
    out = []
    directory = Path(directory)
    if not directory.is_dir():
        return out
    for p in sorted(directory.rglob("*.json")):
        decision = load_decision_file(p)
        if decision is not None:
            out.append(decision)
    return out


def decided_index(decisions):
    """(url_norms, match_keys) of the decisions, the two keys the weekly run hides postings by."""
    urls = {d["body"].get("url_norm") for d in decisions if d["body"].get("url_norm")}
    keys = {d["body"].get("match_key") for d in decisions if d["body"].get("match_key")}
    return urls, keys


def is_decided(keys, row, index):
    urls, match_keys = index
    return (keys.norm_url(row.get("url", "")) in urls
            or keys.match_key(row.get("company", ""), row.get("title", "")) in match_keys)


def parse_day(value):
    try:
        return date.fromisoformat(str(value).strip()[:10])
    except ValueError:
        return None


def chips(row, today):
    out = []
    if str(row.get("new", "")).lower() == "yes":
        out.append("New")
    if str(row.get("priority", "")).lower() == "yes":
        out.append("Priority")
    # Raw value on purpose: norm_text drops "(...)", which is where this flag lives.
    if "province-restricted" in str(row.get("canada", "")).lower():
        out.append("Province-restricted")
    day = parse_day(row.get("deadline", ""))
    if day:
        out.append(f"Deadline {day.isoformat()}" + (" (past)" if day < today else ""))
    return out


def rank_of(row):
    return row["rank"] if isinstance(row.get("rank"), int) else 10**9


def has_tokens(needle_text, haystack_text):
    """Whether the words of `needle_text` appear as a contiguous run of whole words in `haystack_text`."""
    needle, hay = needle_text.split(), haystack_text.split()
    return bool(needle) and any(hay[i:i + len(needle)] == needle for i in range(len(hay) - len(needle) + 1))


def contains(keys, haystack, needle):
    return keys.norm_text(needle) in keys.norm_text(str(haystack))


def cmd_list(keys, args):
    week, rows = load_rows(args.rows)
    index = decided_index(load_decisions(args.decisions))
    today = parse_day(args.today) if args.today else date.today()
    undecided = [r for r in rows if not is_decided(keys, r, index)]
    hidden = len(rows) - len(undecided)

    def keep(r):
        if args.tab != "all" and r.get("tab") != args.tab:
            return False
        if args.new and str(r.get("new", "")).lower() != "yes":
            return False
        if args.priority and str(r.get("priority", "")).lower() != "yes":
            return False
        if args.location and not any(contains(keys, r.get("location", ""), kw) for kw in args.location):
            return False
        if args.company and not contains(keys, r.get("company", ""), args.company):
            return False
        return not (args.title and not contains(keys, r.get("title", ""), args.title))

    def sort_key(r):
        day = parse_day(r.get("deadline", ""))
        if day and today <= day <= today + timedelta(days=7):
            return (0, day.toordinal(), rank_of(r))
        return (1, 0, rank_of(r))

    shown = sorted((r for r in undecided if keep(r)), key=sort_key)
    if args.top is not None:
        shown = shown[: args.top]
    out_rows = [{"rank": r.get("rank"), "company": r.get("company"), "title": r.get("title"),
                 "location": r.get("location"), "url": r.get("url"), "deadline": r.get("deadline", ""),
                 "chips": chips(r, today)} for r in shown]
    result = {"week": week, "total_rows": len(rows), "decided_hidden": hidden,
              "shown": len(out_rows), "rows": out_rows}
    if not args.table:
        return result
    cell = lambda s: str(s).replace("|", "\\|")  # noqa: E731
    lines = [f"Week {week}: {len(out_rows)} shown, {hidden} decided hidden, {len(rows)} rows", "",
             "| Rank | Company | Title | Location | Chips | URL |", "|---|---|---|---|---|---|"]
    lines += [f"| {r['rank']} | {cell(r['company'])} | {cell(r['title'])} | {cell(r['location'])} | "
              f"{cell(', '.join(r['chips']))} | {r['url']} |" for r in out_rows]
    return "\n".join(lines)


def cmd_find(keys, args):
    index = decided_index(load_decisions(args.decisions)) if args.decisions else None
    for path in args.rows:
        week, rows = load_rows(path)
        if args.url:
            target = keys.norm_url(args.url)
            matches = [r for r in rows if keys.norm_url(r.get("url", "")) == target]
        elif args.rank is not None:
            matches = [r for r in rows if r.get("rank") == args.rank] if path == args.rows[0] else []
        else:
            matches = []
            if args.title:
                target = keys.match_key(args.company, args.title)
                matches = [r for r in rows if keys.match_key(r.get("company", ""), r.get("title", "")) == target]
            if not matches:
                company = keys.norm_company(args.company)
                words = keys.norm_text(args.title or "").split()
                # Whole words only, so "okta" never matches "Brokta" (decisions are durable).
                matches = [r for r in rows
                           if has_tokens(company, keys.norm_company(r.get("company", "")))
                           and all(w in keys.norm_text(r.get("title", "")).split() for w in words)]
        if matches:
            out = []
            for r in matches:
                m = dict(r, week=week)
                if index is not None:
                    m["decided"] = is_decided(keys, r, index)
                out.append(m)
            return out
    return []


def decided_at(value):
    if not value:
        return datetime.now().astimezone().isoformat(timespec="seconds")
    if len(value) == 10:
        d = date.fromisoformat(value)
        return datetime(d.year, d.month, d.day, 12).astimezone().isoformat(timespec="seconds")
    return value


def build_doc(keys, args, existing=None, version=None):
    note = args.note or ""
    if existing is not None:
        note = merge_note(existing["body"].get("note"), note)
    data = {
        "schema_version": 1,
        "url": args.url,
        "url_norm": keys.norm_url(args.url) if keys else "",
        "company": args.company,
        "title": args.title,
        "match_key": keys.match_key(args.company, args.title) if keys else "",
        "decision": args.decision,
        "source": "claude_code",
        "decided_at": decided_at(args.decided_at),
        "week_seen": args.week,
        "note": note,
    }
    return {"doc_id": keys.doc_id(args.url) if keys else "",
            "if_version": version, "data": data}


def cmd_doc(keys, args):
    if not args.existing:
        if args.version is not None:
            raise ValueError("--version is only for an existing document; pass --existing too")
        return build_doc(keys, args)
    existing = load_decision_file(args.existing)
    if existing is None:
        raise ValueError(f"--existing {args.existing} is not a decision document")
    version = args.version if args.version is not None else existing["version"]
    if version is None:
        raise ValueError("the existing document's version is unknown (out_dir files hold no version): "
                         "pass --version N from the ArtifactData get result")
    return build_doc(keys, args, existing, version)


def sort_time(decision):
    try:
        t = datetime.fromisoformat(str(decision["body"].get("decided_at", "")))
        return t if t.tzinfo else t.astimezone()
    except ValueError:
        return datetime.min.replace(tzinfo=datetime.now().astimezone().tzinfo)


def cmd_decisions(keys, args):
    out = load_decisions(args.decisions)
    if args.decision:
        out = [d for d in out if d["body"].get("decision") == args.decision]
    if args.url:
        out = [d for d in out if d["body"].get("url_norm") == keys.norm_url(args.url)]
    if args.company and args.title:
        target = keys.match_key(args.company, args.title)
        out = [d for d in out if d["body"].get("match_key") == target]
    elif args.company:
        company = keys.norm_company(args.company)
        out = [d for d in out if has_tokens(company, keys.norm_company(d["body"].get("company", "")))]
    if args.match:
        out = [d for d in out if contains(keys, d["body"].get("company", ""), args.match)
               or contains(keys, d["body"].get("title", ""), args.match)]
    return sorted(out, key=sort_time, reverse=True)


def cmd_pending_add(keys, args):
    entry = build_doc(keys, args)
    entry.pop("if_version")
    path = Path(args.file)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return {"ok": True, "file": str(path), "doc_id": entry["doc_id"]}


def read_pending(path):
    path = Path(path)
    if not path.is_file():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def merge_note(old, new):
    old, new = old or "", new or ""
    if not new or new == old:
        return old
    return f"{old}; {new}" if old else new


def parse_versions(values):
    """{doc_id: version} from repeated `--version DOC_ID=N` flags."""
    out = {}
    for value in values or []:
        doc_id, sep, n = value.rpartition("=")
        if not sep or not doc_id or not n.strip().isdigit():
            raise ValueError(f"--version {value!r}: expected DOC_ID=N")
        out[doc_id] = int(n)
    return out


def cmd_pending_plan(keys, args):
    versions = parse_versions(args.version)
    existing = {d["doc_id"]: d for d in load_decisions(args.decisions)}
    latest = {}  # one write per document: the last pending line for a doc_id wins
    for entry in read_pending(args.file):
        data = dict(entry["data"])
        doc_id = entry.get("doc_id") or keys.doc_id(data["url"])
        data["url_norm"] = data.get("url_norm") or keys.norm_url(data["url"])
        data["match_key"] = data.get("match_key") or keys.match_key(data["company"], data["title"])
        latest.pop(doc_id, None)
        latest[doc_id] = data
    plan, unknown = [], []
    for doc_id, data in latest.items():
        current = existing.get(doc_id)
        version = versions.get(doc_id, current["version"]) if current else None
        if current:
            data["note"] = merge_note(current["body"].get("note"), data.get("note"))
        if current and current["body"].get("decision") == data["decision"]:
            plan.append({"action": "skip", "doc_id": doc_id, "if_version": version, "data": data})
        else:
            if current and version is None:
                unknown.append(doc_id)
            plan.append({"action": "write", "doc_id": doc_id, "if_version": version, "data": data})
    if unknown:
        raise ValueError("version unknown for existing document(s) " + ", ".join(unknown)
                         + ": pass --version DOC_ID=N for each, from the ArtifactData list or get result")
    return plan


def cmd_pending_clear(keys, args):
    path = Path(args.file)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("", encoding="utf-8")
    return {"ok": True, "file": str(path)}


def parser():
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = p.add_subparsers(dest="command", required=True)

    def add(name, keys_required=True):
        s = sub.add_parser(name)
        s.add_argument("--keys", required=keys_required, help="downloaded data/decision_keys.py")
        return s

    s = add("list")
    s.add_argument("--rows", required=True)
    s.add_argument("--decisions", required=True)
    s.add_argument("--top", type=int)
    s.add_argument("--new", action="store_true")
    s.add_argument("--priority", action="store_true")
    s.add_argument("--tab", choices=("main", "below_cut", "all"), default="all")
    s.add_argument("--location", action="append")
    s.add_argument("--company")
    s.add_argument("--title")
    s.add_argument("--today")
    s.add_argument("--table", action="store_true")

    s = add("find")
    s.add_argument("--rows", nargs="+", required=True, help="week files, newest first")
    s.add_argument("--decisions")
    g = s.add_mutually_exclusive_group(required=True)
    g.add_argument("--url")
    g.add_argument("--rank", type=int)
    g.add_argument("--company")
    s.add_argument("--title")

    for name in ("doc", "pending-add"):
        s = add(name, keys_required=name == "doc")
        s.add_argument("--url", required=True)
        s.add_argument("--company", required=True)
        s.add_argument("--title", required=True)
        s.add_argument("--decision", required=True, choices=("applied", "not_interested"))
        s.add_argument("--week", required=True)
        s.add_argument("--note")
        s.add_argument("--decided-at")
        if name == "doc":
            s.add_argument("--existing")
            s.add_argument("--version", type=int, help="the existing document's version (from the get result)")
        else:
            s.add_argument("--file", default=str(DEFAULT_PENDING))

    s = add("decisions")
    s.add_argument("--decisions", required=True)
    s.add_argument("--decision", choices=("applied", "not_interested"))
    s.add_argument("--url")
    s.add_argument("--company")
    s.add_argument("--title")
    s.add_argument("--match")

    s = add("pending-plan")
    s.add_argument("--file", default=str(DEFAULT_PENDING))
    s.add_argument("--decisions", required=True)
    s.add_argument("--version", action="append", metavar="DOC_ID=N",
                   help="an existing document's version (from the list or get result); repeatable")

    s = sub.add_parser("pending-clear")
    s.add_argument("--file", default=str(DEFAULT_PENDING))
    return p


COMMANDS = {"list": cmd_list, "find": cmd_find, "doc": cmd_doc, "decisions": cmd_decisions,
            "pending-add": cmd_pending_add, "pending-plan": cmd_pending_plan,
            "pending-clear": cmd_pending_clear}


def main(argv=None):
    args = parser().parse_args(argv)
    try:
        keys = load_keys(args.keys) if getattr(args, "keys", None) else None
        result = COMMANDS[args.command](keys, args)
    except (KeysError, OSError, ValueError, KeyError) as e:
        print(json.dumps({"ok": False, "error": f"{type(e).__name__}: {e}"}))
        return 1
    print(result if isinstance(result, str) else json.dumps(result, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
