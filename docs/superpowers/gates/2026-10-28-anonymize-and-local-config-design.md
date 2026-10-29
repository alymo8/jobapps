# Gate: Anonymize the repo and move personal settings to a local config: design

- **Spec:** docs/superpowers/specs/2026-10-28-anonymize-and-local-config-design.md
- **Spec SHA-256:** 0938e743d58b4d509d37c50ccee04bd6d1a35d2c837fbe7ce4b8803618d5a2c9
- **Verdict:** pass
- **Date:** 2026-10-28
- **Rounds:** 3 discovery + 1 verification

## Key decisions

- Git history is kept (no rewrite); the maintainer decides when to make the repo public
- One shared repo updated by `git pull`; everything personal is gitignored
- Split into spec A (this) and spec B (templates + `/onboard`)
- Tracked `sources.json` replaced by gitignored `config.local.json` (sources, shortlist, career-ops path, locations, Premium fallback, `targeting`) plus tracked `config.example.json`; skills read JSON directly
- LinkedIn Premium stored only as a fallback behind the existing live plan check
- Country, region, city, currency and phone country move to config `targeting`; the maintainer's values are today's literals; defined behaviour when absent
- Output file names and the cover-letter sign-off come from the profile's `## Contact`; `--check` requires the profile; `--profile` option
- Name literals: `typed, <word> to send` parse-only; `Questions for <…>` any heading; shortlist note becomes "applied by the user on the site" (accepted output change)
- CI personal-data test with generic patterns plus a local gitignored `.personal-terms`; company names checked by PR review
- Docs and ADRs scrubbed by substitution only; ADR 0009 records the design and replaces `sources.json` named in ADRs 0002/0003

## Findings fixed

- round 1 [blocking] Canada/Quebec/Montreal/CAD targeting unscrubbed: config `targeting` with explicit mappings; criterion 2 captures resolved values
- round 1 [minor] Company names added to Scope In; trigger-phrase examples kept; PR review checks
- round 1 [minor] ADR 0009 notes the `sources.json` replacement in ADRs 0002/0003
- round 1 [minor] Name count corrected
- round 2 [blocking] Mechanical scrub broke parsed/stored literals: explicit handling of the three literals
- round 2 [blocking] Three country rules unmapped: scoring Canadian-location, bare-`$` and outreach region rules mapped, absent behaviour stated
- round 3 [blocking] `typed, <name> to send` never written: parse-only with a name-free pattern
- round 3 [blocking] Old `Questions for <name>` heading vs criterion 1: name-free `Questions for <…>` in the batch prompt
- round 3 [blocking] Unsafe /followup and /batch checks: read-only grep comparisons
- round 3 [minor] Shortlist note change named as Decision 6; fixture divergence noted; README history note; `tests/test_pull_sources.py` in scope
- verify 1 [minor] Which skill parses the typed token corrected; grep check reordered and tied to the skill text

## Plan questions

- Precedence for the career-ops folder (settled in spec: arg, env, config, ask) (§2)
- Exact allowlist entries for the personal-data test, confirmed by running it on the scrubbed tree (§3)
- Do `.personal-terms` list every handle variant (username, GitHub handle, LinkedIn vanity)? (§3)
- Gate records scrubbed as text only, with recorded hashes left as historical values? (§2 Docs)
- Does the worktree get a copy of `config.local.json` for the "after" capture, or is it run on `main` after merge? (§4, criterion 2)

## Open

- none
