# ADR 0003: Claude Code writes to the Profile doc

- **Status:** accepted
- **Date:** 2026-10-18

Supersedes [ADR 0002](0002-claude-docs-are-the-source-of-truth.md).

## Context
ADR 0002 made three Claude Docs (the mega resume and both prompts) the only source of truth, with
Claude Code pulling them and never writing back. The user's profile, stories and answers stayed
local-only, so cover letters written in claude.ai could not use them. The profile is also a file
Claude Code writes: `/apply`, `/batch` and `/followup` save every reusable answer the user gives, and
`/batch` saves the Workday work history and the Targeting section there. The user chose (2026-10-18) to
move all three into docs anyway and let Claude Code write to the Profile doc. A test on a
throwaway doc showed that inserting a line inside a code block with a Docs find-replace, and
deleting it again, changes exactly that line.

## Decision
Six Claude Docs (listed in `sources.json`) are the only source of truth: the mega resume, both
prompts, the profile, the stories and the answers. Each holds its content inside one fenced code
block; skills pull them into gitignored `sources/` before reading (`.claude/skills/pull-sources.md`)
and a failed pull stops the run. Claude Code writes only to the Profile doc (`"writable": true`),
only through `.claude/skills/write-source.md`: pull fresh, make one anchored edit, and verify it by
pulling again. Stories and Answers stay read-only from Claude Code.

## Consequences
- Answers saved during a run reach claude.ai at once; there is one profile, not two.
- A write can collide with the user editing the same doc. The procedure detects it (the Docs find
  fails), retries once from a fresh pull, then stops; it never writes to a local file instead.
- A write that changes anything other than the intended lines is caught by the verify pull and
  reported, not repaired.
- The original root `profile.md`, `stories.md` and `answers.md` are retired (Recycle Bin); their
  `.gitignore` lines stay so a restored copy is never committed.
- As before, each pull leaves a saved copy in each doc (no clean-up; see ADR 0002).
