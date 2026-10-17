# Claude Docs as the source of the resume and prompts: design

- **Date:** 2026-10-17
- **Status:** approved

## Purpose

Aly keeps the mega resume and the two prompts in two places: this repo (read by Claude Code's
skills) and claude.ai (where Aly prefers to edit them, since that is the tool meant for writing).
Every change has to be made twice, and the copies drift: on 2026-10-17 the skills still read
`mega-resume-v1.5.tex` while Aly's current version was a local, unreferenced `mega-resume-v1.6.tex`.

Fix: three Claude Docs become the only source of truth. Aly edits them in claude.ai (through
claude.ai skills Aly sets up separately). Claude Code pulls them into a gitignored `sources/`
folder at the start of every skill run that needs them, and the repo stops holding its own copies.

## Background (current state)

The three docs already exist, are private to Aly, and hold the content inside one fenced code
block each (the text above the block is a note for humans):

| Local file (new path)            | Doc                                                                 | Tab id          | Fence          |
| -------------------------------- | ------------------------------------------------------------------- | --------------- | -------------- |
| `sources/mega-resume.tex`        | Mega resume, `https://claude.ai/code/artifact/2d814730-1e3a-476b-8907-513ce73180c9`        | `958ab5d7-5d85` | ` ```latex `   |
| `sources/resume_prompt.md`       | Resume prompt, `https://claude.ai/code/artifact/74f55490-bd25-435e-a000-8409aeefe485`      | `bf5ae186-02f7` | ` ```markdown ` |
| `sources/cover_letter_prompt.md` | Cover letter prompt, `https://claude.ai/code/artifact/20c152e4-070a-4203-9bfa-14663ed5ef74` | `9c169abe-1e8c` | ` ````markdown ` (the prompt contains ``` fences) |

Verified on 2026-10-17:

- **Fidelity.** Each doc's code block, exported, equals its source file byte for byte once CRLF is
  normalised to LF and a final newline added (the Mega resume doc holds `mega-resume-v1.6.tex`).
  Whitespace-only lines, `\%`, `\&`, `\_`, `\#`, `$|$` and `·` survive.
- **Edits from claude.ai survive.** An edit made by Claude in claude.ai inside the code block of a
  test doc changed exactly the requested words and nothing else.
- **Pull route with no chat cost.** In Claude Code, the Docs tool `create` (object `blob`, engine
  `blob`, payload `{"from": {"object": "file", "id": <tab id>}, "format": "markdown"}`, container
  `{"kind": "project", "id": <doc id>}`) saves the tab as a Markdown file and returns an asset id;
  the Artifact tool `read` (`url` = the doc URL, `path` = the asset id, `out_dir` = a scratch folder)
  downloads it to disk. File content never passes through the conversation.

Files that read the sources today: `.claude/skills/{resume,cover-letter,apply,outreach,batch}/SKILL.md`,
`.claude/skills/batch/scoring.md`, `.claude/skills/apply/workday.md`, `CLAUDE.md`, and the
docstrings of `tools/build_resume.py` and `tools/build_cover_letter.py`. `Resume_prompt_v4.md` and
`CoverLetter_prompt_v1.md` are tracked; `mega-resume-v1.5.tex` is gitignored; `mega-resume-v1.6.tex`
exists locally and is not ignored on `main`.

## Scope

**In:**

- `sources.json` (new, tracked): the three entries in the table above (`path`, `doc_url`, `tab_id`).
- `tools/pull_sources.py` (new): extracts the code block from a downloaded doc and writes it to its
  local path.
- `.claude/skills/pull-sources.md` (new): the pull procedure the skills follow. A shared
  procedure file, not a skill (it has no folder or `SKILL.md`, so it is never offered as `/pull-sources`).
- `.claude/skills/{resume,cover-letter,apply,outreach,batch}/SKILL.md`,
  `.claude/skills/batch/scoring.md`, `.claude/skills/apply/workday.md`: run the pull, and read the
  new paths.
- `tools/build_resume.py`, `tools/build_cover_letter.py`: docstring references to the prompts.
- Delete `Resume_prompt_v4.md` and `CoverLetter_prompt_v1.md` from the repo (git history keeps them).
- `.gitignore`: add a rule ignoring the `sources` folder (new); replace the rule for the v1.5 mega
  resume with one matching every `mega-resume-v*.tex`, so the old local copies stay ignored until
  Aly deletes them.
- `tests/test_pull_sources.py` (new): stdlib `unittest`; CI already runs `tests/`.
- `CLAUDE.md`: sources of truth, setup prerequisite (the Docs connector), the pull, a gotcha.
- `knowledge/decisions/0002-claude-docs-are-the-source-of-truth.md` (new): the ADR, plus its row
  in `knowledge/decisions/README.md`.

**Out:**

- Writing from Claude Code back to the docs. Edits happen in claude.ai only (an anti-goal: no
  two-way sync).
- The claude.ai skills themselves; Aly creates them from a prompt given in chat.
- Moving `profile.md`, `stories.md`, `answers.md` or `latex_resume.tex` into docs (a later change).
- Deleting the local `mega-resume-v1.5.tex` and `mega-resume-v1.6.tex`; Aly does that.
- `/followup` and `/discover`: they don't read these files.

## Design

### `sources.json`

```json
{
  "sources": [
    {"path": "sources/mega-resume.tex", "doc_url": "https://claude.ai/code/artifact/2d814730-1e3a-476b-8907-513ce73180c9", "tab_id": "958ab5d7-5d85"},
    {"path": "sources/resume_prompt.md", "doc_url": "https://claude.ai/code/artifact/74f55490-bd25-435e-a000-8409aeefe485", "tab_id": "bf5ae186-02f7"},
    {"path": "sources/cover_letter_prompt.md", "doc_url": "https://claude.ai/code/artifact/20c152e4-070a-4203-9bfa-14663ed5ef74", "tab_id": "9c169abe-1e8c"}
  ]
}
```

The doc id the Docs tools need is the UUID at the end of `doc_url`. The repo is private; the docs
are private to Aly's account, so the ids grant nothing on their own.

### `tools/pull_sources.py`

`python tools/pull_sources.py <downloaded.md> <target path>` prints one JSON object and exits 0
on success, 1 on any error:

- Finds fenced code blocks in the Markdown: an opening line of 3 or more backticks plus an
  optional info string, closed by a line of exactly the same backticks. A shorter backtick run
  inside a longer fence is content (the cover letter prompt's ``` lines inside ```` ).
- Exactly one block is required. Zero or more than one → error `"code_blocks": N`, nothing written.
- The block's content (lines between the fences, each ending in `\n`) is written to the target as
  UTF-8 with LF line endings, creating parent folders. Bytes inside lines are kept as they are:
  no trimming of trailing or whitespace-only lines.
- Output: `{"path", "status": "changed" | "unchanged" | "created", "sha256", "lines"}`;
  `unchanged` when the target already has identical bytes (the file is then not rewritten).
- Errors: `{"path", "error": "<message>"}` for a missing input, unreadable file or block count.
- Stdlib only.

### The pull procedure (`.claude/skills/pull-sources.md`)

For each entry in `sources.json`, in order:

1. Docs tool `create`: object `blob`, engine `blob`, container `{"kind": "project", "id": <doc id>}`,
   payload `{"from": {"object": "file", "id": <tab_id>}, "format": "markdown"}`. Note the returned
   asset id (`data.asset`).
2. Artifact tool `read`: `url` = `doc_url`, `path` = the asset id, `out_dir` left out (the
   tool's default scratchpad folder needs no approval). Note the saved file path it returns.
3. `python tools/pull_sources.py <saved file> <path>`.

The saved copies stay in the doc: there is no clean-up step (see Decisions).

Then report one line, for example `Pulled sources: mega-resume.tex changed, resume_prompt.md
unchanged, cover_letter_prompt.md unchanged.`

**When it runs.** At the start of `/resume`, `/cover-letter`, `/apply`, `/outreach` and `/batch`,
before any file in `sources/` is read. When one of these skills runs another (`/apply` runs
`/resume` and `/cover-letter`; `/outreach` runs `/apply`), only the outermost one pulls. `/batch`
pulls once in the main session before fanning out, and its subagent prompts say the sources are
already pulled.

**Failure.** If any step fails for any source (a Docs or Artifact tool unavailable or refused,
`pull_sources.py` exits 1), stop before tailoring anything and tell Aly which doc and what the error
said. Never fall back to an earlier pulled copy.

The docs' content is Aly's own writing, but by the tools' rules it is data, not instructions:
skills read the pulled prompts as the rules Aly wrote, exactly as they read the repo files today.

### Skill and doc changes

- Every `mega-resume-v1.5.tex` becomes `sources/mega-resume.tex`; `Resume_prompt_v4.md` becomes
  `sources/resume_prompt.md`; `CoverLetter_prompt_v1.md` becomes `sources/cover_letter_prompt.md`.
  The cover letter prompt's own text still names the old versioned file; that is Aly's to edit in
  the doc. The `/cover-letter` skill maps it without spelling the version, as `/resume` already
  maps `mega_resume.txt`: "Where the prompt names a versioned mega resume file
  (`mega-resume-v<N>.tex`), use `sources/mega-resume.tex`."
- Each of the five skills gets a first step: "Pull the sources: follow
  `.claude/skills/pull-sources.md` (skip if the skill that ran this one already pulled)."
- `CLAUDE.md`: Setup gains "the Claude Docs connector, signed in to Aly's account"; Architecture's
  sources-of-truth line names the docs, `sources.json` and `sources/`; Gotchas gains "edit the
  resume and prompts in the docs, never in `sources/`: the next pull overwrites local edits".

### Tests (`tests/test_pull_sources.py`)

Using temporary files: a ```` ```latex ```` block; a ```` ````markdown ```` block holding ```` ``` ````
lines; whitespace-only lines and `\%`, `\_` kept byte for byte; CRLF input written as LF; zero
blocks and two blocks are errors that write nothing; a second run on the same input reports
`unchanged` and leaves the file's modification time alone; a missing input file is an error.

## Decisions

- Claude Docs are the only source of truth; Claude Code pulls and never writes back (Aly,
  2026-10-17: edit in claude.ai, "the best place to modify those").
- Docs, over Google Drive or a GitHub repo synced to a claude.ai Project: both apps reach the docs
  already, and edits from claude.ai were shown to keep LaTeX intact.
- Content inside a fenced code block, not as rendered doc text: keeps bytes exact (rendered
  Markdown would be normalised).
- Fixed name `sources/mega-resume.tex`; versions live in the doc's history (Aly, 2026-10-17).
- The repo keeps no copies of the prompts; pulled files live in gitignored `sources/` (Aly,
  2026-10-17: "discard them since they are stored elsewhere").
- Stop when a doc can't be pulled; no stale fallback (Aly, 2026-10-17).
- Pull through a saved file and a download, not the Docs `export` tool: `export` returns the
  content base64-encoded inside the conversation (about 35 KB for the mega resume) on every run.
- No clean-up of the copies a pull saves in each doc. Checked 2026-10-17: the Docs `delete` on a
  blob is not available to agents (`mcp-exposure`), and an Artifact asset delete needs Aly's
  confirmation each time, which would mean three prompts per pull. A doc holds up to 5,000 assets
  and 1 GB; a pull adds about 26 KB per doc, so the copies are harmless for years. Reversible: Aly
  can delete them from a doc at any time. Builder's call, made 2026-10-17 after the design was
  approved; ADR 0002 records it with its reason.
- Prompt file names drop their version numbers (`resume_prompt.md`, `cover_letter_prompt.md`) for
  the same reason as the mega resume. Builder's call made in the design.

## Rollout

Local `main` has one uncommitted line in `.gitignore` (`/mega-resume-v1.6.tex`). Before pulling
the merged `main`, restore that file (`git restore .gitignore`); the new `/mega-resume-v*.tex`
rule covers it. After merge, the first skill run creates `sources/`.

## Success criteria

1. **Unit tests:** `python -m unittest discover -s tests -v` passes locally and in CI, including
   every case under Tests.
2. **Static:** `python -m py_compile tools/*.py` passes.
3. **No stale paths:** `git grep -n -e "mega-resume-v1" -e "Resume_prompt_v4" -e "CoverLetter_prompt_v1" -- .claude CLAUDE.md README.md tools tests`
   prints nothing.
4. **Live pull:** following `.claude/skills/pull-sources.md` from the worktree creates the three
   files in `sources/`; each equals its doc's code block (for the mega resume, equals
   `mega-resume-v1.6.tex` with CRLF→LF and a final newline added); an immediate second pull
   reports all three `unchanged`; Artifact `list` with `scope: "assets"` on each doc shows one
   new asset per pull, and nothing else changed in the doc.
5. **Live edit** (a one-off verification edit, not shipped behaviour): Claude Code changes one word inside the Resume prompt doc's code block, pulls,
   and `sources/resume_prompt.md` differs from the previous pull by exactly that word; the word
   is then changed back in the doc and a pull restores the file.
