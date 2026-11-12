# ADR 0013: Minimal onboarding; job search as its own skills

- **Status:** accepted
- **Date:** 2026-11-11

Partly supersedes [ADR 0010](0010-onboarding-creates-user-docs-and-shortlist.md) (its onboarding
scope) and amends [ADR 0011](0011-local-source-files-option.md).

## Context
`/onboard` grew to cover prerequisites, a long interview, six sources, config, a career-ops
checkout (Node, `npm install`), the weekly shortlist artifact and its routine or scheduled task,
and a first resume. A new user spent most of the run on job-search setup before seeing a single
resume. career-ops was a second way of finding jobs beside the weekly search prompt, with its own
install and its own config keys (`career_ops_dir`, `discover_locations`).

## Decision
- **Onboarding is minimal:** `/onboard` checks the tools, reads the user's resume, asks a short
  interview (at most 7 topics), writes the six sources and `config.local.json`, and builds a first
  resume. Nothing about finding jobs.
- **Job search is its own skills:** `/scan-jobs` finds postings on demand and writes
  `discovered/<date>.csv`; `/weekly-scan` publishes the shortlist artifact and schedules the weekly
  search (a cloud routine in Docs mode, a local scheduled task in local mode).
- **career-ops is dropped:** Claude searches per `templates/weekly-search-prompt.md` and
  `tools/discover.py --input <rows.json>` only dedupes the rows and writes the CSV.
- **Local files are the default:** sources are six local files (default folder
  `~/jobapps-sources`); Claude Docs are used on `/onboard --docs`.
- **Companies live in the profile:** target and priority companies are in the profile's
  `## Job search` section, not in config.

ADR 0010's creation exception (only the onboarding family creates Docs, artifacts and routines)
now covers `/onboard` (the sources) and `/weekly-scan` (the artifact, routine or scheduled task).

ADR 0011 is amended: local files are the default rather than an option; the local scheduled task is
created by `/weekly-scan`, not `/onboard`; a mode switch happens only on an explicit
`/onboard --docs` or "use local files" request.

## Consequences
- Fewer questions and no Node: a new user reaches a first resume sooner.
- One way of finding jobs, at the cost of Claude usage on every scan.
- Leftover `career_ops_dir` / `discover_locations` keys in an existing config are ignored, never
  deleted; there is no migration.
- `discover.py` does not dedupe against shortlist decisions; `/batch` and `/job-shortlist` keep
  guarding against re-applying.
