# ADR 0002: Claude Docs are the source of truth for the resume and prompts

- **Status:** superseded
- **Date:** 2026-10-17

Superseded by [ADR 0003](0003-claude-code-writes-to-the-profile-doc.md).

## Context
The user edits the mega resume and the resume and cover letter prompts in claude.ai, and Claude Code's
skills read them from this repo. Keeping two copies meant every change was made twice, and they
drifted: on 2026-10-17 the skills read `mega-resume-v1.5.tex` while the current version was a
local, unreferenced v1.6. Claude Docs are reachable from both claude.ai and Claude Code, and a test
showed that LaTeX inside a doc's code block survives an export and an edit from claude.ai byte
for byte.

## Decision
Three Claude Docs (listed in `sources.json`) are the only source of truth for the mega resume and
both prompts. Each holds its content inside one fenced code block. Claude Code never writes to
them: at the start of `/resume`, `/cover-letter`, `/apply`, `/outreach` and `/batch` it pulls each
doc into gitignored `sources/` (`.claude/skills/pull-sources.md`, `tools/pull_sources.py`). The
repo keeps no copies of its own.

## Consequences
- Skills need the Claude Docs connector signed in to the user's account. A pull that fails stops the
  run; there is no fallback to an older copy.
- The pull saves each doc tab as a file inside the doc and downloads it, so the content never
  passes through the conversation. Those saved copies are not cleaned up: deleting a blob is not
  available to agents, and each asset delete needs the user's confirmation. A doc holds up to 5,000
  assets and 1 GB, and a pull adds about 26 KB per doc, so they are harmless for years; the user can
  delete them from a doc at any time.
- Local edits to `sources/` are lost on the next pull; edits belong in claude.ai.
- `profile.md`, `stories.md`, `answers.md` and `latex_resume.tex` are still local-only files.
