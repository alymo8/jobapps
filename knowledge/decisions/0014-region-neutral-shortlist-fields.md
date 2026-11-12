# ADR 0014: Region-neutral shortlist fields, old names still read

- **Status:** accepted
- **Date:** 2026-11-11

## Context
The shortlist schema carried Canada-specific names from its first user: the row field `canada`
(location eligibility) and the count `province_restricted`. Other users would find these
confusing. A rename alone would break live artifacts: a scheduled weekly routine keeps its own
copy of the search prompt and goes on writing the old names, and earlier weeks stay in the
artifact. Separately, `CO_SUFFIX` in `decision_keys.py` (and `index.html`) drops a trailing
`canada` from company names.

## Decision
- New data uses `eligibility` and `region_restricted`. Every reader (`tools/shortlist.py`
  `load_rows`, `templates/shortlist/index.html`) also accepts `canada` and `province_restricted`;
  the restricted chip matches the substring `restricted`, so both "region-restricted" and the
  older "province-restricted" values count.
- `CO_SUFFIX` keeps `canada`. It is harmless for other users ("Acme Canada" matches "Acme"), and
  removing it would change `match_key` for those companies, orphaning recorded decisions, and
  force a re-pin of the keys hash in four places (see the `decision_keys.py` gotcha in
  `CLAUDE.md`).

## Consequences
- Old and new weeks render the same; no migration of artifacts or scheduled routines.
- The fallbacks stay until no artifact holds an old week; removing them is a breaking change.
- `canada` remains in `CO_SUFFIX` by choice; changing it reopens this ADR.
