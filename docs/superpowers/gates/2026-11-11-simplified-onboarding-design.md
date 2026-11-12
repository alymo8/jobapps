# Gate: Simplified onboarding; job search as its own skills: design

- **Spec:** docs/superpowers/specs/2026-11-11-simplified-onboarding-design.md
- **Spec SHA-256:** f76d48246482d0f6d3ab2e3f6239c528bb35e39f7f6cadceaddf05426f3ef1ea
- **Verdict:** pass
- **Date:** 2026-11-11
- **Rounds:** 3 discovery + 0 verification

## Key decisions

- Onboarding cut to tool check, resume, short interview (7 topics), write sources, first resume; career-ops setup and the shortlist/routine leave `/onboard`.
- Job finding moves to `/scan-jobs` (on demand) and `/weekly-scan` (scheduled, publishes the shortlist); `/discover` is deleted.
- career-ops dropped entirely; the scanner is Claude following `templates/weekly-search-prompt.md`.
- Local files become the default storage, Claude Docs only on request (`--docs`); re-runs keep the configured mode, a switch needs an explicit request (author's call).
- Target and priority companies live in a new profile `## Job search` section; `Locations` is added to `## Targeting`; `/scan-jobs` and `/weekly-scan` ask for missing ones.
- `tools/discover.py` kept as a JSON-input dedupe and CSV step; `--since`/`.last-run`/career-ops removed; no dedupe against shortlist decisions added.
- No migration: leftover `career_ops_dir` / `discover_locations` keys are ignored.
- Interview no longer asks score threshold (default 3.5), currency/phone country (inferred), LinkedIn Premium (asked by LinkedIn runs as today), companies, eligibility/compensation (asked by `/apply`) or stories.
- New ADR 0013 partly supersedes ADR 0010, amends ADR 0011, and extends 0010's creation exception to `/weekly-scan`.

## Findings fixed

- round 1 [blocking] `--since` and ranking order undefined for JSON input: cut-off removed; Rank = input order after dedupe.
- round 1 [blocking] Shortlist-decision dedupe unspecified: dropped (dedupe sources as today).
- round 1 [blocking] Criterion 2 failed on ADR 0013: ADR 0013 and its index row allowed.
- round 1 [blocking] ADR 0011 narrowed but not amended: ADR 0013 now amends 0011.
- round 1 [blocking] Re-run / mode switch undefined: mode read from config and kept; explicit switch only; `$ARGUMENTS` = `[--docs] [step]`.
- round 1 [blocking] Sample resume fixture missing: `tests/fixtures/sample-resume.md` added; walkthrough uses a scratch folder.
- round 1 [minor] scoring.md change: now unchanged. Criterion 4 rephrased as a `discover.py` test. ADR 0013 mentions the profile schema change. USD rate, Docs prereq row, URL-less rows settled.
- round 2 [blocking] LinkedIn Premium "written to config" false: now asked by LinkedIn runs as today, not written.
- round 2 [blocking] Tool check let onboarding continue without PyMuPDF: missing fitz now stops.
- round 2 [blocking] `/weekly-scan` source for roles/locations: from profile, asked and saved when missing.
- round 2 [blocking] `/scan-jobs` with missing `Locations`: asked and saved before searching.
- round 2 [blocking] `/job-shortlist` pointed at `/onboard`: message now says `/weekly-scan`.
- round 2 [minor] Purpose step list corrected; local-mode-testing knowledge docs added; manual `/scan-jobs` criterion added.
- round 3 [minor] Score threshold attribution form stated; routine company copy note; criterion 4 empty-result rerun; ADR index Status values given.

## Plan questions

- Does step 4 keep today's post-pull `write-source.md` run (writability proof) for the score threshold? (/onboard step 4)
- Is `location` optional in JSON rows while `company`, `title`, `url` are required? (tools/discover.py)
- Which weekly-prompt sections beyond those listed does `/scan-jobs` follow (Respect my decisions, Scale cap, Before you start, What to flag), and does it read the mega resume? (/scan-jobs)
- Where does `Locations` go in the Targeting key order, and does `/batch`'s offered Targeting key list gain it? (Other files)
- Is `## Job search` added in one `write-source.md` run with both lines? (/scan-jobs)
- Does Docs mode write exactly `sources` and `targeting` to config? (/onboard step 4)
- Separate imports for PyMuPDF and openpyxl in the tool check? (/onboard step 1)
- With no rows left, keep `no new postings` and no CSV, and `/scan-jobs` stops? (tools/discover.py, /scan-jobs)
- Does an onboarding re-run add a missing `Locations` line? (/onboard)
- `/weekly-scan` local `<folder>` = common parent of the `local_path` entries? (/weekly-scan)

## Open

- none
