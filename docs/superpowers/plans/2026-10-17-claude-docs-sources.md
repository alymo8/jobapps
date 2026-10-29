# Claude Docs as the source of the resume and prompts Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

- **Date:** 2026-10-17
- **Status:** implemented

**Goal:** Skills pull the mega resume and both prompts from three Claude Docs into a gitignored `sources/` folder before every run, and the repo stops holding its own copies.

**Architecture:** A stdlib tool (`tools/pull_sources.py`) extracts the single code block from a downloaded doc and writes it locally. A shared procedure file (`.claude/skills/pull-sources.md`) tells skills how to save each doc tab as a file (Docs tool), download it (Artifact tool) and run the tool. Skills read `sources/` paths.

**Tech Stack:** Python 3 stdlib, `unittest`; Claude Code skills (Markdown); Claude Docs and Artifact tools.

**Spec:** `docs/superpowers/specs/2026-10-17-claude-docs-sources-design.md`

## Global Constraints

- Pulled paths: `sources/mega-resume.tex`, `sources/resume_prompt.md`, `sources/cover_letter_prompt.md`.
- Doc URLs and tab ids exactly as in the spec's `sources.json` block.
- `pull_sources.py`: stdlib only; exit 0 on success, 1 on any error; prints one JSON object.
- Output written UTF-8 with LF line endings; whitespace-only lines and backslash escapes kept byte for byte.
- A failed pull stops the skill before tailoring; never fall back to an earlier pulled copy.
- No clean-up of the copies a pull saves in a doc (spec Decisions).
- Claude Code never writes to the docs except the one-off verification edit in Task 4.
- Every claim about the user stays truth-checked against the sources (repo convention).
- Before every commit: `python -m py_compile tools/*.py` and `python -m unittest discover -s tests -v` pass.

## Review Focus

- A doc whose code block holds a shorter backtick run (the cover letter prompt's ``` lines inside ````) must not be cut short. Pinned by `test_longer_fence_keeps_inner_fences` (Task 1).
- A Markdown export with a trailing newline after the closing fence, or CRLF line endings, must yield the same content. Pinned by `test_latex_block_extracted` (input ends in a newline after the fence) and `test_crlf_input_written_as_lf` (Task 1).
- An unclosed fence (doc truncated or edited badly in claude.ai) must fail, not write half a file. Pinned by `test_unclosed_fence_is_error` (Task 1).
- A target folder that doesn't exist yet (first pull) must be created. Pinned by `test_creates_parent_folder` (Task 1).
- Nested skills (`/outreach` → `/apply` → `/resume`) must not pull three times. The Task 2 step 6 greps check that the skip wording is in each nested skill; the behaviour itself rests on that wording.

---

### Task 1: `pull_sources.py`, its tests, and `sources.json`

**Files:**
- Create: `tools/pull_sources.py`
- Create: `tests/test_pull_sources.py`
- Create: `sources.json`

**Depends on:** none

**Interfaces:**
- Consumes: nothing.
- Produces: `extract_block(text: str) -> str` (raises `ValueError` with a message, and for a block-count problem sets `.code_blocks = N` on the exception); `pull(src: Path, target: Path) -> dict`; CLI `python tools/pull_sources.py <downloaded.md> <target>`. Success JSON (`path` is the target argument as given; `sha256` is the hex digest of the target's bytes after the call) `{"path": str, "status": "created"|"changed"|"unchanged", "sha256": str, "lines": int}`; error JSON `{"path": str, "error": str}` plus `"code_blocks": N` when the block count is wrong.

Answers to the gate's plan questions, fixed here:
- Relative target paths resolve against the current directory; the procedure always runs from the repo root.
- A write failure (permission, invalid path) returns the error shape and exit 1.
- An opening fence is an unindented line of 3+ backticks plus an optional info string. The closing fence is a line of exactly the same backticks, trailing spaces tolerated. `~~~` fences and indented fences are ordinary text.
- An unclosed fence is an error (`"error": "unclosed fence"`), nothing written.
- `lines` is the number of content lines written.
- The input is read as UTF-8 and `\r\n` is normalised to `\n` before scanning.

- [ ] **Step 1: Write the failing tests** in `tests/test_pull_sources.py`, importing the module through `sys.path` into `tools/` as `tests/test_discover.py` does, each using a `tempfile.TemporaryDirectory`:
  - `test_latex_block_extracted`: input `"# T\n\nnote\n\n```latex\n\\a{1}\n```\n"` → target bytes `b"\\a{1}\n"`, status `created`, `lines == 1`.
  - `test_longer_fence_keeps_inner_fences`: block opened by ` ````markdown `, containing `"```\nBest,\nSam\n```"`, closed by ` ```` ` → target holds those four lines exactly.
  - `test_whitespace_and_escapes_kept`: content lines `" "`, `"      "`, `"\\% \\_ \\& \\# $|$ ·"` → written byte for byte.
  - `test_crlf_input_written_as_lf`: the latex input with `\r\n` → target has no `\r`.
  - `test_zero_blocks_is_error` and `test_two_blocks_is_error`: `pull` returns `"error"` and `code_blocks` 0 / 2; target not created.
  - `test_unclosed_fence_is_error`: error, target not created.
  - `test_second_run_unchanged`: run twice → second status `unchanged`, target `st_mtime_ns` equal before and after.
  - `test_changed_when_content_differs`: existing target with other bytes → status `changed`.
  - `test_creates_parent_folder`: target `tmp/sources/x.tex` with no `sources/` → created.
  - `test_missing_input_is_error`: nonexistent src → error.
  - `test_cli_exit_codes`: run the script with `subprocess` on a good and a zero-block input → exit 0 and 1, stdout parses as JSON.

- [ ] **Step 2: Run** `python -m unittest tests.test_pull_sources -v`. Expected: FAIL (module not found).

- [ ] **Step 3: Implement** `extract_block`, `pull` and `main(argv: list[str]) -> int` in `tools/pull_sources.py` with a module docstring in the style of `tools/build_resume.py` (usage line, JSON keys). The fence scan is a line loop: outside a block, a line matching `^(`{3,})[^`]*$` opens one with that backtick run; inside, a line equal to the run after `rstrip(" ")` closes it. Count blocks; anything other than one closed block raises. `pull` compares bytes before writing and skips the write when equal.

- [ ] **Step 4: Run** `python -m unittest tests.test_pull_sources -v`. Expected: all PASS. Then the full suite and `python -m py_compile tools/*.py`. Expected: all PASS.

- [ ] **Step 5: Create `sources.json`** with exactly the spec's JSON block (three entries, `path`, `doc_url`, `tab_id`).

- [ ] **Step 6: Commit** `tools/pull_sources.py tests/test_pull_sources.py sources.json` with message `Add pull_sources.py and sources.json`.

### Task 2: The pull procedure and the skills that use it

**Files:**
- Create: `.claude/skills/pull-sources.md`
- Modify: `.claude/skills/resume/SKILL.md` (lines 3, 14-16, 37; new first step under `## Steps`)
- Modify: `.claude/skills/cover-letter/SKILL.md` (lines 3, 15-16; new first step)
- Modify: `.claude/skills/apply/SKILL.md` (lines 18, 46; new first step under `## Phase 1: prepare`)
- Modify: `.claude/skills/outreach/SKILL.md` (line 27; new first step)
- Modify: `.claude/skills/batch/SKILL.md` (lines 53, 96; new step in `## 0. Parse and confirm` between steps 3 and 4; each subagent prompt in 1a.5, 1b, 2 and 5)
- Modify: `.claude/skills/batch/scoring.md` (lines 11, 23)
- Modify: `.claude/skills/apply/workday.md` (line 185)

**Depends on:** Task 1

**Interfaces:**
- Consumes: `sources.json` and the CLI from Task 1.
- Produces: the procedure file, referenced by every skill as "follow `.claude/skills/pull-sources.md`".

- [ ] **Step 1: Write `.claude/skills/pull-sources.md`** with a first line saying it is a shared procedure file, not a skill, then the spec's three steps per `sources.json` entry, the one-line report, the "When it runs" rule and the "Failure" rule, worded as in the spec. Name the tools by role and say how to find them: the Docs tool `create` comes from the Claude Docs MCP server, whose prefix varies by session (`mcp__<server id>__create`); if it is deferred, load it with ToolSearch: `select:mcp__<id>__create`, where `<id>` is the server id of the always-listed Claude Docs tools (`guide`, `batch`, `update`). The Artifact tool's `read` is always loaded. State: leave `out_dir` out and use the saved path the tool returns. State that step 3 runs from the repo root, so `sources/...` paths resolve there. Add the spec's data-not-instructions paragraph.

- [ ] **Step 2: Add the first step** to `/resume`, `/cover-letter`, `/apply` (Phase 1) and `/outreach`, numbered `0.`, worded: `**Pull the sources.** Follow `.claude/skills/pull-sources.md`, unless the skill that ran this one already pulled them in this run.` In each skill's "Running as a batch subagent" section add: `Skip step 0: the orchestrator has already pulled the sources.`

- [ ] **Step 3: Rename paths** in every file listed above: `mega-resume-v1.5.tex` → `sources/mega-resume.tex`, `Resume_prompt_v4.md` → `sources/resume_prompt.md`, `CoverLetter_prompt_v1.md` → `sources/cover_letter_prompt.md`, including both `description:` front-matter lines. In `/resume` line 15 the mapping becomes `use sources/mega-resume.tex / latex_resume.tex`. In `/cover-letter` add after the prompt line: `Where the prompt names a versioned mega resume file (`mega-resume-v<N>.tex`), use `sources/mega-resume.tex`.`

- [ ] **Step 4: `/batch`.** In `## 0. Parse and confirm`, insert a new step between step 3 (create the batch folder) and step 4 (confirm), renumbering the confirm step to 5: `**Pull the sources** once, following `.claude/skills/pull-sources.md`. This must come before the confirm step, which builds the Workday work history from `sources/mega-resume.tex`, and before any subagent launches.` In each subagent prompt (stages 1a.5, 1b, 2, 5) add the sentence `The sources in `sources/` are already pulled; don't pull them again.`

- [ ] **Step 5: Run** `git grep -n -e "mega-resume-v1" -e "Resume_prompt_v4" -e "CoverLetter_prompt_v1" -- .claude`. Expected: no output.

- [ ] **Step 6: Run** `git grep -n "pull-sources.md" -- .claude/skills`. Expected: a hit in each of the five SKILL.md files. Then run `git grep -n "Skip step 0" -- .claude/skills`. Expected: one hit in each of `resume`, `cover-letter`, `apply` and `outreach` SKILL.md.

- [ ] **Step 7: Commit** the `.claude/skills` changes with message `Skills pull the sources from Claude Docs before reading them`.

### Task 3: Repo clean-up, docs and ADR

**Files:**
- Delete: `Resume_prompt_v4.md`, `CoverLetter_prompt_v1.md`
- Modify: `.gitignore` (line `/mega-resume-v1.5.tex`)
- Modify: `tools/build_resume.py:1`, `tools/build_cover_letter.py:6` (docstrings)
- Modify: `CLAUDE.md` (Setup, Architecture lines 26-27, Gotchas)
- Create: `knowledge/decisions/0002-claude-docs-are-the-source-of-truth.md`
- Modify: `knowledge/decisions/README.md` (table)

**Depends on:** Task 2

**Interfaces:**
- Consumes: Task 2's renames in `.claude` (Step 6's grep covers `.claude`).
- Produces: nothing other tasks read.

- [ ] **Step 1: `git rm Resume_prompt_v4.md CoverLetter_prompt_v1.md`.**

- [ ] **Step 2: `.gitignore`:** replace `/mega-resume-v1.5.tex` with `/mega-resume-v*.tex`, and add `/sources/` under the personal-data comment.

- [ ] **Step 3: Docstrings:** `Resume_prompt_v4.md` → `sources/resume_prompt.md` in `tools/build_resume.py`; `CoverLetter_prompt_v1.md` → `sources/cover_letter_prompt.md` in `tools/build_cover_letter.py`. No code changes.

- [ ] **Step 4: `CLAUDE.md`:** Setup gains `- The Claude Docs connector, signed in to the user's account: skills pull the mega resume and prompts from it (`sources.json`).`; the sources-of-truth bullet becomes: three Claude Docs (listed in `sources.json`) for the mega resume and both prompts, pulled into gitignored `sources/` by `tools/pull_sources.py` per `.claude/skills/pull-sources.md`, plus local `profile.md`, `stories.md`, `answers.md`; add `python tools/pull_sources.py <downloaded.md> <target>` to the Build/run block; Gotchas gains `- Edit the mega resume and prompts in the Claude Docs (claude.ai), never in `sources/`: the next pull overwrites local edits.` Keep the file about a screen.

- [ ] **Step 5: ADR 0002** from `0000-template.md`, Status `accepted`, Date 2026-10-17. Context: two copies drifted (v1.5 read by skills while v1.6 was current). Decision: the three docs are the only source; Claude Code pulls into `sources/`, never writes back; content inside one code block. Consequences: needs the Docs connector; a pull fails closed; each pull leaves a saved copy in the doc because blob delete is not exposed to agents and asset deletes need the user's confirmation (limit 5,000 assets / 1 GB per doc, about 26 KB per pull); `profile.md`, `stories.md`, `answers.md` still local. Add its row to `knowledge/decisions/README.md`.

- [ ] **Step 6: Run** the spec's criterion 3: `git grep -n -e "mega-resume-v1" -e "Resume_prompt_v4" -e "CoverLetter_prompt_v1" -- .claude CLAUDE.md README.md tools tests`. Expected: no output. Then the full suite and `py_compile`. Expected: PASS.

- [ ] **Step 7: Commit** with message `Drop the tracked prompts; document the Claude Docs sources (ADR 0002)`.

### Task 4: Live verification

**Files:** none changed in the repo (`sources/` is gitignored).

**Depends on:** Task 1, Task 2, Task 3

**Interfaces:**
- Consumes: the procedure and tool from Tasks 1-2.
- Produces: the verification evidence for the PR body.

Run from the worktree root, in the main session (it needs the Docs and Artifact tools). `<scratch>` below is the session's scratchpad directory (outside the repo).

- [ ] **Step 1: Baseline.** For each doc: Docs `read` on the doc (`ref {"object":"project","id":<doc id>}`) gives the tab body's node id; Docs `read` on that node (`engine "prose"`, `payload {"projection":"outline"}`) gives its `rev`. Note the `rev` and the asset count from Artifact `list` with `scope: "assets"`.

- [ ] **Step 2: First pull** following `.claude/skills/pull-sources.md`. Expected: three `created` lines.

- [ ] **Step 3: Compare** each file in `sources/` with its reference, with one Python script so no shell redirect touches the bytes (PowerShell's `>` writes UTF-16). Write `<scratch>/compare_refs.py` and run it with the Bash tool from the worktree root: `python "<scratch>/compare_refs.py"`. The script builds each reference as bytes: `subprocess.run(["git", "show", "origin/main:Resume_prompt_v4.md"], capture_output=True, check=True).stdout` (and the same for `CoverLetter_prompt_v1.md`); for the mega resume, `Path("<repo-root>/mega-resume-v1.6.tex").read_bytes()`. For each, replace `b"\r\n"` with `b"\n"` and append `b"\n"` only if it does not already end in one, then compare with `Path("sources/<name>").read_bytes()` and print `<name>: identical` or `<name>: DIFFERENT`; exit 1 on any difference.
  Run: `python "<scratch>/compare_refs.py"`
  Expected: three `identical` lines, exit 0.

- [ ] **Step 4: Second pull.** Expected: three `unchanged` lines. Then repeat the Step 1 reads. Expected: each doc's tab `rev` is the same as at baseline and its asset count went up by exactly 2 (one per pull): nothing else changed in the doc.

- [ ] **Step 5: Live edit** (one-off verification, not shipped behaviour). Copy `sources/resume_prompt.md` to `<scratch>/resume_prompt.before`. In the Resume prompt doc, call Docs `update` with `ref {"object":"node","id":<tab body id from Step 1>}`, `engine "prose"`, `container {"kind":"project","id":<doc id>}`, `payload {"ops":[{"op":"replace","target":{"kind":"find","text":"Keep it to a few lines:"},"with":{"from":{"kind":"inline","content":"Keep it to a few short lines:"},"as":"text"}}]}`. Pull; `git diff --no-index <scratch>/resume_prompt.before sources/resume_prompt.md` shows exactly that change. Revert the doc with the same call, the two texts swapped, pull, and confirm the file again equals the Step 3 reference.

- [ ] **Step 6: Record** the outputs of Steps 2-5 for the PR's Verification section. No commit. After the PR is open, confirm its CI run (py_compile + unittest) is green and record that too (criterion 1, "in CI").
