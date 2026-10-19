# Plan gate: Outreach without apply Implementation Plan

- **Plan:** docs/superpowers/plans/2026-10-19-outreach-without-apply.md
- **Plan SHA-256:** 45c33dfb636163fde74fd0333d5310c01bfb8aa6c7c6e907976f750c33ca4f5b
- **Spec:** docs/superpowers/specs/2026-10-19-outreach-without-apply-design.md
- **Spec SHA-256:** 54c7b3039f1fa134696b2216131ead2e4228bcd8ba93a2f8c006017e87122998
- **Verdict:** pass-with-decisions
- **Decisions approved:** 2026-10-19
- **Approved by:** /ship (auto)
- **Date:** 2026-10-19
- **Rounds:** 3 discovery + 1 verification

## Plan-introduced decisions

- The posting-level batch approval is the line `APPROVED <YYYY-MM-DD>: outreach`, written as the last line of `## Shortlist` in `outreach.md` and matched by `^APPROVED \d{4}-\d{2}-\d{2}: outreach$`.
- The batch execute subagent learns its mode from a `Mode:` line in the execute prompt (the application part also needs `APPROVED <date>: submit`); a new prompt line `Application only` makes prepare and execute run only the application for already-messaged postings in `outreach --apply`.
- In `/batch outreach --apply`, application-only postings run `/apply` Phase 1 through the outreach skill's batch section.
- Stage 1b never overwrites a pre-run status of `applied`, `outreach-*`, `outreach-only-*`, `in-conversation`, `no-response` or `closed`, and writes only Notes `resume ok <date>` for them.
- A global re-message guard: no run sends a new outreach message or request to anyone already under `## Sent` in that posting's `outreach.md`.

## Findings fixed

- round 1 [blocking] New apply description still matched criterion 6: reworded to "/outreach --apply runs it first"; checks use the spec's exact pattern.
- round 1 [blocking] `/batch outreach --apply` execute could re-message: `Application only` execute line skips step 5; re-message guard added.
- round 1 [blocking] `/followup` legend trigger unchanged: trigger is now "lacks `outreach-only`" in all four skills (Global Constraints).
- round 1 [minor] Git Bash path conversion of `/`-leading patterns: those `rg` checks run in PowerShell.
- round 1 [minor] Test helpers undefined: `write_apps` and `status_urls` given.
- round 1 [minor] `/followup` typed-for-the user leftovers: listed in Task 5.
- round 1 [minor] Stage 1b protected only `applied`: extended, Notes text named; scoring left as today per spec.
- round 1 [minor] Review Focus cited a missing read-through: Task 7 Step 4a added; CI-green deferred to shipping flow.
- round 2 [blocking] Test snippet didn't compile: one-line f-string with `\n`; `STATUSES` placed at module level.
- round 2 [blocking] Prepare subagent couldn't learn "application only": `Application only` line in the stage-2 prompt too.
- round 2 [minor] Step 0.2 skip sentence stale: reworded.
- round 2 [minor] "attachment impossible" in batch execute NEEDS USER: dropped.
- round 3 [blocking] Criterion 4 evidence had no home: Task 7 Step 5b appends `## Verification evidence` to the plan; PR copies it.
- round 3 [minor] Legend `rg -F -c` quoting: uses `-f <scratch file>`.
- round 3 [minor] Batch model-routing row said "attach": Task 4 Step 3b.

## Open

- none
