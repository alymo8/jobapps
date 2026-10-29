# ADR 0011: Local source files as an onboarding option

- **Status:** accepted
- **Date:** 2026-10-29

Amends ADR 0010 on four points; 0010 stays accepted. This widens
[ADR 0010](0010-onboarding-creates-user-docs-and-shortlist.md) rather than reversing or narrowing
it. [ADR 0002](0002-claude-docs-are-the-source-of-truth.md) (superseded) is background only.

## Context
ADR 0010 has `/onboard` create six Claude Docs as the user's sources of truth, a cloud routine for
the weekly shortlist, and Claude Code writing only to the Profile doc. Some users would rather keep
their resume, prompts, profile, stories and answers as plain files on their own machine, without
the Claude Docs connector. The rest of the repo reads only the pulled copies in `sources/`, so the
storage of the sources can vary without touching the skills that use them.

## Decision
Four points of ADR 0010's Decision change:

- The source of truth is six Claude Docs **or** six local files outside the repo, chosen at
  onboarding.
- Local files hold their content without a fenced code block.
- Claude Code writes only to the profile source (Doc or local file), only through
  `.claude/skills/write-source.md`.
- In local mode `/onboard` creates a local scheduled task (Claude desktop app) instead of a cloud
  routine for the weekly shortlist.

And:

- Mode is per entry (`local_path` vs `doc_url` in a `config.local.json` `sources` entry); there is
  no global mode key.
- Local files live in a folder the user picks, outside the repo and its worktrees.
- The local pull (`python tools/pull_sources.py --local <local file> <target>`) copies into
  `sources/`, so downstream skills are unchanged.

## Consequences
- The Docs path is unchanged; no existing config needs editing.
- Local files have no version history: the user backs them up.
- The weekly task runs only while the desktop app is open.
- Switching mode is a re-run of `/onboard`.
