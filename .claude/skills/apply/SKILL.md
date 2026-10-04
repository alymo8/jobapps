---
name: apply
description: Build the tailored resume for a job posting (/resume) and fill the online application in Chrome, then submit only after the user's explicit OK. Use when the user runs /apply or asks to apply to a posting; /outreach runs this first.
argument-hint: <posting URL> | <posting dir> --submit
---

# /apply — /resume + fill the application, submit on OK

All paths are relative to `jobapps/`. Uses the Chrome browser (load the `claude-in-chrome` skill
before the first browser call). Two phases: **prepare** (fill the form) and **submit** (only on the user's OK).
Submitting is irreversible and outward-facing: **never click Submit without an explicit OK from the user
for this specific application in this session.**

## Phase 1: prepare

1. **Resume.** If `postings/<dir>/` already has a resume PDF that passed verification (its
   `changelog.md` exists), reuse it. Otherwise run the full `/resume` skill steps first.
2. **Answers source.** Read `profile.md` (reusable answers) and `mega_resume.tex` (facts).
3. **Open the application** in a new Chrome tab (the posting URL; on Greenhouse the form is on the
   same page under "Apply"). Read the whole form first with `read_page`/`get_page_text` and list
   every field: label, type, required or optional, options for selects.
4. **Answer every field**, writing `postings/<dir>/application.md`: one line per field,
   `label | answer | source` where source is `profile`, `mega_resume`, `posting` or `ASK`.
   - Contact fields: `profile.md`. Resume upload: the posting's PDF (`file_upload`).
   - Cover letter: skip if optional. If required, draft one from `mega_resume.tex` facts only, save
     it as `postings/<dir>/cover_letter.md`/`.pdf`, and mark it for the user's review.
   - "Why this company/role" free text: draft 2–4 sentences from the posting + mega resume facts,
     mark `draft` so the user sees it.
   - Voluntary EEO questions: use `profile.md`; if `ASK`, ask the user (never guess these).
   - Anything not answerable from `profile.md` or `mega_resume.tex`: **ask the user**, all such questions
     at once, in one message. Save each answer that is reusable into `profile.md` under the right heading.
   - Never invent facts (dates, employers, degrees, authorization, salary).
5. **Fill the form** in Chrome (`form_input`/`computer`; React selects need clicking the option).
   Upload the resume. Then re-read the form and confirm each field shows the intended value and the
   upload shows the right filename.
6. **Stop for approval.** Show the user a compact summary: role, company, resume filename, and the table
   from `application.md` (highlight `draft` and newly-answered rows). Update `applications.md` to
   `ready`. Ask: "Submit? (ok / edits)".

## Phase 2: submit (on the user's "ok" only)

1. Apply any edits the user gave; re-verify the changed fields.
2. Click Submit. Handle what follows:
   - CAPTCHA: ask the user to solve it in the open tab, then continue.
   - Email verification code (Greenhouse sometimes sends one): ask the user for the code, enter it.
   - Validation errors: fix and re-show only what changed before submitting again.
3. **Verify:** the confirmation page/message is shown. Screenshot it to
   `postings/<dir>/confirmation.png` if possible, otherwise record its text in `application.md`.
4. Update `applications.md` row to `applied` with the date. Report done.

## Postings that can't be applied to

In a normal (non-batch) run: if the site needs an account the user doesn't have, the form can't be
filled or submitted after a retry, or the user decides to skip it, add or update its row in `dlq.md`
(reason `BLOCKED` / `FAILED` / `SKIPPED`, with what would unblock it under `Needs`, status `open`)
and tell the user. The resume stays in the posting folder for a manual application.

## Running as a batch subagent

When the prompt says you are a batch subagent (orchestrated by the `batch` skill): run Phase 1
steps 1–5 **without asking the user anything**, in your own Chrome tab only. Put every unanswerable field
in `application.md` as `ASK` with the exact question and options, leave that field empty, and record
the tab URL at the top of `application.md`. If the site needs an account login or sign-up, or a
CAPTCHA blocks the form, stop and report it as a blocker (don't create accounts). End with a short
report: posting dir, number of `ASK` fields, blockers. **Never submit in a batch subagent.**

## Batch execute mode

Run only when `application.md` contains `APPROVED <date>: submit`. Open the application in your own
new tab (the earlier tab may be gone), fill it from the `application.md` table (which now holds
the user's answers and edits, no `ASK` left; if one is left, stop and report it), upload the resume,
re-verify every field, then run Phase 2 steps 2–3 (the orchestrator updates `applications.md`; never write it in batch). CAPTCHA or email code → stop and reply
`NEEDS USER: ...` with the tab URL instead of asking.
