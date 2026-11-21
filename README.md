# jobapps

A job-search workspace: tailored resumes and cover letters, application form answers,
and LinkedIn outreach for each posting, driven by Claude Code skills.

## What it does

From finding postings to following up with people at the company. Claude finds postings, tailors
resumes and drafts LinkedIn messages; you submit every application and send every message yourself
([ADR 0015](knowledge/decisions/0015-manual-applying-and-outreach.md)).

```mermaid
%%{init: {"htmlLabels": false, "flowchart": {"htmlLabels": false, "padding": 20}}}%%
flowchart LR
    subgraph S1["1 · Find postings"]
        direction TB
        S10["Job scan (on demand<br/>or weekly)"] --> S11["Ranked<br/>shortlist"] --> S12["You pick<br/>postings"]
    end
    subgraph S2["2 · Tailor"]
        direction TB
        S20["Read the<br/>posting"] --> S21["Match it to<br/>your resume"] --> S22["Resume +<br/>cover letter"]
    end
    subgraph S3["3 · Apply"]
        direction TB
        S30["Tailored PDF<br/>per posting"] --> S31["You apply<br/>by hand"] --> S32["Mark it<br/>applied"]
    end
    subgraph S4["4 · Reach out"]
        direction TB
        S40["Your LinkedIn<br/>connections"] --> S41["Recruiters<br/>and managers"] --> S42["Drafts you<br/>send yourself"]
    end
    subgraph S5["5 · Follow up"]
        direction TB
        S50["Who accepted<br/>or replied?"] --> S51["Draft message,<br/>nudge, reply"] --> S52["Log the<br/>status"]
    end
    S1 --> S2 --> S3 --> S4 --> S5
    S5 ~~~ PAD["room for the zoom buttons"]
    style PAD fill:none,stroke:none,color:transparent
```

**Many postings at once:** `/batch` runs the same steps over a whole list, with one review sheet
for what you apply to and send.

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
        S30["Tailored<br/>resumes"] --> S31["Recruiter<br/>review"] --> S32["Draft LinkedIn<br/>messages"]
    end
    subgraph S4["4 · You review"]
        direction TB
        S40["One review<br/>sheet"] --> S41["Apply and<br/>send by hand"]
    end
    subgraph S5["5 · Record"]
        direction TB
        S50["Mark applied<br/>and sent"] --> S51["Update<br/>trackers"]
    end
    S1 --> S2 --> S3 --> S4 --> S5
    S5 ~~~ PAD["room for the zoom buttons"]
    style PAD fill:none,stroke:none,color:transparent
```

## Setup

With Nix, run `nix develop` in the repo first (`flake.nix` brings Python and LaTeX). Run `/onboard` in Claude Code: it checks your tools, reads your resume and runs it past a resume panel, asks a few questions about what you are looking for, writes your six sources (local files, or Claude Docs with `/onboard --docs`) and config, and builds a first resume. `/scan-jobs` and `/weekly-scan` find postings afterwards.

### How onboarding works

`/onboard` is re-runnable: on a second run it asks "keep / redo" before changing anything that
exists.

```mermaid
%%{init: {"htmlLabels": false, "flowchart": {"htmlLabels": false, "padding": 20}}}%%
flowchart LR
    subgraph S1["1 · Your resume"]
        direction TB
        S10["Tool<br/>check"] --> S11["Share your<br/>resume"] --> S12["Resume<br/>panel"]
    end
    subgraph S2["2 · A few questions"]
        direction TB
        S20["Roles, terms,<br/>countries"] --> S21["Pay floor,<br/>missing facts"] --> S22["Write six<br/>sources"]
    end
    subgraph S3["3 · First resume"]
        direction TB
        S30["Pick a real<br/>posting"] --> S31["Build the<br/>resume"] --> S32["Check it fits<br/>one page"]
    end
    S1 --> S2 --> S3
    S3 ~~~ PAD["room for the zoom buttons"]
    style PAD fill:none,stroke:none,color:transparent
```

### Manual setup (fallback)

1. **Prerequisites.** Python 3 and `pdflatex` on PATH (`nix develop` gives both), or MiKTeX; Chrome
   with the Claude in Chrome extension (for `/outreach` and `/followup`, which only read LinkedIn);
   the Claude Docs connector, signed in to your account (Docs only).
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
     `/job-shortlist` says to run `/weekly-scan`.
   - `linkedin_premium` (optional): `true` or `false`, the fallback when a LinkedIn run cannot tell
     your plan from the page. Absent: the skill asks you.
   - `targeting` (optional): `eligible_regions` (where you may work without a visa),
     `search_countries` (where the scan looks; default `eligible_regions`; `/scan-jobs --country`
     overrides it for one run), `home_city`, `currency`, `phone_country`. Absent: no eligibility
     screen, no city or region preference, amounts in USD with no conversion.
4. **Optional:** create a gitignored `.personal-terms` file, one term per line (your name, handles,
   email, phone, Doc ids); `tests/test_no_personal_data.py` then also checks tracked files for them
   locally (CI runs only the generic patterns).
5. **Optional:** run `/weekly-scan` for the weekly shortlist artifact used by `/job-shortlist` (by
   hand: publish `templates/shortlist/` and schedule `templates/weekly-search-prompt.md`, filled in).

## Map

- [`CLAUDE.md`](CLAUDE.md) — how the workspace is laid out and how to work in it.
- Local only, not tracked: `applications.md` (status per posting), `postings/` (per-posting
  folders), `batches/` (`/batch` manifests), `discovered/` (`/scan-jobs` CSVs), `dlq.md`, and the personal source files.
- [`.claude/skills/`](.claude/skills/) — `/onboard`, `/scan-jobs`, `/weekly-scan`, `/resume`, `/cover-letter`, `/outreach`, `/followup`, `/batch`, `/job-shortlist`.
- [`templates/`](templates/) — generic starting material `/onboard` uses.
- [`knowledge/`](knowledge/README.md) — what the project knows: research, context, domain docs.
- [`knowledge/decisions/`](knowledge/decisions/README.md) — decision records.
- [`docs/superpowers/`](docs/superpowers/README.md) — design specs and implementation plans.
