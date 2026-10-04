# Cover letter prompt

## Inputs

- The job posting (`postings/<dir>/posting.md`, or a URL to fetch).
- Sources of facts, and **the only sources of facts**:
  - `mega-resume-v1.5.tex`: experience, projects, research, education, metrics.
  - `stories.md`: STAR stories. Facts under Situation / Task / Action / Result are usable. Anything
    under **Open** is an unconfirmed note: never state it.
  - `answers.md`: answers Aly wrote for past applications, in Aly's own voice. Reuse facts and
    phrasing that fit; don't paste a whole answer.
  - `profile.md`: what Aly wants next, career goals, framing rules (section "Career goals and cover
    letters"), languages, location.
- The posting's tailored resume and `changelog.md` if they exist: the letter should back the same
  story the resume tells, and the changelog lists the gaps to steer around.

---

## Task

Write one cover letter, tailored to this posting, that makes a confident, positive case for Aly and
for the fit with this specific role and company. Deliver `postings/<dir>/cover_letter.md`: plain,
paste-ready text (no Markdown headings, bold or bullets), paragraphs separated by blank lines.

---

## Hard rules

**Exact opening and closing.** The first line is exactly `Dear hiring team,` and the letter ends
with exactly these two lines:

```
Best,
Aly
```

If the posting is written in French, write the letter in French with `Bonjour à l'équipe de
recrutement,` and `Cordialement,` / `Aly`. Otherwise English.

**Length: about one page.** 300 to 400 words including the greeting and sign-off, in 4 paragraphs
(5 at most).

**Truthfulness.** Every claim (metric, technology, scope, date, title, outcome) traces to one of
the sources above. Rephrase and re-emphasize freely; never invent, inflate, or move a metric or a
technology from one project to another. Clients are always anonymized ("a major U.S. bank", "an
engineering consulting client"). Accenture is framed as: promoted and specialized as an applied AI
engineer.

**Positive, no gaps.** Never mention a requirement Aly doesn't meet, never apologize or hedge
("although I haven't...", "I may not have..."). Lead with the closest real strength instead, and
never claim the missing skill.

**Tailored, not generic.** Name the company and the role. Address at least two of the posting's
own requirements or problems, in the posting's vocabulary where it honestly applies, and connect
each to concrete evidence. A sentence that would fit any company's letter unchanged earns its place
only in the close.

---

## Structure

1. **Hook (2-3 sentences).** The role, and why this company: something specific from the posting
   (the product, the problem, the stage, the customers), tied to what Aly is looking for next
   (`profile.md`: building one product in depth, ownership, growth).
2. **Strongest proof (4-6 sentences).** The one or two experiences that best match the posting's
   top requirements, with their outcomes and numbers.
3. **Second proof or story (3-5 sentences).** Another angle the posting cares about (evals and
   reliability, client-facing delivery, end-to-end ownership, leadership, speed), from a project or a
   `stories.md` story.
4. **Close (2-3 sentences).** What Aly would bring to this team, and enthusiasm for a conversation.
   No restating the resume.

Choosing evidence: prefer recent production AI work (Accenture AI engineering, Clinic Ops,
Cold-Chain Dispatch, Safi, claude-kit) unless the posting points elsewhere (e.g. research, Java
backend, banking). One distinctive detail beats three generic ones.

---

## Voice

- First person, active, concrete. Short sentences over long ones.
- Tone adapts to the company: formal and polished for banks and large enterprises; warm and
  direct for startups and AI-native product companies.
- One line of personality (McGill varsity squash, timing walking routes to find the fastest one, Claude enthusiast and
  claude-kit author) is allowed only for startups or culture-heavy postings, and at most one.
- Avoid filler: "I am writing to express my interest", "I believe I would be a great fit",
  "passionate", "synergy", "fast-paced environment", "leverage". No em dashes; use commas, colons,
  or separate sentences.

---

## Verify before delivering

1. `python tools/build_cover_letter.py postings/<dir>/cover_letter.md --check`: `ok` must be true
   (word count, exact greeting and sign-off). Without `--check` it also builds the one-page PDF;
   do that only when the form needs an upload, then look at the PNG.
2. Truth check: go sentence by sentence and confirm each claim against a source. Write the mapping
   under `## Cover letter truth check` in `postings/<dir>/changelog.md` (create the file if
   missing): `claim | source file + item`.
3. Re-read the posting: the letter answers its top two or three requirements.

## What to report

A few lines: what the letter emphasizes and why, which posting requirements it addresses, and any
sentence whose wording Aly should sanity-check.
