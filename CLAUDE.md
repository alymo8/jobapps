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
python tools/read_postings.py <file.xlsx|.csv|.txt|dlq.md|url> [--rows 1-20] [--new] [--all] [--for outreach]
python tools/discover.py [--since N] [--exclude <list>] [--location <kw> ...] [--career-ops <dir>]  # -> discovered/<date>.csv
python tools/pull_sources.py <downloaded.md> <target>                      # doc code block -> sources/ (see .claude/skills/pull-sources.md)
python -I tools/shortlist.py list --keys <decision_keys.py> --rows <latest.json> --decisions <dir> --top 10 --table  # see job-shortlist skill
python -m unittest discover -s tests -v                                     # unit tests (CI runs them)
python -m py_compile tools/*.py                                  # CI runs this and the tests
```

## Architecture in brief

- Sources of truth: six Claude Docs (listed in `sources.json`) for the mega resume, both prompts,
  the profile, stories and answers, pulled into gitignored `sources/` per
  `.claude/skills/pull-sources.md`. Of the six source Docs, Claude Code writes only to the Profile doc, through
  `.claude/skills/write-source.md` ([ADR 0003](knowledge/decisions/0003-claude-code-writes-to-the-profile-doc.md)).
- Skills in `.claude/skills/`: `/discover` (career-ops scanner → CSV) → `/resume` → `/apply`; `/outreach` (LinkedIn only; `--apply` to apply first) → `/followup`;
  `/cover-letter` when a form offers one; `/batch` fans these out over many postings;
  `/job-shortlist` reads the weekly shortlist artifact and records applied / not-interested decisions.
- Weekly shortlist: a claude.ai artifact (URL in `.claude/skills/job-shortlist/SKILL.md`). Claude Code
  reads its `data/*` and writes only its `decisions` collection, keys from its `decision_keys.py`
  via `tools/shortlist.py` ([ADR 0004](knowledge/decisions/0004-job-shortlist-artifact-decisions.md)).
  The apply flow asks "Mark <company> – <title> as applied?".
- `/batch` stage 1a.5 scores each posting (`.claude/skills/batch/scoring.md`, `sonnet`) against `## Targeting` in `sources/profile.md` and dead-letters low scores as `LOW-SCORE` before resumes.
- Per posting: `postings/<Company>-<id>/` holds `posting.md`, the resume `.tex`,
  `application.md`, `cover_letter.md`, `outreach.md`, `changelog.md`.
- Trackers: `applications.md` (one row per posting, updated in place), `dlq.md`
  (postings that couldn't be processed), `batches/<timestamp>-<mode>/manifest.md`.

## Conventions

- Never submit an application without Aly's explicit OK. On LinkedIn, messages to Aly's existing
  connections and replies need Aly's OK (names shown first); requests and messages to new people
  go out without it ([ADR 0005](knowledge/decisions/0005-linkedin-approval-only-for-existing-connections.md)).
- Everything written about Aly must be truth-checked against the source files above.
- The repo holds only the setup (skills, tools, docs). Personal sources, `sources/`,
  `postings/`, `batches/`, `discovered/`, `archive/` and the trackers are local-only and gitignored;
  never commit them.

## Gotchas

- `build_cover_letter.py` reads the letter header (name, phone, email, links) from the
  `## Contact` bullets of `sources/profile.md` (pull first); keep those keys when editing the
  Profile doc.
- Edit the sources in the Claude Docs (claude.ai), never in `sources/`: the next pull overwrites
  local edits.
- `tools/` scripts aren't ruff-clean at the default 88-column limit; CI byte-compiles them and runs the unittest suite (no linter).
- `tests/fixtures/decision_keys.py` is a pinned copy of the shortlist artifact's keys file (`-text` in
  `.gitattributes`); refreshing it also means updating `FIXTURE_SHA256` in `tests/test_shortlist.py`.
- `ArtifactData list` on an empty `decisions` collection writes no files to `out_dir`;
  `shortlist.py` treats a missing directory as no decisions.

## Pointers

- Knowledge base: [`knowledge/`](knowledge/README.md)
- Decisions: [`knowledge/decisions/`](knowledge/decisions/README.md)
- Specs and plans: [`docs/superpowers/`](docs/superpowers/README.md)
- Session hygiene: use `claude-kit:lean-context` when exploring; `/handoff` before `/clear`.
