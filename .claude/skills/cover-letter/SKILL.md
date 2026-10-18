---
name: cover-letter
description: Write a tailored, one-page cover letter for one job posting, following sources/cover_letter_prompt.md, from sources/mega-resume.tex, stories.md, answers.md and profile.md, truth-checked. Use when the user runs /cover-letter or asks for a cover letter; /apply runs it whenever a form offers a cover letter.
argument-hint: <posting URL | posting dir> [--pdf]
---

# /cover-letter: tailored cover letter for one posting

All paths are relative to `jobapps/` (the project root).

## Inputs

- `$ARGUMENTS`: a posting dir (`postings/<dir>`), a posting URL, or pasted posting text. `--pdf`
  also builds the one-page PDF (for forms that only take an upload). If empty, ask for it.
- `sources/cover_letter_prompt.md`: **the rules. Read it in full every run and follow it exactly.**
  Where the prompt names a versioned mega resume file (`mega-resume-v<N>.tex`), use
  `sources/mega-resume.tex`.
- Fact sources it names: `sources/mega-resume.tex`, `stories.md`, `answers.md`, `profile.md`.

## Steps

0. **Pull the sources.** Follow `.claude/skills/pull-sources.md`, unless the skill that ran this one
   already pulled them in this run.
1. **Get the posting.** If `postings/<dir>/posting.md` exists, use it. For a URL with no folder
   yet, find the folder whose `posting.md` has that `- URL:` line; if none, fetch and save the
   posting exactly as the `resume` skill's steps 1-2 do (WebFetch, Chrome fallback, same folder
   naming and `posting.md` format).
2. **Read the sources**: the prompt, the posting, the four fact files, and the posting's resume
   `.tex` and `changelog.md` if present (same story as the resume; gaps to steer around).
3. **Write** `postings/<dir>/cover_letter.md` per the prompt. If one already exists, say so and
   ask whether to rewrite (batch subagent: keep it, report it as done).
4. **Check:** `python tools/build_cover_letter.py postings/<dir>/cover_letter.md --check`. Fix and
   rerun until `ok` is true. With `--pdf`, run it without `--check`, then **Read the PNG and look at
   it** (one page, header intact, no overflow, paragraphs separated).
5. **Truth check** per the prompt, written under `## Cover letter truth check` in
   `postings/<dir>/changelog.md`. Fix or flag any claim without a source.
6. **Report**: the prompt's "What to report", then the full letter text verbatim. Open the file for
   Aly (`Invoke-Item postings/<dir>/cover_letter.md`, or the PDF when built).

## Running as a batch subagent

When the prompt says you are a batch subagent (or `/apply` runs this inside a batch subagent): Skip step 0: the orchestrator has already pulled the sources.
Do steps 1-5, don't open files, and don't ask the user anything. End with: posting dir, word count,
`ok`, PDF path if built, and any sentence to sanity-check.
