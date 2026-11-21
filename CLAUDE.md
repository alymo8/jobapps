# jobapps

Project memory file: how to navigate and work in this repo. Keep it to about a
screen; update it in the same change that makes it stale. This file is complete on
its own. If the repo sits inside the maintainer's claude-kit workspace, the
`CLAUDE.md` one level up adds development-process rules (worktrees, spec and plan
gates); without it, nothing here changes.

## Setup / prerequisites

- Python 3 for `tools/` (stdlib plus PDF rendering libs used by the build scripts).
- `pdflatex` on PATH, or MiKTeX installed via scoop (`build_resume.py` falls back to it).
- With Nix: `nix develop` (`flake.nix`) gives both, plus PyMuPDF and openpyxl. Flakes see only
  git-tracked files: `git add flake.nix flake.lock`, or use `nix develop path:.`.
- Chrome with the Claude-in-Chrome extension for `/outreach`, `/followup` (read-only LinkedIn).
- The Claude Docs connector (Docs mode only), signed in to the user's account: skills pull the sources listed in
  `config.local.json` (README "Setup").

## Build, run, check

```
python tools/build_resume.py postings/<dir>/<name>.tex          # compile + JSON checks (1 page, fill, skills lines)
python tools/build_cover_letter.py postings/<dir>/cover_letter.md [--check]
python tools/read_postings.py <file.xlsx|.csv|.txt|dlq.md|url> [--rows 1-20] [--new] [--all] [--for outreach]
python tools/discover.py --input <rows.json> [--exclude <list>] [--location <kw> ...]  # dedupe -> discovered/<date>.csv (used by /scan-jobs)
python tools/pull_sources.py <downloaded.md> <target>                      # doc code block -> sources/ (see .claude/skills/pull-sources.md)
python tools/pull_sources.py --local <local file> <target>             # local source file -> sources/
python -I tools/shortlist.py list --keys <decision_keys.py> --rows <latest.json> --decisions <dir> --top 10 --table  # see job-shortlist skill
python -m unittest discover -s tests -v                                     # unit tests (CI runs them)
python -m py_compile tools/*.py                                  # CI runs this and the tests
```

## Architecture in brief

- Sources of truth: six Claude Docs or six local files outside the repo, chosen at /onboard (local files by default; listed in `config.local.json` `sources`) for the mega resume, both prompts,
  the profile, stories and answers, pulled into gitignored `sources/` per
  `.claude/skills/pull-sources.md`. Of the six sources, Claude Code writes only to the profile source (Doc or local file), through
  `.claude/skills/write-source.md` ([ADR 0010](knowledge/decisions/0010-onboarding-creates-user-docs-and-shortlist.md),
  [ADR 0011](knowledge/decisions/0011-local-source-files-option.md),
  [ADR 0013](knowledge/decisions/0013-minimal-onboarding-and-claude-job-scan.md)).
- Skills in `.claude/skills/`: `/onboard` sets up a new user (resume, short interview, sources, first resume; templates in `templates/`); `/scan-jobs` (Claude job search → CSV; `--country` for one run) → `/resume` → the user applies by hand;
  `/weekly-scan` publishes the shortlist and schedules the search, weekly or daily ([ADR 0013](knowledge/decisions/0013-minimal-onboarding-and-claude-job-scan.md), [ADR 0016](knowledge/decisions/0016-internship-targeting-and-search-countries.md)); `/outreach` (LinkedIn drafts) → `/followup`;
  `/cover-letter` when a form offers one; `/batch` fans `/resume` and outreach drafting out over many postings;
  `/job-shortlist` reads the weekly shortlist artifact and records applied / not-interested decisions.
- Weekly shortlist: a claude.ai artifact (URL in `config.local.json` `shortlist`). Claude Code
  reads its `data/*` and writes only its `decisions` collection, keys from its `decision_keys.py`
  via `tools/shortlist.py` ([ADR 0010](knowledge/decisions/0010-onboarding-creates-user-docs-and-shortlist.md)).
  "I applied to X" goes through its "Record applied", which also updates `applications.md`.
- `/batch` stage 1a.5 scores each posting (`.claude/skills/batch/scoring.md`, `sonnet`) against `## Targeting` in `sources/profile.md` (internship lines: job type, terms, length, graduation, GPA) and dead-letters low scores as `LOW-SCORE` before resumes.
- `/onboard` runs a resume panel on the user's resume (`.claude/skills/onboard/panel.md`, adapted from `/hiring-panel`): its findings become interview questions and mega-resume wording fixes.
- After each resume build, a fresh `opus` subagent grades it as a recruiter (`.claude/skills/resume/recruiter-review.md`):
  score /10, one improvement pass below 9, then final, low score or not (`/batch` stage 1c; [ADR 0012](knowledge/decisions/0012-recruiter-review-one-pass.md)).
- Per posting: `postings/<Company>-<id>/` holds `posting.md`, the resume `.tex`, `review.md`,
  `application.md`, `cover_letter.md`, `outreach.md`, `changelog.md`.
- Trackers: `applications.md` (one row per posting, updated in place), `dlq.md`
  (postings that couldn't be processed), `batches/<timestamp>-<mode>/manifest.md`.

## Conventions

- Claude never submits an application and never sends, connects or types on LinkedIn: it tailors
  resumes and drafts send sheets; the user applies and sends by hand and says what was done
  ([ADR 0015](knowledge/decisions/0015-manual-applying-and-outreach.md)).
- LinkedIn runs use one tab at a time, recycled every 8 page opens (`.claude/skills/linkedin-tab.md`,
  [ADR 0007](knowledge/decisions/0007-light-linkedin-runs.md)); `/batch` does LinkedIn work one posting at a time.
- Everything written about the user must be truth-checked against the source files above.
- The repo holds only the setup (skills, tools, docs). Personal sources, `sources/`,
  `postings/`, `batches/`, `discovered/`, `archive/`, `config.local.json`, `.personal-terms` and the
  trackers are local-only and gitignored;
  never commit them.

## Gotchas

- `build_cover_letter.py` reads the letter header (name, phone, email, links) from the
  `## Contact` bullets of `sources/profile.md` (pull first); keep those keys when editing the
  Profile doc.
- Edit the sources in the Claude Docs (claude.ai) or in their `local_path` files, never in `sources/`: the next pull overwrites
  local edits.
- `tools/` scripts aren't ruff-clean at the default 88-column limit; CI byte-compiles them and runs the unittest suite (no linter).
- CI (`ci.yml`) runs only on pull requests and pushes to `main`; a feature-branch push runs only
  `secret-scan`, so CI results appear once the PR is open.
- `applications.md` statuses and the legend line are written by four skills (outreach, job-shortlist,
  batch, followup); change a status rule or the legend in all four, byte-identical.
- `tests/fixtures/decision_keys.py`: the key functions match the shortlist artifact's keys file; the
  docstring is neutral, so the file is not byte-identical to it (`-text` in `.gitattributes`);
  refreshing the functions also means updating `FIXTURE_SHA256` in `tests/test_shortlist.py` and
  `KEYS_CODE_SHA256` in `tools/shortlist.py` (a docstring-free code hash: `shortlist.py` refuses to
  run a downloaded keys file that does not match it);
  `templates/shortlist/data/decision_keys.py` is pinned to the same hash, so refresh it with them.
- `tests/test_no_personal_data.py` scans every tracked file; on the maintainer's machine it also
  checks the gitignored `.personal-terms`. For ad-hoc checks use `git grep -n -i -w -F -f
  .personal-terms`; plain `grep -F -f .personal-terms` core-dumps in Git Bash.
- A new git worktree has none of the gitignored local files (`config.local.json`, `.personal-terms`,
  `sources/`): copy the first two in from the main checkout and pull the sources there; copy any
  new ones back before removing the worktree.
- Send sheets can tell the user: when a profile's Connect button opens no dialog, open
  `https://www.linkedin.com/preload/custom-invite/?vanityName=<vanity>`; when Message opens
  nothing, use Messaging → New message.
- `ArtifactData list` on an empty `decisions` collection writes no files to `out_dir`;
  `shortlist.py` treats a missing directory as no decisions. Its saved files carry no `version`
  (only the tool's result text shows `version N`), so `shortlist.py doc --existing` and `pending-plan`
  take it as `--version` and fail rather than emit `if_version: null`.
- Git Bash heredocs turn `\\` into `\`: write LaTeX with the Write/Edit tools, not `cat <<EOF`.
- Testing local mode end to end (scheduled task, auditing a run): [knowledge/technical/local-mode-testing.md](knowledge/technical/local-mode-testing.md).
- The Artifact tool publishes only files under the session's working directory or scratchpad: from a
  worktree outside the repo, copy `templates/shortlist/` to the scratchpad first.

## Pointers

- Knowledge base: [`knowledge/`](knowledge/README.md)
- Decisions: [`knowledge/decisions/`](knowledge/decisions/README.md)
- Specs and plans (design history): [`docs/superpowers/`](docs/superpowers/README.md)
- Session hygiene: keep long command output (tests, builds) out of the main context; with the
  optional claude-kit plugin, use `claude-kit:lean-context` when exploring and `/handoff` before `/clear`.
