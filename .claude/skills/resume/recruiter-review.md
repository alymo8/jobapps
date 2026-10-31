# Recruiter review — one read, at most one improvement pass

Run by a fresh subagent (`opus`) on a resume that has already passed `build_resume.py` and the truth
check. It reads the resume as a recruiter screening for this posting, scores it, improves it once
if the score is below 9, then finalizes. There is never a second improvement pass, and a low final
score is still handed over, with the feedback.

All paths are relative to the repo root. `<dir>` is the posting dir, `<tex>` its resume `.tex`.

## Inputs

- `postings/<dir>/posting.md`: the role you are hiring for.
- The resume as the recruiter sees it: run `python tools/build_resume.py <tex>` and Read the PNG at
  the path in `png`. Score from the PNG, not from the `.tex`.
- For the improvement pass only: `<tex>`, `sources/mega-resume.tex` (the only source of facts),
  `sources/resume_prompt.md` (the rules; read it in full before editing), and `postings/<dir>/score.md`
  if it exists (its real gaps must never be claimed).

## 1. First read: score out of 10

Read the posting, then spend a recruiter's first pass on the page (6–10 seconds: titles, company
names, the first words of each bullet, the skills block), then read it in full. Score each area
out of 10 and give 1–3 concrete feedback lines per area, in a recruiter's voice, each naming what
to change ("I'm hiring for Kafka at scale; it's only in the skills list, not in any bullet"):

1. **Relevance:** the posting's must-haves and strongest nice-to-haves are visible, early, and
   backed by experience bullets, not only listed as skills; the most relevant role and bullets lead.
2. **Readability:** skimmable in one pass; bullets open with the outcome or action; no dense blocks,
   jargon a recruiter can't parse, or filler.
3. **Recruiter signals:** quantified impact, seniority and scope that match the role's level,
   the posting's own keywords (an ATS search would find them), and no red flags (unexplained
   gaps, title mismatch, irrelevant content taking space).

**Score** = the rounded mean of the three, out of 10 (an integer). Be a demanding recruiter: 9–10
means you would forward it to the hiring manager without hesitation.

## 2. Gate

- **Score ≥ 9:** no changes. Go to 4.
- **Score < 9:** do exactly one improvement pass (3).

## 3. One improvement pass

1. Copy `<tex>` to `<tex>.pre-review` (the fallback).
2. Apply the feedback by re-selecting, reordering and rewording material **from
   `sources/mega-resume.tex` only**, following `resume_prompt.md`. Never add a skill, metric, tool,
   scope or date the mega resume does not support; a gap the mega resume can't fill stays a gap and
   goes in the feedback as "not addressable".
3. `python tools/build_resume.py <tex>` until `ok` is true (1 page, fill 0.95–0.98, skills lines
   ≤ 5); Read the PNG for the prompt's visual checks. Truth-check every changed bullet against the
   mega resume.
4. If the build can't be made `ok`, or a change fails the truth check and can't be fixed, restore
   `<tex>.pre-review` over `<tex>`, rebuild it, and record `improvement reverted: <why>`.
5. Delete `<tex>.pre-review`.

## 4. Final score

Re-read the final PNG once and give the **final score** out of 10 (the same three areas; no further
changes, whatever it says). Without an improvement pass, the final score is the first score.

## 5. Write the results

`postings/<dir>/review.md`:

```
# Recruiter review: <Company> – <Title>

- Score: <first>/10 → final <final>/10
- Improvement pass: yes | no (score ≥ 9) | reverted: <why>

## Feedback (first read)
### Relevance — <n>/10
- ...
### Readability — <n>/10
- ...
### Recruiter signals — <n>/10
- ...

## Changes made
- <one line per change, with the mega-resume source of any new or reworded line>  (or "none")

## Still open
- <feedback the final resume doesn't address, and why (not addressable from the mega resume, page space)>  (or "none")
```

Then append to `postings/<dir>/changelog.md`:

```
## Recruiter review
- Score: <first>/10 → final <final>/10 (postings/<dir>/review.md)
- Top feedback: <the most important still-open line, or the most important change made>
```

and, if the resume changed, update the changelog's `fill` and `skills_lines` numbers to the final
build's.

## Final reply

At most 4 lines: posting dir, `review <first>/10 → <final>/10`, improvement pass (yes / no /
reverted), top feedback line, final `ok` and fill.
