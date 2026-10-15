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
2. **Answers source.** Read `profile.md` (reusable answers) and `mega-resume-v1.5.tex` (facts).
   When the form has free-text or cover letter fields, also read `answers.md` (the user's past free-text
   answers) and `stories.md` (STAR behavioral stories, indexed by leadership principle).
3. **Open the application** in a new Chrome tab (the posting URL; on Greenhouse the form is on the
   same page under "Apply"). Read the whole form first with `read_page`/`get_page_text` and list
   every field: label, type, required or optional, options for selects.

   **Workday** (`*.myworkdayjobs.com`, `*.myworkdaysite.com`, or an Apply button leading there):
   read `.claude/skills/apply/workday.md` and follow it instead of steps 3–6 here and Phase 2
   (sign-in through Chrome's saved password, Apply Manually, step-by-step fill, stop before the
   consent checkbox).
4. **Answer every field**, writing `postings/<dir>/application.md`: one line per field,
   `label | answer | source` where source is `profile`, `mega_resume`, `answers`, `stories`,
   `posting` or `ASK`.
   - Contact fields: `profile.md`. Resume upload: the posting's PDF (`file_upload`).
   - Cover letter: **whenever the form offers one, optional or required**, run the `cover-letter`
     skill (`postings/<dir>/cover_letter.md`; reuse it if it exists). Paste the text into the cover
     letter text box when there is one (Greenhouse: "Enter manually"); if the form only takes a file,
     run it with `--pdf` and upload `the user_Cover_Letter_<Company>.pdf`. Row in
     `application.md`: `Cover letter | pasted text / <pdf name> | cover_letter.md, **draft**`.
   - "Why this company/role" free text: draft 2–4 sentences from the posting + mega resume facts,
     mark `draft` so the user sees it.
   - Other free text (LLM/AI experience, "most interesting thing you've built", "what should we
     know about you"): start from the closest `answers.md` answer, tailor it to the posting and the
     field's length limit, mark `draft`.
   - Behavioral ("tell me about a time..."): pick the story from the `stories.md` index, write it as
     a short STAR paragraph, mark `draft`. Never state an item under a story's **Open** as fact.
   - Voluntary EEO questions: use `profile.md`; if `ASK`, ask the user (never guess these).
   - Anything not answerable from `profile.md`, `mega-resume-v1.5.tex`, `answers.md` or `stories.md`:
     **ask the user**, all such questions at once, in one message. Save each answer that is reusable into `profile.md` under the right heading.
   - Never invent facts (dates, employers, degrees, authorization, salary).
5. **Fill the form** in Chrome (`form_input`/`computer`; React selects need clicking the option).
   **Never press Enter in any form field, dropdown or input**: Enter can submit the form (it did,
   2026-10-04, OpenTable). Pick dropdown options by clicking the option, then re-read the field.
   Upload the resume. Then re-read the form and confirm each field shows the intended value and the
   upload shows the right filename (and the cover letter box holds the full letter, not truncated).
6. **Stop for approval.** Show the user a compact summary: role, company, resume filename, and the table
   from `application.md` (highlight `draft` and newly-answered rows), plus the full cover letter
   text verbatim if there is one. Update `applications.md` to
   `ready`. Ask: "Submit? (ok / edits)".

## Phase 2: submit (on the user's "ok" only)

1. Apply any edits the user gave; re-verify the changed fields.
2. Click Submit. Handle what follows:
   - CAPTCHA: ask the user to solve it in the open tab, then continue.
   - Email verification code (Greenhouse sometimes sends one): ask the user for the code, enter it.
   - Validation errors: fix and re-show only what changed before submitting again.
3. **Verify:** the confirmation page/message is shown. Screenshot it to
   `postings/<dir>/confirmation.png` if possible, otherwise record its text in `application.md`.
4. **Close the application's tabs** (`tabs_close_mcp`), only once step 3 has verified the
   confirmation: every tab you opened for this posting (the form, the posting page, sign-in or
   other pop-up tabs). Never close a tab you didn't open. On a CAPTCHA, a code, an error, a
   failure or a skip, leave them open for the user.
5. Update `applications.md` row to `applied` with the date. Report done.

## Postings that can't be applied to

In a normal (non-batch) run: if the site needs an account the user doesn't have, the form can't be
filled or submitted after a retry, or the user decides to skip it, add or update its row in `dlq.md`
(reason `BLOCKED` / `FAILED` / `SKIPPED`, with what would unblock it under `Needs`, status `open`)
and tell the user. The resume stays in the posting folder for a manual application.

Workday: no usable saved login, if the user can't sign in now or skips it (`workday.md` section 3) → `BLOCKED`, Detail `NO-WORKDAY-LOGIN <tenant> <workday url>: ...`,
`Needs` "the user signs in / creates the account at <tenant> and lets Chrome save the password";
playbook failures → `FAILED` (see `workday.md`).

## Running as a batch subagent

When the prompt says you are a batch subagent (orchestrated by the `batch` skill): run Phase 1
steps 1–5 **without asking the user anything**, in your own Chrome tab only. Put every unanswerable field
in `application.md` as `ASK` with the exact question and options, leave that field empty, and record
the tab URL at the top of `application.md`. Workday postings follow `workday.md`: sign in through Chrome's autofill and fill up to the consent
checkbox; only `NO-WORKDAY-LOGIN <tenant> <workday url>` (no usable saved login) or
`NO-WORKDAY-HISTORY` (no `## Workday work history` in `profile.md`) blocks. On any other site, if
it needs an account login or sign-up, or a CAPTCHA blocks the form, stop and report it as a
blocker. Never create accounts or type passwords. End with a short
report: posting dir, number of `ASK` fields, blockers. **Never submit in a batch subagent.**

## Batch execute mode

Run only when `application.md` contains `APPROVED <date>: submit`. Open the application in your own
new tab (the earlier tab may be gone), fill it from the `application.md` table (which now holds
the user's answers and edits, no `ASK` left; if one is left, stop and report it), upload the resume,
paste or upload the cover letter from `cover_letter.md` (approved text, verbatim) if the table has one,
re-verify every field, then run Phase 2 steps 2–4 (step 4 closes only the tabs this execute run
opened; the orchestrator closes the prepare tab and updates `applications.md`; never write it in batch). CAPTCHA or email code → stop and reply
`NEEDS USER: ...` with the tab URL instead of asking.

Workday: sign in per `workday.md` section 3, resume the saved draft (section 4), check every saved
step against `application.md`, then run section 11 (which never writes `applications.md` in
batch). No usable saved login → reply `NEEDS USER: sign in at <tenant>` with the tab URL.
