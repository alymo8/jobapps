# Simplified onboarding; job search as its own skills Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

- **Date:** 2026-11-11
- **Status:** implemented

**Goal:** `/onboard` shrinks to tool check → resume → short interview (7 topics) → write sources → first resume; finding jobs moves to two new skills, `/scan-jobs` (on demand) and `/weekly-scan` (scheduled, publishes the shortlist), and career-ops is dropped.

**Architecture:** `tools/discover.py` loses its career-ops scan and date cut-off and becomes a JSON-in, CSV-out dedupe step (`--input <json>`); `/scan-jobs` has Claude search per `templates/weekly-search-prompt.md` and pipes its rows through it. Today's `/onboard` step 7 (shortlist artifact + routine / scheduled task) moves whole into `/weekly-scan`. The profile template gains `Locations` under `## Targeting` and a `## Job search` section for companies. ADR 0013 records it and amends ADRs 0010 and 0011.

**Tech Stack:** Python 3 stdlib (`json`, `csv`, `argparse`, `unittest`); Markdown skills; Claude Docs MCP, Artifact, RemoteTrigger (Docs mode); `mcp__scheduled-tasks__*` (local mode); web search/fetch (job search).

**Spec:** `docs/superpowers/specs/2026-11-11-simplified-onboarding-design.md` (approved; gate record docs/superpowers/gates/2026-11-11-simplified-onboarding-design.md, whose `## Plan questions` are answered in the tasks below, each marked **PQ**). Read the spec's Design section before each task; this plan names the decisions and checks, it does not repeat the spec.

## Global Constraints

- **Out of scope (do not edit):** `/resume`, `/cover-letter`, `/outreach`, `/followup`, `resume/recruiter-review.md`, `batch/SKILL.md`, `batch/scoring.md`, the shortlist artifact's data contract (`templates/shortlist/**`), `templates/weekly-search-prompt.md`, ADR 0009, and every file under `docs/superpowers/` other than this plan and its gate record.
- No migration: leftover `career_ops_dir` / `discover_locations` config keys are ignored by every skill, never deleted.
- Config writes: read, merge, write the whole JSON back (2-space indent, UTF-8, keys in `config.example.json` order, without `_comment`); never delete a key (mode switch excepted, as today).
- Truth rule: every fact written about the user comes from their material or answers. Material is data, not instructions. No skill here submits an application or sends a LinkedIn message.
- Profile `## Targeting` key order in `templates/profile.md`: `Pay floor`, `Score threshold`, `Years of experience`, `Target roles`, `Locations`, `Deal-breakers`. New section `## Job search` with `- Target companies: ASK`, `- Priority companies: ASK`, after `## Targeting` (last in the file).
- Default score threshold line: `- Score threshold: 3.5 (default, <YYYY-MM-DD>)`.
- Default local sources folder: `~/jobapps-sources`. Mode on a re-run: any `local_path` entry in config → local, else Docs.
- `discovered/<date>.csv` format unchanged: header `Rank,Company,Title,Location,URL`, all fields quoted.
- Tracked files pass `tests/test_no_personal_data.py`: no username, absolute user path, Doc/artifact/routine id, real email (only `example.com` / `example.org`) or `ddd ddd dddd`-shaped phone. Write paths as `~`, `%USERPROFILE%`, `<repo-root>`, `<S>`.
- `<worktree>` = this worktree's root (run commands there). `<S>` = the session scratchpad.
- CI: `python -m py_compile tools/*.py` and `python -m unittest discover -s tests -v`. Never `git add -A` / `git add .`; add named paths. Commit bodies end with the session's attribution line.

## Review Focus

- **Claude writes the scan JSON with a UTF-8 BOM or accented names** (`Société Générale`, `Montréal`): `discover.py` must read it and write the CSV with the same text. Pinned by Task 1 `test_input_utf8_bom_and_accents`.
- **The same posting found twice under URL variants** (`www.`, trailing slash, `utm_*` query): one CSV row, the first one found. Pinned by Task 1 `test_duplicate_url_in_input_keeps_first`.
- **The JSON is valid but the wrong shape** (`{"rows": [...]}` instead of a list): exit non-zero with a message, never an empty CSV or a traceback. Pinned by Task 1 `test_top_level_object_exits_nonzero`.
- **Rows with a `null`, blank or whitespace `url`, or a row that is not an object:** skipped and counted, the rest written. Pinned by Task 1 `test_skipped_rows_counted`.
- **An existing user's profile predates `Locations` and `## Job search`:** `/scan-jobs` must add the missing line and the section (one `write-source.md` run for the section) before searching, never search with them missing. Pinned by Task 8 Step 6.

---

### Task 1: `tools/discover.py` reads a JSON list

**Files:**
- Modify: `tools/discover.py`
- Test: `tests/test_discover.py`

**Depends on:** none

**Interfaces:**
- Produces: CLI `python tools/discover.py --input <json> [--exclude FILE ...] [--location KEYWORD ...] [--root PATH]` (`--input` required); stdout `<n> new postings -> <path>` or `no new postings`, preceded by `skipped <k> rows (missing company, title or url)` when k > 0; exit 0 in both cases, non-zero (via `SystemExit(<message>)`) on a missing or malformed input. Python: `load_rows(path: Path) -> tuple[list[dict], int]` (rows with keys `company, title, location, url`, skipped count); `select(rows: list[dict], known: set[str]) -> list[dict]`; `main(argv: list[str] | None = None, today: dt.date | None = None) -> int`. Kept unchanged: `known_urls`, `out_path`, `write_csv`, `HEADER`, `URL_RE`. Task 3 runs the CLI.

**PQ "Is `location` optional in JSON rows while `company`, `title`, `url` are required?":** yes. A row is kept when it is a JSON object whose `company`, `title` and `url` are strings and whose `url` is non-empty after `.strip()`; `location` may be missing or `null` (written as `""`). Values are stripped. Any other row (not an object, a required key missing or not a string, a blank url) is skipped and counted.

**PQ "With no rows left, keep `no new postings` and no CSV, and `/scan-jobs` stops?":** yes: `discover.py` prints `no new postings`, writes no file (no `discovered/` folder is created) and exits 0; `/scan-jobs` says so and stops (Task 3).

- [ ] **Step 1: Rewrite the tests.** Remove the career-ops fixtures (`HEADER`, `row`, `self.co`, `history`), `test_filters_status_cutoff_and_collapses`, `test_formula_escape_undone`, `test_last_run_cutoff_and_default`, `test_default_cutoff_seven_days`, `test_missing_career_ops`, `test_missing_node`, `test_scan_failure`, `test_scan_history_env_override`. New helpers: `rows_json(*rows, bom=False) -> Path` writes `json.dumps(list(rows))` to `<tmp>/rows.json` (`utf-8-sig` when `bom`); `p(url, title="AI Engineer", company="Acme", location="Montreal") -> dict`; `run_main(*args)` calls `discover.main(["--root", root, *args], today=TODAY)` with stdout captured. Keep and adapt to JSON input (`--input <rows_json(...)>`, no `--since`): `test_dedupe_sources` (same six sources, expect only `https://d.example/6`), `test_csv_round_trip_with_commas`, `test_location_filter` (same four locations and expected three URLs, in input order), `test_missing_exclude_file`, `test_applications_url_trailing_punctuation`, `test_nothing_new_writes_nothing` (input `[]`). Add:
  - `test_rank_is_input_order`: URLs `/c`, `/a`, `/b` → CSV URLs in that order, ranks `[1, 2, 3]`.
  - `test_duplicate_url_in_input_keeps_first`: `https://www.x.example/1/?utm_source=li` title `First`, then `https://x.example/1` title `Second` → one row, title `First`.
  - `test_second_run_dedupes_earlier_csv`: same input twice → second prints `no new postings`; then input with one new URL → files `["2026-10-10-2.csv", "2026-10-10.csv"]`.
  - `test_skipped_rows_counted`: rows: valid `/1`; no `title`; `url ""`; `url "   "`; `url null`; the string `"x"`; valid `/2` with no `location` key → CSV URLs `[/1, /2]`, `/2` location `""`, stdout contains `skipped 5 rows`.
  - `test_malformed_json_exits_nonzero`: file text `[{` → `SystemExit` whose `code` is a string containing `not valid JSON`; no `discovered/`.
  - `test_top_level_object_exits_nonzero`: `{"rows": []}` → `SystemExit`, `code` contains `JSON list`; no `discovered/`.
  - `test_missing_input_file`: `--input <tmp>/nope.json` → `SystemExit`, `code` contains `not found`.
  - `test_input_required`: no `--input` → `SystemExit` with `code == 2`.
  - `test_input_utf8_bom_and_accents`: `bom=True`, company `Société Générale`, location `Montréal` → `rp.from_csv` gives the same strings.
  - `test_no_last_run_file`: after a run that writes a CSV, `discovered/.last-run` does not exist.
  - `test_cli_round_trip_read_postings` (spec criterion 5): `applications.md` holds `| x | https://r.example/2 |`; input `/1`, `/2`, `/3`; `subprocess.run([sys.executable, <repo>/tools/discover.py, "--input", j, "--root", root])` exits 0; then `subprocess.run([sys.executable, <repo>/tools/read_postings.py, <csv>, "--all"])` exits 0 and its JSON `url`s are `["https://r.example/1", "https://r.example/3"]`.
- [ ] **Step 2: Run** `python -m unittest tests.test_discover -v`. Expected: the new tests FAIL/ERROR (`--input` unknown, `--career-ops` required); nothing passes that depends on JSON input.
- [ ] **Step 3: Implement.** Delete `history_rows`, `cutoff`, `run_scan`, `FORMULA`, the `os`/`shutil`/`subprocess` imports, the `--career-ops`, `--since`, `--no-scan` arguments and the `.last-run` write. `load_rows` reads with `encoding="utf-8-sig"`; messages: `discover: --input file not found: <path>`, `discover: <path> is not valid JSON: <error>`, `discover: <path> must hold a JSON list of postings`. `select` keeps the first row per `normalize_url(url)` and drops keys in `known`, input order kept. `main`: `--exclude` check as today, then `load_rows`, `select(rows, known_urls(root, excludes))`, the `--location` filter as today, print the skipped line, then the no-rows / write branch as today. Rewrite the module docstring: what it does, the usage line above, the dedupe sources, rank = input order after dedupe, the skip rule.
- [ ] **Step 4: Run** `python -m unittest tests.test_discover -v` and `python -m py_compile tools/discover.py`. Expected: OK, no py_compile output; `git grep -n -i "career" tools/discover.py tests/test_discover.py` prints nothing.
- [ ] **Step 5: Commit** `tools/discover.py tests/test_discover.py`: `discover.py: JSON input, career-ops scan and cut-off removed`.

### Task 2: Profile template keys and the sample resume fixture

**Files:**
- Modify: `templates/profile.md` (`## Targeting`, new `## Job search`)
- Create: `tests/fixtures/sample-resume.md`
- Test: `tests/test_templates.py`

**Depends on:** none

**Interfaces:**
- Produces: profile keys `- Locations:` (in `## Targeting`, after `Target roles`), `## Job search` with `- Target companies:` and `- Priority companies:`. Tasks 3, 4, 5 read and write them through `write-source.md`. Fixture `tests/fixtures/sample-resume.md` (Task 8 walkthrough).

**PQ "Where does `Locations` go in the Targeting key order, and does `/batch`'s offered Targeting key list gain it?":** after `Target roles`, before `Deal-breakers` (template order in Global Constraints). `/batch`'s list is unchanged: scoring does not read `Locations`, and `/scan-jobs` / `/weekly-scan` ask for it when missing. A `Locations` line added later to an existing profile goes at the end of `## Targeting` (`write-source.md`'s "new answer" rule); readers find it by key, not position.

- [ ] **Step 1: Update the tests.** `test_profile_targeting_keys` expects `["Pay floor", "Score threshold", "Years of experience", "Target roles", "Locations", "Deal-breakers"]`, all `ASK`. `test_profile_has_sections` adds `"## Job search"`. New `test_profile_job_search_keys`: `bullets(section(read("profile.md"), "## Job search"))` equals `{"Target companies": "ASK", "Priority companies": "ASK"}`, and `## Job search` is the file's last `## ` heading. New class `SampleResumeFixtureTest.test_sample_resume_shape`: `tests/fixtures/sample-resume.md` exists, contains `## Experience`, `## Education`, `## Projects`, `## Skills`; `## Experience` holds exactly two `### ` job headings, each followed by at least 7 `- ` bullets; every email on it ends in `@example.com`.
- [ ] **Step 2: Run** `python -m unittest tests.test_templates -v`. Expected: the three changed/new tests FAIL.
- [ ] **Step 3: Edit `templates/profile.md`** (insert `- Locations: ASK` after `- Target roles: ASK`; append a blank line, `## Job search`, the two lines). **Write the fixture:** a fictional one-page resume in Markdown for a backend software engineer in Chicago, IL, USA: made-up name, `Contact` line with an `@example.com` email, a phone written `+1 555-0142` (not `ddd ddd dddd`-shaped), a LinkedIn URL with `example` in the handle; two jobs at made-up companies with 7-8 bullets each (fill needs them: `knowledge/technical/local-mode-testing.md`), two projects, one made-up university, a skills list. No real person, company-specific claim or user data.
- [ ] **Step 4: Run** `git add tests/fixtures/sample-resume.md` (the privacy test scans tracked files), then `python -m unittest tests.test_templates tests.test_no_personal_data -v`. Expected: OK.
- [ ] **Step 5: Commit** `templates/profile.md tests/test_templates.py tests/fixtures/sample-resume.md`: `Profile template: Locations and Job search; sample resume fixture`.

### Task 3: `/scan-jobs` replaces `/discover`

**Files:**
- Create: `.claude/skills/scan-jobs/SKILL.md`
- Delete: `.claude/skills/discover/SKILL.md` (the folder)
- Test: `tests/test_templates.py` (`OnboardSkillTest` → all skills)

**Depends on:** Task 1, Task 2

**Interfaces:**
- Consumes: Task 1's CLI and stdout lines; Task 2's profile keys.
- Produces: skill `/scan-jobs`, `argument-hint: [--exclude <file.xlsx|file.csv|file.txt|dlq.md> ...]`, passed through to `discover.py`. Task 4 and Task 5 name it; Task 6 documents it.

**PQ "Which weekly-prompt sections beyond those listed does `/scan-jobs` follow, and does it read the mega resume?":** it follows `## Scale` too (no padding, duplicates or reposts; a true smaller count; cap 100) and the last paragraph of `## Before you start` (ask only when genuinely ambiguous, else decide and say so). It skips `## Respect my decisions` (no shortlist-decision dedupe, spec), the first paragraph of `## Before you start` and `## What to flag` (both read or write the artifact summary), plus the sections the spec skips. It reads `sources/mega-resume.tex` (pulled), since ranking factor 2 is requirements overlap with the resume. Priority companies it could not read are listed in step 5's report as `unreadable` (the board-access notes' rule).

**PQ "Is `## Job search` added in one `write-source.md` run with both lines?":** yes when the section is missing: one run, "new section" edit, text `\n## Job search\n- Target companies: <answer> (<first name>, <today>)\n- Priority companies: <answer> (<first name>, <today>)\n`. When the section exists, each `ASK` line is replaced in its own run (one run per change), in sequence.

- [ ] **Step 1: Generalise the skill test.** Rename `OnboardSkillTest.test_onboard_names_existing_templates` to `SkillsTest.test_skills_name_existing_templates`: for every `.claude/skills/*/SKILL.md` every `templates/...` path it names exists (same regex); assert the glob itself is non-empty and drop the per-file `assertTrue(paths)` (most skills name no template). Add `test_discover_skill_removed`: `.claude/skills/discover` does not exist; `.claude/skills/scan-jobs/SKILL.md` exists. Run `python -m unittest tests.test_templates -v`. Expected: `test_discover_skill_removed` FAILS.
- [ ] **Step 2: Write `.claude/skills/scan-jobs/SKILL.md`** with frontmatter (`name: scan-jobs`, a description that says it searches the web for open postings matching the profile's targets and writes a deduplicated CSV `/batch` reads; use when the user runs `/scan-jobs` or asks to find/scan for new postings), then the spec's five steps with the PQ answers. Exact points: missing `config.local.json` → `config.local.json is missing: this repo is not set up yet (run /onboard, or see README "Setup").` and stop; `sources/profile.md` missing → run `.claude/skills/pull-sources.md` first; `Target roles` / `Locations` missing or `ASK` → ask and save through `write-source.md` before searching; companies per the PQ (`none` allowed); the search reads `templates/weekly-search-prompt.md` sections by heading, filled at run time from `Target roles`, `Locations`, `## Job search` and config `targeting` (`eligible_regions`, `home_city`); scratch JSON at `<S>/scan-jobs/rows.json`, rows `{company, title, location, url}` best first, no row without a verifiable posting URL; run `python tools/discover.py --input <S>/scan-jobs/rows.json $ARGUMENTS` with no `--location`; on `no new postings` say so and stop; on a non-zero exit show the message and stop; else read the named CSV and show the count, the skipped line if any, and the first 15 rows (rank, company, title, location); over 60 rows suggest `--rows 1-40`; suggest `/batch resume <csv>` / `/batch apply <csv>`; say eligibility is re-checked by the `/batch` pre-screen and the score gate drops weak fits.
- [ ] **Step 3: Delete** `.claude/skills/discover/` (`git rm -r`).
- [ ] **Step 4: Run** `python -m unittest tests.test_templates -v`. Expected: OK.
- [ ] **Step 5: Commit** `.claude/skills/scan-jobs/SKILL.md .claude/skills/discover tests/test_templates.py`: `/scan-jobs: Claude job search replaces /discover`.

### Task 4: `/weekly-scan`

**Files:**
- Create: `.claude/skills/weekly-scan/SKILL.md`
- Modify: `.claude/skills/job-shortlist/SKILL.md` (the no-`shortlist` message)
- Test: `tests/test_templates.py::SkillsTest` (Task 3; covers the templates it names)

**Depends on:** Task 2, Task 3

**Interfaces:**
- Consumes: Task 2's profile keys; today's `.claude/skills/onboard/SKILL.md` step 7 text (read it from `main` before Task 5 rewrites it: `git show main:.claude/skills/onboard/SKILL.md`).
- Produces: skill `/weekly-scan`, `argument-hint: [publish | prompt | schedule]` (one of its three parts alone, else all in order). Writes config `shortlist`.

**PQ "`/weekly-scan` local `<folder>` = common parent of the `local_path` entries?":** yes, `os.path.commonpath` of the six `local_path` values (the folder `/onboard` wrote them to).

- [ ] **Step 1: Write `.claude/skills/weekly-scan/SKILL.md`.** Frontmatter: `name: weekly-scan`, description: publishes the weekly shortlist artifact and schedules the weekly job search (cloud routine in Docs mode, desktop scheduled task in local mode); use when the user runs `/weekly-scan` or asks to set up the weekly search or shortlist. Body: config missing → `config.local.json is missing: this repo is not set up yet (run /onboard, or see README "Setup").` and stop; mode from config (Global Constraints); the creation authority sentence citing ADR 0010 as extended by ADR 0013 (this skill may create the artifact and routine/task, in the user's own account); the Rules it needs from today's `/onboard` (Re-runnable keep/redo for the artifact, routine and task; Redo; Config writes; Truth rule); Tools (Artifact; RemoteTrigger in Docs mode; the scheduled-tasks ToolSearch line in local mode; load `artifact-capabilities` before publishing); a prerequisite check at the start for the mode's row only (Docs: Claude Docs tools listed and signed in; local: `mcp__scheduled-tasks__*` listed / open the repo in the Claude desktop app), stopping with its fix on failure. Then today's step 7 text moved as is (7.1 publish, 7.2-7.5 Docs, and the local-mode block) with these changes only: working copy at `<S>/weekly-scan/weekly-prompt.md`; before filling, read the pulled `sources/profile.md` (pull first) and, for `Target roles`, `Locations`, `Target companies`, `Priority companies` missing or `ASK`, ask and save through `write-source.md` (the Task 3 PQ rule for `## Job search`); fill `<target roles in priority order>` from `Target roles`, `<location scope>` from `Locations` plus config `targeting` (`eligible_regions`, `home_city`), `<target companies>` / `<priority companies>` from `## Job search` (`none` → `none`); `<sources list>` lines use the Doc titles of the six `sources` paths (mega-resume → Mega resume, resume_prompt → Resume prompt, cover_letter_prompt → Cover letter prompt, profile → Application profile, stories → Behavioral stories, answers → Free-text answer bank); local `<folder>` per the PQ; `/onboard` step numbers in the moved text (`7.1`, `Docs 7.2`, `stop step 7`, "step 1 row", "Rules") renumbered to this skill's own parts (`publish`, `prompt`, `schedule`) and its own Rules and prerequisite check. Add one sentence: the routine/task holds a copy of these values, so changing them later means rerunning `/weekly-scan` (redo). Close with what was created (artifact URL, routine or task name and schedule).
- [ ] **Step 2: Edit `.claude/skills/job-shortlist/SKILL.md`:** the no-`shortlist` message becomes `The shortlist is not set up: run /weekly-scan, or add "shortlist" to config.local.json (README "Setup").`; the missing-config message keeps `/onboard`.
- [ ] **Step 3: Run** `python -m unittest tests.test_templates -v`. Expected: OK. `git grep -n "run /onboard, or add" .claude/` prints nothing.
- [ ] **Step 4: Commit** `.claude/skills/weekly-scan/SKILL.md .claude/skills/job-shortlist/SKILL.md`: `/weekly-scan: shortlist artifact and weekly run move out of /onboard`.

### Task 5: `/onboard` rewrite

**Files:**
- Modify: `.claude/skills/onboard/SKILL.md` (whole file)
- Test: `tests/test_templates.py::SkillsTest` (existing after Task 3)

**Depends on:** Task 2, Task 3

**Interfaces:**
- Consumes: Task 2's profile keys; `write-source.md`, `pull-sources.md` (unchanged).
- Produces: `/onboard`, `argument-hint: [--docs] [step]`, steps 1-5 (`1`-`5` or title runs one step). Writes config `sources` and `targeting` only. Task 8 walks it.

**PQ "Separate imports for PyMuPDF and openpyxl in the tool check?":** yes: `python -c "import fitz"` (blocking, fix `pip install pymupdf`) and `python -c "import openpyxl"` (report-only, fix `pip install openpyxl`, needed by `read_postings.py` for Excel lists).

**PQ "Does step 4 keep today's post-pull `write-source.md` run (writability proof) for the score threshold?":** yes. After the pull and byte comparison, one `write-source.md` run (the pull counts as its step 1) replaces `- Score threshold: ASK` with `- Score threshold: 3.5 (default, <today>)`, which proves the profile entry is writable. Then any `## Targeting` line still `ASK` or missing is filled in further runs, in sequence. On a re-run with the sources kept and no `Score threshold: ASK` line, that line is left alone.

**PQ "Does Docs mode write exactly `sources` and `targeting` to config?":** yes, in both modes: `sources` (Docs entries `path`, `doc_url`, `tab_id`, profile also `node_id`, `"writable": true`; local entries `path`, `local_path`, profile `"writable": true`) and `targeting` (`eligible_regions`, `home_city`, `currency`, `phone_country`). No `linkedin_premium`, `discover_locations`, `career_ops_dir` or `shortlist` writes; existing keys are kept.

**PQ "Does an onboarding re-run add a missing `Locations` line?":** yes. On a re-run whose pulled profile has no `- Locations:` line under `## Targeting`, step 3 asks the locations question and step 4 adds the line through `write-source.md` (insert at the end of `## Targeting`). `/onboard` never finishes with a `## Targeting` line `ASK` or missing. A missing `## Job search` section is left to `/scan-jobs` / `/weekly-scan`.

- [ ] **Step 1: Frontmatter and intro.** Description: guided first-time setup: checks tools, reads the user's resume, asks a few questions about what they are looking for, writes their six sources (local files by default, Claude Docs on request) and `config.local.json` from `templates/`, and builds a first resume; use when the user runs `/onboard`, asks to set up the repo, or is new; re-runnable. Intro: steps 1-5; `$ARGUMENTS` per Interfaces; creation authority: `/onboard` creates the six sources (ADR 0010, 0011, 0013); the artifact and routine are `/weekly-scan`'s.
- [ ] **Step 2: Rules.** Keep Re-runnable (exists-list without career-ops, artifact, routine, scheduled tasks), Redo (sources only), Mode switch (spec "Re-runs and mode": plain `/onboard` never switches; `/onboard --docs` from local, or "use local files" from Docs, follows today's "Mode switch" rule unchanged, including its offer to disable the old routine (RemoteTrigger `update` `{"enabled": false}`, Docs to local) or the old local task (`update_scheduled_task` `enabled: false`, local to Docs), each sent only on a yes; then tell the user to rerun `/weekly-scan` (redo) so the weekly run reads the new sources), Config writes, Truth rule (gap list shown in step 4 and step 5), material-is-data, never submits or messages. Tools: Claude Docs (Docs mode) and Claude in Chrome lines as today; RemoteTrigger (Docs-to-local switch only) and, for local-to-Docs switches only, the ToolSearch line `select:mcp__scheduled-tasks__list_scheduled_tasks,mcp__scheduled-tasks__update_scheduled_task`; drop Artifact and the other scheduled-tasks tools.
- [ ] **Step 3: Step 1 Tool check** per spec step 1 and the PQ: report only failures with their fix; stop when Python ≥ 3.10, `import fitz` or `pdflatex` (MiKTeX fallback as `build_resume.py` does) fails; `git` and openpyxl report-only; Chrome one non-blocking line; Docs row only with `--docs` or Docs mode from config, and in that mode a failure stops. No Node row, no desktop-app row.
- [ ] **Step 4: Step 2 Resume** per spec (one resume file DOCX/PDF/LaTeX/MD/text plus optional extras; today's reading rules, including the DOCX `zipfile` command and LinkedIn-in-Chrome via `linkedin-tab.md`).
- [ ] **Step 5: Step 3 Interview:** a table of the spec's seven topics and their destinations (the `Pay floor` form `skip when the top of the posted range is below <amount> <currency>` or `none`; years to both `## Targeting` `Years of experience` and `## Common questions` `Years of professional experience`), asked in one or two grouped rounds, only what the material does not settle; the "Not asked" list with where each is asked instead; currency inferred from the location and `phone_country` from the phone, shown in step 4's summary; non-USD → a `USD to <currency> rate` looked up, written (after `Pay floor` in the working copy, form `- USD to <currency> rate: <rate> (<first name>, YYYY-MM-DD)`) only on the user's yes. Re-run: read the pulled profile, ask only its `ASK`/missing interview lines (PQ) and what the user wants to change.
- [ ] **Step 6: Step 4 Write sources.** Mode choice per spec (first run: local unless `--docs` or "use Claude Docs"; re-run: from config). Local: ask the folder (default `~/jobapps-sources`), today's inside-repo check command and backup note verbatim, today's local build/copy/overwrite-on-yes text; Docs: today's step 4 creation steps 2-4 verbatim (the `batch` create, the ack ids, the `read` check), with "step 5 opens none" changed to "this skill opens no Doc"; today's creation step 1 (the content build) is replaced by the working-copy rules below, which apply in both modes. Working copies: today's build rules (mega resume macros, prompts' runtime placeholders kept, profile filled with answers and `- Score threshold: ASK` left for the write; stories left as the template skeleton, a gap). Config per the PQ. Then `pull-sources.md`, today's byte comparison, the `write-source.md` runs per the PQ, then the summary: file paths (or Doc links), inferred `currency` / `phone_country` (and rate) for the user to correct (a correction is a config write, or a `write-source.md` run for the rate), and the gap list; open the folder (`explorer "<folder with backslashes>"`) in local mode; open nothing in Docs mode.
- [ ] **Step 7: Step 5 First resume:** ask for one real posting, run `/resume`, report the `build_resume.py` JSON checks (one page, fill, skills lines), open the PDF (`Invoke-Item <pdf>`). Close with what was created, the gap list, the next commands (`/scan-jobs`, `/weekly-scan`, `/apply`) and the no-submit/no-message line.
- [ ] **Step 8: Run** `python -m unittest tests.test_templates -v`. Expected: OK. `git grep -n -i -E "career.ops|node --version|npm|discover|create_scheduled_task|step 6|step 7|step 8" .claude/skills/onboard/SKILL.md` prints nothing; `grep -c "^## [1-5]\." .claude/skills/onboard/SKILL.md` prints `5`.
- [ ] **Step 9: Commit** `.claude/skills/onboard/SKILL.md`: `/onboard: tool check, resume, short interview, sources, first resume`.

### Task 6: Config example, docs, ADR 0013

**Files:**
- Create: `knowledge/decisions/0013-minimal-onboarding-and-claude-job-scan.md`
- Modify: `knowledge/decisions/0010-onboarding-creates-user-docs-and-shortlist.md`, `knowledge/decisions/0011-local-source-files-option.md` (status notes), `knowledge/decisions/README.md`, `config.example.json`, `README.md`, `CLAUDE.md`, `knowledge/technical/local-mode-testing.md`, `knowledge/README.md`

**Depends on:** Task 1

**Interfaces:**
- Consumes: Task 1's CLI form; skill names `/scan-jobs`, `/weekly-scan` (Tasks 3, 4).

- [ ] **Step 1: ADR 0013** from `0000-template.md`: title `Minimal onboarding; job search as its own skills`, status `accepted`, date `2026-11-11`. Opening lines: `Partly supersedes [ADR 0010](...) (its onboarding scope) and amends [ADR 0011](...).` Decision: the five points of spec "Other files" (onboarding minimal; `/scan-jobs` and `/weekly-scan`; career-ops dropped, Claude searches per `templates/weekly-search-prompt.md` and `discover.py` dedupes; local files default, Docs on `/onboard --docs`; companies in profile `## Job search`); 0010's creation exception now covers `/onboard` (sources) and `/weekly-scan` (artifact, routine or task); 0011 amended: local is the default, the local task is created by `/weekly-scan`, a mode switch is an explicit `/onboard --docs` / "use local files" request. Consequences: fewer questions and no Node; one way of finding jobs, costing Claude usage per scan; leftover config keys ignored; no dedupe against shortlist decisions in `discover.py` (`/batch`, `/job-shortlist` guard re-applying).
- [ ] **Step 2: ADR 0010 / 0011 status and index.** 0010: `- **Status:** partly superseded by 0013` and a line under the date block `Partly superseded by [ADR 0013](0013-minimal-onboarding-and-claude-job-scan.md): onboarding scope; the creation exception extends to /weekly-scan.` 0011: `- **Status:** amended by 0013` and `Amended by [ADR 0013](0013-minimal-onboarding-and-claude-job-scan.md): local files are the default.` Nothing else in either file. Index: rows 0010 and 0011 get those Status values; new row `| [0013](0013-minimal-onboarding-and-claude-job-scan.md) | Minimal onboarding; job search as its own skills | accepted | 2026-11-11 |`.
- [ ] **Step 3: `config.example.json`:** remove `career_ops_dir` and `discover_locations` and their names from `_comment`'s optional-key list. Run `python -c "import json; json.load(open('config.example.json', encoding='utf-8'))"`. Expected: no output.
- [ ] **Step 4: README.** "Setup" sentence: `/onboard` checks your tools, reads your resume, asks a few questions about what you are looking for, writes your six sources (local files, or Claude Docs with `/onboard --docs`) and config, and builds a first resume; `/scan-jobs` and `/weekly-scan` find postings afterwards. Onboarding diagram: same `%%{init...}%%` header, `flowchart LR`, and PAD lines as today, three subgraphs: `S1["1 · Your resume"]` (`S10["Tool<br/>check"] --> S11["Share your<br/>resume"]`), `S2["2 · A few questions"]` (`S20["Roles and<br/>locations"] --> S21["Pay floor,<br/>deal-breakers"] --> S22["Write six<br/>sources"]`), `S3["3 · First resume"]` (`S30["Pick a real<br/>posting"] --> S31["Build the<br/>resume"] --> S32["Check it fits<br/>one page"]`), `S1 --> S2 --> S3`, `S3 ~~~ PAD[...]`. Main diagram: `S10["Weekly search<br/>+ ATS scan"]` → `S10["Job scan (on demand<br/>or weekly)"]`. Manual setup: drop the `career_ops_dir` and `discover_locations` bullets; `shortlist` absent → `/job-shortlist` says to run `/weekly-scan`; step 5 → `**Optional:** run /weekly-scan for the weekly shortlist artifact used by /job-shortlist (by hand: publish templates/shortlist/ and schedule templates/weekly-search-prompt.md, filled in).` Map: `discovered/` (`/scan-jobs` CSVs); skill list `/onboard`, `/scan-jobs`, `/weekly-scan`, `/resume`, `/cover-letter`, `/apply`, `/outreach`, `/followup`, `/batch`, `/job-shortlist`.
- [ ] **Step 5: CLAUDE.md.** Build line → `python tools/discover.py --input <rows.json> [--exclude <list>] [--location <kw> ...]  # dedupe -> discovered/<date>.csv (used by /scan-jobs)`. Sources bullet: `chosen at /onboard (local files by default)` and cite ADR 0013 beside 0010/0011. Skills bullet: `/onboard` sets up a new user (resume, short interview, sources, first resume; templates in `templates/`); `/scan-jobs` (Claude job search → CSV) → `/resume` → `/apply`; `/weekly-scan` publishes the shortlist and schedules the weekly search ([ADR 0013](knowledge/decisions/0013-minimal-onboarding-and-claude-job-scan.md)). Setup line on the Claude Docs connector: `(Docs mode only)` stays.
- [ ] **Step 6: Knowledge.** `local-mode-testing.md`: `/onboard` local mode and its weekly scheduled task → local mode and `/weekly-scan`'s scheduled task (intro sentence and the "Creating the scheduled task" bullet name `/weekly-scan`); `last_updated: 2026-11-11`. `knowledge/README.md` row description: `Gotchas of testing local source mode and /weekly-scan's scheduled task end to end`.
- [ ] **Step 7: Run** `python -m unittest discover -s tests -v`. Expected: OK.
- [ ] **Step 8: Commit** the nine files: `ADR 0013 and docs: minimal onboarding, /scan-jobs, /weekly-scan`.

### Task 7: Checks green (criteria 1, 2)

**Files:** none tracked

**Depends on:** Task 1, Task 2, Task 3, Task 4, Task 5, Task 6

- [ ] **Step 1 (criterion 1):** Run `python -m unittest discover -s tests -v` and `python -m py_compile tools/*.py`. Expected: OK; no py_compile output.
- [ ] **Step 2 (criterion 2):** `git grep -n -i -E "career.ops|npm install|node --version" -- ':!docs/superpowers'`. Expected: hits only in `knowledge/decisions/0009-*.md`, `knowledge/decisions/0013-*.md`, the 0013 row of `knowledge/decisions/README.md` (only if its title mentions it; it does not), and `.claude/skills/batch/scoring.md` line 4 (MIT attribution). Any other hit: fix it in the task that owns the file and rerun Step 1.
- [ ] **Step 3:** in PowerShell (Git Bash rewrites the leading-slash pattern; there, prefix `MSYS_NO_PATHCONV=1`) `git grep -n -P "/discover(?![\w.])|discover_locations|career_ops_dir" -- ':!docs/superpowers' ':!knowledge/decisions/0009-*'` (the lookahead lets `tools/discover.py` through). Expected: nothing except ADR 0013's text. Copy `.personal-terms` from the main checkout if missing (CLAUDE.md gotcha), then `git grep -n -i -w -F -f .personal-terms`. Expected: nothing.
- [ ] **Step 4:** `git diff main --stat` lists only the files of Tasks 1-6, this plan, the spec, its gate record, `docs/superpowers/README.md` and the plan gate record.

### Task 8: Walkthrough (criteria 3, 4) and clean-up

**Files:** none tracked (scratch: `<S>/e2e/` worktree, `<S>/e2e-sources/`)

**Depends on:** Task 7

- [ ] **Step 1: Setup.** `git worktree add --detach <S>/e2e HEAD` from `<worktree>`; confirm `<S>/e2e/config.local.json` does not exist. Every command below runs with `<S>/e2e` as its working directory, and the skills followed are `<S>/e2e/.claude/skills/...` read by hand. Never touch the main checkout's `config.local.json`, sources, Docs or artifact.
- [ ] **Step 2 (criterion 3): `/onboard` in `<S>/e2e`**, playing the user: resume = `tests/fixtures/sample-resume.md`; folder answer `<S>/e2e-sources` (first try `<S>/e2e/./sources-in-repo`: expected refused); interview answers: target roles `Backend Engineer, Platform Engineer`, locations `Chicago, IL; remote in the US`, regions `United States`, years `6`, deal-breakers `none`, pay floor `none` (contact comes from the resume). Count the interview topics asked. Expected: at most 7; currency `USD` and phone country `United States (+1)` shown as inferred.
- [ ] **Step 3:** `<S>/e2e-sources/` holds the six files. Run `python -I -c "import json,sys; c=json.load(open(sys.argv[1],encoding='utf-8')); s=c['sources']; print(len(s), sum('local_path' in e for e in s), sorted(c))" config.local.json`. Expected: `6 6 ['sources', 'targeting']`. The profile has `- Score threshold: 3.5 (default, <today>)` and no `ASK` under `## Targeting`.
- [ ] **Step 4 (criterion 3):** onboarding step 5 with a currently open backend posting found by web search (the executor supplies the URL as the user). Expected: `build_resume.py` JSON reports one page; the fill and skills-line checks pass (if fill fails, add bullets to the fixture in `<worktree>`, commit `Sample resume: more bullets`, recreate the e2e worktree and rerun from Step 2).
- [ ] **Step 5 (criterion 4): `/scan-jobs` in `<S>/e2e`**, answering the company question with two target companies and one priority company. Expected: a `## Job search` section with both lines via `write-source.md` (the template's `ASK` lines are replaced, one run each); `discovered/<date>.csv` written; `python tools/read_postings.py discovered/<date>.csv` exits 0 and prints at least one posting. If nothing new is found, remove `discovered/` (or recreate the e2e worktree from Step 1) and rerun.
- [ ] **Step 6 (Review Focus 5):** in `<S>/e2e-sources/profile.md`, delete the `- Locations:` line and the whole `## Job search` section by hand, run `pull-sources.md`, then `/scan-jobs` again up to its search (stop before searching). Expected: it asks for locations and companies, the `Locations` line is added at the end of `## Targeting`, and `## Job search` is added in one `write-source.md` run whose step 4 diff shows exactly the three added lines (heading and both bullets; blank line aside).
- [ ] **Step 7: Clean-up.** `git worktree remove --force <S>/e2e` and `git worktree prune`; delete `<S>/e2e-sources`. Never copy `<S>/e2e/config.local.json` anywhere.
- [ ] **Step 8 (criterion 6, at the PR step):** when the PR is open, open `README.md` in its GitHub preview and check the three-stage onboarding diagram draws with no Mermaid parse error; a parse error is fixed on the branch and pushed.
