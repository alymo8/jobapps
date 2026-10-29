# Plan gate: Workday applications in /apply and /batch Implementation Plan

- **Plan:** docs/superpowers/plans/2026-10-05-workday-apply.md
- **Plan SHA-256:** 11219719189b535480e6c47496bc5c0f6aee18400236edd7e5d28f2b095e7e1a
- **Spec:** docs/superpowers/specs/2026-10-05-workday-apply-design.md
- **Spec SHA-256:** a05025676b6862a5f9a669076225df11fc3e0f64d0d841c6c16bc0ef53951cb9
- **Verdict:** pass-with-decisions
- **Date:** 2026-10-05
- **Rounds:** 3 discovery + 0 verification
- **Decisions approved:** 2026-10-05

## Plan-introduced decisions

- P1: In /batch stages 2 and 5, two postings of the same Workday tenant never run at once; the second waits.
- P2: Prompt pickers without Enter: type, wait 2 s, click the option, else browse via the list icon. No match: Skills → `skipped (no option)`; any other picker field → `ASK`.
- P3: The one-line street address is split on commas into Address Line 1 / City / Province (abbreviation → full name, e.g. QC → Quebec) / Postal Code.
- P4: Before stage 2, a posting counts as Workday when its URL host is Workday, or its dlq.md Detail or posting.md contains myworkdayjobs.com, myworkdaysite.com or "Workday (".
- P5: The batch review shows per Workday posting the tenant, stop step, quoted consent label and After approval rows; their ASKs join the deduplicated questions.
- P6: Element refs come from `find`, falling back to `read_page` (interactive).
- P7: Batch acceptance runs `/batch apply dlq.md --reason BLOCKED` trimmed at confirmation to a posting <req-id>, a posting <req-id> and one Workday posting with a non-Workday URL; only the kept rows are marked retried. "No password typed" is evidenced by grepping subagent transcripts.
- P8: A required field answered ASK: normal run asks the user that step's ASKs at once and continues; batch subagent leaves the step unsaved and stops there (posting goes to review ready with ASKs); execute mode returns NEEDS USER for later unanswerable fields. Only non-ASK validation errors failing twice are FAILED.
- P9: When the mega resume gives only a year for a job date, the user is asked for the month; the history section is appended at the end of profile.md.

## Findings fixed

- round 1 [blocking] Task 7 URLs dropped by read_postings.py: selection now via dlq.md, trimmed at confirmation.
- round 1 [blocking] Wrong transcript path for "no password typed": points to ~/.claude/projects/.../subagents/agent-<id>.jsonl with a non-empty sanity check.
- round 1 [blocking] Manifest grep for data it never holds: verification reads applications.md, dlq.md and the newest review.md.
- round 1 [blocking] Required ASK fields block Save and Continue: playbook section 5 rule added (P8); section 11 fills unreached steps.
- round 1 [minor] History pre-check limited to apply/outreach modes; stage 5 insertion point named; section 10 batch reporting; non-Workday-URL posting added to Task 7; prerequisites commit plan/README and cleanup step added.
- round 2 [blocking] Trimming the retry list could leave rows retried: only kept rows marked, with before/after count check and revert rule.
- round 2 [minor] Garbled Task 7 expected text fixed; "3b." made a sub-bullet.
- round 3 [minor] Baseline count taken before invoking /batch; third posting id in the grep; javascript_tool added to typing grep; Task 6 password check given a command.

## Open

- none
