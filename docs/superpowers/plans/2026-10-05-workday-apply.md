# Workday applications in /apply and /batch Implementation Plan

- **Status:** approved
- **Date:** 2026-10-05

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Let `/apply` (and `/batch` subagents) sign in to Workday through Chrome's saved password and fill the whole Workday application wizard up to an approval point, instead of dead-lettering every Workday posting as `BLOCKED`.

**Architecture:** No product code. A new Markdown playbook `.claude/skills/apply/workday.md` that `/apply` loads for Workday hosts; targeted edits to `.claude/skills/apply/SKILL.md` and `.claude/skills/batch/SKILL.md`; ADR 0001. Then local-only data (a `## Workday work history` section in the gitignored `profile.md`) and two live acceptance runs in Chrome.

**Tech Stack:** Claude Code skills (Markdown + YAML frontmatter), the `claude-in-chrome` browser tools, Git Bash / PowerShell on Windows, Python 3 (`py_compile` only).

**Spec:** `docs/superpowers/specs/2026-10-05-workday-apply-design.md` (approved, gate-passed: record at docs/superpowers/gates/2026-10-05-workday-apply-design.md). This plan copies everything the executor needs from it.

## Context for a cold executor

- Repo: `C:\Users\alymo\Desktop\Github\jobapps` (remote `origin` = `https://github.com/alymo8/jobapps.git`, branch `main`). Aly's personal job-application workspace. "Aly" is the user; refer to Aly with they/them.
- Committed: skills (`.claude/skills/<name>/SKILL.md`), `tools/`, prompts, `docs/`, `knowledge/`. **Local-only and gitignored, never commit:** `profile.md`, `mega-resume-v1.5.tex`, `stories.md`, `answers.md`, `postings/`, `batches/`, `archive/`, `applications.md`, `dlq.md`.
- `/apply` today: Phase 1 prepare (resume, read sources, open form, list fields into `postings/<dir>/application.md` as `label | answer | source`, fill, stop at step 6 "Submit? (ok / edits)"), Phase 2 submit on Aly's OK. Sections "Postings that can't be applied to", "Running as a batch subagent", "Batch execute mode".
- `/batch`: sections `0. Parse and confirm` (step 4 "Confirm before launching"), `1a` pre-screen, `1b` resume, `2. Prepare stage` (Chrome, max 2 subagents, subagent prompt quoted in a `>` block), `3. Review sheet`, `4. Record approvals`, `5. Execute stage`, `6. Finish`, `Dead-letter queue`.
- `dlq.md` columns include `reason` and `detail`; reasons are `CLOSED`, `UNREADABLE`, `FAILED`, `BLOCKED`, `INELIGIBLE`, `SKIPPED`. `tools/read_postings.py dlq.md --reason BLOCKED` selects open rows with exactly that reason. 13 open rows are Workday account blockers (Morgan Stanley ×2, RBC ×2, Manulife ×2, Thomson Reuters ×2, PSP, Intact, Simpro, Workday, Mastercard). Several have non-Workday posting URLs (Built In, workopia, careers.intactfc.com) and reach Workday only behind Apply.
- `profile.md` `## Contact` keys: `Full name`, `Preferred first name`, `Email`, `Phone`, `Location`, `Street address (when a form requires it)` (one line: street, city, province abbreviation, postal code), `LinkedIn`, `GitHub`, ... `## Common questions` has `How did you hear about us: Company careers page, always` and `Previously worked at / applied to this company: answer per company (default: No, ask ...)`.
- **Spike facts (2026-10-05, Manulife JR26071949):** opening Sign In, Chrome autofilled email + saved password; clicking Sign In logged in (header shows the email and "Candidate Home"). First load hit `community.workday.com/maintenance-page`; a reload fixed it. Coordinate clicks failed under the cookie banner; `find` element refs worked. Apply offers Autofill with Resume / Apply Manually / Use My Last Application (the last errored: "you don't have a previous application"). Steps: My Information, My Experience, Application Questions, Voluntary Disclosures, Review (some tenants add Self Identify).

## Prerequisites (do these first, in order)

1. **Clean, current `main`** (workspace rule): `git -C C:/Users/alymo/Desktop/Github/jobapps branch --show-current` → `main`; `git fetch`. Commit this plan, its gate record `docs/superpowers/gates/plans/2026-10-05-workday-apply.md` and the regenerated `docs/superpowers/README.md` on `main`. Then `git status -sb` must show a clean tree, ahead only by the spec/gate/plan commits, behind 0; push them (`git push`) with Aly's OK. Anything else → **stop and ask Aly**.
2. **Worktree:** `superpowers:using-git-worktrees`, branch `feat/workday-apply`. Tasks 1–4 run there.
3. Tasks 5–7 run in the **main checkout after the merge**: they need local `profile.md`, `mega-resume-v1.5.tex`, `postings/`, `dlq.md`, and Chrome with the claude-in-chrome extension, with Aly's Workday passwords saved in Chrome.

## Decisions this plan adds (spec left them to the plan)

- **P1. Same-tenant serialization.** In `/batch` stages 2 and 5, never run two postings of the same Workday tenant at once (they share one Chrome session and one candidate profile); queue the second behind the first.
- **P2. Prompt pickers without Enter.** Workday prompt fields (How Did You Hear, Field of Study, Skills, Degree): click the field, type the search text, wait 2 s, click the matching option from the list. If no list appears, click the field's list/prompt icon and browse the categories. Still no match: for Skills, record `skipped (no option)` in `application.md`; for any other field, `ASK`. Never press Enter.
- **P3. Address split.** `Street address` from `profile.md` is split on commas: part 1 → Address Line 1, part 2 → City, part 3 (`QC` → `Quebec`, the Province dropdown's full name; other abbreviations to their full province name) plus postal code (the remaining tokens) → Province and Postal Code.
- **P4. Workday detection before stage 2.** A picked posting counts as Workday if its URL host is Workday, or its `dlq.md` Detail or `postings/<dir>/posting.md` contains `myworkdayjobs.com`, `myworkdaysite.com` or `Workday (`.
- **P5. Batch review per Workday posting** shows the tenant, the stop step, the quoted consent label (or "no consent checkbox") and the `After approval` rows; `ASK` rows among them go into the deduplicated questions like any other `ASK`.
- **P6. Element refs** come from `find` (natural-language query), falling back to `read_page` `filter: interactive`.
- **P7. Batch acceptance selection and evidence.** Task 7 runs `/batch apply dlq.md --reason BLOCKED` and trims the list to the chosen Workday rows at section 0 "Confirm before launching". "No password typed" is checked by grepping each prepare subagent's transcript (`~/.claude/projects/C--Users-alymo-Desktop-Github-jobapps/<session-id>/subagents/agent-<id>.jsonl`) for `type`/`form_input` actions and inspecting each hit.
- **P8. Required `ASK` fields.** A Workday step with an empty required field can't be saved. Normal run: ask Aly that step's `ASK`s in one message, then continue. Batch subagent: record the `ASK` rows, leave the step unsaved and stop there (that is the stop step); the posting goes to review as `ready` with `ASK`s. Execute mode resumes from the draft; a later step with a field not answerable from `application.md` → `NEEDS ALY`. Only a non-`ASK` validation error that fails twice is `FAILED`.
- **P9. Month-only gaps.** When the mega resume gives only a year for a job date, Aly is asked for the month (never inferred). The history section is appended at the end of `profile.md`.

## Global Constraints

- Never click Submit without Aly's explicit OK for that application in this session; never send LinkedIn messages without OK.
- Claude never types into a password field, never fills or submits Create Account, never creates accounts.
- Never press Enter in any form field, dropdown or input.
- Cookie banners: click **Decline**.
- Everything written about Aly is truth-checked against `profile.md`, `mega-resume-v1.5.tex`, `answers.md`, `stories.md`.
- Workday blockers use DLQ Reason `BLOCKED` (or `FAILED`), Detail `NO-WORKDAY-LOGIN <tenant> <workday url>: <what was seen>` or `NO-WORKDAY-HISTORY`; no new Reason code.
- Tenant name: `<tenant>.wdN.myworkdayjobs.com/...` → `<tenant>.wdN`; `wdN.myworkdaysite.com/[<locale>/]recruiting/<tenant>/<site>/...` → `<tenant>.wdN`.
- Batch execute subagents never write `applications.md`.
- Never commit `profile.md`, `postings/`, `batches/`, `applications.md`, `dlq.md`.

## Review Focus

- A tenant where Chrome autofills the email but not the password (saved for another tenant only) → treated as no usable login, never typed (Task 2, section 3 text; Task 6 checks the run).
- A posting on Built In / workopia whose Apply leads to Workday → playbook kicks in, Detail carries the Workday URL (Task 2 "Detecting" text; Task 7 includes a non-Workday-URL posting if available).
- Tenant profile already holding entries from an earlier application → entries edited/deleted to match exactly (Task 2 section 7; Task 6 checks the page against the section).
- Consent checkbox on Voluntary Disclosures with Self Identify after it → Self Identify answers in `After approval`, filled only after OK (Task 2 sections 9–11; Task 6 records which shape Manulife has).
- Workday maintenance page on first load → reload up to twice before `FAILED` (Task 2 section 1).

---

### Task 1: ADR 0001

**Files:**
- Create: `knowledge/decisions/0001-workday-sign-in-via-chrome-saved-passwords.md`
- Modify: `knowledge/decisions/README.md` (append one table row)

**Interfaces:** Produces the ADR path that Task 2's `workday.md` links to.

- [ ] **Step 1: Failing check**

Run: `test -f knowledge/decisions/0001-workday-sign-in-via-chrome-saved-passwords.md && grep -c "0001" knowledge/decisions/README.md`
Expected: non-zero exit (file missing).

- [ ] **Step 2: Write the ADR**

```markdown
# ADR 0001: Workday sign-in via Chrome saved passwords

- **Status:** accepted
- **Date:** 2026-10-05

## Context
Workday postings are the largest group of blocked applications: every Workday tenant has its own
candidate account, and `/apply` stopped at the sign-in wall. Aly has accounts at many tenants with
passwords saved in Chrome. A spike on 2026-10-05 (Manulife) showed Chrome autofills the email and
password when the Sign In dialog opens, and clicking Sign In logs in. Claude's browser rules forbid
it to type passwords or create accounts on third-party sites.

## Decision
Claude signs in to Workday only by letting Chrome autofill the saved credentials and clicking
Sign In. It never types into a password field and never fills Create Account. With no usable
saved login, Aly signs in or creates the account in the open tab (normal run), or the posting is
dead-lettered as `BLOCKED` with Detail `NO-WORKDAY-LOGIN <tenant> <workday url>: ...` (batch).
Save and Continue between wizard steps (a draft on Aly's account) needs no approval; ticking the
terms/consent checkbox and Submit need Aly's explicit OK.

## Consequences
Workday postings flow through `/apply` and `/batch` like Greenhouse ones once a tenant has a saved
login. Each new tenant still needs Aly once (create the account, let Chrome save the password).
Rejected: Aly signs in by hand every time (slow in batches); Claude types a stored password
(credentials in context, disallowed); Claude creates accounts (disallowed).
```

- [ ] **Step 3: Add the index row** — append to the table in `knowledge/decisions/README.md`:

```markdown
| [0001](0001-workday-sign-in-via-chrome-saved-passwords.md) | Workday sign-in via Chrome saved passwords | accepted | 2026-10-05 |
```

- [ ] **Step 4: Check passes** — rerun Step 1's command. Expected: prints `1`.
- [ ] **Step 5: Commit** — `git add knowledge/decisions && git commit -m "ADR 0001: Workday sign-in via Chrome saved passwords"` (with the Co-Authored-By trailer).

### Task 2: Workday playbook `.claude/skills/apply/workday.md`

**Files:**
- Create: `.claude/skills/apply/workday.md`

**Interfaces:**
- Consumes: ADR path from Task 1.
- Produces: numbered sections `## 1. Load` … `## 11. Submit`, plus `## Detecting Workday` and `## Work history section`, which Task 3 and Task 4 reference by number/name.

- [ ] **Step 1: Failing check**

Run: `for n in 1 2 3 4 5 6 7 8 9 10 11; do grep -q "^## $n\. " .claude/skills/apply/workday.md || echo "missing $n"; done`
Expected: errors / `missing 1` … `missing 11`.

- [ ] **Step 2: Write the file** with exactly this content:

````markdown
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
`filter: interactive`), never screen coordinates. **Never press Enter.** Cookie banner: **Decline**.

Prompt pickers (How Did You Hear, Degree, Field of Study, Skills): click the field, type the search
text, wait 2 seconds, click the matching option. No list → click the field's list/prompt icon and
browse the categories. Still no match: Skills → `skipped (no option)` in `application.md`; any
other field → `ASK`. Re-read the field after picking.

## 3. Sign in

If the header already shows Aly's email, skip. Otherwise click **Sign In** and take a screenshot.

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
- Skills: each skill from the section (section 2 picker rule).
- Resume/CV: upload the posting's tailored resume PDF (`file_upload`); confirm the filename shows.
- Websites: LinkedIn and GitHub from `profile.md` `## Contact`.
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
value traceable to it), shown to Aly in full, saved only after Aly approves. Missing in a normal
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
````

- [ ] **Step 3: Check passes** — rerun Step 1. Expected: no output. Also `grep -c "Never type into the password field" .claude/skills/apply/workday.md` → `1`.
- [ ] **Step 4: Commit** — `git add .claude/skills/apply/workday.md && git commit -m "/apply: Workday playbook"`.

### Task 3: Wire the playbook into `.claude/skills/apply/SKILL.md`

**Files:** Modify `.claude/skills/apply/SKILL.md` (step 3, "Postings that can't be applied to", "Running as a batch subagent", "Batch execute mode").

**Interfaces:** Consumes `workday.md` section numbers 3, 4, 11 and the "Detecting Workday" rule from Task 2.

- [ ] **Step 1: Failing check**

Run: `grep -c "workday.md" .claude/skills/apply/SKILL.md`
Expected: `0`.

- [ ] **Step 2: Step 3.** After the existing step 3 paragraph (ending "...options for selects."), add a new indented paragraph:

```markdown
   **Workday** (`*.myworkdayjobs.com`, `*.myworkdaysite.com`, or an Apply button leading there):
   read `.claude/skills/apply/workday.md` and follow it instead of steps 3–6 here and Phase 2
   (sign-in through Chrome's saved password, Apply Manually, step-by-step fill, stop before the
   consent checkbox).
```

- [ ] **Step 3: "Postings that can't be applied to".** Append to that section:

```markdown
Workday: no usable saved login → `BLOCKED`, Detail `NO-WORKDAY-LOGIN <tenant> <workday url>: ...`,
`Needs` "Aly signs in / creates the account at <tenant> and lets Chrome save the password";
playbook failures → `FAILED` (see `workday.md`).
```

- [ ] **Step 4: "Running as a batch subagent".** Replace the sentence
`If the site needs an account login or sign-up, or a CAPTCHA blocks the form, stop and report it as a blocker (don't create accounts).`
(it wraps across lines; match it as text) with:

```markdown
Workday postings follow `workday.md`: sign in through Chrome's autofill and fill up to the consent
checkbox; only `NO-WORKDAY-LOGIN <tenant> <workday url>` (no usable saved login) or
`NO-WORKDAY-HISTORY` (no `## Workday work history` in `profile.md`) blocks. On any other site, if
it needs an account login or sign-up, or a CAPTCHA blocks the form, stop and report it as a
blocker. Never create accounts or type passwords.
```

- [ ] **Step 5: "Batch execute mode".** Append:

```markdown
Workday: sign in per `workday.md` section 3, resume the saved draft (section 4), check every saved
step against `application.md`, then run section 11 (which never writes `applications.md` in
batch). No usable saved login → reply `NEEDS ALY: sign in at <tenant>` with the tab URL.
```

- [ ] **Step 6: Check passes**

Run: `grep -c "workday.md" .claude/skills/apply/SKILL.md; grep -c "NO-WORKDAY-LOGIN" .claude/skills/apply/SKILL.md; grep -c "stop and report it as a blocker (don't create accounts)" .claude/skills/apply/SKILL.md`
Expected: first count `4` or more, second `2` or more, third `0`.
- [ ] **Step 7: Commit** — `git commit -am "/apply: route Workday postings to the playbook"`.

### Task 4: `/batch` changes in `.claude/skills/batch/SKILL.md`

**Files:** Modify `.claude/skills/batch/SKILL.md` (section 0 step 4, section 2 prompt and Blockers sentence, section 3 review sheet, section 5, Dead-letter queue `Needs` example).

**Interfaces:** Consumes the Detail prefixes and tenant rule from Task 2.

- [ ] **Step 1: Failing check**

Run: `grep -c "NO-WORKDAY-LOGIN" .claude/skills/batch/SKILL.md`
Expected: `0`.

- [ ] **Step 2: Section 0, step 4.** Append to step 4 (after "...is the go for the rest."):

```markdown
   **Workday history:** in `apply` or `outreach` mode, if any picked posting is Workday (URL host `myworkdayjobs.com` /
   `myworkdaysite.com`, or its `dlq.md` Detail or `postings/<dir>/posting.md` contains one of those
   or `Workday (`) and `profile.md` has no `## Workday work history`, build that section from
   `mega-resume-v1.5.tex` (format in `.claude/skills/apply/workday.md`, "Work history section"),
   show it in full in this same message, and save it on Aly's approval before any prepare subagent.
```

- [ ] **Step 3: Section 2.** In the quoted subagent prompt replace `(e.g. needs an account login, CAPTCHA before the form, closed)` with `(e.g. needs an account login (non-Workday), NO-WORKDAY-LOGIN <tenant> <workday url>, CAPTCHA before the form, closed)`. In the paragraph after it replace `Blockers (needs an account login/sign-up, CAPTCHA before the form, unsupported site)` with `Blockers (needs an account login/sign-up (non-Workday), NO-WORKDAY-LOGIN / NO-WORKDAY-HISTORY from a Workday posting, CAPTCHA before the form, unsupported site)`. Then add after the "never more than 2" sentence: `Never run two postings of the same Workday tenant at once (shared session and candidate profile); queue the second.`

- [ ] **Step 4: Section 3.** In item 2 ("Per posting"), append: ` For Workday postings: the tenant, the step the fill stopped on, the consent checkbox label quoted (or "no consent checkbox"), and the "After approval" rows; their ASKs join item 1.` Under item 3 ("Dead-lettered in this run"), add this indented sub-bullet:

```markdown
   - **Workday logins needed**: every `open` row in `dlq.md` whose Detail starts with
     `NO-WORKDAY-LOGIN` (not only this run's), grouped by tenant; rows from this run marked
     `(this run)`. Per tenant: one sign-in URL (the `<workday url>` from the Detail of its first such
     row) and the posting dirs it would unblock. After signing in or creating the accounts (Chrome
     saves the passwords), re-run `/batch <apply|outreach> dlq.md --reason BLOCKED` in each row's
     original mode.
```

- [ ] **Step 5: Section 5.** Insert as a new sentence right after `Only for postings with a recorded approval.` in section 5: `Same-tenant Workday postings run one at a time, as in stage 2.`

- [ ] **Step 6: Dead-letter queue.** Replace `("Aly creates a Workday account at <tenant>",` with `("Aly signs in / creates the account at <tenant> (Chrome saves the password)",`.

- [ ] **Step 7: Check passes**

Run: `for p in "NO-WORKDAY-LOGIN" "Workday history" "same Workday tenant\|Same-tenant Workday" "Aly creates a Workday account"; do grep -c "$p" .claude/skills/batch/SKILL.md; done`
Expected: `3` or more, then `1`, then `2`, then `0`.

- [ ] **Step 8: Static criterion 1 + byte-compile**

Run: `python -m py_compile tools/*.py && echo ok`
Expected: `ok` (no Python changed; ruff not needed).
- [ ] **Step 9: Commit, PR, merge.** `git commit -am "/batch: Workday logins list, history pre-check, same-tenant serialization"`; push the branch; open a PR (body ends with the Claude Code attribution line); wait for green CI (it runs `py_compile`); squash-merge only with Aly's OK (or under `/ship`); `git pull` on `main`. Set spec and plan Status to `implemented` only after Tasks 5–7 pass.

- [ ] **Step 10: Clean up the workspace.** Use `superpowers:finishing-a-development-branch`: remove and prune the `feat/workday-apply` worktree, delete the branch locally and on the remote. Run: `git worktree list; git branch -a | grep workday-apply` Expected: no `feat/workday-apply` worktree or branch.

### Task 5: Build `## Workday work history` in local `profile.md` (main checkout)

**Files:** none committed (edits the local, gitignored `profile.md` only; nothing to commit).

- [ ] **Step 1:** Read `mega-resume-v1.5.tex` fully. Draft the section in the exact format of `workday.md` "Work history section": every job (most recent first) with MM/YYYY dates exactly as the mega resume states them, every degree, at most 15 skills that appear in the mega resume. Every value must be traceable to a line of the mega resume; if a date is only a year, `ASK` Aly for the month.
- [ ] **Step 2:** Show the full draft to Aly verbatim; apply edits; save under a new `## Workday work history` heading at the end of `profile.md` only after Aly's explicit approval.
- [ ] **Step 3: Check**

Run: `grep -c "^## Workday work history" profile.md; git status --porcelain profile.md | wc -l`
Expected: `1`, then `0` (still ignored; no commit).

### Task 6: End-to-end `/apply` on Manulife (main checkout, success criterion 2)

**Files:** none committed (writes local `postings/Manulife-JR26071949/application.md` and `applications.md` only).

- [ ] **Step 1:** Run `/apply https://manulife.wd3.myworkdayjobs.com/MFCJH_Jobs/job/Montreal-Quebec/Agentic-Engineer--Innovation_JR26071949` (posting dir `postings/Manulife-JR26071949`, resume already built).
- [ ] **Step 2: Verify:**
  - It reached the approval point; every step before the consent step is saved (wizard shows them complete).
  - Run: `grep -n "| ASK" postings/Manulife-JR26071949/application.md`
    Expected: only questions not answerable from `profile.md`, `mega-resume-v1.5.tex`, `answers.md`, `stories.md` (list them for Aly).
  - Every Work Experience and Education entry on the My Experience page equals `## Workday work history` (compare field by field with `get_page_text`).
  - The resume upload shows the tailored PDF's filename.
  - No password was typed. With `T=~/.claude/projects/C--Users-alymo-Desktop-Github-jobapps/<session-id>.jsonl` (this session's transcript):
    Run: `grep -o '"action":"type"[^}]*\|form_input[^}]*\|javascript_tool[^}]*' $T`
    Expected: each hit inspected; none targets a password or Create Account field.
- [ ] **Step 3:** Submitting is Aly's call: only on Aly's "ok", run `workday.md` section 11. Record which consent shape Manulife has in the verification notes.

### Task 7: Batch acceptance (main checkout, success criterion 3)

**Files:** none committed during the run (writes local `batches/`, `dlq.md`, `postings/`); Step 3 commits the Status change of the spec and plan.

- [ ] **Step 1:** Run `/batch apply dlq.md --reason BLOCKED`. At section 0 "Confirm before launching", trim the list to: RBC `R-0000182590`, Thomson Reuters `JREQ202780`, and one open Workday row whose posting URL is not a Workday host (PSP, Simpro or Intact; skip Intact if the extension still can't read its domain). Substitute another open Workday row if one is resolved.
  Before invoking `/batch`, run `grep -c "| retried |" dlq.md` and note the count. For this run, skip batch section 0 step 2's marking of every picked row: set **only the kept rows** to `retried`, and only after Aly confirms the trimmed list.
  Run (after launch): `grep -c "| retried |" dlq.md`
  Expected: the noted count plus the number of kept rows. If higher, set every trimmed row back to `open`.
- [ ] **Step 2: Verify:**
  - Run: `B=$(ls -d batches/*-apply | tail -1); grep -n "Workday logins needed" -A12 $B/review.md; grep -n "R-0000182590\|JREQ202780\|<third posting id>" applications.md dlq.md` (substitute the third kept posting's id, e.g. `R4868`, `JR101959` or `R152942`)
    Expected: each posting's `applications.md` row is `ready`, or its `dlq.md` row is Reason `BLOCKED` with Detail starting `NO-WORKDAY-LOGIN <tenant> <workday url>`, and that tenant appears in `review.md`'s "Workday logins needed" list with that URL. For the third (non-Workday-URL) posting, that URL is a Workday host, not the Built In / workopia / careers URL.
  - For each prepare subagent id `<id>` (from the batch's launch results) and this session's id `<session-id>`, with `T=~/.claude/projects/C--Users-alymo-Desktop-Github-jobapps/<session-id>/subagents/agent-<id>.jsonl`:
    Run: `test -s $T && grep -c "claude-in-chrome" $T; grep -o '"action":"type"[^}]*\|form_input[^}]*\|javascript_tool[^}]*' $T`
    Expected: the file is non-empty with a non-zero claude-in-chrome count (so an empty grep means "no typing", not "no transcript"); each typing hit is inspected and none targets a password or Create Account field.
- [ ] **Step 3:** Report the evidence for criteria 1–3 to Aly; on all passing, set spec and plan Status to `implemented` (commit on `main` via the normal PR flow or as Aly directs).

## Success criteria (from the spec)

1. **Static:** `apply/SKILL.md` references `workday.md` at step 3, batch-subagent and batch-execute sections; `workday.md` has sections 1–11; `batch/SKILL.md` no longer lists a Workday login as an automatic blocker; ADR 0001 exists and is indexed; `python -m py_compile tools/*.py` passes.
2. **End-to-end `/apply`** on Manulife JR26071949 reaches the approval point with every step before the consent checkbox saved; no `ASK` except questions not answerable from the source files; Work Experience and Education equal `## Workday work history`; the resume upload shows the tailored PDF's filename. Submitting is Aly's call.
3. **Batch:** `/batch apply` over at least 2 Workday postings from `dlq.md`; each ends `ready` or `NO-WORKDAY-LOGIN <tenant>` with the sign-in URL in the review's "Workday logins needed" list; no subagent types a password or fills Create Account.
