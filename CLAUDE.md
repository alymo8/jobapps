# jobapps

Project memory file: how to navigate and work in this repo. Keep it to about a
screen; update it in the same change that makes it stale. Workspace-wide rules live
in the workspace `CLAUDE.md` one level up.

## Setup / prerequisites

- Python 3 for `tools/` (stdlib plus PDF rendering libs used by the build scripts).
- `pdflatex` on PATH, or MiKTeX installed via scoop (`build_resume.py` falls back to it).
- Chrome with the Claude-in-Chrome extension for `/apply`, `/outreach`, `/followup`.

## Build, run, check

```
python tools/build_resume.py postings/<dir>/<name>.tex          # compile + JSON checks (1 page, fill, skills lines)
python tools/build_cover_letter.py postings/<dir>/cover_letter.md [--check]
python tools/read_postings.py <file.xlsx|.csv|.txt|dlq.md|url> [--rows 1-20] [--new] [--all]
python tools/discover.py [--since N] [--exclude <list>] [--location <kw> ...] [--career-ops <dir>]  # -> discovered/<date>.csv
python -m unittest discover -s tests -v                                     # unit tests (CI runs them)
python -m py_compile tools/*.py                                  # CI runs this and the tests
```

## Architecture in brief

- Sources of truth: `mega-resume-v1.5.tex` (all experience), `profile.md`, `stories.md`,
  `answers.md`; prompts `Resume_prompt_v4.md`, `CoverLetter_prompt_v1.md`.
- Skills in `.claude/skills/`: `/discover` (career-ops scanner → CSV) → `/resume` → `/apply` → `/outreach` → `/followup`;
  `/cover-letter` when a form offers one; `/batch` fans these out over many postings.
- `/batch` stage 1a.5 scores each posting (`.claude/skills/batch/scoring.md`, `sonnet`) against `## Targeting` in `profile.md` and dead-letters low scores as `LOW-SCORE` before resumes.
- Per posting: `postings/<Company>-<id>/` holds `posting.md`, the resume `.tex`,
  `application.md`, `cover_letter.md`, `outreach.md`, `changelog.md`.
- Trackers: `applications.md` (one row per posting, updated in place), `dlq.md`
  (postings that couldn't be processed), `batches/<timestamp>-<mode>/manifest.md`.

## Conventions

- Never submit an application or send a LinkedIn message without the user's explicit OK.
- Everything written about the user must be truth-checked against the source files above.
- The repo holds only the setup (skills, tools, prompts, docs). Personal sources,
  `postings/`, `batches/`, `discovered/`, `archive/` and the trackers are local-only and gitignored;
  never commit them.

## Gotchas

- `build_cover_letter.py` reads the letter header (name, phone, email, links) from the
  `## Contact` bullets in the local `profile.md`; keep those keys when editing it.
- `tools/` scripts aren't ruff-clean at the default 88-column limit; CI byte-compiles them and runs the unittest suite (no linter).

## Pointers

- Knowledge base: [`knowledge/`](knowledge/README.md)
- Decisions: [`knowledge/decisions/`](knowledge/decisions/README.md)
- Specs and plans: [`docs/superpowers/`](docs/superpowers/README.md)
- Session hygiene: use `claude-kit:lean-context` when exploring; `/handoff` before `/clear`.
