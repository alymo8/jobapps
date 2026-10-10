# Gate: Score gate in /batch and posting discovery: design

- **Spec:** docs/superpowers/specs/2026-10-10-score-gate-and-discovery-design.md
- **Spec SHA-256:** 976da917ea9bba5c47f012cc24c76eb567cde69a6dc04069e88ebf37e9610db9
- **Verdict:** pass
- **Date:** 2026-10-10
- **Rounds:** 3 discovery + 2 verification (first run); rerun after a scope change: 3 discovery + 2 verification

## Key decisions

- Discovery supplements the external target lists; it does not replace them.
- Call career-ops' `scan.mjs` as a subprocess; no porting or vendoring, no changes to career-ops system files.
- `scan-history.tsv` is the discovery source, read by position (first 7 columns, formula escaping undone, earliest row per normalized URL), not `pipeline.md`.
- Discover dedupes on normalized URLs (`normalize_url`), including earlier `discovered/*.csv`; `read_postings.py` keeps exact matching. `read_source(path, start_rank=1)` covers xlsx/csv/tsv/txt; `main()` keeps the `dlq.md` and URL branches.
- Low scores are auto-dead-lettered as `LOW-SCORE` without pausing; `LOW-SCORE` joins `NEVER_RETRY`.
- Pay floor: top of posted range below 100k CAD → `PAY-FLOOR`; threshold 3.5; overall = round(0.7 × fit + 0.3 × pay, 1); fit and pay are integers; pay never below 3; third-party estimates on the source page count as posted pay; hourly × 2080; other currencies count as no range.
- Fit bands defined by real gaps (no quoted evidence) and minor gaps (partial evidence); nice-to-have gaps never lower fit; seniority over by more than 2 years is a real gap.
- Legitimacy tiers: Caution signals (over 60 days, boilerplate, repeat), Suspicious signal (title/requirements contradiction); Suspicious = Suspicious signal or 2+ Caution; Suspicious caps at 3.0. Posted date from `- Posted:` or quoted text; `Fetched:` alone does not count.
- Contractor wording is a note only.
- `sonnet` scores with the existing escalation to `opus`; scorer reads `applications.md` and `dlq.md` read-only; no web research.
- `--reason LOW-SCORE` retries from `dlq.md` bypass the gate; a single posting is overridden with its URL plus `--min-score 0 --all`; `--min-score 0` turns off all skipping including `PAY-FLOOR`.
- Missing `## Targeting` that the user declines to add → run continues without 1a.5 (Score `n/a`).
- Both parts ship in one change: the user's accepted override of one-subsystem-per-spec.
- New stdlib `unittest` tests run in CI.
- `CLAUDE.md` and `README.md` are updated in this change (repo rule: update `CLAUDE.md` in the change that makes it stale).
- Postings with `changelog.md` are neither scored nor gated; the gate applies to every other posting reaching it with a `score.md`, from this run or earlier, except overrides.
- A `PAY-FLOOR` posting still gets fit and legitimacy; `score.md` shows `PAY-FLOOR (<capped display score>)`.
- An override that reaches 1b with an ok resume sets its `dlq.md` row to `resolved`; `dlq_skip` uses its own `{CLOSED, INELIGIBLE}` set so resolved `LOW-SCORE` rows aren't held.
- Role-type check: core responsibilities outside `Target roles` cap fit at 2. Seniority uses the lower end of a range. Fit 3 = exactly one real gap (any minor gaps) or no real gap and 2+ minor gaps.
- Bare `$` currency from labels, else location, else USD; with several ranges, the posting's Canadian location (Montreal first), else any Canadian range, else the first.
- Repeats: `applications.md` row with a different `Posting dir`, or `dlq.md` row with a different URL.
- Discovery collapses `added` rows to the earliest per URL before the cut-off.
- `--min-score` is ignored without `## Targeting`; `- Posted:`/`- Published:`/`- Updated:` headers count for age, measured to the scoring date.

## Findings fixed

- round 1 [blocking] Two independent subsystems in one spec: Purpose states their independence and the one-change rationale; Decisions records it.
- round 1 [blocking] Override via `--reason LOW-SCORE` re-dead-letters: added the Override paragraph (those retries skip the gate).
- round 1 [blocking] Scorer inputs exclude files the rubric requires: prompt adds `applications.md` and `dlq.md` read-only.
- round 1 [blocking] score.md example contradicts the scales: integers stated; example now `Fit: 4 | Pay: 5`, `Overall: 4.3`.
- round 1 [blocking] Posting-age signal has no source date: date source named.
- round 1 [blocking] URL-normalization helper does not exist: `normalize_url` and `read_source` specified as new functions.
- round 1 [blocking] scan-history.tsv layout wrong for v1.35: 14 positional columns, escaping, repeated `added` rows described; reader specified.
- round 1 [minor] Story-bank restore off-topic: removed.
- round 2 [blocking] `read_source(path)` cannot keep `main()` unchanged: signature `read_source(path, start_rank=1)`, dlq/URL branches stay in `main()`.
- round 2 [blocking] Fit scale hinges on undefined gaps: real and minor gaps defined.
- round 2 [blocking] posting.md header claim false: Background corrected; `- Posted:` counts; relative dates resolved.
- round 2 [blocking] Career-ops prerequisite out of date: reworded as a check.
- round 2 [minor] DeepMind expectation: "fit 2 or lower, overall below 3.5".
- round 2 [minor] Criterion 3 comparison: "compared with `normalize_url`".
- round 2 [minor] Single-row override: retry-all behaviour stated, `--rows` and per-URL override named.
- round 3 [blocking] Per-URL override filtered out: now `--min-score 0 --all`.
- round 3 [blocking] Legitimacy tiers unmapped: signal list and tier table added.
- round 3 [blocking] Third header style: YAML frontmatter and `- URL 1:` named; scorer reads all three styles.
- round 3 [blocking] career-ops state out of date: `location_filter` marked in place; repair committed as `f6677ed9`.
- round 3 [minor] Fit bands 1 and 2 overlap: band 1 redefined, wins over 2.
- round 3 [minor] Criterion 3 URL extraction: "URLs extracted with `POSTING_URL`".
- verify 1 [blocking] Wrong YAML-frontmatter count: 7, with `apply_url:` in all and `posting_url:` in some.

- rerun round 1 [blocking] CLAUDE.md/README edits out of scope (from the plan gate): added to Scope In.
- rerun round 1 [blocking] Overridden LOW-SCORE stays blocked: `resolved` on success; `dlq_skip` own set.
- rerun round 1 [blocking] PAY-FLOOR score.md undefined: exact lines, Score column and review line.
- rerun round 1 [blocking] changelog postings scored?: neither scored nor gated.
- rerun round 1 [minor] Published/Updated headers; `--min-score` without Targeting.
- rerun round 2 [blocking] DeepMind can't score low: role-type check with `Target roles`.
- rerun round 2 [blocking] bare `$` and several ranges: currency and range-choice rules.
- rerun round 2 [blocking] seniority range: lower end.
- rerun round 2 [minor] URL-less posting.md files noted; dry run outside `/batch` noted.
- rerun round 3 [blocking] repeats self-match: defined per file.
- rerun round 3 [blocking] gate scope for earlier scores: stated.
- rerun round 3 [blocking] cut-off vs collapse order: collapse first.
- rerun round 3 [blocking] fit band one real + minor gaps: defined.
- rerun round 3 [minor] `pay <p>`; PAY-FLOOR cap; Scope lists all read_postings changes; dlq_skip wording.
- rerun verify 1 [blocking] accepted-gap rationale false: reworded to the step-0 confirmation safeguard.

## Plan questions

- Does the gate re-apply an existing `score.md` to the current threshold in a non-override run (e.g. `--all` or a different `--min-score`)? (Gate)
- Does a posting whose scoring fails after the `opus` retry go to `dlq.md` as `FAILED` with stage `score`? (Stage 1a.5)
- Which postings enter 1a.5: those that skipped 1a because `posting.md` existed, and those that already have a `changelog.md`? (Stage 1a.5)
- How do the tests point `read_postings.py`'s `ROOT`/`DLQ` and `discover.py` at fixture files: patched module constants, or a root argument? (Tests and CI)
- Does the CSV `URL` column hold the raw scan-history URL or the normalized one? (Discovery)
- What date does `discovered/.last-run` hold, and is it updated when nothing new is found? (Discovery step 6)
- Which URLs in `applications.md` count for dedupe: any URL in any row, or only the column `statuses()` reads? (Discovery step 4)
- How is criterion 3 checked if the real run finds no new postings (e.g. a larger `--since`)? (Success criteria)
- How are `--exclude` files read, and what about unsupported extensions? (Discovery step 4)
- What order do CSV rows go in? (Discovery step 6)
- Does an empty status count as `added`? (Discovery step 3)
- What happens to a `retried` `LOW-SCORE` row when a run is abandoned before 1b? (Gate)
- What does the Score column show for postings that are not scored? (Gate)
- How is the single-URL override detected so its row gets resolved? (Gate)
- Are `LOW-SCORE` postings listed in both review tables? (`/batch` changes)

## Open

- none
