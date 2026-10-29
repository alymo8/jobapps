# Weekly job shortlist: data contract

Artifact: this artifact (the shortlist artifact; its URL is `shortlist.artifact_url` in the repo's `config.local.json`).
Schema version: 1. Fields can be added but are never renamed or removed.

## Published files (written by the weekly run, read-only for everyone else)

Read these with the Artifact tool: `action: "read"`, this artifact's `url`, and the file's `path`.

- `data/index.json`: `{schema_version, latest, weeks: [{week, json, csv, total, new}]}`. Newest week first. `json` can be null for weeks that only have a CSV. Before the first weekly run: `{"schema_version": 1, "latest": null, "weeks": []}`.
- `data/latest.json`: identical to the newest `data/<week>.json`. Before the first weekly run it is an empty week: `week`, `generated_at` and `baseline_compared` null, every count 0, `summary_md` "", and `rows`, `coverage` and `flags` empty.
- `data/<week>.json` contains:
  - `schema_version`, `week`, `generated_at`, `baseline_compared`.
  - `counts`: `total`, `ranked`, `below_cut`, `new`, `new_in_ranked`, `priority`, `province_restricted`, `unverified`, `likely_live`. Optionally also `hidden_applied` and `hidden_not_interested`.
  - `summary_md`.
  - `rows[]`: `rank`, `tab` (main|below_cut), `company`, `title`, `location`, `work_mode`, `company_type`, `priority` (Yes/No), `canada` (location eligibility: Confirmed | Confirmed (region-restricted) | Unverified; the name is kept), `new` (Yes/No), `status` (Open|Likely live), `deadline`, `fit_notes`, `url`, `score`.
  - `coverage[]`, `flags[]`.
- `data/<week>.csv`: `rank,tab,company,title,location,work_mode,company_type,priority,canada,new,url`.
- `data/decision_keys.py`: reference implementation of the key functions below. The page's JavaScript matches it exactly.

## Decisions (artifact database, collection `decisions`)

This collection is how postings get removed from future lists. Two parties write to it:

- The user, from the page, using the Applied / Not interested buttons. These are stored with `source: "user"`.
- Claude Code, when the user applies through it or says they're not interested. These are stored with `source: "claude_code"`.

The weekly run reads the collection and hides every matching posting from the next list.

**Document path:** `decisions/<doc_id>`, where `doc_id = "u-" + sha256(norm_url(url)).hexdigest()[:24]`. Writing the same posting twice overwrites one document, so writes are idempotent.

**Document body:**

```
{
  "schema_version": 1,
  "url": "<posting URL; copy it exactly from the shortlist row when the job came from there>",
  "url_norm": "<norm_url(url)>",
  "company": "<company as in the shortlist row, else as posted>",
  "title": "<exact posted title>",
  "match_key": "<norm_company(company) + '|' + norm_text(title)>",
  "decision": "applied" | "not_interested",
  "source": "user" | "claude_code",
  "decided_at": "<ISO 8601 timestamp>",
  "week_seen": "<shortlist week the row came from, or \"\" if not from the shortlist>",
  "note": "<optional free text, e.g. 'tailored resume v3, cover letter sent' or 'too senior'>"
}
```

**How the weekly run matches decisions.** A posting is hidden from every future list if EITHER of these holds:

1. `norm_url(posting.url)` equals a decision's `url_norm`.
2. `match_key(posting.company, posting.title)` equals a decision's `match_key`. This catches the same role reposted under a different URL, or found on Built In instead of the ATS.

An "Undo" on the page deletes the document, and the posting can then appear again.

**Normalization** (see `data/decision_keys.py`):

- `norm_url`:
  - Lowercase the host and drop a leading `www.`.
  - Strip trailing `/` from the path.
  - Keep the query string unchanged, because `?gh_jid=` identifies some jobs.
  - Drop the scheme and the fragment.
- `norm_text`:
  - Remove `(...)`.
  - Apply NFKD and strip accents.
  - Lowercase.
  - Replace each run of non-`[a-z0-9]` characters with a single space, then trim.
- `norm_company`: apply `norm_text`, then drop trailing `inc, ltd, llc, corp, corporation, canada, group, co, the` (always keeping at least one word).
