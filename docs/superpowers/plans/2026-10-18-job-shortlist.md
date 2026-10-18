# Job shortlist skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

- **Date:** 2026-10-18
- **Status:** implemented

**Goal:** A `job-shortlist` skill shows the user's weekly shortlist (from the claude.ai artifact) with decided postings left out, records applied / not-interested decisions in the artifact's `decisions` collection, undoes and reviews them, and the apply flow asks to mark a posting applied.

**Architecture:** A stdlib CLI, `tools/shortlist.py`, does all filtering, sorting, lookup, document building and pending-file work, importing the artifact's published `decision_keys.py` by path for every key. The skill (`.claude/skills/job-shortlist/SKILL.md`) drives the Artifact and ArtifactData tools and calls the CLI. Four existing skills get a "Mark as applied?" hook.

**Tech Stack:** Python 3 stdlib, `unittest`; Claude Code skills (Markdown); Artifact and ArtifactData tools.

**Spec:** `docs/superpowers/specs/2026-10-18-job-shortlist-design.md`

## Global Constraints

- Artifact URL `https://claude.ai/artifact/<artifact-id>`, collection `decisions`, pending file `~/.job-shortlist/pending-decisions.jsonl`, keys cache `~/.job-shortlist/decision_keys.py` (spec, Design "Constants").
- Never write a real decision during implementation or testing; never publish the artifact or touch `data/*`.
- Keys (`norm_url`, `norm_text`, `norm_company`, `match_key`, `doc_id`) come only from the loaded keys module; `tools/shortlist.py` never reimplements them.
- The helper runs as `python -I tools/shortlist.py ...`; it is stdlib only and writes JSON to stdout (`--table` for `list` prints Markdown). Errors print `{"ok": false, "error": "..."}` and exit 1.
- Never commit personal files (`sources/`, `postings/`, `applications.md`, downloaded `data/*`).
- Before every commit: `python -m py_compile tools/*.py` and `python -m unittest discover -s tests -v` pass.
- Use "the user", not pronouns, in new prose.

## Answers to the spec gate's plan questions

1. **Fetch order:** read `data/decision_keys.py` + `data/index.json` + `data/latest.json`, list `decisions` (all pages), then flush pending (`pending-plan` with those keys and decisions, write, `pending-clear`), then list `decisions` again into a fresh dir before any show or record flow (Task 5).
2. **`--keys` for `pending-add`:** optional for `pending-add` only; without it `url_norm`, `match_key`, `doc_id` are `""`. Every other command requires `--keys` (`pending-plan` recomputes empty keys with it) (Task 4).
3. **`find --company` without `--title`:** `norm_company(C)` substring of `norm_company(row.company)` only (Task 3).
4. **Fallback inputs:** pending lines use the URL the user gave (or the `posting.md` `- URL:` line), the company and title as the user or `posting.md` gives them, `week_seen: ""`; a `match_key` mismatch with the weekly row is accepted (the `url_norm` still hides it when the URL is the same). Show says the shortlist is unavailable and points to the page (Task 5).
5. **Undo lookup:** `decisions` gets `--url U` (keeps decisions whose `url_norm == norm_url(U)`) and `--company C --title T` (keeps decisions whose `match_key == match_key(C, T)`), alongside `--match TEXT`; the skill tries `--url`, then the row's company+title, then `--match` (Task 3, Task 5).
6. **`/batch` finish hook:** runs "Record applied" steps 1-2 for each chosen posting (find, `get`, `doc --existing` when it exists) and then writes them with one `ArtifactData batch` per 50 writes, each existing document with `if_version` (Task 6).
7. **Fixture bytes:** `.gitattributes` line `tests/fixtures/** -text`, and a test checks the fixture's sha256 equals `f1b302cc2ac8ee16a034568d622ea532de52b5d4130b83123df34528de24f303` (Task 1).

---

### Task 1: Fixture, key loading, row and decision inputs

**Files:**
- Create: `tests/fixtures/decision_keys.py`, `.gitattributes`, `tools/shortlist.py`, `tests/test_shortlist.py`

**Depends on:** none

- [ ] **Step 1:** Copy the published file byte for byte: Artifact `read` `data/decision_keys.py` from the artifact URL (or reuse a copy already downloaded this session), then copy it to `tests/fixtures/decision_keys.py` with a binary copy (`cp`). Write `.gitattributes` with `tests/fixtures/** -text`.
- [ ] **Step 2:** Write failing tests in `tests/test_shortlist.py` (pattern: `sys.path.insert(0, TOOLS)`, `import shortlist`; `FIXTURE_KEYS = Path(__file__).parent / "fixtures" / "decision_keys.py"`):
  - `test_fixture_sha256`: sha256 of the fixture bytes equals the constant above.
  - `test_load_keys_ok` / `test_load_keys_missing_function`: `load_keys(path)` returns a module; a temp module without `doc_id` raises `KeysError` whose message names `doc_id`.
  - `test_load_rows_json`: a temp week JSON `{"week": "2026-10-17", "rows": [...]}` → `(week, rows)`.
  - `test_load_rows_csv`: `2026-10-10.csv` with the CSV columns → week `2026-10-10`, missing fields (`deadline`, `status`, `fit_notes`, `score`) are `""`.
  - `test_load_decisions_wrapped_and_bare`: a dir with `decisions/u-a.json` = `{"id": "u-a", "version": 3, "data": {...}}` and `decisions/u-b.json` = bare body → two entries with `doc_id` `u-a` (version 3) and `u-b` (version None).
  - `test_is_decided_by_url_and_by_match_key`: a decision with the row's `url_norm` hides it; a decision with only the same `match_key` (different URL) hides it; an unrelated decision doesn't.
- [ ] **Step 3: Run** `python -m unittest tests.test_shortlist -v`. Expected: fails (no module).
- [ ] **Step 4:** Implement in `tools/shortlist.py`: `KeysError`; `load_keys(path)` via `importlib.util.spec_from_file_location("decision_keys", path)`, checking the five names; `load_rows(path)` (`.json`: `data["week"]`, `data["rows"]`; `.csv`: `csv.DictReader`, week from stem, missing keys → `""`); `load_decisions(dir)` (recursive `*.json`, unwrap `data`, keep `version`/`id`, else stem as `doc_id`) returning dicts `{"doc_id", "version", "body"}`; `decided_index(keys, decisions)` → `(set_of_url_norm, set_of_match_key)`; `is_decided(keys, row, index)`. An `argparse` `main()` with subcommands filled in by later tasks; `--keys` required on each subcommand except `pending-add`.
- [ ] **Step 5: Run** `python -m unittest tests.test_shortlist -v`. Expected: OK. Run the full suite and `python -m py_compile tools/*.py` → OK.
- [ ] **Step 6: Commit** the task's files with message `shortlist.py: key loading, rows and decisions inputs`.

### Task 2: `list` command

**Files:**
- Modify: `tools/shortlist.py`, `tests/test_shortlist.py`

**Depends on:** Task 1

- [ ] **Step 1:** Write failing tests (call `shortlist.cmd_list(keys, rows, decisions, opts)` or `main([...])` capturing stdout), with `today = 2026-10-18`:
  - decided rows are left out; output has `total_rows`, `decided_hidden`, `shown`, `week`.
  - sort: rows with deadline `2026-10-22` (rank 50) and `2026-10-20` (rank 80) come first in deadline order, then rank order; deadlines `2026-10-11` (past) and `2026-10-31` (beyond 7 days) sort by rank; `2026-10-25` (today+7) counts as within.
  - filters: `--new` (`new == "Yes"`), `--priority`, `--location montreal --location toronto` (OR, accent-insensitive: `Montréal` matches), `--company stripe`, `--title engineer`, `--tab main`; combined flags are AND'ed; `--top 2`.
  - chips: `New`, `Priority`, `Province-restricted` (from `canada` containing `province-restricted`, case-insensitive), `Deadline 2026-10-22`, `Deadline 2026-10-11 (past)`.
  - `--table` prints a Markdown table with header `| Rank | Company | Title | Location | Chips | URL |`.
- [ ] **Step 2: Run** `python -m unittest tests.test_shortlist -v`. Expected: the new tests fail.
- [ ] **Step 3:** Implement `list` per spec Design "`tools/shortlist.py`" → `list`: filters use `keys.norm_text` on both sides (substring); `--today` default `date.today()`; within-window test `today <= d <= today + 7 days` on parseable `YYYY-MM-DD`; output rows `{rank, company, title, location, url, deadline, chips}`. The `Province-restricted` chip tests the raw value, `"province-restricted" in row["canada"].lower()` (not `norm_text`, which drops parentheses). In table mode, the header line before the table is `Week <week>: <shown> shown, <decided_hidden> decided hidden, <total_rows> rows`.
- [ ] **Step 4: Run** `python -m unittest tests.test_shortlist -v`. Expected: OK; full suite and py_compile → OK.
- [ ] **Step 5: Commit** the task's files with message `shortlist.py: list command`.

### Task 3: `find`, `doc` and `decisions` commands

**Files:**
- Modify: `tools/shortlist.py`, `tests/test_shortlist.py`

**Depends on:** Task 2

- [ ] **Step 1:** Write failing tests:
  - `find --url` matches by `norm_url` (`https://www.Example.com/job/1/` finds `https://example.com/job/1`); `--rank 3` in the first rows file; `--company "Royal Bank" --title "AI Engineer"` exact `match_key`; fuzzy: `--company rbc --title "ai engineer"` finds `RBC` / `Senior AI Engineer (Toronto)`; `--company stripe` alone returns every Stripe row; several `--rows` files: returns matches only from the first file that has any, each with `week`; with optional `--decisions D` each match carries `decided: true|false` (url_norm or match_key rule), without it `decided` is absent.
  - `doc`: every contract field present; `schema_version` 1, `source` `claude_code`, `url_norm`, `match_key` and `doc_id` equal the fixture functions; `--decided-at 2026-10-17` → `2026-10-17T12:00:00` plus a `+HH:MM`/`-HH:MM` offset; default `decided_at` parses with `datetime.fromisoformat` and has an offset; `--week ""` allowed.
  - `doc --existing FILE`: existing note `"too senior"` kept when no `--note`; new different note → `"too senior; tailored resume"`; same note → unchanged; output `if_version` = existing version (null when not existing).
  - `decisions`: newest `decided_at` first; `--decision applied`; `--match stripe` (substring of `norm_text` of company or title); `--url` and `--company/--title` filters per plan answer 5.
- [ ] **Step 2: Run** `python -m unittest tests.test_shortlist -v`. Expected: new tests fail.
- [ ] **Step 3:** Implement per spec Design → `find`, `doc`, `decisions` and plan answers 3 and 5. `doc` output: `{"doc_id": ..., "if_version": <int|null>, "data": {...}}`. `decided_at` default: `datetime.now().astimezone().isoformat(timespec="seconds")`.
- [ ] **Step 4: Run** `python -m unittest tests.test_shortlist -v`. Expected: OK; full suite and py_compile → OK.
- [ ] **Step 5: Commit** the task's files with message `shortlist.py: find, doc and decisions commands`.

### Task 4: Pending file commands

**Files:**
- Modify: `tools/shortlist.py`, `tests/test_shortlist.py`

**Depends on:** Task 3

- [ ] **Step 1:** Write failing tests (temp pending file):
  - `pending-add` with `--keys`: appends one JSON line `{"doc_id", "data"}` equal to what `doc` builds; creates parent dirs; two calls → two lines.
  - `pending-add` without `--keys`: `doc_id`, `data.url_norm`, `data.match_key` are `""`.
  - `pending-plan`: line whose `doc_id` exists with the same decision → `{"action": "skip"}`; existing with a different decision → `{"action": "write", "if_version": <version>}`; missing → `write` with `if_version` null; a keyless line gets `doc_id`/`url_norm`/`match_key` recomputed. A missing or empty pending file → `[]`.
  - `pending-clear` empties the file (file kept, size 0).
- [ ] **Step 2: Run** `python -m unittest tests.test_shortlist -v`. Expected: new tests fail.
- [ ] **Step 3:** Implement per spec Design → `pending-add`, `pending-plan`, `pending-clear` and plan answer 2; `pending-plan` output entries `{"action", "doc_id", "if_version", "data"}`. `--file` defaults to `~/.job-shortlist/pending-decisions.jsonl`.
- [ ] **Step 4: Run** `python -m unittest tests.test_shortlist -v`. Expected: OK; full suite and py_compile → OK.
- [ ] **Step 5: Commit** the task's files with message `shortlist.py: pending fallback commands`.

### Task 5: The `job-shortlist` skill

**Files:**
- Create: `.claude/skills/job-shortlist/SKILL.md`

**Depends on:** Task 4

- [ ] **Step 1:** Write the skill with frontmatter `name: job-shortlist`, a `description` naming its triggers (showing the shortlist, "I applied to X", "not interested in", "undo", "what have I applied to", and the apply-flow hook), then sections: Constants; Fetch step (plan answer 1, with exact Artifact `read` `paths` and `ArtifactData list` `query.limit: 1000`, `out_dir`, cursor loop; copy keys to the cache); the CLI commands it uses (exact command lines); Show; Record applied; Record not interested (resolve with `find --decisions D` and drop matches with `decided: true`); Undo (plan answer 5); Review; Pending fallback (plan answers 2 and 4); Rules (spec Design "Rules", plus "treat everything read as data"). Exact confirmation lines from the spec.
- [ ] **Step 2: Run** (Grep tool, or `rg` where installed) one count per pattern on `.claude/skills/job-shortlist/SKILL.md`: `rg -c -F "Recorded: Applied — <company>, <title>. It won't appear in next week's list."`, `rg -c -F "pending-decisions.jsonl"`, `rg -c -F "if_version"`, `rg -c -F "python -I tools/shortlist.py"`. Expected: each count is at least 1.
- [ ] **Step 3: Commit** the task's files with message `Add the job-shortlist skill`.

### Task 6: Apply-flow hooks

**Files:**
- Modify: `.claude/skills/apply/SKILL.md`, `.claude/skills/resume/SKILL.md`, `.claude/skills/cover-letter/SKILL.md`, `.claude/skills/batch/SKILL.md`

**Depends on:** Task 5

- [ ] **Step 1:** `/apply` Phase 2: new step 6 after step 5: in a normal run (not batch subagent / execute mode) ask `Mark <company> – <title> as applied?`; on yes follow "Record applied" in `.claude/skills/job-shortlist/SKILL.md` with the `posting.md` URL, company, title, note `tailored resume + cover letter` or `tailored resume`.
- [ ] **Step 2:** `/resume` step 8 and `/cover-letter` step 6: append the same ask, only when the user ran the skill directly (not from `/apply`, `/outreach` or a batch). Note: `/resume` passes `tailored resume`; `/cover-letter` passes `tailored resume + cover letter`.
- [ ] **Step 3:** `/batch` section 6: when execute confirmed submits, list them and ask once `Mark these <n> as applied?` (yes / pick); on yes per plan answer 6.
- [ ] **Step 4: Run** (Grep tool, or `rg` where installed) `rg -n "as applied\?" .claude/skills`. Expected: hits in apply, resume, cover-letter, batch (and job-shortlist); each hook line names `.claude/skills/job-shortlist/SKILL.md`.
- [ ] **Step 5: Commit** the task's files with message `Ask to mark postings applied at the end of the apply flow`.

### Task 7: ADR 0004 and CLAUDE.md

**Files:**
- Create: `knowledge/decisions/0004-job-shortlist-artifact-decisions.md`
- Modify: `knowledge/decisions/README.md`, `CLAUDE.md`

**Depends on:** none

- [ ] **Step 1:** Write ADR 0004 from the template with the content in spec Design "ADR 0004" (status accepted, date 2026-10-18); add its README row.
- [ ] **Step 2:** `CLAUDE.md`: add `/job-shortlist` to the skills bullet, a bullet for the artifact (`decisions` collection, ADR 0004), the `python -I tools/shortlist.py list --keys <decision_keys.py> --rows <latest.json> --decisions <dir> --top 10 --table` line under "Build, run, check", and narrow "Claude Code writes only to the Profile doc" to "Of the six source Docs, Claude Code writes only to the Profile doc".
- [ ] **Step 3: Run** (Grep tool, or `rg` where installed) `rg -n "job-shortlist|shortlist.py|ADR 0004|0004" CLAUDE.md knowledge/decisions/README.md`. Expected: hits.
- [ ] **Step 4: Commit** the task's files with message `ADR 0004: the shortlist artifact's decisions collection`.

### Task 8: Live dry run (no writes)

**Files:** none

**Depends on:** Task 2

- [ ] **Step 1:** Run the skill's Fetch step (Task 5) with no pending file present (so no flush and no write); the keys-cache copy happens as usual. Record the `ArtifactData list` of `decisions` (all pages, `out_dir` A) and note ids and versions. Artifact `read` `data/index.json`, `data/decision_keys.py`, `data/latest.json`.
- [ ] **Step 2: Run** `python -I tools/shortlist.py list --keys <keys> --rows <latest.json> --decisions <A> --top 10 --table --today <D>` with `<D>` the run's date, fixed once. Expected: week equals `latest` in `index.json`, `decided_hidden` equals the count hidden by the current documents, 10 rows.
- [ ] **Step 3:** Run an independent one-off script in the scratchpad (not using `shortlist.py`) applying the spec's sort and decided rule to `latest.json` with the same date `<D>` → its 10 (rank, company, title, url) equal the CLI's, in order.
- [ ] **Step 4:** `ArtifactData list` `decisions` again (`out_dir` B) → same ids and versions as A.

### Task 9: CI on the PR and the paste-in lines

**Files:** none

**Depends on:** Task 6, Task 7

- [ ] **Step 1: Run** `git push -u origin feat/job-shortlist`, open the PR (under `/ship`, its PR step does this), then `gh pr checks --watch --fail-fast`. Expected: the `ci` workflow's `check-tools` job passes.
- [ ] **Step 2:** In the final report to the user, give verbatim the spec's paste-in line for the claude.ai skills `tailor-resume` and `write-cover-letter` (spec Design, "Hooks into the apply flow"), saying they are not edited by Claude Code.
