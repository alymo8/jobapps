# ADR 0004: The shortlist artifact's decisions collection

- **Status:** accepted
- **Date:** 2026-10-18

## Context

A scheduled weekly run in claude.ai publishes the user's job shortlist as an artifact
(its URL is kept in the maintainer's local config). Its page's Applied / Not interested buttons
write documents to the artifact's `decisions` database collection, and the weekly run hides every
posting that matches one (by normalised URL or by company + title key). Postings the user applied to
through Claude Code kept coming back, because Claude Code never told the artifact.

## Decision

- The artifact's `data/CONTRACT.md` and `data/decision_keys.py` are the source of truth for the
  shortlist data and for the decision keys and document ids.
- Claude Code reads `data/*` and writes only to the `decisions` collection (`source: "claude_code"`),
  through `.claude/skills/job-shortlist/SKILL.md`. It never publishes the artifact or changes the
  page, its capabilities or `data/*`; the weekly run owns those.
- `tools/shortlist.py` imports the downloaded `decision_keys.py` by path and is run with
  `python -I`, since the file is downloaded content.
- The apply flow (`/apply`, `/resume`, `/cover-letter`, `/batch`) asks to mark a posting applied.
- When the tools are unavailable, decisions wait in `~/.job-shortlist/pending-decisions.jsonl` and
  are flushed on the next run.

ADR 0003's "Claude Code writes only to the Profile doc" is about the six source Docs and is not
changed.

Rejected: reimplementing the keys in `tools/` (would drift silently from the page's JavaScript if
the contract file changes); recording decisions only in `applications.md` (the weekly run can't
see it).

## Consequences

Decided postings leave next week's list whichever side recorded them. The skill depends on the
Artifact and ArtifactData tools being available in Claude Code; without them decisions queue
locally. A change to the keys file is picked up on the next run; the test fixture is a pinned
snapshot and needs refreshing by hand if the contract file changes.
