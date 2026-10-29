# Anonymize the repo and move personal settings to a local config: design

- **Date:** 2026-10-28
- **Status:** approved

## Purpose

This repo is one person's job-search workspace: the maintainer's name, Claude Docs links,
shortlist artifact URL and machine paths are written into the tracked skills, tools and docs. The
maintainer wants to hand the repo to other job seekers who clone it and `git pull` later
improvements. This spec is the first of two:

- **A (this spec):** every tracked file is free of personal data; personal settings move to a
  gitignored local config the skills read; a CI test keeps it that way.
- **B (`2026-10-28-templates-and-onboard-design.md`, later):** templates for new users and an
  `/onboard` skill that fills the local config and creates their sources. B builds on A's config
  shape.

After A, someone else could already use the repo by filling the config by hand (README "Setup").

**Anti-goal (overrides everything else):** the maintainer's own use must not change. Same sources,
same prompts, same weekly routine and artifact, same LinkedIn behaviour, same file names, same
output. A change that makes the repo shareable at the cost of the maintainer's results is a
failure even if it technically works.

In this spec, "the maintainer" is the repo owner and "the user" is whoever runs the skills on their
own machine (the maintainer included).

## Background (current state)

Verified 2026-10-28 on `main` at `9b72e15` (#20). The repo is private on GitHub, 76 tracked files.

- **Personal name in tracked files:** the maintainer's first name appears in about 50 tracked files
  (about 175 times in the 13 skill files under `.claude/skills/`, plus `CLAUDE.md`, `README.md`,
  every spec, plan, gate record and most ADRs). In skills it carries the approval rules
  ("submit only after <name>'s explicit OK", "messages to <name>'s existing connections").
- **Private links:** `sources.json` (tracked) lists the six source Claude Docs
  (`path`, `doc_url`, `tab_id`, and `node_id`/`writable` on the Profile entry); it is read by
  `.claude/skills/pull-sources.md` and `.claude/skills/write-source.md`.
  `.claude/skills/job-shortlist/SKILL.md` "Constants" holds the shortlist artifact URL and title.
- **Machine paths:** `.claude/skills/batch/SKILL.md` subagent prompts hard-code the repo's absolute
  path (6 places). `.claude/skills/discover/SKILL.md` step 1 names the maintainer's career-ops
  folder and hard-codes a list of Canadian cities as the default `--location`. Older plans hold
  absolute paths, the GitHub remote, and transcript paths.
- **LinkedIn plan:** `.claude/skills/outreach/SKILL.md`, `.claude/skills/followup/SKILL.md` and
  `.claude/skills/linkedin-tab.md` name the maintainer but already handle both plans:
  `linkedin-tab.md` checks the plan once per run from what LinkedIn shows (the "unlimited notes
  with Premium" dialog text, "Use N of M InMail credits", "Reactivate Premium") and asks the user
  only when the page does not settle it; it defines Free limits (about 3 notes a month, 200
  characters). `outreach` and `followup` defer to that check.
- **Output file names:** `.claude/skills/resume/SKILL.md` writes
  `postings/<dir>/<Full_Name>_Resume_<Company>.tex` with the maintainer's full name hard-coded;
  `tools/build_cover_letter.py` writes `<Full_Name>_Cover_Letter_<Company>.tex/.pdf` the same way
  and `.claude/skills/apply/SKILL.md` uploads that PDF. `tests/test_build_resume.py` uses a
  name-based file name.
- **Tools:** `tools/build_cover_letter.py` hard-codes the maintainer's first name as the sign-off
  in `FORMS` (`check()` compares the letter's last two lines against it); it already reads the
  letter header from the `## Contact` bullets of `sources/profile.md` through `contact()`, which
  strips a trailing parenthetical note from each value, and reports `MISSING_PROFILE` when the
  file is absent. The `## Contact` bullets include `Full name` and `Preferred first name`.
  `tools/shortlist.py` docstring names the maintainer. `tests/fixtures/decision_keys.py` (pinned
  by `FIXTURE_SHA256` in `tests/test_shortlist.py`) has the maintainer's name in its docstring;
  `tests/test_shortlist.py` uses a decision `source` value derived from the name.
- **Maintainer-specific targeting in skills:** the skills hard-code the maintainer's country,
  province, city and currency: `batch/SKILL.md` (stage 1a "Canada-eligible?", the INELIGIBLE rule
  "excludes candidates based in Canada or Quebec", CAD in DLQ lines and the review-sheet example),
  `resume/SKILL.md` (the same Canada/Quebec ineligibility rule), `batch/scoring.md` (annual CAD
  conversion, `USD to CAD rate`, "use the one for the posting's Canadian location (Montreal
  first)" when several ranges are listed, the bare-`$` rule "Canada → CAD, United States → USD",
  CAD score bands), `outreach/SKILL.md` (prefer people "covering the posting's location or
  Canada/North America", the maintainer's home city as fallback location),
  `apply/workday.md` (phone country `Canada (+1)`), `discover/SKILL.md` (Canada eligibility
  note). `sources/profile.md` `## Targeting` holds `Pay floor` (in CAD) and `USD to CAD rate`.

## Scope

**In:**

- Every tracked file: remove the maintainer's name, username, email, phone, street address,
  machine paths, Claude Docs / artifact / routine ids and URLs, GitHub remote, and the names of
  companies the maintainer applied to (exceptions in Design §2).
- The maintainer-specific targeting listed in Background moves to config `targeting` (Design §2),
  in `.claude/skills/batch/SKILL.md`, `.claude/skills/batch/scoring.md`,
  `.claude/skills/resume/SKILL.md`, `.claude/skills/outreach/SKILL.md`,
  `.claude/skills/apply/workday.md`, `.claude/skills/discover/SKILL.md`.
- `config.example.json` (new), `.gitignore`, removal of `sources.json` from tracking.
- `.claude/skills/pull-sources.md`, `.claude/skills/write-source.md`,
  `.claude/skills/job-shortlist/SKILL.md`, `.claude/skills/discover/SKILL.md`,
  `.claude/skills/batch/SKILL.md`, `.claude/skills/linkedin-tab.md`,
  `.claude/skills/resume/SKILL.md`, `.claude/skills/apply/SKILL.md`: read the config as below,
  plus the name scrub in every skill file.
- `tools/build_cover_letter.py`, `tools/shortlist.py`, `tests/test_build_cover_letter.py`,
  `tests/test_build_resume.py`, `tests/test_shortlist.py`, `tests/test_pull_sources.py`,
  `tests/fixtures/decision_keys.py`,
  `tests/fixtures/profile.md` (new).
- `tests/test_no_personal_data.py` (new), run in CI by the existing unittest step.
- `CLAUDE.md`, `README.md` (including a new "Setup" section for filling the config by hand).
- `knowledge/decisions/0009-shared-repo-and-local-config.md` (new) and its row in
  `knowledge/decisions/README.md`.
- Migration of the maintainer's current values into their local config (on their machine only).

**Out:**

- Templates and `/onboard` (spec B).
- Rewriting git history. Old commits keep the maintainer's name, paths and earlier design docs
  (decision 1). The current tree is clean; history is not.
- Making the GitHub repo public or adding collaborators (the maintainer does it, after looking at
  what old commits show).
- Any change to the maintainer's Claude Docs, weekly routine, shortlist artifact, `sources/`,
  `postings/`, trackers, or other gitignored files, except creating their `config.local.json`
  and `.personal-terms` and deleting the untracked `sources.json` once its content is in
  `config.local.json`.
- Account-level claude.ai skills outside the repo, and the maintainer's auto-memory.
- Changing what any skill does for the maintainer: approval rules, LinkedIn caps and routes,
  scoring, resume and letter rules all keep their meaning.

## Design

### 1. Local config

- **`config.local.json`** at the repo root, gitignored. Shape:

  ```json
  {
    "sources": [
      {"path": "sources/mega-resume.tex", "doc_url": "...", "tab_id": "..."},
      ...same six entries and fields as today's sources.json...
    ],
    "shortlist": {"artifact_url": "...", "title": "..."},
    "career_ops_dir": "...",
    "discover_locations": ["...", "..."],
    "linkedin_premium": true,
    "targeting": {
      "eligible_regions": ["...", "..."],
      "home_city": "...",
      "currency": "...",
      "phone_country": "..."
    }
  }
  ```

  `sources` is required. The other keys are optional: absent means the feature is not set up
  (`shortlist`, `career_ops_dir`), no default location filter (`discover_locations`), plan
  unknown (`linkedin_premium`), or, for `targeting`, see "Targeting" in §2.
- **`config.example.json`**, tracked, same shape with placeholder values (six `sources` entries,
  the Profile entry with `node_id` and `writable: true`) and a `"_comment"` key pointing to README
  "Setup".
- **`sources.json` is removed from tracking** (`git rm --cached`); its content moves into
  `config.local.json` and the local `sources.json` is then deleted. `sources.json`,
  `config.local.json` and `.personal-terms` are added to `.gitignore`.
  `.claude/skills/pull-sources.md` and `.claude/skills/write-source.md` read
  `config.local.json` `sources` instead of `sources.json`, with the same fields.
- **Missing config:** a skill that needs `config.local.json` and finds it missing stops and says
  the repo is not set up yet (README "Setup"). A skill that needs an optional key that is absent
  says which feature is not set up. Spec B changes these messages to point to `/onboard`.
- No Python helper; skills read the JSON directly. `tools/discover.py` keeps its
  `--career-ops` / `CAREER_OPS_DIR` interface; the skill passes the config value.

### 2. Anonymising tracked files

- **Skills** say "the user" where they say the maintainer's name today. The user is addressed
  directly in conversation ("show the user", "ask the user"). Every rule keeps its meaning: e.g.
  "submit only after the user's explicit OK", "messages to the user's existing LinkedIn
  connections need the user's OK". Frontmatter `description`s are rewritten the same way and keep
  their trigger phrases (they drive skill triggering).
- **Name literals that are data, not prose:** three tokens contain the name and are read back or
  stored, so they are handled explicitly. No tracked file keeps the name; old forms are matched by
  a name-free pattern:
  - `typed, <name> to send`: an old-log action only. Today `followup/SKILL.md` parses it from
    older `postings/*/outreach.md` logs and `outreach/SKILL.md` mentions it; neither writes it. It
    stays parse-only; the skills describe it as "`typed, <word> to send` (any single word)".
  - `Questions for <name>`: the changelog section `resume/SKILL.md` writes, which the resume batch
    subagent reports back in its reply (`batch/SKILL.md` stage prompt). New writes use
    `Questions for the user`; the batch prompt asks for the changelog's `Questions for <…>`
    section, any heading of that form.
  - `applied by <name> on the site`: the free-text note written to the shortlist `decisions`
    collection (`job-shortlist/SKILL.md`). New writes use `applied by the user on the site`. This
    is the one accepted change to the maintainer's output (decision 6); no key, id or field the
    page or weekly run reads is affected.
- **Paths:** `/batch` subagent prompts say "in the repo root `<repo-root>`" and the orchestrator
  substitutes the actual absolute path at launch. `/discover` reads `career_ops_dir` and
  `discover_locations` from config; with no `--location` argument and no `discover_locations`, it
  passes no location filter; with no `--career-ops`, no `CAREER_OPS_DIR` and no `career_ops_dir`
  it asks the user for the path (as today).
- **LinkedIn plan:** the per-run plan check in `linkedin-tab.md` stays exactly as it is and stays
  authoritative; outreach and followup keep deferring to it. Only its last branch changes:
  "if none of these settles it, ask the user" becomes "use `linkedin_premium` from config if set,
  else ask the user". Live page evidence always wins over the stored value, so a lapsed Premium
  is still detected.
- **Targeting:** every hard-coded country, province, city and currency listed in Background reads
  config `targeting` instead: `eligible_regions` (the ineligibility rule becomes "excludes
  candidates based in any of `eligible_regions`"; the stage 1a check becomes "eligible for
  `eligible_regions`?"), `home_city` (scoring's "<home_city> first", outreach's fallback
  location), `currency` (scoring's conversion, score bands and DLQ lines use it; the profile key
  is read as `USD to <currency> rate`), `phone_country` (Workday phone country code). The
  maintainer's values are today's (`["Canada", "Quebec"]`, their city, `CAD`, `Canada (+1)`), so
  every rule reads exactly as now for them. The three location rules map as: scoring's "the
  posting's Canadian location" → "a posting location in `eligible_regions`"; the bare-`$` rule →
  "a location in `eligible_regions` → `currency`, a United States location → USD, else USD";
  outreach's "Canada/North America" → "`eligible_regions`". Absent `targeting`: no eligibility
  screen, no city or region preference (the first listed range is used, outreach prefers only the
  posting's location), amounts in USD with no conversion, and Workday asks the user for the phone
  country.
  Score band amounts stay as written today (they are in the user's currency).
- **Shortlist skill:** "Constants" reads the artifact URL and title from config `shortlist`. Its
  description's example trigger phrases ("Montreal ones", "what's at Stripe", "skip the Okta
  ones") stay: they illustrate phrasing and are not data about the user's applications.
- **career-ops folder precedence:** `--career-ops` argument, then `CAREER_OPS_DIR`, then config
  `career_ops_dir`, then ask.
- **Renamed headings:** the `linkedin-tab.md` section titled with the maintainer's name becomes
  "The user's plan and each person's message route", and the cross-references to it in
  `outreach/SKILL.md` and `followup/SKILL.md` change in the same commit.
- **Output file names:** derived from `Full name` in `sources/profile.md` `## Contact` (trailing
  parenthetical note stripped as `contact()` already does, spaces → `_`):
  `<Full_Name>_Resume_<Company>.tex` and `<Full_Name>_Cover_Letter_<Company>.tex/.pdf`. For the
  maintainer the names are unchanged. Touches `resume/SKILL.md`, `apply/SKILL.md`,
  `build_cover_letter.py` (and its usage docstring) and `tests/test_build_resume.py` (neutral
  example name).
- **Cover letter check:** `build_cover_letter.py` `check()` still compares the letter's last two
  lines against `[closing word, name]` (field `signoff_ok` unchanged): the closing word from
  `FORMS[greeting]`, and the name line against `Preferred first name` from `sources/profile.md` `## Contact` (same note-stripping as
  `contact()`; falls back to the first word of `Full name`) instead of the hard-coded name in
  `FORMS`; `FORMS` keeps the greeting → closing-word mapping. When the profile is missing,
  `--check` reports `ok: false` with the existing `MISSING_PROFILE` error, as the PDF build already
  does. A `--profile <path>` option (default `sources/profile.md`) replaces the profile path for
  every use in the tool (sign-off check, letter header, file name), so
  `tests/test_build_cover_letter.py` can use `tests/fixtures/profile.md` (fictional person). The
  existing `test_check_needs_no_profile` is inverted (it now expects `MISSING_PROFILE`) and the
  tool's usage docstring is updated to match.
- **Other tool and fixture text:** `shortlist.py` docstring made generic;
  `tests/fixtures/decision_keys.py` docstring made generic and `FIXTURE_SHA256` updated (the key
  functions are unchanged, so it still matches the page's JS, but it is no longer byte-identical
  to the artifact's keys file; the `CLAUDE.md` gotcha about the fixture says so);
  `tests/test_shortlist.py` uses a neutral decision `source` value; `tests/test_pull_sources.py`
  uses a neutral sign-off name in its fixture text.
- **Docs:** all specs, plans, gate records, ADRs, `knowledge/`, `CLAUDE.md`, `README.md`,
  `.github/` scrubbed: the name becomes "the user" (or "the maintainer" where history needs it),
  absolute paths become `<repo-root>` / `%USERPROFILE%`, links to the maintainer's docs, artifacts
  and routine become a description ("the shortlist artifact"). Company names from the maintainer's
  own applications are removed ("a company"), with one exception kept as it explains a rule: the
  2026-10-04 Enter-key submit incident in `apply/SKILL.md`. Meaning is kept; these stay accurate
  records. ADR edits are limited to these substitutions, so no decision changes meaning and the
  decision-log rule (never delete or change a decision; supersede instead) holds. Company names
  are not in `.personal-terms`; the PR review checks for them.
- **README "Setup":** prerequisites (Python, `pdflatex`/MiKTeX, Chrome with Claude in Chrome, the
  Claude Docs connector), then: create your six source Docs (one fenced code block each), copy
  `config.example.json` to `config.local.json` and fill it, optionally set up career-ops and the
  shortlist. Spec B replaces the manual steps with `/onboard`. A short note states that git
  history predates the cleanup and still holds the maintainer's earlier details.

### 3. Personal-data test

`tests/test_no_personal_data.py`, run by the existing `python -m unittest discover` in CI:

- **Generic patterns, always on:** claude.ai artifact and doc URLs with ids
  (`claude\.ai/(code/)?artifact/[0-9A-Za-z-]{10,}`), routine ids (`trig_[0-9A-Za-z]{10,}`),
  absolute user paths (`[A-Za-z]:[\\/]Users[\\/][^<%\s]`, `/home/[a-z]`, `/Users/[a-z]`),
  email addresses outside `example.com`/`example.org` and `noreply@` addresses, and phone numbers
  in North American form (`\(?\d{3}\)?[-. ]\d{3}[-. ]\d{4}`).
- **Personal terms, local only:** if the gitignored `.personal-terms` file exists (one term per
  line, case-insensitive whole-word), every term is also searched. The maintainer's copy holds
  their name(s), username, email, phone and street. In CI the file is absent and this part is
  skipped, so the tracked test itself contains no personal term.
- Scans every file from `git ls-files`, skipping binary files (a NUL byte in the first 8 KB). An allowlist inside the test (a
  list of `(path glob, regex)` pairs, each with a one-line reason) covers legitimate hits. A hit
  reports file, line and pattern.

### 4. Maintainer migration

Run once on the maintainer's machine during implementation, before any skill reads the new config:

- Write `config.local.json` from today's `sources.json` (all fields copied verbatim), the shortlist
  URL and title from today's job-shortlist skill, the career-ops folder and city list from today's
  discover skill, `linkedin_premium: true`, and `targeting` with the literal values in today's
  skill text. Then delete the local `sources.json`.
- Write `.personal-terms`.
- `sources/`, `postings/`, trackers, Docs, routine and artifact untouched.

### 5. ADR 0009

`knowledge/decisions/0009-shared-repo-and-local-config.md`: the repo is shared and updated by
`git pull`; everything personal (source links, shortlist URL, career-ops path, locations, Premium
fallback) lives in gitignored `config.local.json`, which replaces tracked `sources.json`; a CI test
(`tests/test_no_personal_data.py`) plus a local `.personal-terms` list keeps personal data out of
tracked files; git history is not rewritten. It notes that `config.local.json` `sources`
replaces the `sources.json` named in ADRs 0002 and 0003, whose decisions are otherwise unchanged.

## Decisions

1. **Git history is kept** (maintainer confirmed 2026-10-28). Files are cleaned in normal commits;
   no rewrite or force-push. Anyone who can read the repo can read old commits; the maintainer
   decides when to make it public after reviewing them.
2. **One shared repo, updated by `git pull`** (confirmed). Everything a user creates or edits in
   normal use is gitignored so pulls never conflict.
3. **Two specs: this one first, templates and `/onboard` after** (confirmed).
4. **LinkedIn Premium is stored as a fallback** behind the existing live plan check (builder's
   call, to keep the maintainer's behaviour; the maintainer asked for Premium to be an onboarding
   question, which spec B adds).
5. *Builder's calls, marked here:* config file name `config.local.json`; skills read JSON directly
   (no helper module); personal terms live in a separate gitignored `.personal-terms` file;
   output file names derive from the profile's `Full name`.
6. **Accepted output change:** the shortlist decision note reads `applied by the user on the site`
   instead of naming the maintainer (builder's call; it is free text no reader parses).

## Success criteria

Agreed with the maintainer 2026-10-28. Each is checked and its evidence reported.

1. **No personal data in tracked files.** `tests/test_no_personal_data.py` passes in CI (generic
   patterns) and on the maintainer's machine with `.personal-terms` present (all terms).
   Evidence: test output from both.
2. **The maintainer is unaffected.** Before the change, capture: the six pulled `sources/` files
   (`pull-sources.md`); the generated `.tex` and the `--check` JSON report (paths removed) of
   `build_cover_letter.py` on an existing `postings/*/cover_letter.md`, plus the output file
   name; the shortlist artifact URL and the `data/latest.json` rows read by `/job-shortlist show`;
   the career-ops path and `--location` list `/discover --no-scan` would use; the resume file
   name `/resume` would write; and the targeting values each changed skill resolves (eligible
   regions, home city, currency, phone country), which after the change must equal the literal
   values in today's skill text. After the change, capture the same and compare: each must be
   identical (`.tex` byte for byte, rows and reports as JSON). Before and after captures happen on
   the same day (the letter `.tex` embeds the date) and with no Saturday weekly run between them;
   PDFs are not compared (they carry timestamps). The two parse-only patterns are checked
   read-only, without running `/followup` or `/batch`: list the lines of the maintainer's existing
   `postings/*/outreach.md` that the old literal `typed, <name> to send` matches and the lines the
   new `typed, <word> to send` pattern matches (a `grep -E` of each), and the same for
   `Questions for <…>` headings in existing `postings/*/changelog.md`; each pair of lists must be
   equal, and the pattern used in the grep must be the one the changed `followup`, `outreach` and
   `batch` text names. Then, as the maintainer's sign-off, the
   maintainer runs `/resume` on a posting that already has a pre-change resume and compares the
   two PDFs side by side; they confirm it is as good as before.
3. **Existing checks pass.** `python -m unittest discover -s tests -v` and
   `python -m py_compile tools/*.py` green locally and in CI.

## Risks

- **Scrubbing changes a skill's meaning.** Mitigation: the rewrite is mechanical name → "the user"
  plus targeted edits; the PR review diffs each skill for rule changes; criterion 2.
- **Skill triggering changes** when descriptions lose the name. Mitigation: keep trigger phrases;
  check that `/resume`, `/apply` etc. still trigger in the maintainer's session.
- **Old commits expose personal data.** Accepted (decision 1); stated in the README.
