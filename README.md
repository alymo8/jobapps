# jobapps

A job-search workspace: tailored resumes and cover letters, application form answers,
and LinkedIn outreach for each posting, driven by Claude Code skills.

## What it does

From finding postings to following up with people at the company. Every step reads your six
sources (resume, prompts, profile, stories, answers), and nothing is submitted, and no message goes
to an existing connection, without your OK.

```mermaid
flowchart TD
    SRC[("Your six sources<br/>Claude Docs or local files")] -->|pull| LOCAL["sources/<br/>working copies"]

    subgraph FIND["1 · Find postings"]
        WEEKLY["Weekly routine<br/>searches the web"] --> SHORT["Shortlist artifact<br/>ranked postings"]
        SHORT --> JS["/job-shortlist<br/>browse, mark applied or skip"]
        DISC["/discover<br/>career-ops ATS scan"] --> CSV["discovered/date.csv"]
        LIST["Your own lists<br/>Excel, CSV, URLs"]
    end

    subgraph TAILOR["2 · Tailor"]
        RES["/resume<br/>one-page LaTeX resume,<br/>compiled and checked"]
        CL["/cover-letter<br/>when the form asks for one"]
    end

    subgraph APPLY["3 · Apply"]
        FILL["/apply<br/>fills the form in Chrome"] --> OK{"Your OK?"}
        OK -->|yes| SUBMIT["Submitted"]
    end

    subgraph REACH["4 · Reach out on LinkedIn"]
        OUT["/outreach<br/>your connections first,<br/>then recruiters and hiring managers"]
        FU["/followup<br/>accepted, silent, replied,<br/>plus new people"]
        OUT --> FU
    end

    LOCAL -.->|read by every step| TAILOR
    FIND --> TAILOR
    RES --> CL --> FILL
    SUBMIT --> OUT
    FU --> TRACK[("applications.md<br/>status per posting")]
```

`/outreach` also works without applying (it reuses the tailored resume), and `/apply` asks
whether to mark the posting as applied on the shortlist.

**Many postings at once:** `/batch resume|apply|outreach <list>` runs the same steps over a whole
list with subagents. It pre-screens eligibility, scores each posting against your targeting (low
scores go to `dlq.md`), builds the resumes, prepares the forms and messages, then shows one review
sheet so you approve everything in a single round before it submits and sends.

```mermaid
flowchart LR
    L["List of postings"] --> P["Pre-screen<br/>eligibility, duplicates"] --> S["Score<br/>vs your targeting"]
    S -->|low score| D[("dlq.md")]
    S --> R["Resumes"] --> PR["Prepare forms<br/>and messages"] --> RV{"One review sheet<br/>your approvals"} --> X["Submit and send"]
    X --> M[("batches/…/manifest.md<br/>applications.md")]
```

## Setup

Run `/onboard` in Claude Code: it checks prerequisites, asks for your material and targets, creates your six Docs (or six local files), config, career-ops scan, shortlist and weekly routine (or a local scheduled task).

### How onboarding works

`/onboard` is re-runnable: on a second run it asks "keep / redo" before changing anything that
exists.

```mermaid
flowchart TD
    A["1 · Prerequisites<br/>Python, pdflatex, git, Node,<br/>Claude in Chrome"] --> B["2 · Collect material<br/>resume, cover letters,<br/>LinkedIn, past answers"]
    B --> C["3 · Interview<br/>only what the material doesn't settle:<br/>contact, eligibility, pay, target roles,<br/>locations, deal-breakers, stories"]
    C --> Q{"Where do your<br/>sources live?"}
    Q -->|"Claude Docs (default)"| D1["4 · Create six Claude Docs"]
    Q -->|"Local files"| D2["4 · Write six files to a<br/>folder outside the repo"]
    D1 & D2 --> CFG["config.local.json<br/>+ pull into sources/ and verify"]
    CFG --> E["5 · Show the sources<br/>and the gaps left to fill"]
    E --> F["6 · career-ops<br/>clone, portals.yml from your<br/>roles, companies, locations"]
    F --> G["7 · Publish the shortlist artifact"]
    G --> G1{"Mode"}
    G1 -->|Docs| H1["Weekly cloud routine"]
    G1 -->|Local| H2["Weekly local scheduled task<br/>in the Claude desktop app"]
    H1 & H2 --> I["8 · First tailored resume<br/>to check the whole chain"]
    I --> DONE(["Ready: /discover, /resume,<br/>/apply, /outreach, /batch"])
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
