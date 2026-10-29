# Resume tailoring prompt

## Inputs

- `sources/mega-resume.tex` (my full history). **This is the only source of facts.**
- `sources/mega-resume.tex` is also the style/format reference: preamble, custom commands, header, section order, tone.
- Job posting: pasted below, or a URL (fetch it if it's a URL).

**Job posting:**

<<<PASTE POSTING OR URL HERE>>>

---

## Task

Produce a **one-page** LaTeX resume tailored to the posting above, built by selecting and rewriting content from the mega resume, using the reference resume's format.

Deliver:
1. `<Full_Name>_Resume_<Company>.tex` (`<Full_Name>`: my full name with underscores for spaces; company name in PascalCase, no spaces, e.g. `..._Acme.tex`)
2. The compiled `.pdf` of that exact file
3. A short changelog (see "What to report")

---

## Hard rules

**Truthfulness.** Every claim must trace to a line in the mega resume. Rephrase, compress, and re-emphasize freely; never invent, inflate, or transfer a metric, technology, date, or scope from one item to another. If the posting asks for something I don't have, leave the gap (don't paper over it). If a bullet's wording drifts far enough from the source that you're unsure it's still accurate, flag it in the changelog rather than shipping it silently.

**Format.** Reuse the reference resume's preamble, custom commands (`\resumeSubheading`, `\resumeSubheadingContinued`, `\resumeSubheadingDegree`, `\resumeProjectHeading`), and header block verbatim. Contact line stays exactly as-is. Keep 11pt and the existing margins.

**One page, filled.** Exactly one page, and roughly **95% full**. A one-page resume with a half-empty bottom third is a failed output, not a safe one. Verified by compiling and looking at it, not by estimating.

---

## Content selection

Order sections as in the reference: Summary, Skills, Experience, Education, Research/Projects. Drop or reorder sections only if the posting makes it clearly better (say so in the changelog).

- **Summary:** 1 to 2 lines, rewritten to lead with what this posting most wants. Keep <the credential or affiliation the summary always mentions, if any>.
- **Experience:** <most relevant current role> gets the most bullets (3 to 5). <other roles> get 1 to 2 each. Prefer bullets with concrete outcomes over bullets that list tools.
- **Research:** exempt from the age rule below (<why, e.g. it's tied to a degree>). Include at 2 bullets each when relevant to the posting.
- **Education:** compress to the minimum that still shows <the degrees, GPA and affiliations to always show>.

### Age rule (what is off the table)

By default, **nothing before <cutoff role and date> appears on the resume.** That means:

- **Roles cut:** <older roles and internships>.
- **Projects cut:** <older projects>.

Override this only with a very strong, posting-specific argument (for example the posting is a direct hit for one of the cut items). If you override, say why in the changelog.

**Named exceptions:**
- **<project kept despite its age>** stays eligible by default. Include it unless space genuinely forces a cut, and flag the cut if you make one.
- **<project included only on fit>** is included only when it beats another candidate project on fit with this specific posting.

### Project priority

<your strongest recent projects> are the strongest signals for most of the roles listed under `## Targeting` in `sources/profile.md`. Pick on fit rather than recency, but expect these to be the usual shortlist. Give each included project 2 to 3 bullets.

Mirror the posting's own vocabulary where it's honestly applicable (if they say "evaluation harness," don't call it "testing framework"). Don't keyword-stuff.

---

## Skills section

Keep this section short and targeted. It is a relevance filter, not an inventory. A crowded skills block buries the few things this posting actually cares about, so the default posture is to cut.

- **Hard cap: the whole section renders in 5 lines or fewer in the PDF** (not counting the section rule). Fewer is fine. Verified visually on the rendered page, not by counting characters.
- **Two categories may share one line** whenever it saves space (for example Certifications and Languages), not only when the 5-line cap forces it. Use a `tabular` row placed right after the previous line's `\\` and followed by its own `\\`: `\begin{tabular}{@{}l@{\hspace{0.3cm}}l@{}} \textbf{Data \& ML}: ... & \textbf{Databases}: ... \end{tabular} \\` (the `@{}` edges keep the row aligned with the other categories; without the `\\` after `\end{tabular}`, the next category runs onto the same line). A shared row cannot wrap: if the pair is too long it runs past the right margin (an Overfull `\hbox` warning), so shorten the items or pair differently. Two per line is the maximum; don't cram three unless all three are genuinely short.
- **No category may wrap to a second line.** If one wraps, cut items until it fits, or move it onto a shared line with a shorter neighbour.
- Keep the reference's subheadings. Drop a whole category rather than pad it with filler, and merge thin categories instead of giving each its own line.
- Within each category, keep only skills that are (a) relevant to this posting **and** (b) among my genuine strengths per the mega resume. The mega resume lists far more than belongs on any single tailored resume. Long-tail items I've touched once do not belong here.
- If a skill is not backed by an experience bullet, a project bullet, or a certification, it needs a strong reason to appear.
- Languages and Certifications stay by default (<why languages matter for my target market, if they do>). Drop a certification only if it's clearly irrelevant to the posting.
- If the section is over 5 lines, cut in this order: least-relevant category entirely, then long-tail items inside the biggest category, then pair two surviving categories onto one line.

---

## Fitting the page

You are encouraged to tighten `\vspace` aggressively to buy room for more content. The target is a dense, full page that still reads as breathable.

**If it overflows:** trim bullet wording, then tighten `\vspace`, then drop the weakest bullet from the oldest remaining role, then drop a whole project.

**If it underfills (below roughly 90%):** add content back, in this order: restore a cut bullet from <most relevant current role>, add a third bullet to the strongest project, restore a cut project from the shortlist. Never fill space by adding skills back (the 5-line cap holds regardless of how much room is left).

**Never:** shrink the font below 11pt, narrow the margins past the reference, or compress spacing to the point that bullets visually collide or the page reads as a wall of text. Bullets need visible separation between entries, and section rules need clear air above and below.

---

## Compile and verify

Compile it yourself. If `pdflatex` isn't present, install a TeX Live subset (`texlive-latex-base`, `texlive-latex-extra`, `texlive-fonts-extra` for `fontawesome5`, `texlive-lang-english`).

Before delivering, confirm all of the following:

1. Compiles with no errors; note any Overfull `\hbox` warnings and fix ones that push text into the margin.
2. `pdfinfo` (or equivalent) reports exactly **1 page**.
3. Render the page to an image and **look at it**. Check: content reaches roughly 95% down the page; the skills section is 5 lines or fewer and no category wraps; no bullet collides with the line above; no orphaned single word on its own line; entries are still visually separated; section rules and dates align as in the reference.
4. Filename matches the required pattern and the PDF is the compile of that exact `.tex`.

If it doesn't fit, underfills, or doesn't look right, iterate. Don't hand over a version you haven't visually inspected.

---

## What to report

Keep it to a few lines:
- What you emphasized and why, given this posting.
- What you cut from the mega resume that was a close call, and any age-rule override you made.
- Any gap between the posting's requirements and my actual background, stated plainly, so I can decide how to handle it in a cover letter or interview.
- Any bullet whose rewording you want me to sanity-check for accuracy.

---

## Before you start

Ask only questions that would actually change the output (for example an ambiguous company name for the filename, or a posting requirement you can't tell whether my background covers). Otherwise make the call, note it in the changelog, and proceed.
