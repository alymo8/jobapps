# Outreach without apply Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

- **Date:** 2026-10-19
- **Status:** draft

**Goal:** `/outreach` and `/batch outreach` message people on LinkedIn without applying unless Aly asks (`--apply`). New `outreach-only-*` statuses keep "messaged but not applied" visible, and the skills follow Aly's standing LinkedIn rules: "interested", no attachment, never InMail.

**Architecture:** One small code change: `tools/read_postings.py` gets a `--for outreach` skip set, with unit tests. The rest are Markdown skill edits in `.claude/skills/{outreach,apply,batch,followup}/`, plus `CLAUDE.md` and ADR 0006.

**Tech Stack:** Python 3 stdlib, `unittest`; Claude Code skills (Markdown).

**Spec:** `docs/superpowers/specs/2026-10-19-outreach-without-apply-design.md` (approved; its gate record is under docs/superpowers/gates/ with the same file name). Read the spec's Design section before each skill task. It is the source for every rule below, and this plan does not repeat it in full.

## Why (from the spec, settled with Aly 2026-10-19; do not relitigate)

- `/outreach` is LinkedIn-only by default. It applies only with `--apply` or when Aly asks in plain words. When unsure, it does not apply.
- The tailored resume is still built (`/resume`, no form) because messages quote it.
- There are new statuses `outreach-only-ready` / `outreach-only-sent`. Reusing `outreach-*` was rejected because the in-place Status cell would lose whether Aly applied.
- The `sources/profile.md` `## LinkedIn outreach` rules are folded in: say "interested", never "applied"; attach nothing and never say a resume is attached; never InMail; send a free message when LinkedIn offers one (Open Profile), else a connection request; send approved messages directly.
- ADR 0005's approval classes (existing connection vs new) and all caps stay unchanged.

## Global Constraints

- Mode line strings (identical in `outreach` and `batch`): `Mode: outreach only (no application)` and `Mode: outreach + apply`.
- Posting-level batch approval mark: a line `APPROVED <YYYY-MM-DD>: outreach`, the last line of the `## Shortlist` section of `postings/<dir>/outreach.md`. Matching regex: `^APPROVED \d{4}-\d{2}-\d{2}: outreach$`.
- Legend line, byte-identical wherever it appears:
  ``Status: `resume` → `ready` (form filled, awaiting OK) → `applied` → `outreach-ready` → `outreach-sent` → `in-conversation` | `no-response` | `closed`; not applied: `outreach-only-ready` → `outreach-only-sent`.``
- `## Sent` channels: `message (existing connection)`, `free message (open profile)`, `connection request with note`, `connection request (no note)`. Old logs with `InMail` or `typed, Aly to send` stay parseable.
- Notes-cell texts: `form filled <date>, not submitted`, `form filled <date>, awaiting OK`, `outreach again <date>`, `outreach again <date>, approval pending`.
- The repo is public-safe for this repo's rules: no private repo names or usernames in tracked files.
- `tools/` code is not ruff-clean by design. Match the surrounding style. CI runs `python -m py_compile tools/*.py` and `python -m unittest discover -s tests -v`.

## Review Focus

- A posting already `applied` but never messaged must be picked by `/batch outreach` (`--for outreach`). Covered by Task 1's tests.
- An `outreach-only-*` posting must still be picked by `/batch apply` (default skip set). Covered by Task 1's tests.
- `--for` with a value other than `outreach` keeps today's behaviour. Covered by Task 1's `test_for_other_value_is_default`.
- Re-running `/outreach` (with or without `--apply`) on an already-messaged row never messages the same people again. Checked in Task 7's read-through, with step numbers in the PR body.
- No message text says Aly applied, mentions InMail, or attaches a resume. Checked by Task 7's `rg` check.

---

### Task 1: `read_postings.py --for outreach`

**Files:**
- Modify: `tools/read_postings.py` (docstring lines 1-17, `DONE` at line 28, `main` arg loop and skip filter)
- Test: `tests/test_read_postings.py`

**Depends on:** none

**Interfaces:**
- Produces: CLI option `--for outreach`; module constant `OUTREACH_DONE: set[str]`.

- [ ] **Step 1: Write the failing tests** in `ReadPostingsTest`. Tests patch `rp.ROOT` to a temp dir, as `setUp` already does. Add a helper that writes `self.root / "applications.md"` with one row per status in the 7-column shape `statuses()` parses: `cells[4]` is `postings/<dir>`, `cells[5]` is the status, `cells[6]` holds the URL. For example:
  `| 2026-10-19 | b | Co | T | postings/D<i> | <status> | https://s.example/<i> |`
  Use statuses `applied, outreach-ready, outreach-sent, outreach-only-ready, outreach-only-sent, in-conversation, ready` for i = 1..7, and pass the seven URLs as arguments.

```python
STATUSES = ["applied", "outreach-ready", "outreach-sent", "outreach-only-ready",
            "outreach-only-sent", "in-conversation", "ready"]

def test_default_skips_applied_and_outreach(self):
    self.write_apps()
    got = self.run_main(*self.status_urls())
    self.assertEqual(sorted(x["status"] for x in got),
                     sorted(["outreach-only-ready", "outreach-only-sent", "in-conversation", "ready"]))

def test_for_outreach_picks_applied_not_messaged(self):
    self.write_apps()
    got = self.run_main(*self.status_urls(), "--for", "outreach")
    self.assertEqual(sorted(x["status"] for x in got), ["applied", "ready"])

def test_for_outreach_all_keeps_everything(self):
    self.write_apps()
    got = self.run_main(*self.status_urls(), "--for", "outreach", "--all")
    self.assertEqual(len(got), 7)

def test_for_other_value_is_default(self):
    self.write_apps()
    got = self.run_main(*self.status_urls(), "--for", "apply")
    self.assertEqual(len(got), 4)
```

- [ ] **Step 2: Run the tests to verify they fail.** Run `python -m unittest tests.test_read_postings -v`. Expected: the `--for` tests FAIL or ERROR, because `--for` is treated as a source path.

- [ ] **Step 3: Implement.** Add `OUTREACH_DONE = {"outreach-ready", "outreach-sent", "outreach-only-ready", "outreach-only-sent", "in-conversation", "no-response", "closed"}` next to `DONE` (which is unchanged). In `main`, parse `--for <value>`. The skip filter uses `OUTREACH_DONE` when the value is `outreach`, else `DONE`. `--all` still bypasses it. Add `[--for outreach]` to the docstring's Usage line, plus one sentence: with `--for outreach`, already-messaged postings are skipped and `applied` ones are kept.

- [ ] **Step 4: Run the tests to verify they pass.** Run `python -m unittest discover -s tests -v` and `python -m py_compile tools/read_postings.py`. Expected: all OK.

- [ ] **Step 5: Commit** `tools/read_postings.py tests/test_read_postings.py`, message `read_postings: --for outreach skip set`.

### Task 2: `/outreach` skill

**Files:**
- Modify: `.claude/skills/outreach/SKILL.md`

**Depends on:** none

**Interfaces:**
- Consumes: the Global Constraints strings.
- Produces: the step numbering that Tasks 4 and 5 refer to (steps 0–6 keep their numbers).

- [ ] **Step 1: Frontmatter.** Set `argument-hint: <posting URL> | <posting dir> [--apply]`. Set `description` to the spec's text (Design, "`/outreach` arguments"), verbatim. Retitle the H1 to `# /outreach — LinkedIn messages (apply only with --apply)`.
- [ ] **Step 2: Arguments section.** Add a short `## Apply or not` section after the intro. It covers the spec's `--apply` / plain-request / "when unsure, don't apply" rule, and says the final report mentions `/apply <posting>` when it didn't apply.
- [ ] **Step 3: Step 1.** Replace "Apply first" with the spec's step 1 for both paths. Without `--apply`: resolve the dir, run `/resume` (build only) if there is no compiled resume, the stop list, the `*-ready` resume, and the `approval pending` note treated like `*-ready`. With `--apply`: today's "Apply first", plus the exceptions for `outreach-only-*`/`in-conversation`/`no-response`/`closed` (apply only, skip steps 2–6) and for `outreach-ready`/`outreach-sent` (skip `/apply`, then follow the no-apply rules).
- [ ] **Step 4: Step 3 wording.** In all drafts, "that Aly applied" becomes "that Aly is interested in the role". Remove the InMail subject and the "With Premium InMail credits…" sentence. Add the spec's wording rules as bullets: interested, never applied; never say a resume is attached and attach nothing.
- [ ] **Step 5: Step 5 routes.** An existing connection gets the approved text sent directly, with no attachment. Delete the 2026-10-04 iframe/attach bullet and the "type the text, leave it unsent" path. A new person gets a free message carrying (b) when the profile offers "Free message" (Open Profile); otherwise the request with note (a) or no note per budget. Never InMail: if only InMail is offered, send the request.
- [ ] **Step 6: Step 6 log and status.** Set the channel list to the Global Constraints list (old values stay parseable by `/followup`). Remove `typed, Aly to send` from new logs. Status writes follow the spec's "Statuses": `outreach-only-*` vs `outreach-*` by prior row; `ready` gets the `form filled <date>, not submitted` note; a continued run keeps the status and adds the `outreach again` note. Add the legend safety net (exact line from Global Constraints) when the legend lacks `outreach-only`. In the final report, remove "tabs waiting for Aly".
- [ ] **Step 7: Budget section.** Rename it to `## Invitation budget` and drop the InMail sentence.
- [ ] **Step 8: Batch sections.** "Running as a batch subagent": the prompt's mode line decides. With `Mode: outreach only (no application)`, skip `/apply` and run steps 2–3. With `Mode: outreach + apply`, today's text, except that a row with pre-run status `outreach-only-*`/`in-conversation`/`no-response`/`closed` runs `/apply` Phase 1 only. "Batch execute mode": the application part runs only with `Mode: outreach + apply` and an `APPROVED <date>: submit`. LinkedIn sends need, for new people, the posting's `APPROVED <date>: outreach` mark (Global Constraints) or (with `--apply`) a submit approval; existing connections still need their per-person `APPROVED <date>`.
- [ ] **Step 9: Verify.**
  Run: `rg -n -i "applied|InMail|attach" .claude/skills/outreach`
  Expected: every hit is a status name, `--apply`, a "never" rule, or old-channel parsing.
- [ ] **Step 10: Commit** with message `outreach: LinkedIn only unless --apply; profile wording rules`.

### Task 3: `/apply` and Workday status rules

**Files:**
- Modify: `.claude/skills/apply/SKILL.md` (description line 3; Phase 1 step 6; Phase 2 step 5)
- Modify: `.claude/skills/apply/workday.md` (section 10, the "Normal run: set `applications.md` to `ready`" sentence)

**Depends on:** none

- [ ] **Step 1:** In the description, replace "; /outreach runs this first." with "; /outreach runs this first only with --apply."
- [ ] **Step 2:** In Phase 1 step 6, add: if the row is `outreach-only-ready` or `outreach-only-sent`, keep the status and add `form filled <date>, awaiting OK` to Notes instead of setting `ready`. Make the same change to `workday.md` section 10's normal-run sentence.
- [ ] **Step 3:** In Phase 2 step 5, map the status the row had before this run: `outreach-only-ready` → `outreach-ready`, `outreach-only-sent` → `outreach-sent`, else `applied`. A declined or failed submit leaves the row unchanged. Add the legend safety net with the exact line.
- [ ] **Step 4: Verify.**
  Run: `rg -n "outreach-only" .claude/skills/apply` and `rg -n "/outreach runs this first\." .claude/skills`
  Expected: the first hits both `SKILL.md` and `workday.md`; the second returns nothing.
- [ ] **Step 5: Commit** with message `apply: keep outreach-only statuses through prepare and submit`.

### Task 4: `/batch` outreach modes

**Files:**
- Modify: `.claude/skills/batch/SKILL.md`

**Depends on:** Task 1

- [ ] **Step 1:** Add `[--apply]` to `argument-hint`. In step 0.1, `--apply` only counts in `outreach` mode; in other modes it is ignored with a one-line note. Step 0.2: in `outreach` mode without `--apply`, append `--for outreach` to the `read_postings.py` call; with `--apply`, keep today's call. Keep each posting's `status` from `postings.json` as its **pre-run status**, which every later status choice uses. Step 0.5: the confirm message names the mode, and the Workday-history check runs only in `apply` mode or `outreach --apply`.
- [ ] **Step 2: Stages 1a.5 and 1b.** In `outreach` mode, a posting whose pre-run status is `applied` skips scoring (1a.5). Stage 1b leaves its `applications.md` Status unchanged and writes only Notes.
- [ ] **Step 3: Stage 2 prompt.** Add the mode line (Global Constraints) to the prepare prompt in outreach mode. With `--apply`, a posting whose pre-run status is `outreach-only-*`/`in-conversation`/`no-response`/`closed` gets the application part only.
- [ ] **Step 4: Review sheet and questions.txt.** In outreach-only mode, postings have no application, form-question or submit parts: only the LinkedIn part (questions.txt part 5) and decisions.
- [ ] **Step 5: Stage 4.** In outreach-only mode, skip the `application.md` `APPROVED <date>: submit` write. For each posting Aly did not skip, write `APPROVED <date>: outreach` as the last line of `## Shortlist` in `outreach.md`; Aly's reply without a `skip` for the posting is the go. Per-person existing-connection marks work as today.
- [ ] **Step 6: Stage 5.** "Only for postings with a recorded approval" also counts the `APPROVED <date>: outreach` mark. Add the mode line to the execute prompt.
- [ ] **Step 7: Finish (`applications.md` writes).** Statuses follow the spec's "Statuses", using the pre-run status. Outreach-only: `outreach-only-*`, or `outreach-*` when the pre-run status was `applied`/`outreach-ready`. Prepare on an `outreach-only-*` row keeps the status and adds Notes `form filled <date>, awaiting OK`. Post-submit mapping in `apply` and `outreach --apply`: `outreach-only-ready` → `outreach-ready`, `outreach-only-sent` → `outreach-sent`, else `applied`. Add the legend safety net. Ask "Mark these <n> as applied?" only when something was submitted.
- [ ] **Step 8: Verify.**
  Run: `rg -n "outreach-only|--for outreach|Mode: outreach|APPROVED <date>: outreach" .claude/skills/batch/SKILL.md`
  Expected: hits in step 0.2, the stage 2 and stage 5 prompts, stage 4 and the finish step.
- [ ] **Step 9: Commit** with message `batch: outreach mode is LinkedIn only unless --apply`.

### Task 5: `/followup`

**Files:**
- Modify: `.claude/skills/followup/SKILL.md`

**Depends on:** none

- [ ] **Step 1:** Change the nudge text: "a reminder that Aly applied and messaged earlier" becomes "a reminder that Aly is interested in it and messaged earlier".
- [ ] **Step 2:** In the `accepted` row and the send rules, (b) is sent directly with no attachment. Remove the "type it in the thread, Aly attaches the resume" bullet and its "Aly attaches the resume" text. Keep the `typed <date>, not sent` note for old logs. Add "Never InMail."
- [ ] **Step 3:** In step 3b (adding a new person), use the free message carrying (b) when offered, else the connection request (with note while the budget lasts), never InMail. Classify a `free message (open profile)` entry like a sent (b): `replied`/`silent`/`waiting`, never `accepted`/`stale-pending`.
- [ ] **Step 4:** Status transitions start from the current list plus `outreach-only-ready`, `outreach-only-sent`. Replace the legend safety-net line with the exact Global Constraints line.
- [ ] **Step 5: Verify.**
  Run: `rg -n -i "applied|InMail|attach" .claude/skills/followup`
  Expected: only status names, "never" rules, and old-log or draft-heading parsing (e.g. "InMail Body").
- [ ] **Step 6: Commit** with message `followup: interested wording, no attachment, outreach-only statuses`.

### Task 6: ADR 0006 and `CLAUDE.md`

**Files:**
- Create: `knowledge/decisions/0006-outreach-separate-from-apply.md` (from `0000-template.md`)
- Modify: `knowledge/decisions/README.md` (new row)
- Modify: `CLAUDE.md` (architecture skills line; the `read_postings.py` command line)

**Depends on:** none

- [ ] **Step 1:** Write the ADR with status accepted and date 2026-10-19. Context, Decision and Consequences come from the spec's "ADR 0006" section. Add a README row: `| [0006](0006-outreach-separate-from-apply.md) | Outreach separate from apply | accepted | 2026-10-19 |`.
- [ ] **Step 2:** In `CLAUDE.md`, the skills line becomes `` `/discover` (career-ops scanner → CSV) → `/resume` → `/apply`; `/outreach` (LinkedIn only; `--apply` to apply first) → `/followup`; ``, with the rest of that bullet unchanged. Add `[--for outreach]` to the `read_postings.py` line. Keep `CLAUDE.md` about a screen long.
- [ ] **Step 3: Verify.**
  Run: `rg -n "0006" knowledge/decisions/README.md` and `rg -n "for outreach|--apply. to apply first" CLAUDE.md`
  Expected: one README row; two CLAUDE.md hits.
- [ ] **Step 4: Commit** with message `ADR 0006: outreach separate from apply`.

### Task 7: Verify the spec's success criteria

**Files:**
- Modify: `docs/superpowers/specs/2026-10-19-outreach-without-apply-design.md` (Status → `implemented`), and this plan (Status → `implemented`)

**Depends on:** Task 1, Task 2, Task 3, Task 4, Task 5, Task 6

- [ ] **Step 1:** Run `python -m unittest discover -s tests -v` and `python -m py_compile tools/*.py`. Expected: OK, with 74 tests (70 plus 4).
- [ ] **Step 2:** Run `rg -n -i "applied|InMail|attach" .claude/skills/outreach .claude/skills/followup`. Classify every hit as allowed (spec criterion 3).
- [ ] **Step 3:** Run `rg -n "/apply|Submit|submit" .claude/skills/outreach/SKILL.md .claude/skills/batch/SKILL.md`. Attribute each outreach-relevant hit to the `--apply` path, to `apply` mode, or to a forbid rule. Write a "Paths" table for the PR body that lists the steps each of the four paths runs (`/outreach`, `/outreach --apply`, `/batch outreach`, `/batch outreach --apply`).
- [ ] **Step 4:** Run `rg -n "outreach-only" .claude/skills tools CLAUDE.md`. It must hit outreach, apply, batch, followup and read_postings. Run `rg -F -c` on the exact legend line across the four skills. Expected: 1 in each.
- [ ] **Step 5:** Run `rg -n "/outreach runs this first\." .claude/skills` (expected: nothing) and `ls knowledge/decisions/0006-*`.
- [ ] **Step 6:** Set the spec and plan Status to `implemented`, then commit with message `Mark outreach-without-apply spec and plan implemented`.
