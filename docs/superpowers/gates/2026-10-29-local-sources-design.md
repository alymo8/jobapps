# Gate: Local source files as an onboarding option: design

- **Spec:** docs/superpowers/specs/2026-10-29-local-sources-design.md
- **Spec SHA-256:** 476090379f868b5b0f3b2572a26e97657017ea2d9face278f000be3b208013b0
- **Verdict:** pass
- **Date:** 2026-10-29
- **Rounds:** 3 discovery + 1 verification

## Key decisions

- Local mode is offered to anyone at onboarding, no reason needed; Docs stays the default and the Docs path does not change (Purpose, Decision 1)
- Local users' weekly shortlist runs as a desktop-app scheduled task (`weekly-job-report`), only while the app is open, run once at onboarding (Design 6 step 7, Decision 2)
- Local files live in a user-picked folder outside the repo and its worktrees, default `~/jobapps-sources` (Design 2, Decision 3)
- The local pull copies into `sources/`, so downstream skills do not change (Design 3-4, Decision 4)
- Mode is per entry (`local_path` vs `doc_url`), no global key; `/onboard` writes all six in one mode (Design 1, Decision 5)
- Local files have no code fence (Design 1, Decision 6)
- The weekly Excel goes to `<folder>/reports/<week>.xlsx`, via a line local mode appends to the filled prompt (Design 6 step 7, Decision 7)
- The profile stays the only writable source; locally it is edited with the Edit tool through `write-source.md` (Design 5)
- The weekly prompt template's sources line becomes mode-neutral (`<sources list>`), a small wording change for Docs users (Design 7)
- Switching modes is a redo of the storage question: all six entries rewritten whole, the old routine or task disabled only on a yes, old files left in place; migrating content is out of scope (Design 6, Scope Out)
- ADR 0011 widens ADR 0010, which stays accepted (Design 8)
- Tests run in a separate checkout without the maintainer's config, on a new test artifact; clean-up deletes each test object with the user's confirmation (Success criteria)

## Findings fixed

- round 1 [blocking] Template placeholder rename breaks a test outside Scope In: `tests/test_templates.py` added to Scope In
- round 1 [blocking] ADR 0002 is superseded, not accepted: ADR 0011 amends only ADR 0010; Background corrected
- round 1 [blocking] Redo of the local task and onboard Rules unspecified: Rules local equivalents added; task updated in place
- round 1 [minor] README manual-setup fallback: step 2 and 3 local alternatives named
- round 1 [minor] Whitespace-only file test added to the `--local` test list
- round 2 [blocking] Excel had no route to `<folder>/reports/`: local step 7 appends a save line to the filled prompt; also writes `shortlist` to config and stops on a create failure
- round 2 [minor] "Three points" listing four: corrected
- round 2 [minor] pull-sources Failure line covers every `--local` error
- round 2 (plan, settled) test checkout and config isolation written into criterion 2
- round 3 [blocking] Mode switch through redo undefined: "Mode switch" bullet added; Scope Out reworded
- round 3 [minor] Docs step 7.2 placeholder and other Docs-only wording added to Scope In
- round 3 [minor] ADR 0011 states it widens 0010
- verify 1 [minor] Re-used scheduled task stays paused after a switch back: in-place update passes `enabled: true`

## Plan questions

- Does `--local` strip a leading UTF-8 BOM, and convert a lone CR? (Design 3)
- Does local `write-source.md` Read `local_path` before Edit, and how is a CRLF local profile handled against LF anchors? (Design 5)
- Step 1 runs before the mode is known: report both rows as conditional and re-check after step 3? (Design 6 step 1)
- How is "inside the repo or any worktree" detected, and is a missing folder created? (Design 2)
- How does `/onboard` wait for the asynchronous `run_scheduled_task` run, and with what timeout? (Design 6 step 7)
- Which permission mode and tool approvals must the local task have so unattended runs don't stall? (Design 6 step 7, Risks)
- Finding an existing task by artifact URL needs a Read of each task's `SKILL.md`? (Design 6 step 7)
- Does criterion 5 also confirm the run read the six local files and the decisions collection? (Success criterion 5)
- Does the onboard Tools section gain a ToolSearch load of `mcp__scheduled-tasks__*`? (Design 6)
- Does `pull-sources.md`'s title and Tools section change wording? (Design 4)
- Where does criterion 1's maintainer pull run, from a freshly pulled `sources/`? (Success criterion 1)

## Open

- none
