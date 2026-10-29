# Plan gate: Templates and /onboard for new users Implementation Plan

- **Plan:** docs/superpowers/plans/2026-10-28-templates-and-onboard.md
- **Plan SHA-256:** d37452c41b9dbb9d187d4e703d84fd50b768d28ac065199dcce85aba8e41de66
- **Spec:** docs/superpowers/specs/2026-10-28-templates-and-onboard-design.md
- **Spec SHA-256:** b6b4584c8bf5b93e87a4d4d433149597c69d6937a47ba99371d9624e9d9dc4a0
- **Verdict:** pass-with-decisions
- **Decisions approved:** 2026-10-29
- **Approved by:** /ship (auto)
- **Date:** 2026-10-29
- **Rounds:** 3 discovery + 1 verification

## Plan-introduced decisions

- `/onboard` writes a default `Score threshold` of 3.5 into the profile (through one `write-source.md` run, which doubles as the writability check) unless the user gives a value (Task 5)
- `USD to <currency> rate` is left out of the profile template and of USD profiles; for other currencies it is the user's value, or a looked-up rate written only on the user's yes (Task 2, Task 5)
- The weekly prompt template is generalised from the routine's own prompt (RemoteTrigger `get`); the prompt artifact is used instead when RemoteTrigger is unavailable or the `get` prompt lacks `# Weekly job search prompt` (Task 1)
- The new user's weekly prompt reads the `data/*` contract from `data/CONTRACT.md` on their own shortlist artifact, not a repo path (Task 3)
- `templates/shortlist/data/decision_keys.py` is byte-identical to `tests/fixtures/decision_keys.py` (neutral docstring), pinned by a test and `.gitattributes -text`; the task stops if the artifact's functions differ (Task 4)
- `templates/shortlist/capabilities.json` equals the maintainer's artifact's stored capabilities (`{"db": {}, "user": {}}` on 2026-10-28); any extra non-data artifact file is copied and published too (Task 1, Task 4, Task 5)
- The profile template drops `## Workday work history` (the Workday flow builds it) and the maintainer's dated preference lines (Task 2)
- The new user's routine is named `Weekly job report` and the artifact titled `Weekly job shortlist`; the `create` body copies the maintainer's routine's top-level fields, account-specific ids from the user's RemoteTrigger `list` or asked; the e2e test routine is named `Weekly job report (onboard test)` (Task 4, Task 5, Task 7)
- `discover_locations` are the interview's location keywords verbatim (plus `Remote` if accepted); the same list goes into `portals.yml` `location_filter.allow`, with `home_city` in `always_allow` (Task 5)
- Boards are resolved from career-ops' example entries or provider URL patterns; a company with no supported ATS board goes into `portals.yml` with `enabled: false` and is listed to the user (Task 5)
- Prerequisites: Python 3.10+, PyMuPDF and openpyxl; DOCX resumes read with stdlib `zipfile` + `xml.etree` (Task 5)
- Source Docs use a 4-backtick fence; templates are tested to hold no run of 4+ backticks (Task 2, Task 5)
- The test persona: a ~1.5-page PDF resume, currency USD, no priority companies, Premium `no`, one company with no ATS board (Task 7)
- README "Map" also gains `/onboard` and a `templates/` bullet (Task 6)

## Findings fixed

- round 1 [blocking] Tasks 3 and 4 edit a test file only Task 2 creates: Task 3 depends on Tasks 1-2, Task 4 on Tasks 1-3
- round 1 [blocking] Onboard template-path test would match the career-ops `templates/portals.example.yml`: regex skips prefixed paths; skill writes `<career-ops-dir>/templates/...`
- round 1 [blocking] e2e `/job-shortlist` shares the maintainer's pending-decisions file: Task 1 records it, Task 7 stops if non-empty and checks after, Task 8 compares
- round 1 [minor] Empty-data test written before CONTRACT.md is read: contract read first; `week`/`rows` named; shortlist.py check added
- round 1 [minor] Mega-resume mapping implicit: macro-per-entry mapping added to the skill
- round 1 [minor] README Map edits beyond scope: kept, noted as keeping the Map accurate
- round 2 [blocking] Skills section named `Technical Skills`: source section names verbatim (`\section{Skills}` etc.), test added
- round 2 [blocking] RemoteTrigger `create` body unspecified: derived from the captured maintainer routine; disable `update` body specified
- round 2 [blocking] `tab_id`/`node_id` field names deferred to e2e: executor reads the maintainer's Profile doc to find the field paths before writing the skill
- round 2 [minor] CR bytes in macro names restored; capabilities from the captured record; `from tests.test_shortlist import FIXTURE_SHA256`; list wrappers commented out; distinct test routine name
- round 3 [blocking] Weekly prompt may be a pointer: falls back to the prompt artifact; other inputs listed
- round 3 [blocking] Task 3 used CONTRACT.md before Task 4 fetched it, and a repo path: non-data artifact files fetched in Task 1; prompt points at the artifact's `data/CONTRACT.md`
- round 3 [blocking] Shortlist page supporting files: every non-weekly-data artifact path fetched, tested and published
- round 3 [minor] Capabilities equality with the record; keys cache backed up and restored; ambiguous "it"; old shortlist message grep; term list kept separate from `.personal-terms`
- verify 1 [minor] Task 3 consumes `weekly-inputs.txt` and the contract copy, adds no extra placeholders; `capabilities.json` excluded from published files

## Open

- none
