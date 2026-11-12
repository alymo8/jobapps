---
title: Testing local source mode end to end
status: stable
last_updated: 2026-11-11
sources: the end-to-end run of the local-sources spec (criteria 2-5)
---

# Testing local source mode end to end

What tripped the first end-to-end run of local mode and `/weekly-scan`'s weekly scheduled task.

- **Creating the scheduled task** (`/weekly-scan`). Auto mode's classifier may refuse
  `mcp__scheduled-tasks__create_scheduled_task`; get the user's explicit OK, then call it again.
  The task keeps the session's Auto mode only when it is created in a turn the user typed in the
  desktop app with no subagent still running; otherwise its runs start in the default mode and
  stop at each new tool. The user then answers "Always allow" in the run's session (the approvals
  stay on the task).
- **The task runs in the session's folder.** Create it from the feature worktree, never from the
  main checkout, whose `config.local.json` belongs to the maintainer. Move the session with
  `mcp__ccd_directory__change_directory`; the move takes effect when the turn ends.
- **Auditing a run's reads.** `mcp__ccd_session_mgmt__list_events` shows tool names without
  arguments. Read the run's log instead: the newest `*.jsonl` under
  `%USERPROFILE%/.claude/projects/<session folder slug>/` written during the run (its file name is
  not the `local_...` id), and list its `tool_use` inputs.
- **A fictional persona needs enough material.** With 3 bullets per job, `/resume` stops at fill
  about 0.5 and dead-letters the posting as `FAILED`; 7-8 bullets per job still gave fill 0.83.
  Give each job 9-10 bullets and 2-3 projects (`tests/fixtures/sample-resume.md` reaches 0.96).
- **Walking `/onboard` as a new user:** `git worktree add --detach <scratchpad>/e2e HEAD` has no
  `config.local.json`, so it is a clean first run; answer with `tests/fixtures/sample-resume.md`
  and a sources folder outside the repo. Remove the worktree and folder afterwards.
- **Paths from Python in a Git Bash loop** end in `\r` on Windows (`for p in $(python ...)`), which
  makes `pull_sources.py` crash on the target path; strip them with `tr -d '\r'`.

## Open questions

- None.
