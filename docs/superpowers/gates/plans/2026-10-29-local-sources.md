# Plan gate: Local source files as an onboarding option Implementation Plan

- **Plan:** docs/superpowers/plans/2026-10-29-local-sources.md
- **Plan SHA-256:** 7caa41cde812c63991b1bc9431600e570293032e707947f3c24c4aee56895ccd
- **Spec:** docs/superpowers/specs/2026-10-29-local-sources-design.md
- **Spec SHA-256:** 476090379f868b5b0f3b2572a26e97657017ea2d9face278f000be3b208013b0
- **Verdict:** pass-with-decisions
- **Decisions approved:** 2026-10-29
- **Approved by:** /ship (auto)
- **Date:** 2026-10-29
- **Rounds:** 3 discovery + 2 verification

## Plan-introduced decisions

- `--local` also drops a leading UTF-8 BOM and turns a lone CR into LF, besides CRLF (Task 1)
- A local profile with CR line endings makes `write-source.md` stop and ask the user to re-save it with LF; the file is never converted (Task 3)
- `pull-sources.md` gets the title `# Pull the sources (Claude Docs or local files)` and a first line in its Tools section saying the tools are needed only for `doc_url` entries (Task 3)
- `/onboard` step 1 reports both mode-specific rows as conditional, never blocking on a first run; the chosen mode's row is re-checked right after the storage question and the run stops if it fails (Task 4)
- The folder check expands `~` / `%USERPROFILE%`, resolves symlinks and letter case, and compares against every `git worktree list` root; a missing folder is created only after the user confirms the resolved path (Task 4)
- The onboarding run is awaited through its completion notification, with `list_task_runs` polled about every 5 minutes as a fallback, up to 90 minutes; success is `latest` matching `YYYY-MM-DD`, otherwise step 7 stops (Task 4)
- The local task relies on Auto mode: the user is asked to switch the session to Auto before the create and to answer "always allow" to each tool prompt during the onboarding run; if not saved in Auto, the user is warned weekly runs may stall (Task 4)
- An existing task matches on id `weekly-job-report` without a Read; other tasks are matched by reading each one's `SKILL.md` for the artifact URL (Task 4)
- Criterion 5 also requires the run's events to show a read of the mega resume's `local_path` and an `ArtifactData` `list` on `decisions`; reads of the other five sources are optional (Task 7)
- Criterion 1 pulls twice back to back: in `<main-checkout>` with `main`'s procedure, then in the worktree with the copied config and `sources/`, where all six must be `unchanged`; those copies are deleted from the worktree before the e2e run (Tasks 6, 7)
- The end-to-end run stops `/onboard` step 6 (career-ops) before the clone and writes no `career_ops_dir` (Task 7)

## Findings fixed

- round 1 [blocking] How the e2e run is driven and where the task runs: Task 7 Step 0 follows the clone's skill files by hand with every call run from `<S>/e2e`; Step 1 deletes the maintainer config and `sources/` copies from the worktree
- round 1 [minor] Step 5 heading rename: title kept, local branch added under it
- round 1 [minor] Review Focus 3 test named: a second `write-source.md` run adds a test answer, with a mid-run touch of the file
- round 1 [minor] Clean-up deletes the task with `delete_scheduled_task` after confirmation
- round 1 [minor] `test_local_cli` puts a space in the source path too
- round 1 [minor] Wait uses the completion notification, polling as fallback
- round 2 [blocking] Working-folder check unverifiable: replaced by an events check that no config or `sources/` outside the e2e folders was read
- round 2 [blocking] Criterion 5 required reads the prompt does not ask for: only the mega resume read and the `decisions` list are required
- round 2 [minor] Task 6 Steps 3-4 rerun after a Task 7 template commit
- round 2 [minor] Task 6 Step 4 `--stat` list completed
- round 2 [minor] README manual step 1 edit dropped (not in Scope In)
- round 2 [minor] Task 7: career-ops stops before the clone; the posting comes from the newest `discovered/` CSV, else the user
- round 3 [blocking] CR check written inline into the local `write-source.md` paragraph, with its stop rule and a Failure bullet
- round 3 [minor] Task 1 Step 2 expects FAIL or ERROR (TypeError)
- round 3 [minor] Task 7 Step 1 checks `pwd` is `<worktree>` before the task is created
- verify 1 [blocking] Raw CR byte in the CR-check command replaced with the `\r` escape

## Open

- none
