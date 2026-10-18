# jobapps

Project memory file: how to navigate and work in this repo. Keep it to about a
screen; update it in the same change that makes it stale. Workspace-wide rules live
in the workspace `CLAUDE.md` one level up.

## Setup / prerequisites

- Python 3 for `tools/` (stdlib plus PDF rendering libs used by the build scripts).
- `pdflatex` on PATH, or MiKTeX installed via scoop (`build_resume.py` falls back to it).
- Chrome with the Claude-in-Chrome extension for `/apply`, `/outreach`, `/followup`.
- The Claude Docs connector, signed in to Aly's account: skills pull the mega resume and prompts
  from it (`sources.json`).

## Build, run, check

```
python tools/build_resume.py postings/<dir>/<name>.tex          # compile + JSON checks (1 page, fill, skills lines)
python tools/build_cover_letter.py postings/<dir>/cover_letter.md [--check]
python tools/read_postings.py <file.xlsx|.csv|.txt|dlq.md|url> [--rows 1-20] [--new] [--all]
python tools/discover.py [--since N] [--exclude <list>] [--location <kw> ...] [--career-ops <dir>]  # -> discovered/<date>.csv
python tools/pull_sources.py <downloaded.md> <target>                      # doc code block -> sources/ (see .claude/skills/pull-sources.md)
python -m unittest discover -s tests -v                                     # unit tests (CI runs them)
python -m py_compile tools/*.py                                  # CI runs this and the tests
```

## Architecture in brief

- Sources of truth: three Claude Docs (listed in `sources.json`) for the mega resume and both
  prompts, pulled into gitignored `sources/` (`mega-resume.tex`, `resume_prompt.md`,
  `cover_letter_prompt.md`) per `.claude/skills/pull-sources.md`; plus local `profile.md`,
  `stories.md`, `answers.md` ([ADR 0002](knowledge/decisions/0002-claude-docs-are-the-source-of-truth.md)).
- Skills in `.claude/skills/`: `/discover` (career-ops scanner → CSV) → `/resume` → `/apply` → `/outreach` → `/followup`;
  `/cover-letter` when a form offers one; `/batch` fans these out over many postings.
- `/batch` stage 1a.5 scores each posting (`.claude/skills/batch/scoring.md`, `sonnet`) against `## Targeting` in `profile.md` and dead-letters low scores as `LOW-SCORE` before resumes.
- Per posting: `postings/<Company>-<id>/` holds `posting.md`, the resume `.tex`,
  `application.md`, `cover_letter.md`, `outreach.md`, `changelog.md`.
- Trackers: `applications.md` (one row per posting, updated in place), `dlq.md`
  (postings that couldn't be processed), `batches/<timestamp>-<mode>/manifest.md`.

## Conventions

- Never submit an application or send a LinkedIn message without Aly's explicit OK.
- Everything written about Aly must be truth-checked against the source files above.
- The repo holds only the setup (skills, tools, docs). Personal sources, `sources/`,
  `postings/`, `batches/`, `discovered/`, `archive/` and the trackers are local-only and gitignored;
  never commit them.

## Gotchas

- `build_cover_letter.py` reads the letter header (name, phone, email, links) from the
  `## Contact` bullets in the local `profile.md`; keep those keys when editing it.
- Edit the mega resume and prompts in the Claude Docs (claude.ai), never in `sources/`: the next
  pull overwrites local edits.
- `tools/` scripts aren't ruff-clean at the default 88-column limit; CI byte-compiles them and runs the unittest suite (no linter).

## Pointers

- Knowledge base: [`knowledge/`](knowledge/README.md)
- Decisions: [`knowledge/decisions/`](knowledge/decisions/README.md)
- Specs and plans: [`docs/superpowers/`](docs/superpowers/README.md)
- Session hygiene: use `claude-kit:lean-context` when exploring; `/handoff` before `/clear`.
