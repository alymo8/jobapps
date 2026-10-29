# Cover letter prompt

## Inputs

- The job posting (`postings/<dir>/posting.md`, or a URL to fetch).
- Sources of facts, and **the only sources of facts**:
  - `sources/mega-resume.tex`: experience, projects, research, education, metrics.
  - `sources/stories.md`: STAR stories. Facts under Situation / Task / Action / Result are usable. Anything
    under **Open** is an unconfirmed note: never state it.
  - `sources/answers.md`: answers <first name> wrote for past applications, in <first name>'s own voice. Reuse facts and
    phrasing that fit; don't paste a whole answer.
  - `sources/profile.md`: what <first name> wants next, career goals, framing rules (section "Career goals and cover
    letters"), languages, location.
- The posting's tailored resume and `changelog.md` if they exist: the letter should back the same
  story the resume tells, and the changelog lists the gaps to steer around.

---

## Task

Write one cover letter, tailored to this posting, that makes a confident, positive case for <first name> and
for the fit with this specific role and company. Deliver `postings/<dir>/cover_letter.md`: plain,
paste-ready text (no Markdown headings, bold or bullets), paragraphs separated by blank lines.

---

## Hard rules

**Exact opening and closing.** The first line is exactly `Dear hiring team,` and the letter ends
with exactly these two lines:

```
Best,
<first name>
```

If the posting is written in French, write the letter in French with `Bonjour à l'équipe de
recrutement,` and `Cordialement,` / `<first name>`. Otherwise English.

**Length: about one page.** 300 to 400 words including the greeting and sign-off, in 4 paragraphs
(5 at most).

**Truthfulness.** Every claim (metric, technology, scope, date, title, outcome) traces to one of
the sources above. Rephrase and re-emphasize freely; never invent, inflate, or move a metric or a
technology from one project to another. Clients are always anonymized (e.g. "a major bank", "a consulting
client"). <Current employer> is framed as:
<the framing rule from `sources/profile.md`, "Career goals and cover letters">.

**Positive, no gaps.** Never mention a requirement <first name> doesn't meet, never apologize or hedge
("although I haven't...", "I may not have..."). Lead with the closest real strength instead, and
never claim the missing skill.

**Tailored, not generic.** Name the company and the role. Address at least two of the posting's
own requirements or problems, in the posting's vocabulary where it honestly applies, and connect
each to concrete evidence. A sentence that would fit any company's letter unchanged earns its place
only in the close.

---

## Structure

1. **Hook (2-3 sentences).** The role, and why this company: something specific from the posting
   (the product, the problem, the stage, the customers), tied to what <first name> is looking for next
   (`sources/profile.md`: <what you are looking for next>).
2. **Strongest proof (4-6 sentences).** The one or two experiences that best match the posting's
   top requirements, with their outcomes and numbers.
3. **Second proof or story (3-5 sentences).** Another angle the posting cares about
   (<angles that matter in your field, e.g. reliability, client-facing delivery, end-to-end ownership, leadership, speed>),
   from a project or a `sources/stories.md` story.
4. **Close (2-3 sentences).** What <first name> would bring to this team, and enthusiasm for a conversation.
   No restating the resume.

Choosing evidence: prefer <your most recent, strongest work: roles and projects> unless the posting
points elsewhere (<examples of postings that call for other evidence>). One distinctive detail
beats three generic ones.

---

## Voice

- First person, active, concrete. Short sentences over long ones.
- Tone adapts to the company: formal and polished for banks and large enterprises; warm and
  direct for startups and product companies.
- One line of personality (<hobbies or interests from `sources/profile.md`>) is allowed only for
  startups or culture-heavy postings, and at most one.
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
sentence whose wording <first name> should sanity-check.
