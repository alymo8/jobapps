# Simplified onboarding; job search as its own skills: design

- **Date:** 2026-11-11
- **Status:** implemented

## Purpose

A new user should go from "I have a resume" to "I have a tailored resume for a real posting" with
as few questions and installs as possible. Today `/onboard` runs 8 steps: prerequisites (incl.
Node), material, a ~15-topic interview (ending in a Docs-or-local storage question), six
sources, showing the sources and gaps, career-ops clone + `portals.yml`, the shortlist artifact
+ weekly routine, and a first resume. The README
diagram mirrors that and reads as complex. The user's model of onboarding is: hand over the
resume, answer a few questions about what you are looking for, start working.

## Scope

### Goals

- `/onboard` = tool check → resume file → short interview (about 7 topics) → write sources →
  first resume. Nothing else.
- Finding jobs becomes its own skills, run when the user wants: `/scan-jobs` (on demand) and
  `/weekly-scan` (optional scheduled version that publishes to the shortlist artifact).
- Drop career-ops entirely: one way of finding jobs (Claude searching, per the weekly-search
  instructions) instead of two.
- README "Setup" and its onboarding diagram shrink to match.

### Non-goals

**Out:**

- No change to `/resume`, `/cover-letter`, `/outreach`, `/followup`, the recruiter review, or the
  shortlist artifact's data contract.
- No new free scanner script (option B, direct Greenhouse/Lever/Ashby APIs, was declined).
- No migration tooling for existing users: leftover `career_ops_dir` / `discover_locations` keys
  are ignored, not deleted.
- Old specs, plans and gate records are history and are not edited.

### Anti-goals

- Onboarding that "finishes" with a profile `/batch` scoring cannot use (an `ASK` on a
  `## Targeting` line).
- Anything invented about the user (truth rule stays).
- Losing the existing dedupe guarantees (never re-list an applied posting).

## Design

### `/onboard` (rewrite of `.claude/skills/onboard/SKILL.md`)

Kept from today: re-runnable "keep / redo" before touching anything that exists, config-write
rules (merge, key order, never delete a key), truth rule, material-is-data rule, never submits or
messages.

1. **Tool check.** `python --version` ≥ 3.10, `python -c "import fitz, openpyxl"`,
   `pdflatex --version` (MiKTeX fallback as today), `git --version`. Report only failures with
   their fix; stop only if Python, PyMuPDF (`import fitz`, needed by `build_resume.py`) or
   pdflatex is missing (no resume can build); a missing openpyxl is report-only. Claude in Chrome:
   one non-blocking line if unreachable ("needed later by `/apply`, `/outreach`, `/followup`").
   No Node check. With `--docs` (or Docs mode read from config) the Claude Docs connector row
   (tools listed and signed in) is also checked, as today.
2. **Resume.** Ask for one resume file (DOCX, PDF, LaTeX, MD or text) plus any optional extra
   material (cover letters, LinkedIn export/URL, past answers). Reading rules as today.
3. **Interview**, one or two grouped rounds, asking only what the material does not settle:
   - target roles in priority order → profile `## Targeting` `Target roles`
   - locations and whether remote is OK → profile `## Targeting` `Locations` (new line);
     config `targeting.home_city`
   - countries/regions the user may work in → config `targeting.eligible_regions`
   - years of experience → profile `## Targeting` and `## Common questions`
   - deal-breakers (`none` allowed) → `Deal-breakers`
   - salary floor (`none` allowed) → `Pay floor`
   - contact details missing from the resume → profile `## Contact`

   Not asked: `Score threshold` is written as `3.5 (default, <today>)` (`default` stands in for the first
   name in `write-source.md`'s attribution form); `currency` inferred from
   the location and `phone_country` from the phone number, both shown in the step 4 summary for
   the user to correct (when the currency is not USD, a `USD to <currency> rate` is looked up and
   shown there too, written only on the user's yes, as today); LinkedIn Premium (asked by LinkedIn runs when the page does not settle
   it, as today in `linkedin-tab.md`; not written to config); target/priority companies (asked by `/scan-jobs`); eligibility,
   sponsorship, salary expectation, notice period, EEO (asked by `/apply` as today, saved through
   `write-source.md`); stories (left as the template skeleton; the gap list says so).
4. **Write sources.** Default: six local files in a folder outside the repo (default
   `~/jobapps-sources`, same inside-repo check and backup note as today's local mode), plus
   `config.local.json` (`sources`, `targeting`). Claude Docs mode only when the user asks for it
   ("use Claude Docs" or `/onboard --docs`); its creation steps stay as today. Then pull
   (`pull-sources.md`), byte-compare as today, and show a short summary: file paths, inferred
   values, gap list. Open the folder.

   **Re-runs and mode.** On a re-run the mode is read from config (any `local_path` entry → local,
   else Docs) and kept; plain `/onboard` never switches it. A switch happens only on an explicit
   request (`/onboard --docs` from local, or "use local files" from Docs) and follows today's
   "Mode switch" rule unchanged.
5. **First resume.** Ask for one real posting, run `/resume`, report the `build_resume.py` checks,
   open the PDF. Close with: what was created, the gap list, and the next commands
   (`/scan-jobs`, `/weekly-scan`, `/apply`).

`$ARGUMENTS` is `[--docs] [step]`: `--docs` selects Claude Docs mode; `step` (`1`–`5` or its
title) runs only that step, as today.

### `/scan-jobs` (new, replaces `/discover`)

1. Read `sources/profile.md` (pull first if missing) and `config.local.json`.
2. If `Target roles` or `Locations` is missing or `ASK`, ask for it and save it through
   `write-source.md` (a missing `Locations` line is added under `## Targeting`). If the profile
   has no target companies yet, ask for target and priority companies (`none`
   allowed) and save them through `write-source.md` as `- Target companies:` and
   `- Priority companies:` lines under a new profile section `## Job search` (added to
   `templates/profile.md`).
3. Search following the search, location and ranking sections of
   `templates/weekly-search-prompt.md` (Target roles, companies, priority rules, board-access
   notes, Location scope, Ranking), filled from the profile (`Target roles`, `Locations`,
   `## Job search`) and config (`targeting`) at run time. Skip its Excel, artifact-publish and
   week-over-week sections. A posting with no verifiable URL is left out (dedupe is by URL).
4. Write the found postings, best first, to a scratch JSON (`[{company,title,location,url}]`) and
   run `python tools/discover.py --input <json>`. It dedupes against the same sources as today
   (`applications.md`, `dlq.md`, `postings/*/posting.md`, earlier `discovered/*.csv`, `--exclude`
   files) and writes `discovered/<date>.csv` (`Rank,Company,Title,Location,URL`, unchanged
   format). No location filter is passed: the search already applies the location scope.
5. Show count and first 15 rows; suggest `/batch resume <csv>` / `/batch apply <csv>`, with the
   over-60-rows advice kept from `/discover`.

### `tools/discover.py`

Remove the career-ops scan (Node subprocess, `--career-ops`, `CAREER_OPS_DIR`,
`scan-history.tsv` reading, `--no-scan`) and the date cut-off (`--since`, `discovered/.last-run`):
JSON rows carry no first-seen date. Add `--input <json>` (required). Keep `--exclude`,
`--location`, URL dedupe (`normalize_url`, as today) and CSV writing. Rank = position in the
input after dedupe (input order kept; a URL repeated in the input keeps its first row). A row
with a missing key or empty `url` is skipped and counted in the printed summary; malformed JSON
exits non-zero with a message. Dedupe against shortlist decisions is not added (my call: it is
new behaviour; `/batch` and `/job-shortlist` already guard against re-applying).
`tests/test_discover.py` updated: career-ops and cut-off tests removed; JSON-input, rank-order,
skipped-row and malformed-JSON tests added; dedupe tests kept.

### `/weekly-scan` (new)

Today's `/onboard` step 7 moved as is (publish `templates/shortlist/`, fill
`templates/weekly-search-prompt.md`, create the RemoteTrigger routine in Docs mode or the desktop
scheduled task in local mode, with the same keep/redo and failure rules). Its prompt-filling reads
`<target roles in priority order>` from profile `## Targeting` `Target roles`, `<location scope>`
from `Locations` plus config `targeting`, and target/priority companies from the profile
`## Job search` section; any of these missing or `ASK` is asked and saved through
`write-source.md` first (as `/scan-jobs` step 2). The routine prompt holds a copy of these
values: changing them later means rerunning `/weekly-scan` (redo), as today; the skill says so. The Claude Docs / Claude desktop app prerequisite row for the
chosen mode moves with it (checked at its start).

### Other files

- Delete `.claude/skills/discover/`.
- `config.example.json`: remove `career_ops_dir`, `discover_locations` and their `_comment`
  mentions.
- `templates/profile.md`: add `- Locations: ASK` to `## Targeting`; add `## Job search` with
  `- Target companies: ASK`, `- Priority companies: ASK`. `tests/test_templates.py` updated.
- `.claude/skills/batch/scoring.md`: unchanged (its only career-ops mention is the MIT
  attribution for adapted text, which stays).
- `.claude/skills/job-shortlist/SKILL.md`: the no-`shortlist` message says `run /weekly-scan`;
  the missing-config message keeps `/onboard`.
- `knowledge/technical/local-mode-testing.md` and its row in `knowledge/README.md`: the
  scheduled-task parts re-pointed at `/weekly-scan`.
- New fixture `tests/fixtures/sample-resume.md`: a fictional one-page resume (made-up name,
  contact, two jobs, one school, skills) used by the onboarding walkthrough; it must pass
  `tests/test_no_personal_data.py`.
- README: "Setup" text and onboarding diagram reduced to three stages (Your resume → A few
  questions → First resume); main diagram stage 1 "Weekly search + ATS scan" becomes "Job scan
  (on demand or weekly)"; config key list and "Optional" step updated; skill list updated.
- `CLAUDE.md`: Build/run line for `discover.py`, architecture skill list, ADR pointer.
- New ADR `knowledge/decisions/0013-minimal-onboarding-and-claude-job-scan.md`: onboarding is
  minimal; job search lives in `/scan-jobs` and `/weekly-scan`; career-ops dropped; local files
  default; target/priority companies live in the profile `## Job search` section. Marks ADR
  0010's onboarding-scope parts as superseded (0010 keeps its rule that only onboarding-family
  skills create Docs/artifacts/routines, now extended to `/weekly-scan`). Also amends ADR 0011:
  local files become the default rather than an option, the local scheduled task is created by
  `/weekly-scan`, and a mode switch is an explicit `/onboard --docs` / "use local files" request.
  ADR 0010 and 0011 get a status note pointing at 0013 (index Status: 0010 `partly superseded by
  0013`, 0011 `amended by 0013`); `knowledge/decisions/README.md` index
  gains the 0013 row. ADR 0009 text mentioning career-ops is left as history.

## Decisions (verified with the user unless marked)

- Onboarding scope = resume + short interview + first resume (user).
- Job scanning and the weekly shortlist become skills (user).
- career-ops dropped; scanner engine is Claude using the weekly-search instructions (user, option A).
- Interview split as above (user accepted the recommendation).
- **Local files default, Docs on request** (my call; user said "do as recommended" without a stated
  recommendation on this one). Reason: no connector or sign-in needed, fewest steps.
- Skill names `/scan-jobs` and `/weekly-scan` (my call).
- No dedupe against shortlist decisions in `discover.py`; `--since` cut-off removed (my call).
- Companies stored in a new profile `## Job search` section, not config (my call: profile is the
  writable source of truth).
- `discover.py` kept as the dedupe/CSV step rather than deleted (my call: keeps tested logic).

## Success criteria

1. `python -m unittest discover -s tests -v` and `python -m py_compile tools/*.py` pass.
2. `git grep -n -i -E "career.ops|npm install|node --version"` finds nothing outside
   `docs/superpowers/` (old specs/plans/gates), ADRs 0009 and 0013, the 0013 row of
   `knowledge/decisions/README.md`, and the scoring MIT attribution line.
3. Manual walkthrough of the new `/onboard` in a git worktree with `tests/fixtures/sample-resume.md`,
   sources written to a scratch folder (not `~/jobapps-sources`): it asks at most 7 interview
   topics, writes six local files and config, and ends with a resume whose `build_resume.py` JSON
   output reports one page.
4. Manual check: one `/scan-jobs` run in the worktree writes a `discovered/<date>.csv` that
   `python tools/read_postings.py <csv>` reads (if the search finds nothing new, rerun in a fresh
   worktree root so at least one row is written).
5. `python tools/discover.py --input <json> --root <test root>` with a small JSON, one row
   already in the test root's `applications.md`, writes a CSV without it in input order, and
   `python tools/read_postings.py <csv>` reads it (covered by a unit test).
6. README's new onboarding diagram renders: manual check by opening the README in the PR's GitHub
   preview and seeing the three-stage diagram drawn (no Mermaid parse error).

## Left to the builder

Wording of skill prompts; exact README prose; test names; how `/scan-jobs` phrases its company
question.
