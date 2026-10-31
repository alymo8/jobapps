# ADR 0012: Recruiter review: one read, one improvement pass, then final

- **Status:** accepted
- **Date:** 2026-10-31

## Context

`/resume` checked layout (`build_resume.py`, the PNG) and truth (every claim in the mega resume),
but nothing asked whether a recruiter screening for the posting would move the resume forward:
must-haves visible early, skimmable, quantified, the posting's keywords. The user wanted one
recruiter-style check with one round of improvement, not an open-ended loop.

## Decision

- **A fresh `opus` subagent** reads the built resume as a recruiter (`.claude/skills/resume/recruiter-review.md`),
  scores relevance, readability and recruiter signals, and gives a score out of 10. It sees the PNG
  and the posting, not how the resume was written.
- **The same subagent does the improvement pass.** `/batch` resume subagents can't launch subagents
  of their own, so a separate reviewer and a re-dispatched writer would need two orchestrator
  stages; one "review, then improve once" agent works the same in `/resume` and `/batch` (stage 1c).
- **Score ≥ 9 skips the pass.** Below 9: exactly one pass from the mega resume only, rebuilt and
  truth-checked, reverted if it can't be made `ok`. Then a final re-score, no further changes.
- **A low final score is handed over**, with the feedback in `review.md`; it never dead-letters a
  posting or blocks `/apply`.

## Consequences

One more `opus` agent per resume (roughly doubles resume cost in `/batch`). The final score is graded
by the agent that made the changes, so it is less independent than the first read. Gaps the mega
resume can't fill stay in `review.md` under "Still open", which also surfaces facts on the resume
that the mega resume lacks.
