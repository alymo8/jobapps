# Plan gate: Anonymize the repo and move personal settings to a local config Implementation Plan

- **Plan:** docs/superpowers/plans/2026-10-28-anonymize-and-local-config.md
- **Plan SHA-256:** 6ac9b1ed2121ea53d1a44384b1d93f5d365ea8228aed4aaf5bb2be369465bbf8
- **Spec:** docs/superpowers/specs/2026-10-28-anonymize-and-local-config-design.md
- **Spec SHA-256:** 0938e743d58b4d509d37c50ccee04bd6d1a35d2c837fbe7ce4b8803618d5a2c9
- **Verdict:** pass-with-decisions
- **Decisions approved:** 2026-10-28
- **Approved by:** /ship (auto)
- **Date:** 2026-10-28
- **Rounds:** 3 discovery + 1 verification

## Plan-introduced decisions

- The name-bearing subagent status token becomes `NEEDS USER` in apply, workday, batch and outreach, with no rule for parsing the old form (it lives only in live replies and the current run's manifest).
- Only `pull-sources.md` (and so every skill that pulls), `write-source.md` and `job-shortlist` stop when `config.local.json` is missing; `discover`, `linkedin-tab.md`, scoring, resume, outreach, followup and workday treat a missing file as every optional key absent, so `/discover` runs without any config.
- With no `targeting`, Workday marks the phone-country field `ASK` and asks it with the step's other `ASK`s.
- `.personal-terms` also lists the GitHub handle, the LinkedIn vanity, both forms of the email and phone, and every doc UUID, `tab_id`, `node_id` and the shortlist artifact id; its term match treats `_`, `.`, `-` and a preceding literal `\n`/`\t`/`\r` escape as word boundaries.
- Gate records are scrubbed as text only; their recorded `SHA-256` lines keep their historical values.
- The after capture runs in the worktree with its own `config.local.json`; `<main-checkout>` gets `config.local.json` and `.personal-terms` only after merge, copied from the worktree once the pull has deleted its `sources.json`.
- The skill-triggering risk is checked by a script comparing quoted phrases and `/commands` in old and new descriptions, not by a live triggering session.
- The maintainer's side-by-side `/resume` sign-off is requested after merge and blocks nothing.

## Findings fixed

- round 1 [blocking] Discover's country rationale not covered: Task 4 Step 4 rewrites the clause without a country; Step 5 greps discover for Canada/Montreal/Quebec/Users.
- round 1 [blocking] Missing-config behaviour per skill unspecified: Global Constraints list which skills stop and which treat a missing file as optional keys absent; write-source and job-shortlist steps add the stop.
- round 1 [minor] `git grep -f` term checks: `-F`, `.personal-terms` written without blank/comment lines, Task 9 named authoritative.
- round 1 [minor] `<currency>` added to batch's substitution sentence.
- round 1 [minor] Company-name grep scope: whole tree, non-doc hits fixed and committed in Task 8; job-shortlist body echoes kept.
- round 1 [minor] `check.json` path unified; argv rule excludes the `--profile` flag itself.
- round 2 [blocking] Plan contained the maintainer's first name in a file name: replaced with `<First>`; Task 8's scrub now covers this plan.
- round 2 [minor] Pronouns (he/his) mapped to "the user"/"they", with followup line 12 and outreach line 87 named.
- round 2 [minor] Career-ops not-set-up message dropped (discover asks for the path).
- round 2 [minor] Task 2 expected status mentions the plan files the caller commits.
- round 2 [minor] `preamble(profile)` / `to_tex(text, profile)` added; test argv uses `str(...)`.
- round 2 [minor] Spec and plan quotations of the kept trigger phrases are kept exceptions.
- round 3 [blocking] CI half of criteria 1 and 3 unchecked: Task 10 Step 6 opens the PR, watches `check-tools` and records its log; Step 6b puts it in the evidence.
- round 3 [minor] Term boundary after a literal escape (`\n`, `\t`, `\r`) and its test case.
- round 3 [minor] Outreach line numbers (62, 186); `Street address` key named.

## Open

- none
