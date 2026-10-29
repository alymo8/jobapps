# Gate: Templates and /onboard for new users: design

- **Spec:** docs/superpowers/specs/2026-10-28-templates-and-onboard-design.md
- **Spec SHA-256:** b6b4584c8bf5b93e87a4d4d433149597c69d6937a47ba99371d9624e9d9dc4a0
- **Verdict:** pass
- **Date:** 2026-10-28
- **Rounds:** 3 discovery + 1 verification

## Key decisions

- Templates are generalised from the maintainer's own prompts and tracked in `templates/`
- The shortlist page, contract, keys file, capabilities and empty data files are copied once into `templates/shortlist/`
- New users keep their six sources in Claude Docs, created by `/onboard` in their own account
- `/onboard` covers the Premium question, config `targeting`, career-ops setup and a tailored shortlist and routine; Workday unchanged
- A new user's routine reads its inputs from Doc links in its prompt (no claude.ai project); created enabled via RemoteTrigger, no test run; creation blocked while placeholders remain; manual fallback only when `create` fails
- Unfilled profile answers are written as `ASK`; prompts keep `<placeholders>`; the mega resume leaves gaps out
- ADR 0010 carries forward ADRs 0003 (as amended by 0009) and 0004, with a `/onboard`-only exception, and supersedes them
- End-to-end test uses a fictional persona in the maintainer's account; the test routine is disabled right after creation; all test objects deleted afterwards
- Spec B depends on spec A being merged first

## Findings fixed

- round 1 [blocking] Profile gaps vs the `ASK` convention: profile gaps written as `ASK`; mega resume examples are LaTeX comments
- round 1 [blocking] ADR 0010 carry-forward unclear: carries forward every Decision bullet of 0003 and 0004
- round 1 [blocking] Personal-fact removal uncheckable: criterion 2 adds a term-list check
- round 1 [minor] ADR links repointed in `CLAUDE.md` and `job-shortlist/SKILL.md`
- round 1 [minor] Anti-goal exception for temporary test objects
- round 2 [blocking] Term list clashed with text spec A keeps: one-off scratch list, grep scoped to `templates/` only
- round 2 [blocking] `/onboard` did not write `targeting`: interview asks for it, step 4 writes it
- round 2 [blocking] Shortlist template lacked capabilities and initial data: `capabilities.json` and empty data files added; criterion 1 exercises `/job-shortlist`
- round 2 [blocking] Routine inputs undefined: Doc links in the prompt, filled text is the routine prompt; test objects listed
- round 2 [blocking] Two criteria lacked methods: career-ops validity = `npm install` + one `discover.py` scan; maintainer check via source pulls, artifact file listing and routine `get`
- round 2 [minor] ADR 0010 carries 0003 as amended by 0009; CLAUDE.md bullets named; `pull-sources.md` sentence kept
- round 3 [blocking] Test row in an empty shortlist: verification publishes a fixture row; test routine disabled
- round 3 [blocking] Routine "test run" undefined: removed; enabled routine, placeholder block, fallback only on `create` failure
- round 3 [minor] Step 6 passes `--career-ops <dir>`
- verify 1 [minor] Anti-goal wording matches the disabled test routine

## Plan questions

- How does `/onboard` get each new Doc's `tab_id` and the Profile code-block `node_id`, and check `write-source.md` works? (§2 step 4)
- Which tools read PDF/DOCX/LaTeX/text resumes and how are entries mapped into the mega-resume skeleton? (§2 steps 2, 4)
- Which Python packages count as "build libs" in the prerequisite check? (§2 step 1)
- Where does each interview answer go (profile sections, prompt placeholders, config); defaults for `USD to <currency> rate` and `Score threshold`? (§2 step 3)
- Are `discover_locations` the interview's locations verbatim, and the same values in `portals.yml`? (§2 steps 3, 4, 6)
- How are company boards resolved for `portals.yml`? (§2 step 6)
- Source of the weekly prompt for the template: RemoteTrigger `get` on the routine or the prompt artifact? (§1)
- Is `templates/shortlist/data/decision_keys.py` kept identical to the test fixture? (§1)
- How much material must the test persona have to pass the fill check? (criterion 1)

## Open

- none
