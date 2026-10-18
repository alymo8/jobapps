# Plan gate: Claude Docs as the source of the resume and prompts Implementation Plan

- **Plan:** docs/superpowers/plans/2026-10-17-claude-docs-sources.md
- **Plan SHA-256:** 79f8bd38bafb498d596dfb68cc00a7d30681e2350f78953a252ff2fa2be58b3e
- **Spec:** docs/superpowers/specs/2026-10-17-claude-docs-sources-design.md
- **Spec SHA-256:** deb0f340fa533a1704b7a538d87dd772f350dad67f5ab634c07f2ca0ee871898
- **Verdict:** pass-with-decisions
- **Decisions approved:** 2026-10-17
- **Approved by:** /ship (auto)
- **Date:** 2026-10-17
- **Rounds:** 3 discovery + 0 verification

## Plan-introduced decisions

- The closing fence tolerates trailing spaces; `~~~` fences and indented backtick fences are treated as ordinary text; an unclosed fence is an error that writes nothing (Task 1). Spec says: "closed by a line of exactly the same backticks"; it is silent on trailing spaces, tildes, indentation and unclosed fences.
- Relative target paths resolve against the current directory, and the procedure always runs from the repo root (Task 1, Task 2). Spec says: nothing.
- The block-count error reports `code_blocks` as its own key beside `error` (Task 1). Spec says: "error `"code_blocks": N`" and "`{"path", "error": "<message>"}`" without saying how they combine.
- `/batch` pulls in a new step 4 of `## 0. Parse and confirm`, before the confirm step, because that step builds the Workday work history from the mega resume (Task 2). Spec says: "`/batch` pulls once in the main session before fanning out".
- Live verification compares the prompt files against the tracked files at `origin/main`, and the mega resume against the local `mega-resume-v1.6.tex`, each with CRLF→LF and a final newline added (Task 4). Spec says: "each equals its doc's code block (for the mega resume, equals `mega-resume-v1.6.tex` ...)".
- "Nothing else changed in the doc" is shown by an unchanged tab `rev` from a prose outline read and by the asset count rising by exactly one per pull (Task 4). Spec says: "Artifact `list` with `scope: "assets"` on each doc shows one new asset per pull, and nothing else changed in the doc".
- The one-off live edit changes "Keep it to a few lines:" to "Keep it to a few short lines:" with a Docs prose `update` and then reverts it (Task 4). Spec says: "Claude Code changes one word inside the Resume prompt doc's code block".

## Findings fixed

- round 1 [blocking] `/batch` reads the mega resume before the new pull step runs: the pull is now a new step between steps 3 and 4 of `## 0. Parse and confirm`, before the Workday-history build.
- round 1 [blocking] Task 3 depends on Task 2, but its header said it did not: Task 3 now depends on Task 2.
- round 1 [blocking] The prompt references would get a second final newline: references add a final newline only when missing.
- round 1 [minor] Live-edit diff needs the previous copy saved first: Step 5 copies the file to the scratchpad before the pull.
- round 1 [minor] The "in CI" half of criterion 1 was not checked: Task 4 Step 6 records the PR's CI run.
- round 1 [minor] Mega resume reference path was not absolute: the absolute path is named.
- round 2 [blocking] Reference-building commands broke in either shell: one Python script builds and compares the references as bytes, run with the Bash tool.
- round 2 [minor] Task 2 Step 6's grep could not show the skip lines: a second grep for "Skip step 0".
- round 2 [minor] Live-edit op shape was not spelled out: the full `update` call is given.
- round 2 [minor] Repo-root assumption was not in the procedure file: Task 2 Step 1 states it.
- round 2 [minor] Success JSON `path` value was unspecified: it is the target argument as given.
- round 3 [minor] `<scratch>` was never defined: defined at the top of Task 4.
- round 3 [minor] What `sha256` hashes was not stated: the target's bytes after the call.
- round 3 [minor] The ToolSearch keyword query might miss the Docs `create` tool: uses `select:` with the Docs server id.
- round 3 [minor] Review Focus overstated two checks: reworded to name the tests and what the greps check.

## Open

- none
