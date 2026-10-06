# Workday playbook for /apply

Loaded by `/apply` step 3 for Workday postings; it replaces `/apply` steps 3–6 and Phase 2 for
them. Everything else in `/apply` (resume, sources, `application.md` format, truth rules) holds.
Decision record: `knowledge/decisions/0001-workday-sign-in-via-chrome-saved-passwords.md`.

## Detecting Workday

A posting is Workday when its URL, or the page its Apply button leads to, has a host ending in
`.myworkdayjobs.com` or `.myworkdaysite.com`. A posting found elsewhere (company careers page,
Built In, workopia) switches to this playbook when Apply lands on a Workday host.

Tenant name (used in DLQ rows and the batch review):
- `<tenant>.wdN.myworkdayjobs.com/...` → `<tenant>.wdN` (e.g. `manulife.wd3`).
- `wdN.myworkdaysite.com/[<locale>/]recruiting/<tenant>/<site>/...` → `<tenant>.wdN`.

Blockers use the existing DLQ Reason `BLOCKED` (or `FAILED`), never a new code. The Detail starts with
`NO-WORKDAY-LOGIN <tenant> <workday url>: <what was seen>` (`<workday url>` = the Workday page where
Sign In was tried) or `NO-WORKDAY-HISTORY`.

## 1. Load

Navigate to the posting. If the tab lands on `community.workday.com/maintenance-page` or shows
"Workday is currently unavailable", wait 5 seconds and reload the posting URL, at most twice.
Still unavailable → `FAILED`, Detail "Workday maintenance page".

## 2. Clicking rule

Click buttons, links and options through element refs from `find` (fallback: `read_page` with
`filter: interactive`). **Never press Enter.** Cookie banner: **Decline**.

Exceptions, seen on Manulife (2026-10-05), where a ref click lands on the wrong item or nothing:
- Dropdown and picker options: lists re-render under the click, so a ref often selects a
  neighbour. Open the list, take a screenshot, then click the option by position. Re-read the
  field (`get_page_text` or the button text) after every pick.
- Long lists (Language, Field of Study): typing the name while the list is open (type-ahead)
  scrolls to and highlights it; then screenshot and click it by position. Virtualized lists
  (Field of Study, Certification) can also be scrolled from `javascript_tool` by setting the
  listbox's `scrollTop` and dispatching a `scroll` event.
- **Save and Continue by position:** if a ref click on Save and Continue leaves the step unchanged
  with no errors, take a screenshot and click the button by position (it moves when the page is
  scrolled to the bottom). Confirm with `get_page_text` that the current step advanced.

Prompt pickers (How Did You Hear, Degree, Field of Study): click the field and browse the list
(typing does not filter it without Enter). No match: `ASK`, or the approved fallback in
`profile.md` (e.g. Field of Study → Computer Science). Re-read the field after picking.

**Search-only fields** (Skills, Certifications on Manulife): options appear only after an
Enter-triggered search, and the browse icon lists just the first 100 alphabetically. Don't try
them: record `skipped (search-only field)` in `application.md` and mention it at the approval
point (the resume carries skills and certifications).

## 3. Sign in

If the header already shows Aly's email, skip. Otherwise click **Sign In** and take a screenshot.
Judge "filled" from the screenshot (email text and masked password dots visible), not from field
values read from the page: Chrome hides an autofilled password from the page until a click. If
unsure, treat it as filled and let a Sign In error decide. Never pick a credential from Chrome's
suggestion dropdown (it may belong to another tenant); accept only what Chrome fills on its own.

- Email **and** password both filled by Chrome → click the dialog's **Sign In** button, wait 3
  seconds, confirm the header shows the email.
- Either field empty, Sign In returns an error (wrong credentials, account not found), or Workday
  asks for a verification code → no usable saved login. **Never type into the password field.
  Never fill or submit Create Account.**
  - Normal run: tell Aly the tenant; leave the tab on Sign In (or on **Create Account** when the
    error says no account exists) and ask Aly to sign in or create the account in that tab and let
    Chrome save the password. Continue when Aly says done.
  - Batch subagent: stop; report blocker `NO-WORKDAY-LOGIN <tenant> <workday url>: <what was seen>`
    (the orchestrator records it as `BLOCKED` with that Detail).

## 4. Start

Click **Apply**, then **Apply Manually**. Never Autofill with Resume or Use My Last Application. If
Workday offers to continue an existing draft for this posting, or the wizard opens on a later step,
continue it.

## 5. Each step

On every step: `get_page_text` and `read_page` (`filter: interactive`); list every field in
`application.md` (`label | answer | source`, with a `### <step name>` heading per step); fill;
re-read and confirm each value; click **Save and Continue**. Save and Continue saves a draft on
Aly's account: it is not a submission and needs no approval. Field errors → fix and save again; a
step that still fails after one retry → `FAILED` with the error text.

Required field answered `ASK` (the step can't be saved with it empty):
- Normal run: ask Aly all of this step's `ASK`s in one message, fill the answers, continue.
- Batch subagent: record the `ASK` rows, leave the step unsaved, and stop there; this is the stop
  step for section 10. Batch execute later resumes from the saved draft and fills the rest from
  `application.md`; a field on a later step not answerable from it → `NEEDS ALY`.
- Only a validation error that is not an `ASK` and fails after one retry is `FAILED`.

## 6. My Information

From `profile.md` `## Contact` and `## Common questions`.
- How Did You Hear About Us: the `profile.md` answer (Company careers page), or the closest option.
- Previously worked for the organization: `profile.md`; if not answerable, `ASK`.
- Name: `Full name` split into first/last; preferred name from `Preferred first name` if asked.
- Address: split `Street address` on commas: part 1 → Address Line 1, part 2 → City; the
  province abbreviation → its full name in the Province dropdown (`QC` → `Quebec`); the rest →
  Postal Code.
- Phone: device type `Mobile`, country code `Canada (+1)`, number from `Phone`, unless `profile.md`
  says otherwise.

## 7. My Experience

Source: `profile.md` `## Workday work history` (see "Work history section"; missing → build it
first).
- Read what the tenant profile already holds. Edit or delete entries so the step ends up matching
  the section exactly: same jobs, same order, same values.
- Work Experience, per job: Job Title, Company, Location, "I currently work here", From and To
  typed as MM/YYYY, Role Description pasted from the section.
- Education, per degree: School, Degree (closest option; none fits → `ASK`), Field of Study
  (closest option), dates when asked.
- Skills: search-only on most tenants (section 2): record `skipped (search-only field)`.
- Certifications, Languages (optional sections): Languages from `profile.md` (bilingual / native →
  Fluent, intermediate → Intermediate). Certifications are search-only on most tenants: skip.
- Resume/CV: upload the posting's tailored resume PDF (`file_upload`); confirm the filename shows.
- Websites: LinkedIn and GitHub from `profile.md` `## Contact`. Workday rejects
  `linkedin.com/in/...`: always type `https://www.linkedin.com/in/<handle>`.
- Any field the section doesn't cover → `ASK`.

## 8. Application Questions

Same rules as `/apply` step 4 (`profile`, `mega_resume`, `answers`, `stories`, `posting`, `draft`,
`ASK`). Cover letter, when offered: the `cover-letter` skill, as in `/apply` step 4.

## 9. Voluntary Disclosures / Self Identify

EEO answers from `profile.md`; never guessed; `ASK` when absent. The terms / consent checkbox
(e.g. "I consent to the terms and conditions") is **not** ticked. The step that holds it (the
*consent step*) is filled but cannot be saved, so the run stops there:
- Fields on the consent step are filled and recorded in `application.md`.
- Steps after the consent step and before Review (e.g. Self Identify) can't be reached yet: prepare
  their answers from `profile.md` by the same rules (EEO section, else `ASK`) and record them in
  `application.md` under `### After approval`.
- No consent checkbox anywhere: fill every step before Review; the last one is filled but left
  unsaved, and the run stops there.

## 10. Approval point

Replaces `/apply` step 6 for Workday: the same summary (role, company, resume filename, the
`application.md` table with `draft` and new rows highlighted, the cover letter verbatim if any),
plus the tenant, the step the run stopped on, the consent checkbox label quoted (or "no consent
checkbox"), and the `After approval` rows. Normal run: set `applications.md` to `ready` (in batch
the orchestrator does it). Ask "Submit? (ok / edits)". Aly's "ok" approves ticking that consent
checkbox, filling the `After approval` rows, and submitting.

Batch subagent: don't ask; end with the batch report, adding the tenant, the stop step, the consent
label (or "no consent checkbox") and the `After approval` rows.

## 11. Submit

1. Apply Aly's edits.
2. On the stop step, re-fill any field that is empty or differs from `application.md` (the unsaved
   step may be blank after a reload or in a new tab).
3. Tick the consent checkbox, if there is one; **Save and Continue**.
4. Fill the `After approval` steps, and any step not reached before the stop (section 5 `ASK`
   rule), from `application.md` (section 5 rules); **Save and Continue** until **Review**.
5. `get_page_text` the Review page; check every value against `application.md`; fix mismatches.
6. Click **Submit**. Confirm the "submitted" message or the application listed in Candidate Home.
   Screenshot to `postings/<dir>/confirmation.png`.
7. Normal run: `/apply` Phase 2 step 4 (update `applications.md` to `applied`). Batch execute mode:
   never write `applications.md` (the orchestrator does).

## Work history section

`profile.md` `## Workday work history`, local-only. Built once from `mega-resume-v1.5.tex` (every
value traceable to it; when it gives only a year for a job date, ask Aly for the month, never
infer it), shown to Aly in full, saved only after Aly approves. Missing in a normal
run → build, show, wait for approval. Missing in a batch subagent → report blocker
`NO-WORKDAY-HISTORY` (recorded as `BLOCKED`). Format:

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

Websites are not repeated here; section 7 reads them from `## Contact`.
