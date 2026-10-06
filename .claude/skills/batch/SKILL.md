---
name: batch
description: Run /resume, /apply or /outreach over many job postings at once (an Excel or CSV target list, a text file of URLs, or URLs), using subagents so the main context stays small; all submits and LinkedIn sends still wait for the user's approval, collected in one review sheet. Use when the user runs /batch or asks to do several postings at once.
argument-hint: resume|apply|outreach <file.xlsx|file.csv|file.txt|dlq.md|url ...> [--rows 1-20] [--new] [--limit N] [--all] [--reason BLOCKED]
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
| 1a | Pre-screen: live? Canada-eligible? save `posting.md` | `haiku` | mechanical fetch and check |
| 1b | Resume tailoring | `opus` | truthfulness, content selection, page fit |
| 2 | Form fill + drafted free-text answers | `sonnet` | multi-step Chrome work, React selects |
| 2 | LinkedIn search + message drafts | `sonnet` | judging people, message tone |
| 5 | Submit an approved application | `haiku` | answers fixed; re-fill, verify, click |
| 5 | Send an approved LinkedIn message | `haiku` | verbatim text, attach, send |

**Escalation.** When a subagent's step fails (`FAILED`, `UNREADABLE`, or a garbled/incomplete
report), retry it once with the **next tier up**: `haiku` → `sonnet` → `opus`; a failure at `opus`
gets one more `opus` attempt. Only a failure after the escalated retry goes to the dead-letter queue.
Don't escalate outcomes a better model can't change: `CLOSED`, `INELIGIBLE`, `BLOCKED` (account,
CAPTCHA) or `NEEDS USER`. Record the model that produced each result in the manifest's Result
column (e.g. `ok 0.96 (opus)`, `submitted (haiku→sonnet)`).

## 0. Parse and confirm

1. `$ARGUMENTS`: first word is the mode (`resume`, `apply`, `outreach`); the rest are sources and
   filters. Missing mode or sources → ask.
2. `python tools/read_postings.py <sources> [--rows ..] [--new] [--all] [--reason ..]` → JSON
   list. It skips postings already `applied` or later in `applications.md`, and postings held in
   the dead-letter queue `dlq.md` (see "Dead-letter queue" below), unless `--all`. Apply `--limit N`
   (first N by rank) yourself. When the source is `dlq.md` (a retry run), set each picked row's
   Status to `retried` in `dlq.md` before launching.
3. Create `batches/<YYYY-MM-DD-HHMM>-<mode>/` with `postings.json` (the list) and `manifest.md`:
   a table `# | Rank | Company | Title | Posting dir | Stage | Result`, one row per posting.
4. **Confirm before launching** in one message: mode, number of postings, ranks, the flagged ones
   (unverified Canada eligibility; recommend skipping or keeping), and the rough cost: subagents
   per stage and model (e.g. "4 haiku pre-screens, ~20 opus resumes, ~20 sonnet form fills"). Wait for the user's go. A reply that trims the list (e.g. "skip 14, 97") is
   the go for the rest.
   **Workday history:** in `apply` or `outreach` mode, if any picked posting is Workday (URL host
   `myworkdayjobs.com` / `myworkdaysite.com`, or its `dlq.md` Detail or `postings/<dir>/posting.md`
   contains one of those or `Workday (`) and `profile.md` has no `## Workday work history`, build
   that section from `mega-resume-v1.5.tex` (format in `.claude/skills/apply/workday.md`, "Work
   history section"), show it in full in this same message, and save it on the user's approval before
   any prepare subagent.

## 1a. Pre-screen (every mode) — `haiku`, up to 4 subagents at a time, 5 postings each

Cheap check before any resume is paid for. Skip postings whose dir already has `posting.md`. Split
the rest into chunks of 5 and launch background `general-purpose` subagents with `model: haiku`:

> You are a batch pre-screen subagent in `C:\Users\<user>\Desktop\Github\jobapps`. For each posting
> below, fetch it with the job site's public JSON API where there is one (Greenhouse:
> `https://boards-api.greenhouse.io/v1/boards/<board>/jobs/<id>?questions=true`; Lever:
> `https://api.lever.co/v0/postings/<company>/<id>`; Ashby: `https://api.ashbyhq.com/posting-api/job-board/<board>`),
> else WebFetch. Do not use Chrome. Decide: CLOSED (404, "no longer available", expired),
> INELIGIBLE (the text excludes candidates based in Canada or Quebec; quote it), UNREADABLE (no
> posting text after both methods), or LIVE. For each LIVE posting, create
> `postings/<Company PascalCase>-<job id or short title slug>/posting.md` in the format of
> `postings/Durable-5156304008/posting.md` (header fields, "Application form fields" if the API
> gives them, then the full posting text verbatim, not summarized). Create nothing for the others.
> Postings: <rank. company, title, url — one per line>. Final reply: one line per posting,
> `<rank> LIVE <dir>` / `<rank> CLOSED: <evidence>` / `<rank> INELIGIBLE: <quote>` /
> `<rank> UNREADABLE: <what you tried>`.

`UNREADABLE` escalates (re-run that posting alone with `sonnet`); CLOSED and INELIGIBLE go straight
to the dead-letter queue. LIVE postings move on.

## 1b. Resume stage (every mode) — `opus`, up to 4 subagents at a time

For each LIVE posting without a verified resume (no `postings/<dir>/changelog.md`), launch a
background `general-purpose` subagent with `model: opus`, keeping **at most 4 running**; when one
finishes, launch the next. Prompt:

> You are a batch subagent for the `resume` skill in `C:\Users\<user>\Desktop\Github\jobapps`.
> Read `.claude/skills/resume/SKILL.md` and follow it exactly, including its "Running as a batch
> subagent" section, for posting dir `postings/<dir>` (its `posting.md` is already saved; use it
> instead of refetching). Do not ask the user anything. Final reply, at most 5 lines: posting dir,
> ok (true/false), fill, skills_lines, and "Questions for the user" (or none).

Update each manifest row and its `applications.md` row (you are the only writer of that file) from
the report (Stage `resume`, Result `ok 0.96 (opus)` / `FAILED: ..`). A failed build gets one more
`opus` attempt (see Model routing). **Every posting that ends this stage without an ok resume goes
to the dead-letter queue** and drops out of the later stages.

**Mode `resume` stops here** → go to step 3 (review), with only the resume parts.

## 2. Prepare stage (apply / outreach) — Chrome, at most 2 subagents at a time

All subagents share the user's one Chrome window, so **never more than 2** run at once. Never run two postings of the same Workday tenant at once
(shared session and candidate profile); queue the second. For each posting
with an ok resume, launch a background `general-purpose` subagent with `model: sonnet` (a failed
fill escalates to `opus`):

> You are a batch subagent for the `<apply|outreach>` skill in `C:\Users\<user>\Desktop\Github\jobapps`.
> Read `.claude/skills/<apply|outreach>/SKILL.md` and follow its "Running as a batch subagent"
> section for posting dir `postings/<dir>` (URL <url>). The resume is already built; reuse it.
> Load the `claude-in-chrome` skill first. Create your **own new tab** and use only that tab id;
> never touch, navigate or close other tabs. Never click Submit/Send/Connect. Do not ask the user
> anything. Final reply, at most 5 lines: posting dir, tab URL, number of ASK fields, blockers
> (e.g. needs an account login (non-Workday), NO-WORKDAY-LOGIN <tenant> <workday url>, CAPTCHA before the form, closed), outreach drafts path if any.

Blockers (needs an account login/sign-up (non-Workday), NO-WORKDAY-LOGIN / NO-WORKDAY-HISTORY from a Workday posting, CAPTCHA before the form, unsupported site) go to the
dead-letter queue as `BLOCKED` with what would unblock them; a form fill that fails at `sonnet`
and again at `opus` goes as `FAILED`. Either way the posting drops out of the review's approval list (its resume is still
listed there, so the user can apply by hand).

## 3. Review sheet — one approval round for everything

Write `batches/<id>/review.md` from the posting files (read only what the sheet needs):

1. **Questions, deduplicated across postings.** The same question asked by several forms (salary,
   work authorization, relocation, EEO, "how did you hear") appears once, listing the postings that
   ask it. Reusable answers go to `profile.md` once the user answers.
2. **Per posting** (numbered as in the manifest): company, title, resume PDF path, fill, the
   changelog's gaps and "please sanity-check" lines (one line each), `draft` free-text answers
   verbatim, posting-specific ASKs, blockers. For outreach: the shortlist (name, title, location, why)
   and each drafted message verbatim. For Workday postings: the tenant, the step the fill stopped on,
   the consent checkbox label quoted (or "no consent checkbox"), and the "After approval" rows;
   their ASKs join item 1.
3. **Dead-lettered in this run**: a short table (company, title, reason, needs), not mixed into
   the approval list.
   - **Workday logins needed**: every `open` row in `dlq.md` whose Detail starts with
     `NO-WORKDAY-LOGIN` (not only this run's), grouped by tenant; rows from this run marked
     `(this run)`. Per tenant: one sign-in URL (the `<workday url>` from the Detail of its first such
     row) and the posting dirs it would unblock. After signing in or creating the accounts (Chrome
     saves the passwords), re-run `/batch <apply|outreach> dlq.md --reason BLOCKED` in each row's
     original mode.
4. A **reply format** at the top, e.g.
   `answers: salary=150k CAD, ... | approve: all | except: 3, 7 | edit 5: <text> | outreach 2: ann, bob`.

**Questions go in a separate text file, which is what the user answers** (the user's preference, 2026-10-04).
Write `batches/<id>/questions.txt`: plain text, numbered questions, each followed by an `Answer:`
line, with a suggested answer where there is an obvious one ("leave blank to accept"). Use these
parts, in this order:
1. Reusable answers, deduplicated, each with the postings that ask it.
2. One-off form questions.
3. Drafted free-text answers to OK or edit, each pasted **in full, verbatim**: exactly the text that will go into the form. Never show a summary or a shorthand note. If `application.md` holds only a note for a free-text field, write the full answer first. A note in a free-text cell is not an approvable draft, and the execute subagent must never type a note into a form (Censys, 2026-10-04). Cover letters belong here too: the full `cover_letter.md` text, verbatim.
4. Decisions: which applications to submit, blocked or odd postings, retries.
5. LinkedIn picks per company: the suggested top 3 plus the other names; "ok" accepts the top 3.

**Apply `profile.md` first:** never ask a question it already answers or has a standing rule for
(salary from the posted range, sponsorship by role location, relocation, start date, EEO, and so
on). review.md is the reference with the full texts; questions.txt is the only thing the user fills in.
Open questions.txt for the user (`Invoke-Item`), not review.md. When the user says it's done, re-read it,
save every answer that could come up again to `profile.md` (as a rule when the answer carries
"always" or a condition), and ask any follow-ups in a short `questions-2.txt`.

Post a 5-line summary in chat (counts: ready, ASKs, dead-lettered by reason). Wait. Nothing is
approved by silence or by an approval given for a different posting or an earlier batch.

## 4. Record approvals

Parse the user's reply. Save reusable answers to `profile.md`. For each posting, append to
`postings/<dir>/application.md`: `APPROVED <date>: submit` (with any edits applied to its answer
table), and in `outreach.md` mark each approved person + message `APPROVED <date>`. Anything
unclear → ask before recording. Postings the user skips go to the dead-letter queue as `SKIPPED`
(with the user's reason, if given) so they aren't re-proposed next run; postings the user defers ("not yet")
get Stage `held` in the manifest instead.

## 5. Execute stage — Chrome, at most 2 subagents at a time

Only for postings with a recorded approval. Same-tenant Workday postings run one at a time, as in stage 2. Launch with `model: haiku`; a failed submit or send
(not `NEEDS USER`) escalates to `sonnet`. Subagent prompt:

> You are a batch execute subagent in `C:\Users\<user>\Desktop\Github\jobapps`. Read
> `.claude/skills/<apply|outreach>/SKILL.md`, section "Batch execute mode", and run it for
> `postings/<dir>`. Act only on items marked `APPROVED` in that folder's files. Own tab only.
> If you hit a CAPTCHA, an email verification code, or anything needing the user, stop and reply
> `NEEDS USER: <what, which tab>`. Final reply, at most 5 lines: what was submitted/sent, and proof
> (confirmation text or screenshot path).

On `NEEDS USER`, ask the user (batch these too if several arrive together), then continue that posting
with `SendMessage` to the same subagent. If the user can't resolve it now, or the submit/send fails
twice, dead-letter it (`BLOCKED` / `FAILED`, stage `execute`).

## 6. Finish

Update `manifest.md` and `applications.md`, then report in chat: submitted, sent, held, and
dead-lettered by reason (counts + posting numbers), the manifest path, and the retry command for
anything retryable (`/batch <mode> dlq.md`, or `--reason BLOCKED` once the user has e.g. created the
accounts). Leave `batches/<id>/` in place.

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
- A retried posting that now succeeds: set its row to `resolved`. the user can mark rows `dropped`.

Mirror each dead-lettered posting in the manifest (Result `DLQ: <reason>`) and in `applications.md`
only if it already had a row there.
