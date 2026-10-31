# jobapps

A job-search workspace: tailored resumes and cover letters, application form answers,
and LinkedIn outreach for each posting, driven by Claude Code skills.

## What it does

From finding postings to following up with people at the company. Nothing is submitted, and no
message goes to an existing connection, without your OK.

```mermaid
%%{init: {"htmlLabels": false, "flowchart": {"htmlLabels": false, "padding": 20}}}%%
flowchart LR
    subgraph S1["1 · Find postings"]
        direction TB
        S10["Weekly search<br/>+ ATS scan"] --> S11["Ranked<br/>shortlist"] --> S12["You pick<br/>postings"]
    end
    subgraph S2["2 · Tailor"]
        direction TB
        S20["Read the<br/>posting"] --> S21["Match it to<br/>your resume"] --> S22["Resume +<br/>cover letter"]
    end
    subgraph S3["3 · Apply"]
        direction TB
        S30["Open the form<br/>in Chrome"] --> S31["Fill it from<br/>your profile"] --> S32["Submit on<br/>your OK"]
    end
    subgraph S4["4 · Reach out"]
        direction TB
        S40["Your LinkedIn<br/>connections"] --> S41["Recruiters<br/>and managers"] --> S42["Send a note<br/>or message"]
    end
    subgraph S5["5 · Follow up"]
        direction TB
        S50["Who accepted<br/>or replied?"] --> S51["Message,<br/>nudge, reply"] --> S52["Log the<br/>status"]
    end
    S1 --> S2 --> S3 --> S4 --> S5
```

**Many postings at once:** `/batch` runs the same steps over a whole list, with one review round
for all your approvals.

```mermaid
%%{init: {"htmlLabels": false, "flowchart": {"htmlLabels": false, "padding": 20}}}%%
flowchart LR
    subgraph S1["1 · Your list"]
        direction TB
        S10["Excel, CSV<br/>or URLs"] --> S11["Skip ones<br/>already done"]
    end
    subgraph S2["2 · Screen, score"]
        direction TB
        S20["Check<br/>eligibility"] --> S21["Score vs<br/>your targets"] --> S22["Set low scores<br/>aside"]
    end
    subgraph S3["3 · Prepare"]
        direction TB
        S30["Tailored<br/>resumes"] --> S31["Fill forms<br/>in Chrome"] --> S32["Draft LinkedIn<br/>messages"]
    end
    subgraph S4["4 · You review"]
        direction TB
        S40["One review<br/>sheet"] --> S41["Approve or<br/>skip each"]
    end
    subgraph S5["5 · Run"]
        direction TB
        S50["Submit<br/>approved forms"] --> S51["Send<br/>messages"] --> S52["Update<br/>trackers"]
    end
    S1 --> S2 --> S3 --> S4 --> S5
```

## Setup

Run `/onboard` in Claude Code: it checks prerequisites, asks for your material and targets, creates your six Docs (or six local files), config, career-ops scan, shortlist and weekly routine (or a local scheduled task).

### How onboarding works

`/onboard` is re-runnable: on a second run it asks "keep / redo" before changing anything that
exists.

```mermaid
%%{init: {"htmlLabels": false, "flowchart": {"htmlLabels": false, "padding": 20}}}%%
flowchart LR
    subgraph S1["1 · Prerequisites"]
        direction TB
        S10["Python,<br/>LaTeX, git"] --> S11["Chrome<br/>extension"] --> S12["Claude Docs or<br/>desktop app"]
    end
    subgraph S2["2 · About you"]
        direction TB
        S20["Your resume<br/>and answers"] --> S21["Interview<br/>fills gaps"] --> S22["Docs or<br/>local files?"]
    end
    subgraph S3["3 · Your sources"]
        direction TB
        S30["Write six<br/>sources"] --> S31["Save your<br/>config"] --> S32["Copy into<br/>the repo"]
    end
    subgraph S4["4 · Job search"]
        direction TB
        S40["career-ops<br/>scanner"] --> S41["Shortlist<br/>page"] --> S42["Weekly run"]
    end
    subgraph S5["5 · First resume"]
        direction TB
        S50["Pick a real<br/>posting"] --> S51["Build the<br/>resume"] --> S52["Check it fits<br/>one page"]
    end
    S1 --> S2 --> S3 --> S4 --> S5
```

### Manual setup (fallback)

1. **Prerequisites.** Python 3; `pdflatex` on PATH, or MiKTeX; Chrome with the Claude in Chrome
   extension (for `/apply`, `/outreach`, `/followup`); the Claude Docs connector, signed in to your
   account (Docs only).
2. **Create your six sources** in Claude Docs, each holding its content in one fenced code
   block (the Mega resume in a `latex` block, the rest in `markdown` blocks), or six local files in
   a folder outside the repo (no code fence): Mega resume, Resume
   prompt, Cover letter prompt, Application profile, Behavioral stories, Free-text answer bank.
   Local files are named like their working copies (`mega-resume.tex`, `resume_prompt.md`, ...).
   The working copies they are pulled into are the six `path` values in `config.example.json`
   (`sources/mega-resume.tex`, `sources/resume_prompt.md`, `sources/cover_letter_prompt.md`,
   `sources/profile.md`, `sources/stories.md`, `sources/answers.md`). The profile needs a
   `## Contact` section (`Full name`, `Preferred first name`, phone, email, links).
3. **Copy `config.example.json` to `config.local.json`** (gitignored) and fill it in. One line per key:
   - `sources` (required): one entry per Doc with its `path`, `doc_url` and `tab_id`; the Profile
     entry also has its `node_id` and `"writable": true`; or, for local files, `path` and `local_path`
     (the file's absolute path), the Profile entry also `"writable": true`. Without the file, skills stop and say
     the repo is not set up yet.
   - `shortlist` (optional): `artifact_url` and `title` of your weekly shortlist artifact. Absent:
     `/job-shortlist` says the shortlist is not set up.
   - `career_ops_dir` (optional): your career-ops checkout, used by `/discover`. Absent: `/discover`
     asks for the path.
   - `discover_locations` (optional): location keywords for `/discover`. Absent: no location filter.
   - `linkedin_premium` (optional): `true` or `false`, the fallback when a LinkedIn run cannot tell
     your plan from the page. Absent: the skill asks you.
   - `targeting` (optional): `eligible_regions`, `home_city`, `currency`, `phone_country`. Absent:
     no eligibility screen, no city or region preference, amounts in USD with no conversion, and
     Workday asks you for the phone country.
4. **Optional:** create a gitignored `.personal-terms` file, one term per line (your name, handles,
   email, phone, Doc ids); `tests/test_no_personal_data.py` then also checks tracked files for them
   locally (CI runs only the generic patterns).
5. **Optional:** set up career-ops for `/discover`, and the weekly shortlist artifact for
   `/job-shortlist`: publish `templates/shortlist/` as the artifact and schedule a weekly routine
   from `templates/weekly-search-prompt.md` (filled in).

## Map

- [`CLAUDE.md`](CLAUDE.md) — how the workspace is laid out and how to work in it.
- Local only, not tracked: `applications.md` (status per posting), `postings/` (per-posting
  folders), `batches/` (`/batch` manifests), `discovered/` (`/discover` CSVs), `dlq.md`, and the personal source files.
- [`.claude/skills/`](.claude/skills/) — `/onboard`, `/discover`, `/resume`, `/cover-letter`, `/apply`, `/outreach`, `/followup`, `/batch`.
- [`templates/`](templates/) — generic starting material `/onboard` uses.
- [`knowledge/`](knowledge/README.md) — what the project knows: research, context, domain docs.
- [`knowledge/decisions/`](knowledge/decisions/README.md) — decision records.
- [`docs/superpowers/`](docs/superpowers/README.md) — design specs and implementation plans.
