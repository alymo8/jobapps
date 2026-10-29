---
name: batch
description: Run /resume, /apply or /outreach over many job postings at once (an Excel or CSV target list, a text file of URLs, or URLs), using subagents so the main context stays small; all submits and messages to the user's existing LinkedIn connections wait for the user's approval, collected in one review sheet (connection requests to new people go out without it). Use when the user runs /batch or asks to do several postings at once.
argument-hint: resume|apply|outreach <file.xlsx|file.csv|file.txt|dlq.md|url ...> [--rows 1-20] [--new] [--limit N] [--all] [--reason BLOCKED] [--min-score N] [--apply]
---

# /batch — many postings, subagents, one review

All paths are relative to `jobapps/`. You are the **orchestrator**: you never build a resume, fill
a form or browse LinkedIn yourself. Subagents do that work and write results to files; you read
only their short reports and the files you need for the review sheet. Keep your context small.

## Model routing

Every subagent launch passes `model` explicitly (Agent tool `model` parameter); never rely on the
default. Pick by how much judgment the step needs:

| Stage | Task | Model | Why |
|-------|------|-------|-----|
| 1a | Pre-screen: live? eligible for `<eligible_regions>`? save `posting.md` | `haiku` | mechanical fetch and check |
| 1a.5 | Fit, pay and legitimacy score (`scoring.md`) | `sonnet` | judgment, but no writing |
| 1b | Resume tailoring | `opus` | truthfulness, content selection, page fit |
| 2 | Form fill + drafted free-text answers | `sonnet` | multi-step Chrome work, React selects |
| 2b | LinkedIn search + message drafts | `sonnet` | judging people, message tone |
| 5 | Submit an approved application | `haiku` | answers fixed; re-fill, verify, click |
| 5 | Send an approved LinkedIn message | `haiku` | verbatim text, send |

**Escalation.** When a subagent's step fails (`FAILED`, `UNREADABLE`, or a garbled/incomplete
report), retry it once with the **next tier up**: `haiku` → `sonnet` → `opus`; a failure at `opus`
gets one more `opus` attempt. Only a failure after the escalated retry goes to the dead-letter queue.
Don't escalate outcomes a better model can't change: `CLOSED`, `INELIGIBLE`, `BLOCKED` (account,
CAPTCHA) or `NEEDS USER`. Record the model that produced each result in the manifest's Result
column (e.g. `ok 0.96 (opus)`, `submitted (haiku→sonnet)`).

## 0. Parse and confirm

1. `$ARGUMENTS`: first word is the mode (`resume`, `apply`, `outreach`); the rest are sources and
   filters. Missing mode or sources → ask. `--apply` only counts in `outreach` mode: without it,
   `outreach` mode is LinkedIn only (no application); with it, `outreach` also applies. In
   `resume` or `apply` mode, `--apply` is ignored with a one-line note.
2. `python tools/read_postings.py <sources> [--rows ..] [--new] [--all] [--reason ..]` → JSON
   list. In `outreach` mode without `--apply`, append `--for outreach` to this call; with
   `--apply`, keep the call as it is. It skips postings already `applied` or later in
   `applications.md` (with `--for outreach`: skips already-messaged postings and keeps `applied`
   ones), and postings held in
   the dead-letter queue `dlq.md` (see "Dead-letter queue" below), unless `--all`. `--limit N` and `--min-score N` are handled here, not passed to `read_postings.py`. Apply `--limit N`
   (first N by rank) yourself. When the source is `dlq.md` (a retry run), set each picked row's
   Status to `retried` in `dlq.md` before launching. Keep each posting's `status` from
   `postings.json` as its **pre-run status**; every later status choice in this run uses it.
3. Create `batches/<YYYY-MM-DD-HHMM>-<mode>/` with `postings.json` (the list) and `manifest.md`:
   a table `# | Rank | Company | Title | Posting dir | Stage | Score | Result`, one row per posting.
4. **Pull the sources** once, following `.claude/skills/pull-sources.md`. This comes before the
   confirm step, which builds the Workday work history from `sources/mega-resume.tex`, and before
   any subagent launches.
5. **Confirm before launching** in one message: mode (`Mode: outreach only (no application)` or
   `Mode: outreach + apply` in `outreach` mode), number of postings, ranks, the flagged ones
   (unverified eligibility; recommend skipping or keeping), and the rough cost: subagents
   per stage and model (e.g. "4 haiku pre-screens, 4 sonnet scorers, ~20 opus resumes, ~20 sonnet form fills"). Wait for the user's go. A reply that trims the list (e.g. "skip 14, 97") is
   the go for the rest.
   **Workday history:** in `apply` mode or `outreach --apply` (not in outreach-only mode), if any picked posting is Workday (URL host
   `myworkdayjobs.com` / `myworkdaysite.com`, or its `dlq.md` Detail or `postings/<dir>/posting.md`
   contains one of those or `Workday (`) and `sources/profile.md` has no `## Workday work history`, build
   that section from `sources/mega-resume.tex` (format in `.claude/skills/apply/workday.md`, "Work
   history section"), show it in full in this same message, and save it on the user's approval through `.claude/skills/write-source.md` before
   any prepare subagent.
   **Targeting:** if `sources/profile.md` has no `## Targeting` section, say so in this message and offer to
   add it through `.claude/skills/write-source.md` with these keys: `Pay floor: skip when the top of the posted range is below <amount> <currency>`,
   `USD to <currency> rate`, `Score threshold`, `Years of experience`, `Target roles`, `Deal-breakers` (no `targeting`: `<currency>` is `USD` and the `USD to <currency> rate` key is left out; ask
   the user for the values). If the user declines, the run skips stage 1a.5 and the gate (Score `n/a`), and this message
   says so.
   **Threshold:** `--min-score N` if given, else `Score threshold` from `## Targeting`. Without
   `## Targeting`, `--min-score` is ignored and this message says so.
   `--min-score 0` turns off all skipping, `PAY-FLOOR` included.

## 1a. Pre-screen (every mode) — `haiku`, up to 4 subagents at a time, 5 postings each

In every subagent prompt below, replace `<repo-root>` with the output of `git rev-parse --show-toplevel`, `<eligible_regions>` with config `targeting.eligible_regions` joined by ` or `, and `<currency>` with config `targeting.currency` (`USD` when absent). Without `targeting`, drop the INELIGIBLE clause from the pre-screen prompt.

Cheap check before any resume is paid for. Skip postings whose dir already has `posting.md`. Split
the rest into chunks of 5 and launch background `general-purpose` subagents with `model: haiku`:

> You are a batch pre-screen subagent in the repo root `<repo-root>`. For each posting
> below, fetch it with the job site's public JSON API where there is one (Greenhouse:
> `https://boards-api.greenhouse.io/v1/boards/<board>/jobs/<id>?questions=true`; Lever:
> `https://api.lever.co/v0/postings/<company>/<id>`; Ashby: `https://api.ashbyhq.com/posting-api/job-board/<board>`),
> else WebFetch. Do not use Chrome. Decide: CLOSED (404, "no longer available", expired),
> INELIGIBLE (the text excludes candidates based in any of `<eligible_regions>`; quote it), UNREADABLE (no
> posting text after both methods), or LIVE. For each LIVE posting, create
> `postings/<Company PascalCase>-<job id or short title slug>/posting.md` in the format of
> `posting.md` in `.claude/skills/resume/SKILL.md` step 2 (header fields, "Application form fields" if the API
> gives them, then the full posting text verbatim, not summarized). Create nothing for the others.
> Postings: <rank. company, title, url — one per line>. Final reply: one line per posting,
> `<rank> LIVE <dir>` / `<rank> CLOSED: <evidence>` / `<rank> INELIGIBLE: <quote>` /
> `<rank> UNREADABLE: <what you tried>`.

`UNREADABLE` escalates (re-run that posting alone with `sonnet`); CLOSED and INELIGIBLE go straight
to the dead-letter queue. LIVE postings move on.

## 1a.5. Score (every mode) — `sonnet`, up to 4 subagents at a time, 5 postings each

Which postings: every LIVE posting (including those that skipped 1a because `posting.md` was
already there) that has no `postings/<dir>/changelog.md`. Those with a `score.md` aren't rescored.
Split the rest into chunks of 5 and launch background `general-purpose` subagents with
`model: sonnet`:

> You are a batch scoring subagent in the repo root `<repo-root>`. Read
> `.claude/skills/batch/scoring.md` and follow it for each posting dir below. Inputs:
> `postings/<dir>/posting.md`, `sources/mega-resume.tex`, `sources/profile.md` section `## Targeting`, and
> `applications.md` and `dlq.md` (read only, for the repeats signal). No web access. Write
> `postings/<dir>/score.md` for each. The sources in `sources/` are already pulled; don't pull them
> again. Do not ask the user anything. Final reply: one line per
> posting, `<rank> <dir> <score> | fit <f> | pay <p> | legit <tier> | <reason>`, or
> `<rank> <dir> PAY-FLOOR <top of range in <currency>> | <reason>`. Posting dirs: <rank. dir — one per line>

A garbled or incomplete line gets one retry at `opus` for that posting; still bad → dead-letter it
`FAILED`, stage `score`.

**Gate.** Every posting that reaches the gate with a `score.md` (read its `- Overall:` line), scored
in this run or earlier, is compared with the threshold, except postings with `changelog.md` (Score
`-`) and override postings; write its overall into the manifest's Score column (`PAY-FLOOR` for a pay-floor miss).
Below threshold, or `PAY-FLOOR`:

- `dlq.md` row: Reason `LOW-SCORE`, Stage `score`, Detail `<score>: <reason>` (or
  `PAY-FLOOR <amount> <currency>: <reason>`), Needs `nothing, or /batch <mode> dlq.md --reason LOW-SCORE
  to override`, Status `open`.
- Manifest Result `DLQ: LOW-SCORE 2.8` or `DLQ: LOW-SCORE PAY-FLOOR 95900`. The posting drops out
  of later stages; don't wait for the user.

With `--min-score 0`, nothing is skipped: `PAY-FLOOR` postings keep Score `PAY-FLOOR` (the flag
lives in the Score column; later stages overwrite Result) and go on.

**Override.** In a run whose source is `dlq.md` with `--reason LOW-SCORE`, skip the gate: keep each
posting's `score.md`, set Result `override <score>`, and go on to 1b. That covers every open
`LOW-SCORE` row (narrow with `--rows`). One posting: `/batch <mode> <url> --min-score 0 --all`.
When an overridden posting ends 1b with an ok resume, set its `dlq.md` row to `resolved` (either
override path; a single-URL override is a posting whose `read_postings.py` JSON has
`dlq == "LOW-SCORE"` in a `--min-score 0` run), so later normal runs pick it up.

## 1b. Resume stage (every mode) — `opus`, up to 4 subagents at a time

For each LIVE posting that passed the gate (or every LIVE posting when 1a.5 was skipped) and has no verified resume (no `postings/<dir>/changelog.md`), launch a
background `general-purpose` subagent with `model: opus`, keeping **at most 4 running**; when one
finishes, launch the next. Prompt:

> You are a batch subagent for the `resume` skill in the repo root `<repo-root>`.
> Read `.claude/skills/resume/SKILL.md` and follow it exactly, including its "Running as a batch
> subagent" section, for posting dir `postings/<dir>` (its `posting.md` is already saved; use it
> instead of refetching). Do not ask the user anything. Final reply, at most 5 lines: posting dir,
> ok (true/false), fill, skills_lines, and the changelog's `Questions for <…>` section (any heading of that form), or none.
> The sources in `sources/` are already pulled; don't pull them again.

Update each manifest row and its `applications.md` row (you are the only writer of that file) from
the report (Stage `resume`, Result `ok 0.96 (opus)` / `FAILED: ..`). Scoring (1a.5) runs as
above in every mode. Stage 1b never overwrites a pre-run status of `applied`, `outreach-*`,
`outreach-only-*`, `in-conversation`, `no-response` or `closed`: for those rows it writes only
Notes `resume ok <date>`. A failed build gets one more
`opus` attempt (see Model routing). **Every posting that ends this stage without an ok resume goes
to the dead-letter queue** and drops out of the later stages.

**Mode `resume` stops here** → go to step 3 (review), with only the resume parts.

## 2. Prepare stage (apply / outreach) — Chrome, at most 2 subagents at a time

All subagents share the user's one Chrome window, so **never more than 2** run at once. This stage
never opens LinkedIn: LinkedIn work is stage 2b, one posting at a time. In outreach-only mode there
is no stage 2 (no form); go to stage 2b. Never run two postings of the same Workday tenant at once
(shared session and candidate profile); queue the second. For each posting
with an ok resume, launch a background `general-purpose` subagent with `model: sonnet` (a failed
fill escalates to `opus`):

> You are a batch subagent for the `<apply|outreach>` skill in the repo root `<repo-root>`.
> Read `.claude/skills/<apply|outreach>/SKILL.md` and follow its "Running as a batch subagent"
> section for posting dir `postings/<dir>` (URL <url>). The resume is already built; reuse it.
> The sources in `sources/` are already pulled; don't pull them again.
> Load the `claude-in-chrome` skill first. Create your **own new tab** and use only that tab id;
> never touch, navigate or close other tabs. Never click Submit/Send/Connect. Do not ask the user
> anything. Final reply, at most 5 lines: posting dir, tab id and URL, number of ASK fields, blockers
> (e.g. needs an account login (non-Workday), NO-WORKDAY-LOGIN <tenant> <workday url>, CAPTCHA before the form, closed), outreach drafts path if any.
> <outreach + apply only: the lines `Mode: outreach + apply` and `Application only`>

With `--apply` the prompt carries the mode line `Mode: outreach + apply` and always the extra line
`Application only` (`/apply` Phase 1, no LinkedIn search or drafts). A posting whose pre-run status
is `outreach-only-*`, `in-conversation`, `no-response` or `closed` gets only this part: it skips
stage 2b.

## 2b. LinkedIn stage (outreach) — one subagent at a time

A LinkedIn tab is heavy and grows with use; several at once crashed the user's 16 GB laptop
([ADR 0007](../../../knowledge/decisions/0007-light-linkedin-runs.md)). So exactly **one** LinkedIn
subagent runs at a time; the next starts only after the previous one has reported (its tab is
closed by then). It may run while stage 2 form fills are still going (at most 2 form tabs + 1
LinkedIn tab). Run it for each outreach posting with an ok resume that is not dead-lettered and not
application-only, with `model: sonnet`:

> You are a batch subagent for the `outreach` skill in the repo root `<repo-root>`.
> Read `.claude/skills/outreach/SKILL.md` and follow its "Running as a batch subagent" section for
> posting dir `postings/<dir>` (URL <url>). The resume is already built; the sources in `sources/`
> are already pulled. Load the `claude-in-chrome` skill first, then follow
> `.claude/skills/linkedin-tab.md`: one LinkedIn tab of your own, recycled every 8 page opens,
> closed when you finish. Never touch other tabs. Never click Send/Connect. Do not ask the user
> anything. Final reply, at most 5 lines: posting dir, outreach drafts path, existing connections
> found (names), blockers.
> <the mode line, `Mode: outreach only (no application)` or `Mode: outreach + apply`>
> <outreach + apply only: `LinkedIn only`>

A CAPTCHA or restriction warning here stops stage 2b for every remaining posting (no more LinkedIn
subagents this run); say so in the review.

Blockers (needs an account login/sign-up (non-Workday), NO-WORKDAY-LOGIN / NO-WORKDAY-HISTORY from a Workday posting, CAPTCHA before the form, unsupported site) go to the
dead-letter queue as `BLOCKED` with what would unblock them; a form fill that fails at `sonnet`
and again at `opus` goes as `FAILED`. Either way the posting drops out of the review's approval list (its resume is still
listed there, so the user can apply by hand).

## 3. Review sheet — one approval round for everything

Write `batches/<id>/review.md` from the posting files (read only what the sheet needs):

1. **Questions, deduplicated across postings.** The same question asked by several forms (salary,
   work authorization, relocation, EEO, "how did you hear") appears once, listing the postings that
   ask it. Reusable answers go to `sources/profile.md` through `.claude/skills/write-source.md` once the user answers.
2. **Per posting** (numbered as in the manifest): company, title, resume PDF path, fill, the score line from `score.md` (`<overall> | fit | pay | legit`, for a pay-floor miss `PAY-FLOOR | fit <f> | pay PAY-FLOOR | legit <tier>`; prefixed `override` when the posting came through a `--reason LOW-SCORE` retry or a `--min-score 0` URL override) and its real gaps, any contractor-wording note, the
   changelog's gaps and "please sanity-check" lines (one line each), `draft` free-text answers
   verbatim, posting-specific ASKs, blockers. For outreach: the shortlist (name, title, location, class, why)
   and each drafted message verbatim, existing connections first. For Workday postings: the tenant, the step the fill stopped on,
   the consent checkbox label quoted (or "no consent checkbox"), and the "After approval" rows;
   their ASKs join item 1.
3. **Dead-lettered in this run**: a short table (company, title, reason, needs), not mixed into
   the approval list.
   - **Skipped on score**: a separate table (company, title, score or `PAY-FLOOR <amount>`, reason)
     for this run's `LOW-SCORE` rows (listed here only, not again in the dead-lettered table), with
     the override command
     `/batch <mode> dlq.md --reason LOW-SCORE` (or one URL with `--min-score 0 --all`).
   - **Workday logins needed**: every `open` row in `dlq.md` whose Detail starts with
     `NO-WORKDAY-LOGIN` (not only this run's), grouped by tenant; rows from this run marked
     `(this run)`. Per tenant: one sign-in URL (the `<workday url>` from the Detail of its first such
     row) and the posting dirs it would unblock. After signing in or creating the accounts (Chrome
     saves the passwords), re-run `/batch <apply|outreach> dlq.md --reason BLOCKED` in each row's
     original mode.
4. A **reply format** at the top, e.g.
   `answers: salary=150k <currency>, ... | approve: all | except: 3, 7 | edit 5: <text> | outreach 2: ann, bob`.

**Questions go in a separate text file, which is what the user answers** (the user's preference, 2026-10-04).
Write `batches/<id>/questions.txt`: plain text, numbered questions, each followed by an `Answer:`
line, with a suggested answer where there is an obvious one ("leave blank to accept"). Use these
parts, in this order:
1. Reusable answers, deduplicated, each with the postings that ask it.
2. One-off form questions.
3. Drafted free-text answers to OK or edit, each pasted **in full, verbatim**: exactly the text that will go into the form. Never show a summary or a shorthand note. If `application.md` holds only a note for a free-text field, write the full answer first. A note in a free-text cell is not an approvable draft, and the execute subagent must never type a note into a form (a company, 2026-10-04). Cover letters belong here too: the full `cover_letter.md` text, verbatim.
4. Decisions: which applications to submit, blocked or odd postings, retries.
5. LinkedIn per company: **the names of the user's existing connections** to message, each with its message
   verbatim to OK or edit; then the new people for information only (they get connection requests at
   execute without approval; "skip <name>" drops one).

**Apply `sources/profile.md` first:** never ask a question it already answers or has a standing rule for
(salary from the posted range, sponsorship by role location, relocation, start date, EEO, and so
on). review.md is the reference with the full texts; questions.txt is the only thing the user fills in.
Open questions.txt for the user (`Invoke-Item`), not review.md. When the user says it's done, re-read it,
save every answer that could come up again to `sources/profile.md` through `.claude/skills/write-source.md` (as a rule when the answer carries
"always" or a condition), and ask any follow-ups in a short `questions-2.txt`.

**Outreach-only mode:** postings have no application, form-question or submit parts, in review.md
or questions.txt: only the LinkedIn part (questions.txt part 5) and decisions (part 4).

Post a 5-line summary in chat (counts: ready, ASKs, dead-lettered by reason). Wait. Nothing is
approved by silence or by an approval given for a different posting or an earlier batch.

## 4. Record approvals

Parse the user's reply. Save reusable answers to `sources/profile.md` through `.claude/skills/write-source.md`. For each posting, append to
`postings/<dir>/application.md`: `APPROVED <date>: submit` (with any edits applied to its answer
table), and in `outreach.md` mark each approved person + message `APPROVED <date>`. Anything
unclear → ask before recording.
**Outreach-only mode:** skip the `application.md` `APPROVED <date>: submit` write. For each posting
the user did not skip, write `APPROVED <date>: outreach` as the last line of the `## Shortlist` section
of `postings/<dir>/outreach.md`; the user's reply without a `skip` for the posting is the go. Per-person
`APPROVED <date>` marks for existing connections work as above. In outreach-only mode a posting the user
skips gets Stage `skipped` in the manifest and is not dead-lettered (declining messages must not
keep it out of a later `/batch apply`). In other modes, postings the user skips go to the dead-letter queue as `SKIPPED`
(with the user's reason, if given) so they aren't re-proposed next run; postings the user defers ("not yet")
get Stage `held` in the manifest instead.

## 5. Execute stage — Chrome, at most 2 subagents at a time (1 in `outreach` mode)

In `outreach` mode each execute subagent may send on LinkedIn, so they run **one at a time**
(stage 2b's rule); `apply` mode keeps 2.

Only for postings with a recorded approval (an `APPROVED <date>: outreach` mark in `outreach.md`
counts, so a posting with only new people still reaches execute). Same-tenant Workday postings run one at a time, as in stage 2. Launch with `model: haiku`; a failed submit or send
(not `NEEDS USER`) escalates to `sonnet`. Subagent prompt:

> You are a batch execute subagent in the repo root `<repo-root>`. Read
> `.claude/skills/<apply|outreach>/SKILL.md`, section "Batch execute mode", and run it for
> `postings/<dir>`. Act only on items marked `APPROVED` in that folder's files. Own tab only;
> LinkedIn work follows `.claude/skills/linkedin-tab.md` (one tab, closed when you finish).
> The sources in `sources/` are already pulled; don't pull them again.
> If you hit a CAPTCHA, an email verification code, or anything needing the user, stop and reply
> `NEEDS USER: <what, which tab>`. Final reply, at most 5 lines: what was submitted/sent, and proof
> (confirmation text or screenshot path).
> <outreach mode only: the mode line, `Mode: outreach only (no application)` or `Mode: outreach + apply`>
> <outreach + apply only, for a posting whose pre-run status is `outreach-only-*`, `in-conversation`, `no-response` or `closed`: `Application only`>

In outreach-only mode the execute subagent sends only; nothing is submitted.

The execute subagent closes its own tabs after a confirmed submit (`/apply` Phase 2 step 4). When
it reports a confirmed submit, close that posting's prepare-stage tab too, if it is still open
(`tabs_context_mcp`, then `tabs_close_mcp` on the tab id or URL its prepare subagent reported).
Close no other tab. Leave tabs open for anything held, `NEEDS USER`, failed or dead-lettered.

On `NEEDS USER`, ask the user (batch these too if several arrive together), then continue that posting
with `SendMessage` to the same subagent. If the user can't resolve it now, or the submit/send fails
twice, dead-letter it (`BLOCKED` / `FAILED`, stage `execute`).

## 6. Finish

Update `manifest.md` and `applications.md`, then report in chat: submitted, sent, held, and
dead-lettered by reason (counts + posting numbers), the manifest path, and the retry command for
anything retryable (`/batch <mode> dlq.md`, or `--reason BLOCKED` once the user has e.g. created the
accounts). Leave `batches/<id>/` in place.

**`applications.md` statuses** use each posting's pre-run status
(step 0.2):

- **Outreach-only mode:** `outreach-only-ready` (an existing-connection message waits on the user's OK)
  or `outreach-only-sent`; when the pre-run status was `applied` or `outreach-ready`, use
  `outreach-ready` / `outreach-sent` instead. When the pre-run status was `ready` (a form filled,
  awaiting OK), add `form filled <date>, not submitted` to the Notes cell.
- **Prepare on an already-messaged row** (pre-run `outreach-only-*`, `in-conversation`,
  `no-response` or `closed`, after stage 2): the status stays; the Notes cell gets
  `form filled <date>, awaiting OK`. A declined or failed submit leaves the status unchanged and
  turns that note into `form filled <date>, not submitted`.
- **Post-submit mapping** in `apply` mode and `outreach --apply`: pre-run `outreach-only-ready` →
  `outreach-ready`, `outreach-only-sent` → `outreach-sent`; pre-run `in-conversation`, `no-response`
  or `closed` keep their status and get `applied <date>` in Notes; anything else → `applied`.
- **Legend safety net:** when you write an `applications.md` row and the legend line lacks
  `outreach-only`, rewrite the legend line to:
  ``Status: `resume` → `ready` (form filled, awaiting OK) → `applied` → `outreach-ready` → `outreach-sent` → `in-conversation` | `no-response` | `closed`; not applied: `outreach-only-ready` → `outreach-only-sent`.``

**Shortlist.** Only when something was submitted (never in outreach-only mode): when execute confirmed one or more submits, list them (company, title) and ask once
`Mark these <n> as applied?` (yes / pick some), the batch form of `Mark <company> – <title> as applied?`.
On yes, run steps 1-2 of "Record applied" in `.claude/skills/job-shortlist/SKILL.md` for each chosen
posting (find, `get`, `doc --existing` when the document exists; note `tailored resume + cover letter`
or `tailored resume`), then write them with one `ArtifactData batch` per 50 writes, each existing
document with its `if_version`. Confirm with one `Recorded: Applied — ...` line per posting.

## Dead-letter queue

`dlq.md` (in `jobapps/`) is the one persistent list of postings that couldn't be processed, across
all runs. **Only you (the orchestrator) write it**; subagents report, you record. One row per
posting URL: if a row for the URL exists, update it in place (new date, batch, stage, reason,
detail, status `open`) rather than adding a second row. Columns and reason codes are defined at the
top of `dlq.md`:

- `Detail`: the subagent's evidence in one line (HTTP status, the page's "no longer accepting"
  text, which login wall).
- `Needs`: what would unblock it, concretely ("the user signs in / creates the account at <tenant> (Chrome saves the password)",
  "re-check next week", "nothing, closed").
- `LOW-SCORE` (stage `score`) is written only by the 1a.5 gate; `read_postings.py` never retries it unless `--reason LOW-SCORE` is given.
- A retried posting that now succeeds: set its row to `resolved`. The user can mark rows `dropped`.

Mirror each dead-lettered posting in the manifest (Result `DLQ: <reason>`) and in `applications.md`
only if it already had a row there.
