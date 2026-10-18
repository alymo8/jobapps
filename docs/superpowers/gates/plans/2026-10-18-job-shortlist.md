# Plan gate: Job shortlist skill Implementation Plan

- **Plan:** docs/superpowers/plans/2026-10-18-job-shortlist.md
- **Plan SHA-256:** b33ddbda0eccb293dec71676186ce3f0b52293f7658d2b5f9b19e0c338851857
- **Spec:** docs/superpowers/specs/2026-10-18-job-shortlist-design.md
- **Spec SHA-256:** 98e73f26686897a3d165596b7eb63e95c3984a1f1333f56cf6a9bb3a2bac1b89
- **Verdict:** pass-with-decisions
- **Decisions approved:** 2026-10-18
- **Approved by:** /ship (auto)
- **Date:** 2026-10-18
- **Rounds:** 2 discovery + 0 verification

## Plan-introduced decisions

- The fetch step flushes the pending file after keys, index, latest and decisions are fetched, then re-lists `decisions`, instead of flushing as step 1 (Task 5, plan answer 1).
- Fallback pending lines accept a `match_key` that may differ from the weekly row's, relying on `url_norm` to hide the posting (Task 5, plan answer 4).
- `decisions` gets `--url` (url_norm match) and `--company/--title` (match_key match) filters, and Undo tries URL, then company+title, then `--match` (Task 3, Task 5).
- A new tracked `.gitattributes` with `tests/fixtures/** -text`, plus a sha256 test pinned to `f1b302cc…f303`, keeps the fixture byte-identical (Task 1).
- `/cover-letter` run directly records the note "tailored resume + cover letter", and `/resume` run directly records "tailored resume" (Task 6).

## Findings fixed

- round 1 [blocking] Paste-in lines for the claude.ai skills are never reported: added Task 9 Step 2.
- round 1 [blocking] "CI is green on the PR" is checked by no task: added Task 9 Step 1.
- round 1 [minor] `rg` is not on the Git Bash PATH: checks say Grep tool, or `rg` where installed.
- round 1 [minor] Tasks 2 and 3 edit the same files: Task 3 depends on Task 2.
- round 1 [minor] Province-restricted chip must not go through `norm_text`: Task 2 states the raw-value test.
- round 1 [minor] Note text for the `/resume` and `/cover-letter` hooks: stated in Task 6 Step 2.
- round 2 [minor] Leaving out already-decided postings in not-interested: `find --decisions` adds `decided`; Task 5 uses it.
- round 2 [minor] Task 8 "today": explicit `--today <D>` shared with the independent script.
- round 2 [minor] Task 5 grep: one count per pattern.
- round 2 [minor] Task 8 runs the skill's Fetch step with no pending file.

## Open

- none
