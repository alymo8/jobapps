# Gate: Claude Docs as the source of the resume and prompts: design

- **Spec:** docs/superpowers/specs/2026-10-17-claude-docs-sources-design.md
- **Spec SHA-256:** 0d324e8e0f31f79c503fd42b76843aefb407974bf898a8f1da9a1f8b9d06817f
- **Verdict:** pass
- **Date:** 2026-10-17
- **Rounds:** 2 discovery + 0 verification

## Key decisions

- Three Claude Docs become the only source of truth for the mega resume and both prompts; Claude Code only pulls and never writes back; edits happen in claude.ai (Purpose, Scope Out, Decisions)
- Docs chosen over Google Drive or a GitHub repo synced to a claude.ai Project (Decisions)
- Content lives inside one fenced code block per doc, so bytes stay exact; exactly one block is required (Background, Design)
- Pull goes through a saved blob plus an Artifact download, not `export`, so no content passes through the chat (Background, Decisions)
- Each pull deletes the asset and blob it created in the doc (Design, pull procedure step 4)
- Pulled files go to a gitignored `sources/` under fixed, unversioned names; `Resume_prompt_v4.md` and `CoverLetter_prompt_v1.md` are deleted from the repo (Scope, Decisions)
- The pull runs at the start of `/resume`, `/cover-letter`, `/apply`, `/outreach` and `/batch`; only the outermost skill pulls; `/batch` pulls once before fanning out (Design)
- A failed pull stops the run with no stale fallback; a failed clean-up is reported but does not stop the run (Design)
- `.gitignore` widens the v1.5 rule to every `mega-resume-v*.tex` and ignores `sources/`; Aly deletes the old local copies (Scope, Rollout)
- `/followup`, `/discover`, and moving `profile.md`, `stories.md`, `answers.md`, `latex_resume.tex` into docs stay out of scope (Scope Out)
- New ADR 0002 records the Docs-as-source decision (Scope In)

## Findings fixed

- round 1 [blocking] The `/cover-letter` old-name mapping clashes with the stale-path grep: the mapping now names `mega-resume-v<N>.tex` instead of the literal v1.5 file, so criterion 3's grep stays empty.
- round 1 [minor] Live-edit criterion writes to a doc from Claude Code: criterion 5 is marked a one-off verification edit, not shipped behaviour.
- round 1 [minor] `pull-sources.md` sits loose in `.claude/skills/`: Scope In states it is a shared procedure file, not a skill.

## Plan questions

- Should the download leave `out_dir` out (the tool's default folder needs no approval) or set the scratchpad root? (Design, pull procedure step 2)
- Are relative target paths resolved against the cwd or the repo root, and does a write failure return the `{"path","error"}` shape with exit 1? (Design, `tools/pull_sources.py`)
- Is an unclosed fence an error or a block; are trailing spaces on a closing fence tolerated; are `~~~` fences ignored; is `lines` the content line count? (Design, `tools/pull_sources.py`)
- What exact Docs `delete` arguments remove the blob created in step 1, and do the Docs/Artifact tools need loading through ToolSearch first? (Design, pull procedure)
- The Artifact tool asks Aly to confirm each asset delete, so a pull may prompt three times: accept, or drop the asset delete and keep only the blob delete? (Design, pull procedure step 4)
- How does criterion 4 tell pull-created assets and blobs from existing ones (a listing before and after the pulls)? (Success criteria 4)
- What reference is each prompt doc compared against: the deleted tracked file at `main` (CRLF to LF, final newline added) or a separate export? (Success criteria 4)

## Open

- none
