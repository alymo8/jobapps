---
name: resume
description: Tailor the user's one-page LaTeX resume to a job posting (URL or pasted text) from sources/mega-resume.tex, following sources/resume_prompt.md, compiled and visually verified. Use when the user runs /resume or asks for a resume for a posting; /apply and /outreach run this first.
argument-hint: <posting URL or pasted posting>
---

# /resume — tailored resume for one posting

All paths are relative to the `jobapps/` folder (the project root).

## Inputs

- `$ARGUMENTS`: a posting URL or pasted posting text. If empty, ask for it.
- `sources/resume_prompt.md`: **the rules. Read it in full every run and follow it exactly.** Where it says
  `mega_resume.txt` / `latex_resume.txt`, use `sources/mega-resume.tex` / `latex_resume.tex`.
- `sources/mega-resume.tex`: the only source of facts. `latex_resume.tex`: format reference.

## Steps

0. **Pull the sources.** Follow `.claude/skills/pull-sources.md`, unless the skill that ran this one
   already pulled them in this run.
1. **Get the posting.** For a URL, read it with WebFetch (Greenhouse, Lever and Ashby pages render
   server-side). If WebFetch returns no posting body, open the URL in Chrome (claude-in-chrome skill)
   and use `get_page_text`. Extract: company, title, location(s), work model, requirements, nice-to-haves,
   and the job ID from the URL if present.
2. **Make the posting folder** `postings/<Company>-<JobID or short-title-slug>/` (Company in PascalCase,
   as in the filename rule). If it already exists with a resume in it, say so and ask whether to rebuild.
   Save the posting there as `posting.md`: a `# <Company>: <Title>` heading, then one `- Key: value`
   line each for URL (exactly `- URL: <posting url>`; `tools/read_postings.py` matches on it),
   Company, Title, Location, Fetched (date), then the full text.
3. **Write the resume** `postings/<dir>/the user_Resume_<Company>.tex` per the prompt's
   Hard rules, Content selection, Skills section and Fitting the page. If `postings/<dir>/score.md` exists (from `/batch` scoring), read its Must-haves table first: lead with the evidenced must-haves and steer around the real gaps it lists (never claim them).
4. **Compile and verify:** `python tools/build_resume.py <that .tex>`. It prints JSON:
   `errors`, `overfull`, `pages` (must be 1), `fill` (target 0.95–0.98; this overrides the prompt's "roughly 95%" and "below roughly 90%" underfill threshold: below 0.95 is underfilled), `skills_lines` (≤ 5), `png`.
   Then **Read the PNG at the path in `png` (it is in the temp dir, not next to the .tex) and look at it** for the prompt's visual checks (no wrapped skill category,
   no collisions, no orphan words, dates and rules aligned). Iterate until `ok` is true and the
   page looks right. Never hand over a version whose PNG you have not looked at.
5. **Truth check.** Before delivering, go bullet by bullet: each claim (metric, tech, scope, date)
   must appear in `sources/mega-resume.tex`. Fix or flag anything that doesn't.
6. **Write `postings/<dir>/changelog.md`** with the prompt's "What to report" items, plus the final
   `fill` and `skills_lines` numbers.
7. **Log it:** append a row to `applications.md` (create it with the header from that file's format
   if missing) with status `resume`.
8. **Report** in a few lines: the changelog, the PDF path, and open the PDF for the user
   (`Invoke-Item <pdf>`).

## Running as a batch subagent

When the prompt says you are a batch subagent: skip step 0 (the orchestrator has already pulled the sources), then do steps 1–6 (the orchestrator owns `applications.md`; never write it), don't open the PDF, and **don't ask
the user anything**. If the posting dir already has a verified resume (`changelog.md`), don't
rebuild; report it as done. If `posting.md` is already there (the pre-screen saved it), use it
and skip steps 1–2. Otherwise fetch postings with WebFetch or the ATS's public JSON API (Greenhouse:
`boards-api.greenhouse.io/v1/boards/<board>/jobs/<id>?questions=true`; Lever:
`api.lever.co/v0/postings/<company>/<id>`), not Chrome, since Chrome is reserved for form work.
If the posting is closed (404, "no longer available", expired), create nothing and report
`CLOSED: <evidence>`; if you can't read it (empty page, blocked fetch, login wall) after trying
WebFetch and the ATS API, report `UNREADABLE: <what you tried>`; if it excludes candidates based
in Canada/Quebec, report `INELIGIBLE: <quote>`. The orchestrator puts these in `dlq.md`. Make the call, record it in the changelog under `Questions for the user`, and end with
a short report: posting dir, `ok`, fill, and any questions.

## Postings that can't be processed

In a normal (non-batch) run, if the posting is closed, unreadable, excludes Canada/Quebec, or the
build still fails after iterating, tell the user and add or update its row in `dlq.md` (format at the
top of that file; reason `CLOSED` / `UNREADABLE` / `INELIGIBLE` / `FAILED`, status `open`).

## Questions

Ask only what the prompt's "Before you start" allows (would actually change the output).
