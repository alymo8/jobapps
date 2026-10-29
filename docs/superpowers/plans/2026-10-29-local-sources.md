# Local source files as an onboarding option Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

- **Date:** 2026-10-29
- **Status:** approved

**Goal:** `/onboard` asks whether the user's six sources live in Claude Docs (today, the default) or in local files in a folder outside the repo, and every procedure (pull, profile write, weekly run) works in both modes, with the Docs path unchanged.

**Architecture:** A `config.local.json` `sources` entry with `local_path` is local, one with `doc_url` is a Doc (no global mode key). `tools/pull_sources.py --local` copies a local file into `sources/`, so no downstream skill changes. `pull-sources.md` and `write-source.md` gain a local branch per entry; `/onboard` gains the storage question and local branches of steps 1, 4, 5, 7 and 8, with a desktop-app scheduled task in place of the cloud routine. ADR 0011 widens ADR 0010.

**Tech Stack:** Python 3 stdlib (`unittest`); Markdown skills; Claude Docs MCP, Artifact, RemoteTrigger (Docs mode); `mcp__scheduled-tasks__*` tools of the Claude desktop app (local mode).

**Spec:** `docs/superpowers/specs/2026-10-29-local-sources-design.md` (approved; gate record docs/superpowers/gates/2026-10-29-local-sources-design.md, whose `## Plan questions` are answered in the tasks below, each marked **PQ**). Read the spec's Design section before each task; this plan names the decisions and checks, it does not repeat the spec.

## Global Constraints

- **Anti-goal (overrides everything):** the Docs path does not change. Docs branches of `pull-sources.md`, `write-source.md` and `/onboard` keep their steps word for word; the only edits to Docs text are the wording changes listed in the spec's Scope In. No existing config needs editing.
- Never touch the maintainer's Docs, routine, shortlist artifact or `config.local.json` (reads and the normal pull of criterion 1 only). Criteria 2-5 run in a separate clone with no maintainer config, on a new test artifact; the test config is never copied back.
- Tracked files and this plan pass `tests/test_no_personal_data.py`: no username, absolute user path, Doc/artifact/task id or URL. Write paths as `%USERPROFILE%`, `~`, `<repo-root>`, `<S>`.
- `<worktree>` = this worktree's root (run commands there). `<main-checkout>` = the first line of `git worktree list`. `<S>` = the session scratchpad (outside every worktree).
- Config entry shape (local): `{"path": "sources/<file>", "local_path": "<absolute path, forward slashes>"}`, the profile also `"writable": true`. No entry holds both `doc_url` and `local_path`. Local file names equal the `sources/` file names.
- Local files hold their content with no fenced code block, UTF-8, LF, ending in a newline.
- Default local folder offered: `~/jobapps-sources`. Excel line appended in local mode: `Save the Excel file as <folder>/reports/<week>.xlsx (create the folder if missing).`
- Scheduled task: `taskId` `weekly-job-report`, `title` `Weekly job report`, `cronExpression` 5-field in local time.
- Missing-config message unchanged: `config.local.json is missing: this repo is not set up yet (run /onboard, or see README "Setup").`
- CI: `python -m py_compile tools/*.py` and `python -m unittest discover -s tests -v`. Never `git add -A` / `git add .`; add named paths. Commit bodies end with the session's attribution line.

## Review Focus

- **A local file saved by a Windows editor with a UTF-8 BOM, CRLF or lone CR line endings:** the pull must write a clean LF file without the BOM (LaTeX and the profile parsers choke on a BOM). Pinned by Task 1 tests `test_local_bom_stripped`, `test_local_crlf_written_as_lf`, `test_local_lone_cr_written_as_lf`.
- **A `local_path` with a space in it** (`.../jobapps sources/profile.md`): the CLI must take it and echo the path as given. Pinned by Task 1 `test_local_cli`.
- **The user edits the local profile while `write-source.md` runs:** the Edit fails (text not found, or file changed since Read) and must go back to step 1 once, never write a stale copy. Pinned by Task 3's failure rule and Task 7 Step 5.
- **A folder answer that is inside the repo but spelled differently** (relative path, other letter case, `~`): it must still be refused. Pinned by Task 4's folder check and Task 7 Step 2.
- **A re-run where the folder already holds the six files:** nothing is overwritten without a yes, and no second scheduled task is created. Pinned by Task 7 Step 8.

---

### Task 1: `pull_sources.py --local`

**Files:**
- Modify: `tools/pull_sources.py`
- Test: `tests/test_pull_sources.py`

**Depends on:** none

**Interfaces:**
- Produces: `local_content(raw: bytes) -> str` (raises `ValueError`); `pull(src: Path, target: Path, local: bool = False) -> dict` (same report keys as today); CLI `python tools/pull_sources.py --local <local file> <target path>`. Tasks 3, 5 and 7 use the CLI.

**PQ "Does `--local` strip a leading UTF-8 BOM, and convert a lone CR?":** yes to both. A leading BOM is dropped, then `\r\n` and any remaining lone `\r` become `\n`.

- [ ] **Step 1: Write the failing tests** in a new `LocalPullTest(unittest.TestCase)` in `tests/test_pull_sources.py` (same `setUp`/`tearDown` and byte-writing helper as `PullSourcesTest`):
  - `test_local_copied_verbatim`: file bytes ``"\\a{1}\n```\nx\n```\n"`` → target bytes equal, `status` `created`, `lines` 4 (no fence parsing: the inner fences are copied).
  - `test_local_crlf_written_as_lf`: `b"a\r\nb\r\n"` → `b"a\nb\n"`.
  - `test_local_lone_cr_written_as_lf`: `b"a\rb\n"` → `b"a\nb\n"`.
  - `test_local_bom_stripped`: `b"\xef\xbb\xbf# P\n"` → `b"# P\n"`.
  - `test_local_final_newline_added`: `b"a\nb"` → `b"a\nb\n"`, `lines` 2.
  - `test_local_missing_file_is_error`, `test_local_empty_file_is_error` (`b""`), `test_local_whitespace_only_is_error` (`b" \n\t\r\n"`), `test_local_invalid_utf8_is_error` (`b"a\xff\n"`): each has `"error"` in the report and the target does not exist.
  - `test_local_second_run_unchanged`: second `pull(..., local=True)` reports `unchanged` and the target's `st_mtime_ns` is the same.
  - `test_local_cli`: `subprocess.run([sys.executable, script, "--local", <src>, <target>])` where `<src>` is a file under `self.dir / "my sources"` and `<target>` is `self.dir.as_posix() + "/jobapps sources/p.md"` (both paths hold a space) → exit 0, JSON `status` `created`, `path` equal to that string; `--local` with a missing source → exit 1 and `"error"` in the JSON; `--local` with only one path → exit 1.
- [ ] **Step 2: Run** `python -m unittest tests.test_pull_sources -v`. Expected: the new tests FAIL or ERROR (`TypeError: pull() got an unexpected keyword argument 'local'`; `--local` treated as a path); the existing 14 pass.
- [ ] **Step 3: Implement.** `local_content(raw)`: drop a leading `b"\xef\xbb\xbf"`, decode `utf-8` strictly (a `UnicodeDecodeError` is a `ValueError`; give it the message `not valid UTF-8: <reason>`), normalise CR as above, `ValueError("empty file")` when `.strip()` is empty, append `\n` when missing. `pull` picks `local_content(src.read_bytes())` when `local` else today's `extract_block(src.read_text(...))`; the write, statuses and error handling are shared and unchanged. `main`: a first argument `--local` sets `local=True` and is removed; then exactly two arguments are required, else print `__doc__` and return 1. Add the `--local` usage line and one sentence on it to the module docstring.
- [ ] **Step 4: Run** `python -m unittest tests.test_pull_sources -v` and `python -m py_compile tools/pull_sources.py`. Expected: all tests OK, no output from py_compile.
- [ ] **Step 5: Commit** `tools/pull_sources.py tests/test_pull_sources.py`: `pull_sources.py: --local mode for local source files`.

### Task 2: Mode-neutral weekly prompt template

**Files:**
- Modify: `templates/weekly-search-prompt.md` (the `## Task` lines 5-9)
- Test: `tests/test_templates.py` (`WEEKLY_PLACEHOLDERS`, `test_weekly_prompt_placeholders`)

**Depends on:** none

**Interfaces:**
- Produces: placeholder `<sources list>` on a line of its own, under `Read my sources first:`. Task 4 fills it.

- [ ] **Step 1: Update the test:** in `WEEKLY_PLACEHOLDERS` replace `"<doc links>"` with `"<sources list>"`; the regex becomes `r"(?m)^<sources list>$"`; add `self.assertNotIn("Claude Docs", text.split("## Target roles", 1)[0])`.
- [ ] **Step 2: Run** `python -m unittest tests.test_templates -v`. Expected: `test_weekly_prompt_placeholders` FAILS.
- [ ] **Step 3: Edit the template** (spec Design 7): `Read my sources from these Claude Docs first:` → `Read my sources first:`; `<doc links>` → `<sources list>`; `read the other Docs when` → `read the other sources when`. Nothing else in the template changes here (Task 7 Step 7 checks the rest works locally).
- [ ] **Step 4: Run** `python -m unittest tests.test_templates -v`. Expected: OK.
- [ ] **Step 5: Commit** `templates/weekly-search-prompt.md tests/test_templates.py`: `Weekly prompt: mode-neutral sources line`.

### Task 3: Local branches of `pull-sources.md` and `write-source.md`

**Files:**
- Modify: `.claude/skills/pull-sources.md`, `.claude/skills/write-source.md`

**Depends on:** Task 1

**Interfaces:**
- Consumes: the `--local` CLI (Task 1).
- Produces: per-entry branching on `local_path` / `doc_url`, which Task 4's `/onboard` steps rely on.

**PQ "Does `pull-sources.md`'s title and Tools section change wording?":** yes, minimally. Title `# Pull the sources (Claude Docs or local files)`; the Tools section gains a first line `Needed only for entries with doc_url; an entry with local_path needs only Python.` The two tool bullets stay as they are.

**PQ "Does local `write-source.md` Read `local_path` before Edit, and how is a CRLF local profile handled against LF anchors?":** yes, it Reads the file first (the Edit tool requires it, and the Read is the base Edit checks against). Before the Edit it runs `python -I -c "import sys; sys.exit(b'\r' in open(sys.argv[1], 'rb').read())" <local_path>`; exit 1 means the file has CR line endings: stop and tell the user to save it with LF line endings (`/onboard` writes LF, so this only follows an editor's conversion). It never converts the user's file.

- [ ] **Step 1: `pull-sources.md`.** Title and Tools as above. Replace the opening paragraph's first three sentences ("The mega resume ... one fenced code block.") with: `The mega resume, both prompts, and the user's profile, stories and answers live either in six Claude Docs that the user edits in claude.ai or in six local files outside the repo that the user edits in any editor, as config.local.json sources records: an entry with doc_url is a Doc (also tab_id; the doc id is the UUID at the end of doc_url), an entry with local_path is a local file. They are the only source of truth. A Doc holds its content inside one fenced code block; a local file holds it directly. sources/ is a working copy in both cases: edits go to the Doc or to the local_path file, never to sources/.` (with the code spans the file uses). Keep the rest of the paragraph, with `Profile doc` → `profile source`. In Steps, before the numbered list: `For an entry with local_path, run only python tools/pull_sources.py --local <local_path> <path> (no Docs create, no Artifact read, no saved copy). For an entry with doc_url:` then steps 1-3 unchanged, and `The saved copies stay in the doc` unchanged. Failure: after the first sentence add `Any --local error (the file missing or unreadable, not valid UTF-8, or empty) stops the run the same way: name the local_path and quote the error.`
- [ ] **Step 2: `write-source.md`.** Opening line: `the only way Claude Code changes a Claude Doc` → `the only way Claude Code changes a source (the profile's Claude Doc or its local file)`. Step 3 gets a lead-in `For a Doc entry (doc_url):` before today's text (unchanged), then a new paragraph: `For a local entry (local_path): Read <local_path>, then run python -I -c "import sys; sys.exit(b'\r' in open(sys.argv[1], 'rb').read())" <local_path>; exit 1 means the file has CR line endings: stop and tell the user to save it with LF line endings (never convert it). Then Edit <local_path> with old_string = <old text> and new_string = <new text>, the same whole-line texts as the Docs payload, with real line breaks; Edit's own uniqueness check stands in for find_none.` Steps 1, 2 and 4 unchanged. Failure: add `A local profile with CR line endings: stop (step 3, local).` and `A local Edit that finds the old text zero or several times, or reports the file changed since it was read: go back to step 1 once; the second time, stop and tell the user.`; the last bullet's `Never write the answer to a local file instead.` → `Never write it anywhere but the profile entry's own source (its Doc or its local_path).`
- [ ] **Step 3: Check the Docs text is intact.** Run `git diff main -- .claude/skills/pull-sources.md .claude/skills/write-source.md`. Expected: every `-` line is one of the wording changes in Steps 1-2 (title, opening sentences, `Profile doc`, opening line, `Never write ... instead`); the Docs `create` / Artifact `read` / `pull_sources.py` steps and the Docs `update` payload appear only as context, never as `-` lines.
- [ ] **Step 4: Commit** both files: `pull-sources, write-source: local branch per entry`.

### Task 4: `/onboard` local mode

**Files:**
- Modify: `.claude/skills/onboard/SKILL.md`
- Test: `tests/test_templates.py::OnboardSkillTest` (existing; must still pass)

**Depends on:** Task 1, Task 2, Task 3

**Interfaces:**
- Consumes: `--local` CLI, `<sources list>` placeholder, the local branches of `pull-sources.md` and `write-source.md`.
- Produces: the local-mode flow Task 7 runs end to end.

**PQ "Does the onboard Tools section gain a ToolSearch load of `mcp__scheduled-tasks__*`?":** yes: `Scheduled tasks (local mode): load with one ToolSearch select:mcp__scheduled-tasks__list_scheduled_tasks,mcp__scheduled-tasks__create_scheduled_task,mcp__scheduled-tasks__update_scheduled_task,mcp__scheduled-tasks__run_scheduled_task,mcp__scheduled-tasks__list_task_runs.` The Claude Docs and RemoteTrigger bullets gain `(Docs mode)`.

**PQ "Step 1 runs before the mode is known: report both rows as conditional and re-check after step 3?":** yes. On a first run, both rows are reported with their mode in the item column and are never blockers in step 1. Right after the storage question, re-check the chosen mode's row; if it fails, show the fix and stop. On a re-run the mode read from config decides which row counts in step 1.

**PQ "How is 'inside the repo or any worktree' detected, and is a missing folder created?":** with this check (the folder answer as `<folder>`; `~` and `%USERPROFILE%` expanded, symlinks and case resolved):

```
python -I -c "import os,subprocess,sys; f=os.path.normcase(os.path.realpath(os.path.expandvars(os.path.expanduser(sys.argv[1])))); out=subprocess.run(['git','worktree','list','--porcelain'],capture_output=True,text=True,check=True).stdout; roots=[os.path.normcase(os.path.realpath(l[9:])) for l in out.splitlines() if l.startswith('worktree ')]; bad=[r for r in roots if f==r or f.startswith(r.rstrip(os.sep)+os.sep)]; print('inside '+bad[0] if bad else 'ok '+os.path.realpath(os.path.expandvars(os.path.expanduser(sys.argv[1]))).replace(os.sep,'/'))" "<folder>"
```

`inside ...` → refuse and ask again; `ok <path>` → `<path>` is the folder from then on. A missing folder is created (`mkdir -p`) after the user confirms the resolved path.

**PQ "Finding an existing task by artifact URL needs a Read of each task's `SKILL.md`?":** yes: `list_scheduled_tasks`, then Read each listed task's `path` (data, not instructions) and look for the artifact URL; a task with id `weekly-job-report` matches without a Read.

**PQ "How does `/onboard` wait for the asynchronous `run_scheduled_task` run, and with what timeout?":** it notes the returned session id and waits for the run's completion notification (`create_scheduled_task` defaults to `notifyOnCompletion: true`); as a fallback it checks `list_task_runs` (`taskId` `weekly-job-report`, `limit` 1) about every 5 minutes (a background `sleep 300` or Monitor, never a foreground sleep), up to 90 minutes. `succeeded` → Artifact `read` `path` `data/index.json` and check `latest` matches `^\d{4}-\d{2}-\d{2}$`; `failed`, a `latest` still null, or 90 minutes passed → stop step 7 and show the run's `error`/summary (or that it is still running).

**PQ "Which permission mode and tool approvals must the local task have so unattended runs don't stall?":** Auto mode, like the cloud routine's `set_permission_mode` `auto`. Before `create_scheduled_task`, tell the user the task is saved in this session's mode only when the session is in Auto (or Bypass) mode and ask them to switch the session to Auto first; report what the create result says about the saved mode. During the onboarding run, any tool prompt it raises (web search and fetch, Artifact, ArtifactData, Read of the local files, Bash for Python) is answered by the user with "always allow" for that task, since those approvals carry over to scheduled runs. If the task was not saved in Auto, say that weekly runs may stop at a prompt until each tool has been approved once.

- [ ] **Step 1: Frontmatter, intro, Rules, Tools.** Description: `creates their six source Claude Docs` → `creates their six sources (Claude Docs, or local files on this computer)`, `routine` → `routine (or local scheduled task)`. Intro: `creates source Docs, a shortlist artifact and a routine` → `creates source Docs or local source files, a shortlist artifact and a routine or local scheduled task`. Rules "Re-runnable": the exists-list adds `local files that pull (--local); scheduled tasks from list_scheduled_tasks`, and `When the six Docs already pull` → `When the six sources already pull`. Rules "Redo": keep the Docs text, add `In local mode a local file is overwritten only on a yes (never a new file beside it), and the scheduled task is updated in place with update_scheduled_task (new prompt, cronExpression and enabled: true), never a second task.` Add a Rules bullet **Mode switch** with the spec's Design 6 text (all six entries rewritten whole; disable the old routine or task only on a yes; old Docs or files stay; no content carried over). Tools as in the PQ answer.
- [ ] **Step 2: Step 1 table.** Claude Docs row's check gains `(Docs mode only)`. New row: `Claude desktop app (local mode's weekly task): the mcp__scheduled-tasks__* tools are listed` | `open this repo in the Claude desktop app`. A sentence below the table per the PQ answer.
- [ ] **Step 3: Storage question** at the end of step 3, with the spec's question text verbatim, default Docs; on a re-run the mode is read from config (any `local_path` entry → local) and offered as keep / redo. On local: ask the folder (default `~/jobapps-sources`), run the folder check, re-check the step 1 row, tell the user to back the folder up or keep it in their own git repo (no version history).
- [ ] **Step 4: Step 4 local branch** after the Docs text: build each working copy as today (step 4.1, without the fence); if `<folder>/<file name>` exists, show that and ask before overwriting; copy with `cp <S>/onboard/<file name> <folder>/<file name>` (byte copy, so the file is LF, no fence). No Docs calls. `config.local.json` `sources`: six entries `{"path", "local_path"}`, the profile also `"writable": true`. Then the same checks as Docs mode: `pull-sources.md`, the byte comparison against the working copies for files written in this run, one `write-source.md` run for the score threshold.
- [ ] **Step 5: Step 5 and step 8 local text.** Step 5 keeps its title `## 5. Show the Docs` and its Docs text; add a local branch under it: local mode lists the six `local_path` values and the gap list, says edits go in those files in any editor, never `sources/`, and opens the folder (`explorer "<folder with backslashes>"`). Step 8 closing summary: in local mode the six file paths and the task (`weekly-job-report`, schedule) instead of the Doc links and the routine.
- [ ] **Step 6: Step 7.** Docs 7.2: `<doc links>` → `<sources list>`, same `- <Doc title>: <doc_url>` lines. Add a local branch for 7.2-7.5 after the Docs text: fill `<sources list>` with `- <Doc title>: <local_path>` lines; append the Excel line (Global Constraints, `<folder>` filled, `<week>` kept) as the last line of the `## Output: one Excel file, four tabs` section, i.e. just before `## Publish the results to the shortlist artifact`; the placeholder check as in Docs 7.2. Ask the day and hour (local time, no time zone). Find an existing task (PQ answer); on yes `update_scheduled_task`, else `create_scheduled_task` with the Global Constraints values, `prompt` = the filled prompt, `description` `Weekly job search, published to the shortlist artifact`. Permission mode per the PQ answer. On a create failure, show the error and the filled prompt and stop step 7. Tell the user it runs only while the app is open and a missed run happens at next launch. Run it once with `run_scheduled_task` and wait per the PQ answer. Write `shortlist` to config as Docs mode does (7.5).
- [ ] **Step 7: Run** `python -m unittest tests.test_templates -v`. Expected: OK (`test_onboard_names_existing_templates` still finds every named template). Then `git diff main -- .claude/skills/onboard/SKILL.md`: every `-` line is one of the wording changes in Steps 1-6.
- [ ] **Step 8: Commit** `.claude/skills/onboard/SKILL.md`: `/onboard: local source files option`.

### Task 5: ADR 0011, CLAUDE.md, README, config example

**Files:**
- Create: `knowledge/decisions/0011-local-source-files-option.md`
- Modify: `knowledge/decisions/README.md`, `CLAUDE.md`, `README.md`, `config.example.json`

**Depends on:** Task 1

**Interfaces:**
- Consumes: the `--local` CLI form (Task 1).

- [ ] **Step 1: ADR 0011** from `knowledge/decisions/0000-template.md`, status `accepted`, date `2026-10-29`, title `Local source files as an onboarding option`. Opening line in the form of ADR 0009's: `Amends ADR 0010 on four points; 0010 stays accepted.` Decision: the four points of spec Design 8, plus "mode is per entry (`local_path` vs `doc_url`)", "local files live outside the repo and its worktrees", "the local pull copies into `sources/`, so downstream skills are unchanged". Consequences: Docs path unchanged; local files have no version history (back them up); the weekly task runs only while the desktop app is open; switching mode is a re-run of `/onboard`. ADR 0002 named as background only.
- [ ] **Step 2: Decisions README** row: `| [0011](0011-local-source-files-option.md) | Local source files as an onboarding option | accepted | 2026-10-29 |`.
- [ ] **Step 3: CLAUDE.md.** Build block: after the `pull_sources.py` line add `python tools/pull_sources.py --local <local file> <target>             # local source file -> sources/`. "Sources of truth" bullet: `six Claude Docs` → `six Claude Docs or six local files outside the repo, chosen at /onboard`, and `writes only to the Profile doc` → `writes only to the profile source (Doc or local file)`, citing ADR 0011. Gotcha: `Edit the sources in the Claude Docs (claude.ai), never in sources/` → `Edit the sources in the Claude Docs (claude.ai) or in their local_path files, never in sources/`.
- [ ] **Step 4: README "Setup".** The `/onboard` sentence: `creates your six Docs` → `creates your six Docs (or six local files)`, `weekly routine` → `weekly routine (or a local scheduled task)`. Step 2: add `or six local files in a folder outside the repo (no code fence)`. Step 3 `sources` line: add `or, for local files, path and local_path (the file's absolute path), the Profile entry also "writable": true`.
- [ ] **Step 5: `config.example.json` `_comment`:** append ` For local source files, each sources entry is {"path", "local_path": "<absolute path of your file>"} instead of doc_url / tab_id / node_id; the profile keeps "writable": true.` (JSON-escaped). Run `python -c "import json; json.load(open('config.example.json', encoding='utf-8'))"`. Expected: no output.
- [ ] **Step 6: Run** `python -m unittest discover -s tests -v`. Expected: OK (includes `test_no_personal_data`).
- [ ] **Step 7: Commit** the five files: `ADR 0011 and docs: local source files option`.

### Task 6: Docs path unchanged (criterion 1) and checks green (criterion 6)

**Files:** none tracked

**Depends on:** Task 1, Task 2, Task 3, Task 4, Task 5

**PQ "Where does criterion 1's maintainer pull run, from a freshly pulled `sources/`?":** in two places, in order: first in `<main-checkout>` with `main`'s procedure (an ordinary pull, which refreshes its `sources/`), then copy `<main-checkout>/config.local.json`, `.personal-terms` and `sources/*` into `<worktree>` (CLAUDE.md worktree gotcha) and run the branch's `pull-sources.md` there. Every Doc changed by the user in between would show `changed`, so both pulls run back to back.

- [ ] **Step 1:** Pull in `<main-checkout>` (its `pull-sources.md`), then copy as above. Expected: the one-line report, no error.
- [ ] **Step 2:** In `<worktree>`, follow `.claude/skills/pull-sources.md`. Expected: `Pulled sources: all six unchanged.`; no `--local` call (the config has only `doc_url` entries).
- [ ] **Step 3:** Run `python -m unittest discover -s tests -v` and `python -m py_compile tools/*.py`. Expected: OK, no py_compile output.
- [ ] **Step 4:** `git diff main --stat` lists only the files in Tasks 1-5, this plan, the spec, its gate record, `docs/superpowers/README.md` and the plan gate record under `docs/superpowers/gates/plans/`; `git grep -n -i -w -F -f .personal-terms` prints nothing.

### Task 7: Local onboarding end to end (criteria 2-5) and clean-up

**Files:** none tracked (scratch: `<S>/e2e/`, `<S>/e2e-sources/`, `<S>/persona/`)

**Depends on:** Task 6

**PQ "Does criterion 5 also confirm the run read the six local files and the decisions collection?":** yes. After the run, `mcp__ccd_session_mgmt__list_events` on its session id must show a Read (or Bash read) of the mega resume's `local_path` and an `ArtifactData` `list` on `decisions`; either missing fails criterion 5. Reads of the other five are optional (the prompt says to read them when fit depends on them); any read of one must succeed.

- [ ] **Step 0: How the run is driven.** Steps 2-9 run in this session by following the clone's own files by hand: `<S>/e2e/.claude/skills/onboard/SKILL.md` for `/onboard`, `<S>/e2e/.claude/skills/resume/SKILL.md` for `/resume`, and the clone's `pull-sources.md` / `write-source.md`. Every Bash or Python call runs with the clone as its working directory (`cd <S>/e2e && ...`), and every relative path in those files means a path under `<S>/e2e`. Never invoke the worktree's `/onboard` or `/resume`.
- [ ] **Step 1: Setup.** Run `pwd`. Expected: `<worktree>` (the scheduled task created in Step 2 runs in this session's folder; if it is `<main-checkout>` or anything else, stop and ask the user). Delete `<worktree>/config.local.json` and `<worktree>/sources/` (Task 6's copies; the originals stay in `<main-checkout>`), so no maintainer config is reachable from the worktree whatever folder the scheduled task runs in. `git clone <worktree> <S>/e2e` and `git -C <S>/e2e checkout feat/local-sources`; confirm `<S>/e2e/config.local.json` does not exist. Write a fictional persona to `<S>/persona/` (a text resume with two jobs, one school, one project, and interview answers: target roles, two target companies, one location, threshold default). `list_scheduled_tasks` must show no `weekly-job-report`; if one exists, stop and ask the user.
- [ ] **Step 2: `/onboard` in `<S>/e2e`**, choosing local. First answer the folder `<S>/e2e/./Local-Sources` (inside the clone, differently spelled). Expected: refused. Then `<S>/e2e-sources`. At onboard step 6 (career-ops), stop before the clone (no folder given): no `career_ops_dir` is written, and the run goes on to step 7.
- [ ] **Step 3 (criterion 2):** `<S>/e2e-sources/` holds the six files and no Docs `batch` or `create` was called. Run `python -I -c "import json,sys; s=json.load(open(sys.argv[1],encoding='utf-8'))['sources']; print(len(s), sum('local_path' in e for e in s), sum('doc_url' in e for e in s))" <S>/e2e/config.local.json`. Expected: `6 6 0`.
- [ ] **Step 4 (criterion 4):** the onboarding `write-source.md` run's step 4 diff shows exactly `-- Score threshold: ASK` / `+- Score threshold: 3.5 (<first name>, 2026-10-29)` (or the date of the run), and the line is in `<S>/e2e-sources/profile.md`.
- [ ] **Step 5 (Review Focus 3):** one more `write-source.md` run that adds `- Test question: yes (<first name>, <today>)` to `## Common questions`. After its step 3 Read and before the Edit, append one line `% touched` at the end of `<S>/e2e-sources/profile.md` with Bash. Expected: the Edit reports the file changed since it was read, the run goes back to step 1 once, and the retry's step 4 diff shows exactly `+- Test question: yes (...)` (the `% touched` line is in both the before copy and the result, so it does not show). Then remove both lines by hand and run `pull-sources.md` once.
- [ ] **Step 6 (criterion 5):** the task exists (`list_scheduled_tasks`), the run's events show no read of any `config.local.json` or `sources/` file outside `<S>/e2e` and `<S>/e2e-sources` (the task's working folder is whatever this session's is; Step 1 removed the maintainer's config and sources from `<worktree>`), its SKILL.md prompt (Read its `path` from `list_scheduled_tasks`) lists the six `<S>/e2e-sources/...` paths and the `reports/<week>.xlsx` line; the onboarding run succeeds, the new test artifact's `data/index.json` has `latest` set to a week, and the PQ check of events passes. If it cannot publish, stop and report to the user.
- [ ] **Step 7 (template check, spec Design 7):** if the run stalled on anything cloud-only in the prompt, fix that line of `templates/weekly-search-prompt.md` in `<worktree>` only, rerun Task 2's tests, commit `Weekly prompt: works in a local run`, then rerun Task 6 Steps 3 and 4; else no change.
- [ ] **Step 8 (Review Focus 5):** rerun `/onboard` step 4 and step 7 in `<S>/e2e` with "keep" on the mode: it lists the six files and the task, asks before overwriting any, and `list_scheduled_tasks` still shows one `weekly-job-report`.
- [ ] **Step 9 (criterion 3):** `/resume` on one real posting in `<S>/e2e` (a URL from the newest CSV under `<main-checkout>/discovered/`; if there is none, ask the user for a posting URL): the pull report shows `--local` pulls; `build_resume.py` JSON shows one page, fill and skills-line checks passing.
- [ ] **Step 10: Clean-up.** `update_scheduled_task` `weekly-job-report` `enabled: false`; name the test artifact (URL) and the task to the user and, on their confirmation of each, delete the artifact (Artifact `delete`) and the task (`mcp__scheduled-tasks__delete_scheduled_task`, loaded with ToolSearch), then confirm with `list_scheduled_tasks` that it is gone. Delete `<S>/e2e`, `<S>/e2e-sources`, `<S>/persona`. Never copy `<S>/e2e/config.local.json` anywhere.
