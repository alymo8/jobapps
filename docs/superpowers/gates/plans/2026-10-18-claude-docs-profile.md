# Plan gate: Profile, stories and answers in Claude Docs Implementation Plan

- **Plan:** docs/superpowers/plans/2026-10-18-claude-docs-profile.md
- **Plan SHA-256:** 6db0fb10e43cde7dba046d200b041194beb3d886c5909636f2aba39139f3815b
- **Spec:** docs/superpowers/specs/2026-10-18-claude-docs-profile-design.md
- **Spec SHA-256:** 335f0291d1844f49d7a899ce749206bbb9de2fa177e7f72cd1f008d39d4f63fc
- **Verdict:** pass-with-decisions
- **Decisions approved:** 2026-10-18
- **Approved by:** /ship (auto)
- **Date:** 2026-10-18
- **Rounds:** 2 discovery + 0 verification

## Plan-introduced decisions

- Anchor rule for profile writes: the heading line when the section is empty. When the anchor occurs more than once, extend the find text upward one line at a time until it is unique. Stop and tell the user if the section start is reached first. Never use `nth` (Task 2). Spec says: "Express the change as one edit against a line that appears exactly once in the pulled file".
- Several reusable answers in one reply are saved as several write-procedure runs in sequence, each with its own "Saved to profile" line (Task 2). Spec says: nothing.
- The missing-profile error report keeps `md`, `words`, `greeting_ok` and `signoff_ok` beside `"ok": false` and `"error"`. The check runs before the `.tex` is written, so a run before a pull leaves no `.tex` (Task 1). Spec says: "prints a JSON report with `"ok": false` and `"error": ...` and exits 1".

## Findings fixed

- round 1 [blocking] CLAUDE.md line 35 kept a stale `profile.md`: added to Task 4's Files and Step 1.
- round 1 [blocking] The Workday history save in workday.md did not go through write-source.md: added to Task 3 Step 2 and to Step 5's check.
- round 1 [blocking] The contact() test did not check all six header fields: it asserts the full dict.
- round 1 [minor] Escaped newline in the update call shape: placeholder simplified; newline wording made explicit.
- round 1 [minor] The diff check did not account for header lines or exit code: both stated.
- round 1 [minor] The delete call in Task 5 Step 4 was not fully specified: the full call is given.
- round 2 [minor] Recycle Bin command was not runnable PowerShell: written out in full.
- round 2 [minor] Task 1 Step 2's expected FAIL did not say which tests fail: stated per test.

## Open

- none
