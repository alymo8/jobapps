# Workday applications in /apply and /batch: design

- **Date:** 2026-10-05
- **Status:** implemented

## Purpose

Workday postings (`*.myworkdayjobs.com`, `*.myworkdaysite.com`) are the largest group of blocked
applications: `/apply` and every `/batch` subagent stop at the Workday sign-in wall and file the
posting as `BLOCKED` in `dlq.md`. the user already has Workday candidate accounts at many companies,
with the passwords saved in Chrome. This change lets `/apply` sign in through Chrome's saved
password and fill the full Workday wizard up to the approval point, the same way it handles
Greenhouse today.

## Background (current state)

- `.claude/skills/apply/SKILL.md` has no Workday knowledge. Its batch-subagent section says: "If the
  site needs an account login or sign-up ... stop and report it as a blocker (don't create accounts)."
- `.claude/skills/batch/SKILL.md` subagent prompt lists "needs an account login" as a blocker, and
  the DLQ section gives "the user creates a Workday account at <tenant>" as an example `Needs`.
- `dlq.md` holds 13 open Workday account blockers (Morgan Stanley `ms.wd5` ×2, RBC `rbc.wd3` ×2,
  Manulife `manulife.wd3` ×2, Thomson Reuters `thomsonreuters.wd5` ×2, PSP `investpsp.wd3`,
  Intact `intactfc.wd3`, Simpro `simpro.wd3`, Workday `workday.wd5`, and Mastercard with no tenant
  found). The Salesforce row is resolved (the user applied by hand).
- `profile.md` (local-only, gitignored) has sections `Contact`, `Eligibility`,
  `Compensation & availability`, `Common questions`, `Voluntary self-identification (EEO / diversity)`,
  `Free-text answers`, `Career goals and cover letters`. It has no structured work history.

### Spike findings (2026-10-05, Manulife JR26071949)

1. Opening the Sign In dialog, Chrome autofilled the email and the saved password. Clicking Sign In
   logged in; the header then shows the email and "Candidate Home". Claude never saw the password.
2. The first load redirected to `community.workday.com/maintenance-page` ("Workday is currently
   unavailable"); a reload a few seconds later loaded the posting.
3. While the cookie banner was up, coordinate clicks on the header did nothing; clicks on element
   refs from `find` (Decline, Sign In) worked.
4. Apply opens "Start Your Application" with **Autofill with Resume**, **Apply Manually** and
   **Use My Last Application**. The last one was offered with no previous application on the account,
   then showed "The application didn't autofill because you don't have a previous application" and an
   empty form.
5. The wizard had 5 steps: My Information, My Experience, Application Questions, Voluntary
   Disclosures, Review. My Information held: How Did You Hear About Us (prompt picker), Previously
   worked for the organization (Yes/No), Country, First/Last Name, Address Line 1, City, Province,
   Postal Code, Email (prefilled, read-only), Phone Device Type, Country Phone Code, Phone Number,
   Extension. Tenants vary the step list (some add Self Identify).

## Scope

**In:**
- `.claude/skills/apply/workday.md` (new): the Workday playbook.
- `.claude/skills/apply/SKILL.md`: step 3 points to `workday.md` for Workday URLs (which
  covers steps 3–6 and Phase 2, so step 6 and Phase 2 themselves are not edited); "Postings that
  can't be applied to", the batch-subagent and batch-execute sections gain the Workday variants
  described below.
- `.claude/skills/batch/SKILL.md`: `## Workday work history` built before stage 2 when missing;
  subagent prompt blocker list and the DLQ `Needs` example updated;
  review sheet groups Workday account blockers by tenant.
- `knowledge/decisions/0001-workday-sign-in-via-chrome-saved-passwords.md` (new), the ADR, and its row in
  `knowledge/decisions/README.md`.
- Local, not committed: a new `## Workday work history` section in `profile.md`, built once from
  `mega-resume-v1.5.tex` and approved by the user.

**Out:**
- Other account-walled ATSs (iCIMS, Taleo, SuccessFactors).
- Python tool changes (`tools/`).
- Creating accounts or typing passwords (see Decision 1).
- Chrome extension site-permission problems (e.g. the extension refusing `intactfc.wd3`): these stay
  `BLOCKED` with that detail.

## Design

### Detecting Workday

`/apply` step 3: if the posting or apply URL host ends in `.myworkdayjobs.com` or
`.myworkdaysite.com`, read `.claude/skills/apply/workday.md` and follow it for steps 3–6 and for
Phase 2. A posting found on another site (company careers page, Built In) whose Apply button leads to
a Workday host switches to the playbook at that point. The tenant name, used by the playbook, DLQ
rows and the review sheet:
- `<tenant>.wdN.myworkdayjobs.com/...` → `<tenant>.wdN` (e.g. `manulife.wd3`).
- `wdN.myworkdaysite.com/[<locale>/]recruiting/<tenant>/<site>/...` → `<tenant>.wdN` (the path
  segment after `/recruiting/`).

Every Workday blocker is recorded in `dlq.md` with the existing Reason `BLOCKED` (or `FAILED`), never
a new Reason code. The Detail starts with a fixed prefix so it can be grouped:
`NO-WORKDAY-LOGIN <tenant> <workday url>: <what was seen>` (the Workday page where Sign In was
attempted, which differs from the posting URL for postings found on Built In and similar) or
`NO-WORKDAY-HISTORY`. The retry `/batch <apply|outreach> dlq.md --reason BLOCKED` (the row's
original mode) therefore picks them up unchanged. The 13 existing rows keep their free-form Detail;
they get the prefix the next time they are retried, not by a one-off rewrite.

### Playbook (`workday.md`)

Each part is a numbered section in `workday.md`.

1. **Load.** Navigate to the posting. If the tab lands on `community.workday.com/maintenance-page`
   or shows "Workday is currently unavailable", wait 5 seconds and reload the posting URL, at most
   twice. Still unavailable → `FAILED` with detail "Workday maintenance page".
2. **Clicking rule.** On Workday pages, click buttons, links and options through element refs from
   `find`/`read_page`, not screen coordinates. Never press Enter (existing rule). Cookie banner:
   click **Decline** (privacy-preserving default).
3. **Sign in.** If the header already shows the user's email, skip. Otherwise click **Sign In** and take
   a screenshot.
   - Email and password fields both filled (Chrome autofill) → click the dialog's **Sign In** button,
     wait, confirm the header shows the email.
   - Fields empty, or Sign In returns an error (wrong credentials, account not found), or Workday
     asks for a verification code → this tenant has **no usable saved login**. Claude never types
     into the password field, and never fills the Create Account form.
     - Normal run: tell the user the tenant, leave the tab on Sign In (or on **Create Account** when the
       error says no account exists) and ask the user to sign in or create the account in that tab and
       let Chrome save the password; continue when the user says done.
     - Batch subagent: stop and report blocker `NO-WORKDAY-LOGIN <tenant> <workday url>: <what was
       seen>` (orchestrator records it as `BLOCKED` with that Detail).
4. **Start.** Click **Apply** then **Apply Manually**. Never Autofill with Resume or Use My Last
   Application. If Workday shows an existing draft for this posting ("Continue Application" or the
   wizard opens on a later step), continue it.
5. **Read each step before filling.** On every step: `get_page_text` + `read_page` (interactive),
   list every field into `application.md` as today (`label | answer | source`), fill, re-read and
   confirm values, then click **Save and Continue**. Save and Continue saves a draft on the user's
   account; it is not a submission and needs no approval. If Workday returns field errors, fix
   them and save again; a step that still fails after one retry → `FAILED` with the error text.
6. **My Information.** From `profile.md` `## Contact` and `## Common questions`.
   - "How Did You Hear About Us": a prompt picker; click it, pick the category then the option
     (`profile.md` answer, default "Company careers page" / the closest option). Re-read the field.
   - "Previously worked for the organization": `profile.md`; if not answerable, `ASK`.
   - Phone device type `Mobile`, country phone code `Canada (+1)` unless `profile.md` says otherwise.
7. **My Experience.**
   - Before adding, read what the tenant profile already holds (entries from an earlier
     application at that company). Edit or delete entries so the step ends up matching
     `profile.md` `## Workday work history` exactly: same jobs, same order, same values (Decision 4).
   - Work Experience: per job, Job Title, Company, Location, "I currently work here", From and To
     typed as MM/YYYY into the date field, Role Description pasted from the section.
   - Education: per degree, School, Degree (pick the closest option; if none fits, `ASK`), Field
     of Study (prompt picker, closest option), dates when asked.
   - Skills: type each skill from the section and pick the matching suggestion; skip a skill with
     no matching option.
   - Resume/CV: upload the posting's tailored resume PDF (`file_upload`); confirm the filename shows.
   - Websites: LinkedIn and GitHub URLs from `profile.md` `## Contact`.
   - Any field the section doesn't cover → `ASK`.
8. **Application Questions.** Same rules as `/apply` step 4 (`profile`, `answers`, `stories`,
   `posting`, `draft`, `ASK`). Cover letter upload or text, when offered: `cover-letter` skill as today.
9. **Voluntary Disclosures / Self Identify.** EEO answers from `profile.md`; never guessed; `ASK`
   when absent. The **terms / consent checkbox** (e.g. "I consent to the terms and conditions") is
   **not** ticked (Decision 2). The step that holds it (the *consent step*) is filled but cannot be
   saved, so the run stops there:
   - Fields on the consent step are filled and recorded in `application.md` like any other step.
   - Steps after the consent step and before Review (e.g. Self Identify after Voluntary Disclosures)
     can't be reached yet. Their answers are prepared from `profile.md` by the usual rules (EEO
     fields from the EEO section, else `ASK`), recorded in `application.md` under the heading
     `After approval`, and filled in section 11.
   - A tenant with no consent checkbox: every step before Review is filled; the last one is filled
     but left unsaved, and the run stops there.
10. **Approval point.** Replaces `/apply` step 6 for Workday: the same summary, plus the tenant, the
    step the run stopped on, the consent checkbox label quoted (or "no consent checkbox"), and the
    `After approval` rows. `applications.md` → `ready` (normal runs only; in batch the
    orchestrator writes it). Ask "Submit? (ok / edits)". the user's "ok" approves ticking that consent
    checkbox, filling the `After approval` rows and submitting.
11. **Submit (Phase 2).** Apply edits. On the stop step, re-fill any field that is empty or differs
    from `application.md` (the unsaved step's values may be gone after a reload or in a new tab).
    Tick the consent checkbox if there is one; Save and Continue; fill the `After approval` steps
    from `application.md` the same way (re-read, confirm); Save and Continue to **Review**;
    `get_page_text` the Review page and check every value against `application.md`; click
    **Submit**; confirm the "submitted" message or Candidate Home showing the application;
    screenshot to `postings/<dir>/confirmation.png`. In a normal run, then `/apply` Phase 2 step 4
    (update `applications.md`); in batch execute mode, never (the orchestrator does it).

### `## Workday work history` in `profile.md`

Local-only, built once from `mega-resume-v1.5.tex` (every value traceable to it), shown to the user in
full and saved only after the user approves. When `/apply` hits a Workday posting and the section is
missing, it builds the draft, shows it, and waits for approval (in a batch, the orchestrator does this before any prepare subagent starts; see `/batch` changes. A
subagent that still finds it missing reports blocker `NO-WORKDAY-HISTORY`, recorded as `BLOCKED`).
Format:

```markdown
## Workday work history

### Work experience
- Job Title: <title> | Company: <company> | Location: <city, region> | Current: Yes/No | From: MM/YYYY | To: MM/YYYY or blank
  Role Description: <2-4 plain sentences, no bullets>
(one entry per job, most recent first)

### Education
- School: <school> | Degree: <degree as Workday names it, e.g. Master's Degree> | Field of Study: <field> | From: YYYY | To: YYYY

### Skills
<comma-separated list, at most 15>
```

Websites (LinkedIn, GitHub) are not repeated here; section 7 reads them from `## Contact`.

### `/apply` SKILL.md changes

- Step 3: one paragraph pointing to `workday.md` for Workday hosts.
- "Postings that can't be applied to": a Workday posting with no usable saved login is a `BLOCKED`
  row with Detail `NO-WORKDAY-LOGIN <tenant> <workday url>: ...` and `Needs` "the user signs in / creates the account
  at <tenant> and lets Chrome save the password"; playbook failures are `FAILED`.
- "Running as a batch subagent": the "account login or sign-up" blocker sentence says that Workday
  postings follow `workday.md`, signing in through Chrome autofill, and stop at the consent checkbox;
  only a missing saved login (`NO-WORKDAY-LOGIN`) or missing history section (`NO-WORKDAY-HISTORY`)
  blocks. Other sites' login walls stay blockers. Never create accounts or type passwords.
- "Batch execute mode": for Workday, sign in per playbook section 3, resume the saved draft
  (section 4), check every step against `application.md`, then playbook section 11 (which does not write
  `applications.md` in batch). An unusable
  saved login here → reply `NEEDS USER: sign in at <tenant>` with the tab URL.

### `/batch` SKILL.md changes

- Before stage 2 (prepare): if any picked posting is on a Workday host (apply mode, or outreach,
  which runs /apply) and `profile.md` has no `## Workday work history`, build the draft from
  `mega-resume-v1.5.tex`, show it to the user in full, and save it on approval before launching any
  prepare subagent. This approval is asked together with the section 0 "Confirm before launching" message.
- Subagent prompt blocker examples, and the step-2 "Blockers (...)" sentence: "needs an account
  login" becomes "needs an account login (non-Workday), NO-WORKDAY-LOGIN <tenant>".
- DLQ `Needs` example: "the user signs in / creates the account at <tenant> (Chrome saves the password)".
- Review sheet: a "Workday logins needed" list built from every `open` row in `dlq.md` whose Detail
  starts with `NO-WORKDAY-LOGIN` (not only this run's), grouped by tenant, rows from this run marked
  `(this run)`. Each tenant shows one sign-in URL: the `<workday url>` from the Detail of its first such row
  (a Workday page whose header has Sign In), plus the posting dirs it would unblock, so the user can create or sign in to all of them in one sitting and then
  re-run `/batch <apply|outreach> dlq.md --reason BLOCKED`.

### ADR 0001

`knowledge/decisions/0001-workday-sign-in-via-chrome-saved-passwords.md`, from `0000-template.md`:
Claude signs in to Workday only through Chrome's saved-password autofill and clicking Sign In; it
never types passwords, never creates accounts; Save and Continue drafts are allowed without
approval; the consent checkbox and Submit need the user's OK. Alternatives rejected: the user signs in by
hand every time (slow in batches), Claude types a stored password (credentials in context;
disallowed), Claude creates accounts (disallowed).

## Decisions

Confirmed by the user on 2026-10-05:

1. Sign-in uses Chrome's saved passwords (spike-verified). When a tenant has no account or no saved
   password, Claude opens Sign In / Create Account and the user completes it; Claude never creates
   accounts or types passwords (the user first chose "Claude creates, the user approves"; reversed because
   Claude's browser rules forbid it).
2. Save and Continue between steps needs no approval; the single approval point is before the
   consent checkbox, and the user's "ok" covers ticking it and submitting.
3. Always Apply Manually; never Autofill with Resume or Use My Last Application.
4. Existing entries in a tenant's Workday profile are overwritten to match `## Workday work history`.
5. My Experience is filled from a canonical, the user-approved `## Workday work history` section in
   `profile.md`.

## Success criteria

1. **Static:** `apply/SKILL.md` references `workday.md` at step 3, batch-subagent and batch-execute
   sections; `workday.md` has sections 1–11 as above; `batch/SKILL.md` no longer lists a Workday
   login as an automatic blocker; ADR 0001 exists and is indexed;
   `python -m py_compile tools/*.py` passes.
2. **End-to-end `/apply`** on https://manulife.wd3.myworkdayjobs.com/MFCJH_Jobs/job/Montreal-Quebec/Agentic-Engineer--Innovation_JR26071949:
   reaches the approval point with every step before the consent checkbox saved; no `ASK` except
   questions not answerable from the source files; every Work Experience and Education entry on the
   page equals `## Workday work history`; the resume upload shows the tailored PDF's filename.
   Submitting is the user's call and not part of the criterion.
3. **Batch:** `/batch apply` over at least 2 Workday postings from `dlq.md` (e.g. RBC
   R-0000182590 and Thomson Reuters). Each ends `ready`, or `NO-WORKDAY-LOGIN <tenant>` with the
   sign-in URL in the review's "Workday logins needed" list. No subagent types a password or
   fills Create Account.
