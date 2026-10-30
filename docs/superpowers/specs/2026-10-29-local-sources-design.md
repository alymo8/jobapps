# Local source files as an onboarding option: design

- **Date:** 2026-10-29
- **Status:** approved

## Purpose

`/onboard` today creates the user's six sources (mega resume, resume prompt, cover letter prompt,
profile, stories, answers) as Claude Docs, and a cloud routine reads them through their links
every week. Some users want to keep all of these files on their own machine. This spec makes that
an option `/onboard` asks about: **Claude Docs** (today's setup, the default) or **local files**.
The user does not have to give a reason; either choice is fully supported.

**Anti-goal (overrides everything else):** the Docs path does not change. A user who picks Docs,
and the maintainer's existing setup, behave exactly as before; no existing config needs editing.

In this spec, "the user" is whoever runs the skills on their own machine.

## Background (current state)

- `config.local.json` `sources` lists six entries (`path` under `sources/`, `doc_url`, `tab_id`;
  the profile also `node_id`, `"writable": true`).
- `.claude/skills/pull-sources.md` downloads each Doc and runs `tools/pull_sources.py
  <downloaded.md> <path>`, which writes the Doc's one fenced code block to `sources/<file>`. Every
  skill (`/resume`, `/cover-letter`, `/apply`, `/outreach`, `/batch`, `/followup`) pulls first and
  then reads only `sources/`.
- `.claude/skills/write-source.md` is the only way Claude Code changes a source: one anchored
  Docs `update` on the profile, verified by pulling again.
- `/onboard` (`.claude/skills/onboard/SKILL.md`) step 4 creates the six Docs, step 5 shows their
  links, step 7 publishes the shortlist artifact and creates a cloud routine (RemoteTrigger) whose
  prompt (`templates/weekly-search-prompt.md`) lists the Doc links under "Read my sources from
  these Claude Docs first".
- ADR 0010 holds the current rules: six Claude Docs are the only source of truth, each in one
  fenced code block, and Claude Code writes only to the profile, through `write-source.md`.

## Scope

**In:**

- `tools/pull_sources.py`: a `--local` mode; `tests/test_pull_sources.py`: tests for it.
- `config.example.json` `_comment`, `README.md` "Setup": the local entry shape; manual step 2
  gains "or six local files in a folder outside the repo (no code fence)" and step 3's `sources`
  line the `local_path` alternative.
- `.claude/skills/pull-sources.md`, `.claude/skills/write-source.md`: a local branch per entry.
- `.claude/skills/onboard/SKILL.md`: the storage question, the local equivalents in its Rules
  ("Re-runnable", "Redo"), the local branches of steps 1, 4, 5 and 7, Docs step 7.2's
  placeholder name (`<sources list>`), and the Docs-only wording in its frontmatter description,
  intro and step 8 closing summary (which lists file paths and the task in local mode).
- Other Docs-only wording: README's `/onboard` sentence, `CLAUDE.md`'s "Build, run, check"
  `pull_sources.py` line (gains the `--local` form), `write-source.md`'s opening line.
- `templates/weekly-search-prompt.md`: the sources line made mode-neutral;
  `tests/test_templates.py`: `<doc links>` replaced by `<sources list>` in `WEEKLY_PLACEHOLDERS`
  and in the line regex.
- `knowledge/decisions/0011-local-source-files-option.md` (new) and its row in
  `knowledge/decisions/README.md`; `CLAUDE.md` "Sources of truth" bullet and the "Edit the
  sources in the Claude Docs" gotcha mention the local option.

**Out:**

- Migrating content between Docs and local files. Switching is only a re-run of `/onboard`
  with "redo" on the storage question (section 6, "Mode switch").
- Mixing modes within one setup: `/onboard` writes all six entries in one mode. (The procedures
  work per entry, so a hand-edited mixed config would still work, but it is not a goal.)
- Any change to the downstream skills' reading of `sources/`, to `/job-shortlist`, `/discover`,
  or to the shortlist artifact and its data contract.
- The maintainer's Docs, routine, artifact and `config.local.json`.

## Design

### 1. Config shape

A local entry replaces `doc_url` / `tab_id` / `node_id` with `local_path`, the absolute path of the
user's file:

```json
{"path": "sources/profile.md", "local_path": "C:/Users/<you>/jobapps-sources/profile.md", "writable": true}
```

An entry with `local_path` is local; an entry with `doc_url` is a Doc. There is no separate mode
key. `path` keeps its meaning (the working copy skills read). Local file names equal the
`sources/` file names (`mega-resume.tex`, `resume_prompt.md`, ...).

Local files hold the content directly, with no fenced code block around it (unlike a Doc).

### 2. Where local files live

A folder the user picks, **outside the repo** (default offered: `%USERPROFILE%/jobapps-sources`,
i.e. `~/jobapps-sources`). Outside the repo, git never sees the files, worktree clean-up never
deletes them, and new worktrees find them through `local_path` (only `config.local.json` is copied
in, as today). `/onboard` refuses a folder inside the repo or inside any of its worktrees.

### 3. `tools/pull_sources.py --local`

`python tools/pull_sources.py --local <local file> <target path>`: reads the whole file as UTF-8,
converts CRLF to LF, ensures it ends in a newline, and writes it to the target with the same JSON
report and statuses (`created | changed | unchanged`, `sha256`, `lines`) as today. Errors (exit 1,
nothing written): the file is missing or unreadable, not valid UTF-8, or empty / whitespace only.
No code-block parsing. Without `--local` the tool is unchanged.

Tests: content copied verbatim; CRLF written as LF; missing final newline added; missing file,
empty file, whitespace-only file and invalid UTF-8 are errors that write nothing; second run reports `unchanged`.

### 4. `pull-sources.md`

Per entry: an entry with `local_path` runs only `python tools/pull_sources.py --local <local_path>
<path>` (no Docs `create`, no Artifact `read`, no saved copy); an entry with `doc_url` runs the
existing three steps unchanged. The opening paragraph says the sources live either in Claude Docs
or in local files outside the repo, as `config.local.json` records, and that `sources/` is a
working copy in both cases: edits go to the Doc or to the `local_path` file, never to `sources/`.
The Failure section adds: any `--local` error (missing, unreadable, invalid UTF-8, empty) stops
the run and names the file.
The Claude Docs connector is needed only for Doc entries.

### 5. `write-source.md`

Step 3 gains a local branch: when the profile entry has `local_path`, edit that file with the
Edit tool (`old_string` = `<old text>`, `new_string` = `<new text>`, the same whole-line texts as
the Docs payload; Edit's own uniqueness check stands in for `find_none`). Steps 1, 2 and 4 are
unchanged (the pull is the local pull). Failure: an Edit that finds the text zero or several times
goes back to step 1 once, then stops. The rule "never write the answer to a local file instead"
is reworded to "never write it anywhere but the profile entry's own source (its Doc or its
`local_path`)".

### 6. `/onboard`

- **Storage question**, asked at the end of step 3 (before anything is created): "Keep your six
  sources as Claude Docs (edit in claude.ai) or as local files on this computer?" Default Docs.
  On local, ask for the folder (section 2). On a re-run the current mode is read from the config
  (any `local_path` entry → local) and offered as "keep / redo" like everything else.
- **Rules, local equivalents.** "Re-runnable" also lists local files that pull (`--local`) and
  scheduled tasks from `list_scheduled_tasks`. "Redo" in local mode: a local file is overwritten
  only on a yes (no new file beside it); the scheduled task is updated in place with
  `update_scheduled_task` (new prompt, cron and `enabled: true`), never a second task. The Docs-mode Redo rule is
  unchanged.
- **Mode switch (a redo of the storage question).** It rewrites all six `sources` entries whole
  (no entry ever holds both `doc_url` and `local_path`). Docs to local: offer RemoteTrigger
  `update` `{"enabled": false}` on the old routine; local to Docs: offer `update_scheduled_task`
  `enabled: false` on the old local task; each sent only on a yes. The old Docs or local files
  stay in place. Content is not carried over beyond what steps 2-4 rebuild.
- **Step 1:** the Claude Docs row is marked "Docs mode only"; a new row "Claude desktop app
  (local mode's weekly task)" checks that the `mcp__scheduled-tasks__*` tools are listed.
- **Step 4, local:** build each working copy as today; write it to `<folder>/<file name>`
  (content without a fence, ending in a newline; never overwriting an existing file without a
  yes); write `config.local.json` with local entries (profile also `"writable": true`). Then the
  same checks as today: run `pull-sources.md`, compare each `sources/` file byte for byte with
  its working copy, then one `write-source.md` run for the score threshold.
- **Step 5, local:** list the six file paths (not Doc links) and the gap list; tell the user to
  edit those files in any editor, never `sources/`. Open the folder (`explorer <folder>`).
- **Step 7, local:** publish the artifact exactly as today. Fill the weekly prompt with
  `<sources list>` = one `- <Doc title>: <local_path>` line per file, and the other placeholders
  as today. Instead of RemoteTrigger, create a local scheduled task with
  `mcp__scheduled-tasks__create_scheduled_task`: `taskId` `weekly-job-report`, `title`
  `Weekly job report`, `cronExpression` in local time from the asked day and hour, `prompt` = the
  filled prompt, `description` one line. Ask first if `list_scheduled_tasks` already shows one
  with that id or with the artifact URL in its prompt; on yes, `update_scheduled_task` it (Rules). Tell the user: the task runs only while
  the Claude desktop app is open, and a run missed while it is closed happens at the next launch.
  After filling the prompt, local mode appends to its `## Output` section the line
  `Save the Excel file as <folder>/reports/<week>.xlsx (create the folder if missing).`, with
  `<folder>` filled and `<week>` left for each run; the template and Docs mode are unchanged.
  Local step 7 still writes `shortlist` `{"artifact_url", "title"}` to config, as Docs mode does.
  If `create_scheduled_task` fails, show the error and the filled prompt and stop step 7 (no
  manual fallback). Then run it once now with
  `run_scheduled_task` and check the artifact's `data/index.json` has `latest` set to a week
  (success criterion 5); if the run cannot publish, stop and show the error.

### 7. Weekly prompt template

`Read my sources from these Claude Docs first:` / `<doc links>` becomes `Read my sources first:` /
`<sources list>`, and "read the other Docs" becomes "read the other sources". In Docs mode
`/onboard` fills `<sources list>` with the same Doc-link lines it fills today, so a Docs user's
routine prompt reads the same apart from those words. Anything else in the template that assumes
a cloud run is left as is unless it stops a local run from working (the builder checks).

### 8. ADR 0011

"Local source files as an onboarding option": amends ADR 0010 the way ADR 0009 amended ADRs
0002 and 0003 (0010 stays accepted; 0011 names the points it changes). Four points of 0010's
Decision: the source of truth is six Claude Docs **or** six local files outside the repo, chosen
at onboarding; local files hold their content without a fenced code block; Claude Code writes only
to the profile source (Doc or local file), only through `write-source.md`; and in local mode
`/onboard` creates a local scheduled task instead of a cloud routine. This widens 0010 rather
than reversing or narrowing it, so 0010 stays accepted. ADR 0002 (superseded) is background only.

## Decisions

Confirmed by the user:

1. Local mode is offered to anyone at onboarding; no reason needed.
2. Local users' weekly shortlist runs as a local scheduled task in the desktop app.
3. Local files live in a folder the user picks, outside the repo.

My calls (builder may revisit only if they block):

4. Local pull copies the files into `sources/`, so no downstream skill changes.
5. Mode is per entry (`local_path` vs `doc_url`), no global key.
6. Local files have no code fence.
7. The weekly Excel goes to `<folder>/reports/`.

## Success criteria

1. **Docs path unchanged.** All unit tests pass; the Docs branches of `pull-sources.md`,
   `write-source.md` and `/onboard` are textually the same steps as on `main` (diff shows only
   added local branches and the wording changes listed above); an existing Docs config pulls
   exactly as before (maintainer's pull run once, all six `unchanged`).
2. **Local onboarding end to end.** `/onboard` in local mode with a fictional persona's material
   and a scratch folder outside the repo creates six files there and a `config.local.json` with
   six `local_path` entries; no Doc is created. Criteria 2-5 run in a separate checkout with no
   `config.local.json` (never the maintainer's copy), always on a new test artifact, and the test
   config is never copied back; criterion 1 runs first.
3. **Skills read local files.** `/resume` on one real posting in that setup pulls locally and
   `build_resume.py` reports one page, fill and skills-line checks passing.
4. **Profile write works locally.** The onboarding `write-source.md` run changes the score
   threshold line in the local `profile.md`, and its step 4 diff shows exactly that line.
5. **Weekly task.** The local scheduled task exists with the filled prompt naming the local
   paths; one manual run publishes to the (test) shortlist artifact and `data/index.json` shows
   `latest` set to a week. If it cannot publish, stop and report to the user.
6. **Checks green.** `python -m unittest discover -s tests -v`, `python -m py_compile tools/*.py`
   and `tests/test_no_personal_data.py` pass.

Afterwards the test persona's scratch folder, test artifact and scheduled task are deleted (the
user names and confirms each claude.ai delete first).

## Risks

- A local scheduled task may lack a tool the weekly prompt needs (Artifact publish, web search).
  Criterion 5 catches it before merge.
- Local files have no version history (Docs keep one). `/onboard` tells local users to back the
  folder up or keep it in their own git repo.
