# Profile, stories and answers in Claude Docs Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

- **Date:** 2026-10-18
- **Status:** implemented

**Goal:** Skills read `profile.md`, `stories.md` and `answers.md` from Claude Docs (pulled into `sources/`), and every save to the profile goes to the Profile doc through one verified write procedure.

**Architecture:** Three more entries in `sources.json` reuse the existing pull. A new shared procedure file, `.claude/skills/write-source.md`, makes one anchored find-replace edit in the Profile doc's code block and verifies it by pulling again. Skills and `tools/build_cover_letter.py` switch to the `sources/` paths.

**Tech Stack:** Python 3 stdlib + PyMuPDF (`fitz`), `unittest`; Claude Code skills (Markdown); Claude Docs and Artifact tools.

**Spec:** `docs/superpowers/specs/2026-10-18-claude-docs-profile-design.md`

## Global Constraints

- New paths: `sources/profile.md`, `sources/stories.md`, `sources/answers.md`.
- Doc URLs, tab ids and the profile's `node_id` exactly as in the spec's Background table.
- Only the Profile doc is ever written by Claude Code, only through `.claude/skills/write-source.md`.
- A write conflict retries once from a fresh pull, then stops; never write an answer to a local file.
- Batch subagents never write the profile; the orchestrator does.
- Never commit personal files (`sources/`, `postings/`, root `profile.md`, `stories.md`, `answers.md`).
- Before every commit: `python -m py_compile tools/*.py` and `python -m unittest discover -s tests -v` pass.

## Review Focus

- `build_cover_letter.py` run before any pull (no `sources/profile.md`): must give the JSON error, not a traceback, and write no `.tex`. Pinned by `test_missing_profile_is_json_error` (Task 1).
- `--check` must keep working with no profile at all (it never reads it). Pinned by `test_check_needs_no_profile` (Task 1).
- A save whose anchor line is not unique must not edit the wrong place. Settled in `write-source.md` step 2 (Task 2): multi-line anchor, else stop.
- Several answers in one reply must each be verified. Settled in `write-source.md` (Task 2): one run per answer.
- A `--dry-run` of `/followup` must not write the Profile doc. Checked by Task 3 step 4's wording.

---

### Task 1: `build_cover_letter.py` reads the pulled profile; tests; CI installs PyMuPDF

**Files:**
- Modify: `tools/build_cover_letter.py:61-62` (`PROFILE`, its comment), `:86` (docstring), `main` (missing-profile check)
- Create: `tests/test_build_cover_letter.py`
- Modify: `.github/workflows/ci.yml` (a `pip install pymupdf` step before `py_compile`)

**Depends on:** none

**Interfaces:**
- Consumes: nothing.
- Produces: `PROFILE: Path` = `<repo>/sources/profile.md`; `MISSING_PROFILE: str` = `"sources/profile.md missing: pull the sources first (.claude/skills/pull-sources.md)"`.

Answers to the gate's plan questions, fixed here: the missing-profile check is the first thing in `main`'s non-`--check` branch, before the `.tex` is written or `compile_tex` runs. The error report keeps `md`, `words`, `greeting_ok`, `signoff_ok`, sets `"ok": false`, adds `"error": MISSING_PROFILE`, is printed as usual, and `main` returns 1.

- [ ] **Step 1: Write the failing tests** in `tests/test_build_cover_letter.py`, skipped like `tests/test_build_resume.py` when `fitz` is missing (`@unittest.skipUnless(HAS_FITZ, ...)`, importing the module inside each test). Use a temp dir, a letter `cover_letter.md` of 320 words starting `Dear hiring team,` and ending `Best,\nAly`, placed at `<tmp>/Acme-1/cover_letter.md`:
  - `test_profile_path`: `build_cover_letter.PROFILE.as_posix().endswith("sources/profile.md")`.
  - `test_contact_reads_contact_section`: with `PROFILE` patched (`unittest.mock.patch.object`) to a temp file holding `## Contact` with `- Full name: A B`, `- Phone: 1`, `- Email: a@b.c`, `- Location: Montreal, QC, Canada`, `- LinkedIn: https://www.linkedin.com/in/x`, `- GitHub: https://github.com/y`, then `## Eligibility`: `contact() == {"name": "A B", "phone": "1", "email": "a@b.c", "city": "Montreal", "linkedin": "https://www.linkedin.com/in/x", "github": "https://github.com/y", "linkedin_bare": "www.linkedin.com/in/x", "github_bare": "github.com/y"}`.
  - `test_missing_profile_is_json_error`: `PROFILE` patched to a missing path; `main([letter])` (stdout captured) returns 1; the JSON has `"ok": false`, `"error"` equal to `MISSING_PROFILE`, and `"words"`; no `.tex` exists in `<tmp>/Acme-1/`.
  - `test_check_needs_no_profile`: `PROFILE` patched to a missing path; `main([letter, "--check"])` returns 0 and the JSON has no `"error"`.

- [ ] **Step 2: Run** `python -m unittest tests.test_build_cover_letter -v`. Expected: `test_profile_path` and `test_missing_profile_is_json_error` FAIL (`PROFILE` still at the repo root, no `MISSING_PROFILE`); `test_contact_reads_contact_section` and `test_check_needs_no_profile` already pass.

- [ ] **Step 3: Implement.** `PROFILE = Path(__file__).resolve().parent.parent / "sources" / "profile.md"`, comment `# Contact details come from the pulled Profile doc (gitignored sources/), not the repo.`; docstring of `contact()` names `sources/profile.md`; `MISSING_PROFILE` constant; the check in `main` as described above.

- [ ] **Step 4: Run** `python -m unittest tests.test_build_cover_letter -v`, then the full suite and `python -m py_compile tools/*.py`. Expected: all PASS.

- [ ] **Step 5: CI.** In `.github/workflows/ci.yml`, add `- run: pip install pymupdf` right after `actions/setup-python`. No other change.

- [ ] **Step 6: Commit** `tools/build_cover_letter.py tests/test_build_cover_letter.py .github/workflows/ci.yml` with message `build_cover_letter reads the pulled profile; CI installs PyMuPDF`.

### Task 2: `sources.json`, `pull-sources.md`, and the write procedure

**Files:**
- Modify: `sources.json` (append three entries)
- Modify: `.claude/skills/pull-sources.md` (lines 3-4 skill list, lines 6-9 intro, the "When it runs" list, the Failure wording, a new mapping paragraph)
- Create: `.claude/skills/write-source.md`

**Depends on:** none

**Interfaces:**
- Consumes: the pull procedure and `tools/pull_sources.py` as they are.
- Produces: `.claude/skills/write-source.md`, referenced by Task 3 as "through `.claude/skills/write-source.md`".

- [ ] **Step 1: `sources.json`:** append exactly the spec's three entries (profile with `"node_id": "<node_id>", "writable": true`). Run: `python -c "import json;print(len(json.load(open('sources.json'))['sources']))"`. Expected: `6`.

- [ ] **Step 2: `pull-sources.md`:**
  - Opening skill list: add `/followup`.
  - Intro: "The mega resume, both prompts, and the user's profile, stories and answers live in six Claude Docs that the user edits in claude.ai". Add: "Claude Code writes only to the Profile doc, and only through `.claude/skills/write-source.md`."
  - "When it runs": add `/followup` to the list.
  - Failure: "stop before tailoring anything" becomes "stop before doing anything else".
  - New paragraph, the mapping sentence on ONE line, worded exactly: `Pulled files may name other sources by their old names (`profile.md`, `stories.md`, `answers.md`, a versioned `mega-resume-v<N>.tex`, `CoverLetter_prompt_v1.md`, `Resume_prompt_v4.md`). Each means the matching file in `sources/`.`

- [ ] **Step 3: Write `.claude/skills/write-source.md`.** First line: a shared procedure file, not a skill. Then the spec's five steps, with these settled details (answers to the gate's plan questions):
  - Scope: only entries with `"writable": true` in `sources.json` (today the profile). One run per change: a reply with several reusable answers is several runs, in sequence, one "Saved to profile" line each.
  - Step 1: pull that one entry per `pull-sources.md`; copy the result to `<scratchpad>/profile.before.md`.
  - Step 2, anchor: the last line of the target section (a new answer), the heading line (an empty section), or the file's last line (a new section). It must occur exactly once in the pulled file (count it). If not, extend the anchor upward one line at a time (multi-line find text, ending with the anchor line) until the text occurs once; if the section start is reached first, stop and tell the user. Never use the `nth` option.
  - Step 3, the call (verified 2026-10-18): Docs `update` with `ref {"object":"node","id":<node_id>}`, `engine "prose"`, `container {"kind":"project","id":<doc id>}`, `payload {"ops":[{"op":"replace","target":{"kind":"find","text":"<old text>"},"with":{"from":{"kind":"inline","content":"<new text>"},"as":"text"}}]}`. Both texts are whole lines, each ending in a newline (written `\n` inside the JSON string, which is a real line break in the doc). For an insert, `<new text>` is the old text plus the new lines; for a line replace, the old line and its replacement.
  - Step 4, check: pull again, then `git diff --no-index -U0 <scratchpad>/profile.before.md sources/profile.md`. It exits 1 when the files differ (expected). Ignoring the `---`/`+++` header lines and the `@@` hunk lines, the `+`/`-` lines must be exactly the intended added and removed lines, nothing else.
  - Step 5: the spec's failure rules, word for word in meaning.
  - New answers use `- <question>: <answer> (the user, YYYY-MM-DD)` with today's date.

- [ ] **Step 4: Run** `git grep -n "write-source.md" -- .claude/skills/pull-sources.md`. Expected: one hit. Run `git grep -n "by their old names" -- .claude/skills/pull-sources.md`. Expected: one hit, and that line also contains `answers.md`.

- [ ] **Step 5: Commit** `sources.json .claude/skills/pull-sources.md .claude/skills/write-source.md` with message `Pull profile, stories and answers; add the profile write procedure`.

### Task 3: Skills read the new paths and save through the write procedure

**Files:**
- Modify: `.claude/skills/apply/SKILL.md` (lines 20-22, 34, 43, 45, 47-49, 94)
- Modify: `.claude/skills/apply/workday.md` (every `profile.md`; line 185 "local-only")
- Modify: `.claude/skills/batch/SKILL.md` (lines 55, 59, 99, 177, 209, 213, 221)
- Modify: `.claude/skills/batch/scoring.md` (line 12)
- Modify: `.claude/skills/cover-letter/SKILL.md` (lines 3, 18)
- Modify: `.claude/skills/followup/SKILL.md` (lines 22-24 `--dry-run`, 106-107, 149, 198; new `## 0. Pull the sources` before `## 1. Collect`)

**Depends on:** Task 2

**Interfaces:**
- Consumes: `.claude/skills/write-source.md` and `.claude/skills/pull-sources.md` from Task 2.
- Produces: nothing other tasks read.

- [ ] **Step 1: Paths.** In every file above: `profile.md` → `sources/profile.md`, `stories.md` → `sources/stories.md`, `answers.md` → `sources/answers.md`, including `description:` lines. In `workday.md` line 185, drop ", local-only".

- [ ] **Step 2: Saves.** Each sentence that saves to the profile ends with "through `.claude/skills/write-source.md`": `/apply` line 49 ("Save each answer that is reusable into `sources/profile.md` under the right heading"); `/batch` lines 177, 213, 221, the Workday history save (line 57, "save it on the user's approval") and the Targeting add (line 59-60); `/followup` line 149. Also `apply/workday.md` line 187 ("saved only after the user approves"), the Workday history save in a normal `/apply` run. Each batch-subagent section keeps its rule that subagents never write it.

- [ ] **Step 3: `/followup` step 0.** Insert before `## 1. Collect`: `## 0. Pull the sources` with one line: `Follow `.claude/skills/pull-sources.md`.`

- [ ] **Step 4: `/followup --dry-run`.** The bullet becomes: `--dry-run`: steps 0–4 only. Writes only `sources/` (the pull) and `batches/<id>-followup/`; no `outreach.md` or `applications.md` edits and no Profile doc writes; nothing sent, nothing clicked that sends, connects or withdraws. Report the questions.txt path in chat; do not open it.

- [ ] **Step 5: Run** `git grep -n -E "(^|[^/_a-z])(profile|stories|answers)\.md" -- .claude | grep -v "by their old names"`. Expected: no output. Run `git grep -c "write-source.md" -- .claude/skills`. Expected: at least one hit in each of `apply/SKILL.md`, `apply/workday.md`, `batch/SKILL.md`, `followup/SKILL.md`.

- [ ] **Step 6: Commit** the `.claude/skills` changes with message `Skills read the pulled profile, stories and answers and save through write-source`.

### Task 4: Docs, ADRs and the earlier spec's status

**Files:**
- Modify: `CLAUDE.md` (Architecture sources-of-truth bullet; line 35, the `/batch` stage 1a.5 bullet; Gotchas contact-header line)
- Create: `knowledge/decisions/0003-claude-code-writes-to-the-profile-doc.md`
- Modify: `knowledge/decisions/0002-claude-docs-are-the-source-of-truth.md` (Status)
- Modify: `knowledge/decisions/README.md` (0002 status, 0003 row)
- Modify: `docs/superpowers/specs/2026-10-17-claude-docs-sources-design.md`, `docs/superpowers/plans/2026-10-17-claude-docs-sources.md` (Status)
- Modify: `docs/superpowers/README.md` (regenerated)

**Depends on:** Task 3

**Interfaces:**
- Consumes: nothing.
- Produces: nothing other tasks read.

- [ ] **Step 1: `CLAUDE.md`.** Sources-of-truth bullet: six Claude Docs (listed in `sources.json`) for the mega resume, both prompts, profile, stories and answers, pulled into gitignored `sources/` per `.claude/skills/pull-sources.md`; Claude Code writes only to the Profile doc, through `.claude/skills/write-source.md` ([ADR 0003](knowledge/decisions/0003-claude-code-writes-to-the-profile-doc.md)). Line 35 (`/batch` stage 1a.5 bullet): `profile.md` → `sources/profile.md`. Gotcha line: `build_cover_letter.py` reads the letter header from the `## Contact` bullets of `sources/profile.md` (pull first); keep those keys when editing the Profile doc. Keep the file about a screen.

- [ ] **Step 2: ADR 0003** from `0000-template.md`, Status `accepted`, Date 2026-10-18, with the spec's "ADR 0003" paragraph as Context/Decision/Consequences. ADR 0002: Status `superseded` and a line under it: `Superseded by [ADR 0003](0003-claude-code-writes-to-the-profile-doc.md).` README: 0002's status `superseded`; new row `| [0003](0003-claude-code-writes-to-the-profile-doc.md) | Claude Code writes to the Profile doc | accepted | 2026-10-18 |`.

- [ ] **Step 3: Earlier spec and plan.** Status `implemented` in both 2026-10-17 files. Run: `python %USERPROFILE%/.claude/skills/claude-kit/scripts/spec-index.py docs/superpowers`. Expected: `docs/superpowers/README.md` shows both 2026-10-17 rows `implemented`.

- [ ] **Step 4: Run** the spec's criterion 3: `git grep -n -E "(^|[^/_a-z])(profile|stories|answers)\.md" -- .claude tools CLAUDE.md | grep -v "by their old names"`. Expected: no output. Then the full suite and `py_compile`. Expected: PASS.

- [ ] **Step 5: Commit** with message `Document the profile docs and write-back (ADR 0003); mark the first sources change implemented`.

### Task 5: Live verification

**Files:** none changed in the repo (`sources/` is gitignored).

**Depends on:** Task 1, Task 2, Task 3, Task 4

**Interfaces:**
- Consumes: the procedures and tools from Tasks 1-3.
- Produces: the verification evidence for the PR body.

Run from the worktree root, in the main session (it needs the Docs and Artifact tools). `<scratch>` is the session's scratchpad directory. The main checkout is `<repo-root>`.

- [ ] **Step 1: Pull** all six entries per `.claude/skills/pull-sources.md`. Expected: six report lines, none an error.

- [ ] **Step 2: Compare** the three new files with the main checkout's root files, using one Python script run with the Bash tool (no shell redirects): for each of `profile.md`, `stories.md`, `answers.md`, read `<repo-root>/<name>` as bytes, replace `b"\r\n"` with `b"\n"`, add a final `b"\n"` only if missing, compare with `sources/<name>`; print `identical` or `DIFFERENT`; exit 1 on any difference.
  Run: `python "<scratch>/compare_profile_refs.py"`
  Expected: three `identical`, exit 0.

- [ ] **Step 3: Live write** per `.claude/skills/write-source.md`: add `- Write-back test: remove me (the user, 2026-10-18)` after the last line of `## Common questions` (today: `- Years of Gen AI development experience: 3 (the user, 2026-10-14)`). Expected: step 4's `git diff --no-index -U0` shows exactly one `+` line, that line.

- [ ] **Step 4: Remove it**: Docs `update` with the same `ref`, `engine` and `container` as `write-source.md` step 3, and `payload {"ops":[{"op":"delete","target":{"kind":"find","text":"- Write-back test: remove me (the user, 2026-10-18)\n"}}]}`, pull the profile, and rerun Step 2's script. Expected: three `identical`.

- [ ] **Step 5: Header.** Copy one existing `postings/<dir>/cover_letter.md` from the main checkout to `<scratch>/HeaderTest-1/cover_letter.md`.
  Run: `python tools/build_cover_letter.py "<scratch>/HeaderTest-1/cover_letter.md"`
  Expected: `"ok": true`, `"pages": 1`; Read the PNG it names and see the name, phone, email, Montreal, LinkedIn and GitHub. Then rename `sources/profile.md` to `sources/profile.md.off`, run the same command: expected exit 1 and `"error"` = the missing-profile message; rename it back.

- [ ] **Step 6: Record** the outputs for the PR's Verification section; after the PR opens, record its green CI run (criterion 1). No commit.

## After merge (part of `/ship` clean-up)

Once local `main` is fast-forwarded to the merge: move `<repo-root>/profile.md`, `stories.md` and `answers.md` to the Recycle Bin (PowerShell, once per file: `Add-Type -AssemblyName Microsoft.VisualBasic; [Microsoft.VisualBasic.FileIO.FileSystem]::DeleteFile('<path>', 'OnlyErrorDialogs', 'SendToRecycleBin')`). Expected: none of the three exists; the `.gitignore` lines for them stay.
