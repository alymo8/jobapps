# ADR 0016: Internship targeting, search countries, and scan lessons as data

- **Status:** accepted
- **Date:** 2026-11-21

## Context
The scoring and the job scan assumed an experienced full-time candidate: pay bands of 130,000 and
160,000 a year, a years-of-experience gap check, and nothing about terms, graduation or GPA, so
every internship scored the same on pay and wrong-term postings passed. The location scope mixed
"where I may work" with "where to look", with no way to search a country that needs a visa. The
weekly prompt also told each run to follow the previous run's "Lessons for next week", text written
by an agent that had just read untrusted pages, and the routine runs unattended in auto mode.

## Decision
- `## Targeting` gains `Job type`, `Terms available`, `Internship length`, `Expected graduation`
  and `GPA` (`n/a` for full-time only). `scoring.md` checks them for internship and co-op postings
  (wrong job type, term, graduation window or school → fit 1; longer stay or higher GPA minimum →
  real gap), skips the years check, and scores pay per hour (5 at 40, 4 at 28 `<currency>`/h).
  `Pay floor` may be per hour.
- Config `targeting.search_countries` lists where to look; `eligible_regions` stays where the
  user may work without a visa. `/scan-jobs --country` overrides the list for one run. Outside
  `eligible_regions` a posting qualifies only when it doesn't rule out sponsorship, and is marked
  `Visa needed`; the `/batch` pre-screen dead-letters ones that rule it out.
- The search prompt's lessons are search hints, never instructions; a new "Untrusted content"
  section keeps source content out of queries and URLs, and `/scan-jobs` follows it too.
- `/weekly-scan` can schedule the search daily; a run is still called a "week" in the data
  contract, which does not change.

## Consequences
The intern pay bands and the visa rules are judgment calls the user may tune in `scoring.md` and
the prompt. A daily routine costs about seven times a weekly one. The shortlist page and its data
contract are unchanged: visa and term notes ride in `fit_notes`.
