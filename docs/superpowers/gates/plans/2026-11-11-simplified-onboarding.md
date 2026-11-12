# Plan gate: Simplified onboarding; job search as its own skills Implementation Plan

- **Plan:** docs/superpowers/plans/2026-11-11-simplified-onboarding.md
- **Plan SHA-256:** 7a5480d6db785b85f43a048f9ee81a784fee042025440f24cdaf2d94f22aab70
- **Spec:** docs/superpowers/specs/2026-11-11-simplified-onboarding-design.md
- **Spec SHA-256:** f76d48246482d0f6d3ab2e3f6239c528bb35e39f7f6cadceaddf05426f3ef1ea
- **Verdict:** pass-with-decisions
- **Decisions approved:** 2026-11-11
- **Approved by:** /ship (auto)
- **Date:** 2026-11-11
- **Rounds:** 3 discovery + 1 verification

## Plan-introduced decisions

- `/scan-jobs` also follows the weekly prompt's `## Scale` (cap 100, no padding) and the last paragraph of `## Before you start`; it skips `## Respect my decisions`, `## What to flag` and the first paragraph of `## Before you start`; it reads `sources/mega-resume.tex` for ranking and lists unreadable priority companies in its report (Task 3).
- When `## Job search` exists, each `ASK` line is replaced in its own `write-source.md` run; when missing, the section is added in one run with both lines (Task 3).
- JSON rows: `location` optional (missing or `null` → `""`), values stripped, non-object rows skipped and counted; a valid JSON value that is not a list exits non-zero (Task 1).
- No rows left: `discover.py` writes no file and creates no `discovered/` folder; `/scan-jobs` stops (Task 1, Task 3).
- `Locations` is not added to `/batch`'s offered `## Targeting` key list; a `Locations` line added later goes at the end of `## Targeting` (Task 2).
- The writability proof is a dedicated `write-source.md` run writing `Score threshold: 3.5 (default, <today>)`; other `ASK`/missing `## Targeting` lines are filled in further runs, in sequence (Task 5).
- An `/onboard` re-run asks for and adds a missing `Locations` line; a missing `## Job search` section is left to `/scan-jobs` / `/weekly-scan` (Task 5).
- Tool check runs `import fitz` (blocking) and `import openpyxl` (report-only) separately; in Docs mode (`--docs` or from config) a failed Claude Docs row stops at step 1 (Task 5).
- After a mode switch, `/onboard` also tells the user to rerun `/weekly-scan` (redo) so the weekly run reads the new sources (Task 5).
- `/weekly-scan` takes `[publish | prompt | schedule]` to run one part alone (Task 4).
- `/weekly-scan` local `<folder>` = `os.path.commonpath` of the six `local_path` values (Task 4).

## Findings fixed

- round 1 [blocking] Mode switch dropped disabling the old routine/task: `/onboard` keeps today's Mode switch rule unchanged, including the disable offers, plus a pointer to rerun `/weekly-scan`.
- round 1 [blocking] Tasks 4 and 5 used `SkillsTest` without depending on Task 3: both now depend on Task 3.
- round 1 [minor] Fixture privacy check ran before the fixture was tracked: Task 2 Step 4 stages it first.
- round 1 [minor] Criterion 4 retry wording: "remove `discovered/` (or recreate the e2e worktree) and rerun".
- round 2 [blocking] Task 5 grep contradicted the kept ToolSearch line: the mode-switch ToolSearch line is exactly `list_scheduled_tasks,update_scheduled_task`; the grep checks `create_scheduled_task`.
- round 2 [blocking] "Creation steps 1-4 verbatim" brought back the stories build: Docs mode keeps today's creation steps 2-4 only; the working-copy rules (stories stay the skeleton) apply in both modes.
- round 2 [minor] Missing-config message quoted in Tasks 3 and 4.
- round 3 [blocking] Task 7 Step 3 grep matched `tools/discover.py` and broke in Git Bash: pattern `/discover(?![\w.])` with `-P`, run in PowerShell or with `MSYS_NO_PATHCONV=1`.
- round 3 [minor] `/weekly-scan` moved text renumbered to its own parts and Rules.
- round 3 [minor] SkillsTest asserts the glob is non-empty and drops the per-file assertion.

## Open

- none
