# Plan gate: Score gate in /batch and posting discovery Implementation Plan

- **Plan:** docs/superpowers/plans/2026-10-10-score-gate-and-discovery.md
- **Plan SHA-256:** 58894c0d54b857fa058af53e92a16014318c5209b588d3c7c59a94b02b6cf577
- **Spec:** docs/superpowers/specs/2026-10-10-score-gate-and-discovery-design.md
- **Spec SHA-256:** 976da917ea9bba5c47f012cc24c76eb567cde69a6dc04069e88ebf37e9610db9
- **Verdict:** pass-with-decisions
- **Date:** 2026-10-10
- **Rounds:** 2 discovery + 1 verification (the spec was re-gated between the two discovery rounds)
- **Decisions approved:** 2026-10-10

## Plan-introduced decisions

Approved under Aly's standing instruction for this change: "ship all autonomously, take the recommended decision".

- `discover.py` gains a `--root PATH` flag and a `main(argv, today=None)` signature, used by the tests and by Task 5 to run from the worktree against the main checkout's data.
- `read_postings.py` tests patch the module constants `ROOT` and `DLQ`.
- A posting whose scoring is still garbled after the `opus` retry is dead-lettered `FAILED`, stage `score`.
- 1a.5 includes LIVE postings that skipped 1a because `posting.md` already existed.
- The Score column shows `-` for `changelog.md` postings (`n/a` when `## Targeting` is missing).
- A single-URL override is detected as `dlq == "LOW-SCORE"` in a `--min-score 0` run; such a posting's row is resolved after an ok resume.
- `LOW-SCORE` postings appear only in "Skipped on score", not in the dead-lettered table.
- A `retried` `LOW-SCORE` row from an abandoned run is left as is; the next normal run picks the URL up and re-gates it.
- The CSV `URL` column holds the raw (unescaped) scan-history URL.
- `.last-run` holds the local run date and is written only when a CSV is written.
- Every `http(s)` URL anywhere in `applications.md` counts for dedupe.
- `--exclude` takes several files after one flag (and can be repeated); files are read with `read_source` (unknown extensions as text files of URLs), or `dlq_rows` for a file named `dlq.md`.
- CSV rows are ordered by `first_seen`, oldest first.
- An empty status counts as `added`.
- `normalize_url` also drops the URL fragment.
- A missing `data/scan-history.tsv` exits 1.
- If the real discovery run finds nothing new, criterion 3 is checked with `--no-scan --since 60`.
- Outside `/ship`, pushing the branch and opening the PR needs Aly's approval first.

## Findings fixed

- round 1 [blocking] `test_dedupe_sources` fixture used `HTTPS://`: changed to `https://D.EXAMPLE/2/`.
- round 1 [blocking] Criterion 3 overlap check tautological: `known` built only from applications.md, dlq.md and posting.md URLs.
- round 1 [blocking] CI pass unchecked: Task 5 Step 7 watches `gh pr checks`.
- round 1 [blocking] CLAUDE.md/README edits out of spec scope: spec amended and re-gated.
- round 1 [blocking] career-ops prerequisite and `location_filter` check missing: Task 5 Step 4 added.
- round 1 [minor] override flag in review; DLQ bullet insertion point; `discovered/` untracked note.
- (spec re-gate changes carried into the plan: `dlq_skip` own set and resolved-row test; PAY-FLOOR `score.md` lines; role-type check and `Target roles`; currency and range rules; seniority lower end; collapse-then-cut-off with a re-added-URL test; fit band 3; repeats per file; gate scope.)
- round 2 [blocking] test counts: 9 + 11, `Ran 20 tests`.
- round 2 [blocking] dry-run expectation: always-printed banner, exit 0.
- round 2 [minor] CLAUDE.md Gotchas line; `--exclude` `action="extend", nargs="+"`; Task 1 Step 2 failure text; ask before push outside `/ship`.

## Open

- none
