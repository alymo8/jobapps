# Templates and /onboard for new users: design

- **Date:** 2026-10-28
- **Status:** approved

## Purpose

The maintainer wants to hand this repo to other job seekers (young professionals). On day one a
new user brings their resume, cover letter, profile and anything else they want used; the repo
asks them about themselves and the jobs they want; then they can use `/resume`, `/apply`,
`/outreach`, `/followup`, `/batch`, `/discover` and `/job-shortlist` for their own search.

This is the second of two specs. It depends on spec A
(`2026-10-28-anonymize-and-local-config-design.md`) being merged first: A removes personal data
from tracked files and introduces the gitignored `config.local.json` that this spec's `/onboard`
fills.

**Anti-goal (overrides everything else):** the maintainer's own use must not change. Nothing here
touches the maintainer's Docs, routine, artifact, config or output. The only exception is the
temporary test objects of success criterion 1: new Docs, an artifact and a routine created in the
maintainer's account for a fictional persona, the routine disabled right after creation (or deleted before its
first scheduled run), and all of them deleted afterwards.

In this spec, "the maintainer" is the repo owner and "the user" is whoever runs the skills on their
own machine.

## Background (current state)

Verified 2026-10-28 on `main` at `9b72e15` (#20), with spec A assumed merged.

- **Sources:** each user's six source docs (mega resume `.tex`, resume prompt, cover letter prompt,
  profile, stories, answers) live in Claude Docs in their claude.ai account, each with its content
  in one fenced code block, and are pulled into gitignored `sources/` by
  `.claude/skills/pull-sources.md` using `config.local.json` `sources` (`path`, `doc_url`,
  `tab_id`; the Profile entry also `node_id` and `writable: true`, used by
  `.claude/skills/write-source.md`). Nothing in the repo is a starting point a new user could fill
  in; the maintainer's material exists only in their own Docs.
- **Setup today (after A):** README "Setup" tells a new user to create the Docs and fill
  `config.local.json` by hand. Skills that find no config say the repo is not set up.
- **Weekly shortlist:** a claude.ai routine named "Weekly job report" in the maintainer's account
  (weekly, attached to a claude.ai project whose knowledge holds the mega resume) runs a
  ~14k-character prompt ("# Weekly job search prompt": target roles, target and priority
  companies, board-access notes, location scope, ranking, Excel output, publishing to the
  shortlist artifact, respecting decisions, week-over-week comparison). The prompt and all its
  input files are claude.ai artifacts. The shortlist page (its HTML, `data/*` contract,
  `data/decision_keys.py`) exists only as the maintainer's artifact.
  `.claude/skills/job-shortlist/SKILL.md` reads its URL from config `shortlist`.
- **career-ops:** `/discover` runs an external Node project (`santifer/career-ops` on GitHub)
  cloned outside the repo; its `portals.yml` holds companies, title filters and location filters.
  `/discover` reads its folder from config `career_ops_dir`.
- **ADRs:** ADR 0003 says Claude Code writes only to the Profile doc; ADR 0004 says the shortlist
  skill never publishes the artifact or changes the page (the weekly run owns those).

## Scope

**In:**

- `templates/` (new): generic starting material for the six source docs, the weekly routine
  prompt and the shortlist page.
- `.claude/skills/onboard/SKILL.md` (new).
- Skills' "not set up" messages (from spec A) point to `/onboard`.
- `README.md` "Setup" replaced by "run `/onboard`" (manual steps kept as a fallback);
  in `CLAUDE.md`, the "Skills in `.claude/skills/`" bullet gains `/onboard`, and the
  "Sources of truth" and "Weekly shortlist" bullets' links to ADRs 0003 and 0004 point to ADR 0010.
  `.claude/skills/pull-sources.md`'s "writes only to the Profile doc" sentence stays as is (true
  outside `/onboard`).
- `.claude/skills/job-shortlist/SKILL.md`: its ADR 0004 link repointed to ADR 0010.
- `knowledge/decisions/0010-onboarding-creates-user-docs-and-shortlist.md` (new) and its row in
  `knowledge/decisions/README.md`; ADRs 0003 and 0004 marked `superseded` by 0010.

**Out:**

- Anything in spec A (scrub, config shape, personal-data test).
- Any change to the maintainer's Claude Docs, routine, artifact or `config.local.json`.
- Submitting applications or sending LinkedIn messages during onboarding.

## Design

### 1. Templates

`templates/` (tracked) holds generic starting material built from the maintainer's current
sources with every personal fact removed. Each file keeps the structure and rules of the original
so new users get the same quality bar (decision 1). Spec A's personal-data test covers these
files.

- `resume_prompt.md`, `cover_letter_prompt.md`: the maintainer's prompts, generalised. Personal
  facts, target-role specifics and the maintainer's names become `<placeholders>` filled during
  onboarding or read from the profile.
- `mega-resume.tex`: the LaTeX preamble, macros and section skeleton, with one commented example
  entry per section.
- `profile.md`, `stories.md`, `answers.md`: headings and field bullets (the `## Contact` keys that
  `build_cover_letter.py` reads, `## Targeting` that `/batch` scoring reads, `## LinkedIn
  outreach`, the stories index format) with no content. Every unfilled profile answer is written
  as `ASK`, the profile's existing marker for an unknown answer that `/apply`, `workday.md` and
  `write-source.md` already act on; the profile template never uses `<placeholders>`.
- In `mega-resume.tex`, the example entries are LaTeX comments, so an unfilled skeleton compiles
  to nothing personal and never prints a placeholder.
- `weekly-search-prompt.md`: the weekly routine prompt with the same sections, personal content
  replaced by placeholders (`<target roles in priority order>`, `<target companies>`,
  `<priority companies>`, `<location scope>`, `<shortlist artifact URL>`, `<doc links>`); the
  "Known board-access notes" section keeps notes that are about job boards, not the maintainer.
- `shortlist/`: the shortlist page source, its `data/CONTRACT.md` and `data/decision_keys.py`,
  copied once from the maintainer's artifact (decision 2) with the title and any personal text
  made generic; `capabilities.json`, the page's runtime capabilities as the maintainer's artifact
  declares them (including the database capability behind the `decisions` collection); and empty
  initial data files in the shape `data/CONTRACT.md` defines (`data/index.json`,
  `data/latest.json` with no rows), so the page and `/job-shortlist` work before the first
  weekly run.

### 2. `/onboard`

`.claude/skills/onboard/SKILL.md`. Re-runnable: each step checks what already exists and never
overwrites a Doc, artifact, routine or config entry without asking.

1. **Prerequisites.** Check and report: Claude Docs connector signed in, Claude in Chrome
   connected, Python 3 with the build libs, `pdflatex` or MiKTeX, Node + npm (only needed for
   step 6), `git`. Missing items get install instructions; the skill continues with what it can.
2. **Collect material.** Ask for everything the user wants used: resume (PDF, DOCX, LaTeX or
   text), cover letter(s), LinkedIn profile export or URL, past application answers, anything else.
3. **Interview.** Ask, in a few grouped rounds, for what the material does not settle: preferred
   name and contact details, target roles in priority order, seniority, locations and work
   authorisation, remote/hybrid, target and priority companies, salary floor if any, LinkedIn
   Premium (yes/no), and behavioural stories (prompted from the resume's projects). For spec A's
   config `targeting`: the countries/regions they are eligible to work in (`eligible_regions`),
   home city (`home_city`), salary currency (`currency`) and phone country for forms
   (`phone_country`).
4. **Create the six Claude Docs** in the user's account from `templates/` and their material,
   each content inside one fenced code block (the format `pull-sources.md` expects). Truth rule:
   every fact comes from the user's material or answers; nothing invented. Gaps in the profile
   are written as `ASK`; gaps in the prompts and the weekly-search prompt stay as
   `<placeholders>`; mega resume gaps are simply left out. Every gap is listed. Write `config.local.json`: the six `sources` entries (with the
   Profile entry's `node_id` and `writable: true`), `linkedin_premium` from the Premium answer,
   `targeting` from the step 3 answers, and `discover_locations`. Then run `pull-sources.md` to
   confirm the pull works.
5. **Show the user** each created Doc's link and the list of gaps, so they can edit in claude.ai.
6. **career-ops.** Clone `santifer/career-ops` to a folder the user picks (outside the repo),
   `npm install`, build `portals.yml` from their target companies, titles and locations, run one
   scan (`python tools/discover.py --career-ops <dir>`), write `career_ops_dir` to config.
7. **Shortlist.** Publish a new artifact from `templates/shortlist/` in the user's account, with
   the capabilities from `capabilities.json` and the empty data files. Fill
   `templates/weekly-search-prompt.md` with their answers, their artifact URL and their six Doc
   links; the filled text is the routine's prompt. The new user's routine reads the mega resume
   and other inputs from those Doc links, with no claude.ai project (decision 5). Create the
   routine with RemoteTrigger `create` (schedule asked, default weekly), enabled; `/onboard` does
   not trigger a run itself. Before creating it, `/onboard` lists any `<placeholders>` left in the
   filled prompt and does not create the routine until the user fills or accepts each one. If
   `create` fails, fall back: give the filled prompt and step-by-step instructions to create the
   routine in claude.ai by hand. Tell the user the first scheduled run will show whether the
   routine can read their Doc links, and how to check its result. Write `shortlist` to config.
8. **First run.** Ask for one real posting and run `/resume` on it; report the `build_resume.py`
   checks and show the PDF.

`/onboard` never submits an application or sends a LinkedIn message.

### 3. ADR 0010

`knowledge/decisions/0010-onboarding-creates-user-docs-and-shortlist.md` carries forward every
Decision bullet of ADR 0003 as amended by ADR 0009 (including Claude Code writes only to the
Profile doc) and of ADR 0004 (including the shortlist skill never publishes the artifact or
changes the page), with
one exception each: `/onboard`, at setup time and only in the
onboarding user's own account, creates the six source Docs and publishes a new shortlist artifact
and routine. Outside `/onboard` both rules are unchanged. ADRs 0003 and 0004 are marked
`superseded` by 0010.

## Decisions

1. **Templates are generalised from the maintainer's own prompts** (maintainer confirmed
   2026-10-28), so new users get the same quality bar.
2. **The shortlist page source is copied once from the maintainer's artifact** into
   `templates/shortlist/` (confirmed).
3. **New users keep their sources in Claude Docs** like the maintainer (confirmed); onboarding
   creates them.
4. **Onboarding covers** the Premium question, career-ops setup and a shortlist tailored to the
   user (confirmed); the Workday flow is kept as is (confirmed).
5. *Builder's calls, marked here:* a new user's routine reads its inputs from Doc links in its
   prompt (no claude.ai project); routine creation falls back to manual instructions.

## Success criteria

Agreed with the maintainer 2026-10-28. Each is checked and its evidence reported.

1. **Onboarding works from scratch.** In a fresh clone with a made-up test persona (a fictional
   resume and answers): `/onboard` creates six Docs, `config.local.json` (with `targeting`), one
   shortlist artifact and one routine (or the manual-instruction fallback); for this test only,
   the routine is disabled (RemoteTrigger `update`, `enabled: false`) right after creation so it
   never runs. `pull-sources.md` pulls the six Docs. The verification then publishes a fixture
   `data/latest.json` with one fictional row (shape per `data/CONTRACT.md`) to the test artifact;
   `/job-shortlist show` reads that row and recording one `not-interested` decision on it
   succeeds; `/resume` on one real posting
   builds a one-page PDF that passes `build_resume.py`'s checks. Exactly these test objects (six
   Docs, one artifact, one routine) are created in the maintainer's account and deleted
   afterwards (deletes confirmed by the maintainer). career-ops setup counts as valid when
   `npm install` exits 0 and `python tools/discover.py --career-ops <dir>` completes one scan
   without error using the generated `portals.yml`.
2. **No personal data in templates.** Spec A's `tests/test_no_personal_data.py` passes on the
   maintainer's machine (with their `.personal-terms`) and in CI. In addition, a one-off term list
   is built in a scratch file outside the repo (not `.personal-terms`, which spec A keeps free of
   company names): the employers, schools, project names, cities, and target and priority
   companies found in the maintainer's six sources and weekly prompt, shown to the maintainer.
   `git grep -i -w -F -f <that file> -- templates/` must print nothing. This check covers only
   `templates/`, so text spec A keeps on purpose elsewhere (e.g. the job-shortlist trigger
   examples) does not clash. Evidence: the term count, the empty grep output and both test outputs.
3. **The maintainer is unaffected.** Before and after the change: `config.local.json` compared
   byte for byte; the six sources pulled with `pull-sources.md` and compared byte for byte; the
   shortlist artifact's file listing and version (Artifact `list` with scope `files`) recorded and
   equal; the routine read back (RemoteTrigger `get`) with the same prompt, schedule and enabled
   state.
4. **Existing checks pass.** `python -m unittest discover -s tests -v` and
   `python -m py_compile tools/*.py` green locally and in CI.

## Risks

- **Template leaks personal facts** from the maintainer's prompts. Mitigation: criterion 2, plus
  a read-through of each template.
- **Routine creation for another account** may not be fully possible from Claude Code (project
  knowledge attachment). Mitigation: manual fallback in step 7.
- **Generated Docs invent facts.** Mitigation: the truth rule in step 4; gaps are listed, never
  filled with guesses.
