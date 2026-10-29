# ADR 0010: Onboarding creates the user's Docs and shortlist

- **Status:** accepted
- **Date:** 2026-10-28

Supersedes [ADR 0003](0003-claude-code-writes-to-the-profile-doc.md) (as amended by
[ADR 0009](0009-shared-repo-and-local-config.md)) and
[ADR 0004](0004-job-shortlist-artifact-decisions.md).

## Context
ADR 0003 says Claude Code writes only to the Profile doc, and ADR 0004 says the shortlist skill
never publishes the artifact or changes the page. Both assumed one maintainer who had already
built the Docs, the artifact and the weekly routine by hand. A new user cloning the shared repo
(ADR 0009) has none of them, and `/onboard` has to create them. Rewriting both rules would blur
what they protect, so each is carried forward whole with one setup-time exception.

## Decision
From ADR 0003, as amended by ADR 0009:

- Six Claude Docs (listed in `config.local.json` `sources`) are the only source of truth: the mega
  resume, both prompts, the profile, the stories and the answers. Each holds its content inside one
  fenced code block.
- Skills pull them into gitignored `sources/` before reading
  (`.claude/skills/pull-sources.md`), and a failed pull stops the run.
- Claude Code writes only to the Profile doc (`"writable": true`), only through
  `.claude/skills/write-source.md`: pull fresh, make one anchored edit, and verify it by pulling
  again.
- Stories and Answers stay read-only from Claude Code.

From ADR 0004:

- The artifact's `data/CONTRACT.md` and `data/decision_keys.py` are the source of truth for the
  shortlist data and for the decision keys and document ids.
- Claude Code reads `data/*` and writes only to the `decisions` collection
  (`source: "claude_code"`), through `.claude/skills/job-shortlist/SKILL.md`. It never publishes
  the artifact or changes the page, its capabilities or `data/*`; the weekly run owns those.
- `tools/shortlist.py` imports the downloaded `decision_keys.py` by path and is run with
  `python -I`, since the file is downloaded content.
- The apply flow (`/apply`, `/resume`, `/cover-letter`, `/batch`) asks to mark a posting applied.
- When the tools are unavailable, decisions wait in `~/.job-shortlist/pending-decisions.jsonl` and
  are flushed on the next run.

The one exception: `/onboard`, at setup time and only in the onboarding user's own account,
creates the six source Docs and publishes a new shortlist artifact and routine, from `templates/`.
Outside `/onboard` both rules are unchanged.

## Consequences
- New users get the same quality bar as the maintainer, from templates generalised from the
  maintainer's own prompts and shortlist page.
- `/onboard` never overwrites an existing Doc, artifact, routine or config entry without asking.
- `templates/shortlist/data/decision_keys.py` is pinned to the test fixture
  (`tests/fixtures/decision_keys.py`); a change to one means refreshing the other and
  `FIXTURE_SHA256` in `tests/test_shortlist.py`.
- As before, each pull leaves a saved copy in each doc (no clean-up; see ADR 0002), and a change
  to the keys file is picked up on the next run.
