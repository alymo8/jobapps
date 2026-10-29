# ADR 0009: Shared repo and local config

- **Status:** accepted
- **Date:** 2026-10-28

Amends [ADR 0002](0002-claude-docs-are-the-source-of-truth.md) and
[ADR 0003](0003-claude-code-writes-to-the-profile-doc.md) on one point only: where the source Docs
are listed. Their decisions are otherwise unchanged.

## Context
The repo was one person's workspace: tracked files held the maintainer's name, source Doc links,
shortlist URL, career-ops path, locations and LinkedIn plan. Other job seekers should be able to
clone it, update it with `git pull`, and use it with their own details. Anything a user edits in
normal use therefore has to be untracked, or pulls would conflict, and nothing personal may stay in
tracked files.

## Decision
- The repo is shared and updated by `git pull`.
- Everything personal (source Doc links, shortlist URL, career-ops path, discover locations,
  LinkedIn Premium fallback, targeting) lives in the gitignored `config.local.json`, which replaces
  the tracked `sources.json`. `config.local.json` `sources` replaces the `sources.json` named in
  ADRs 0002 and 0003. `config.example.json` is the tracked template; README "Setup" explains it.
- A CI test, `tests/test_no_personal_data.py`, scans every tracked file for generic personal-data
  patterns, and a gitignored `.personal-terms` list adds the maintainer's own terms on their
  machine, so personal data stays out of tracked files.
- Git history is not rewritten: files are cleaned in normal commits, and the history still holds
  the maintainer's earlier details.

## Consequences
- A new user sets up once from README "Setup" and then only pulls; no merge conflicts from
  personal files.
- A skill that needs `config.local.json` stops with a not-set-up message when it is missing; an
  absent optional key disables only its feature.
- Anyone who can read the repository can read its old commits; the maintainer decides when to make
  it public after reviewing them.
- The maintainer's own behaviour is unchanged, apart from the shortlist note now reading
  "applied by the user on the site".
