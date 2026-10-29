# Anonymize the repo and move personal settings to a local config Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

- **Date:** 2026-10-28
- **Status:** approved

**Goal:** Every tracked file is free of the maintainer's personal data; personal settings live in a gitignored `config.local.json` that the skills read; a unittest (`tests/test_no_personal_data.py`) keeps it that way; the maintainer's results are unchanged.

**Architecture:** One Python change (`tools/build_cover_letter.py` takes the sign-off name and output file name from the profile, with a `--profile` option), one new test module (a scanner over `git ls-files`), and Markdown edits: skills read `config.local.json` directly (no helper), the maintainer's name becomes "the user", hard-coded country/city/currency becomes config `targeting`, and docs are scrubbed by substitution. A before/after capture proves the maintainer's outputs are identical.

**Tech Stack:** Python 3 stdlib, `unittest`, PyMuPDF (already used); Claude Code skills (Markdown); Claude Docs and Artifact tools for the captures.

**Spec:** `docs/superpowers/specs/2026-10-28-anonymize-and-local-config-design.md` (approved; its gate record is under docs/superpowers/gates/ with the same file name). Read the spec's Design section before each task; this plan names the decisions and checks, it does not repeat the spec.

## Global Constraints

- **Anti-goal (overrides everything):** the maintainer's own use must not change: same sources, prompts, weekly routine and artifact, LinkedIn behaviour, file names, output. The one accepted output change is the shortlist note `applied by the user on the site` (spec decision 6).
- **This plan and every file you write must itself pass the personal-data test:** never write the maintainer's name, username, email, phone, street, an absolute user path, a Claude Docs / artifact / routine id or URL, the GitHub remote, or a company the maintainer applied to. Refer to them as "the maintainer's first name", `<repo-root>`, `<main-checkout>`, `<career-ops-dir>`, "the shortlist artifact", "a company". The values are in `.personal-terms` and `config.local.json` once Task 2 has run.
- **Paths used in this plan:** `<worktree>` = this worktree's root (where you run commands). `<main-checkout>` = the repo's main working tree (first line of `git worktree list`); it holds the maintainer's gitignored `sources/`, `postings/`, `applications.md`. `<S>` = the session scratchpad directory. Never write into `<main-checkout>` before Task 10's post-merge steps, and never change its `sources/`, `postings/` or trackers.
- **Config file:** `config.local.json` at the repo root, gitignored; shape exactly as spec §1 (`sources` required; `shortlist`, `career_ops_dir`, `discover_locations`, `linkedin_premium`, `targeting` optional). Skills read it as JSON with the Read tool or `python -c "import json; ..."`; no helper module.
- **Missing-config message (exact wording, every skill that needs the file):** `config.local.json is missing: this repo is not set up yet (README "Setup").` **Missing optional key:** `<feature> is not set up: add "<key>" to config.local.json (README "Setup").` with `<feature>` = `The shortlist` (the only optional key with a not-set-up stop; discover asks for the career-ops path instead). **Which skills stop on a missing file:** `pull-sources.md` (so every skill that pulls: resume, cover-letter, apply, outreach, batch, followup), `write-source.md` and `job-shortlist` stop with the missing-config message. `discover`, `linkedin-tab.md`, `batch/scoring.md`, `resume`, `outreach`, `followup` and `apply/workday.md`, when they read an optional key, treat a missing file as every optional key absent (spec's absent-`targeting` / plan-unknown behaviour); in practice the pull has already stopped them.
- **"The user":** skills say "the user" where they name the maintainer, and pronouns for the maintainer (he/his/him) become "the user" / "the user's" / "they"; rules keep their meaning; frontmatter `description`s keep every trigger phrase and `/command`.
- **Name-free literals (byte-exact):**
  - parse-only old-log action, described as ``typed, <word> to send` (any single word)``; regex `typed, \S+ to send`;
  - changelog heading written as `Questions for the user`; the batch resume prompt asks for "the changelog's `Questions for <…>` section (any heading of that form)"; regex `Questions for .+`;
  - shortlist note `applied by the user on the site`;
  - subagent status token `NEEDS USER` (replaces the name-bearing `NEEDS <NAME>` token in `apply/SKILL.md`, `apply/workday.md`, `batch/SKILL.md`, `outreach/SKILL.md`; the token lives only in live replies and this run's manifest, so no parse-old rule is needed);
  - renamed heading `The user's plan and each person's message route` (linkedin-tab.md) and its cross-references in outreach and followup.
- **Targeting placeholders in skill text:** `<eligible_regions>`, `<home_city>`, `<currency>`, `<phone_country>`, each "from `config.local.json` `targeting`"; absent `targeting` behaviour exactly as spec §2 "Targeting".
- **Output file names:** `<Full_Name>_Resume_<Company>.tex` and `<Full_Name>_Cover_Letter_<Company>.tex/.pdf`, `<Full_Name>` = profile `## Contact` `Full name`, trailing parenthetical note stripped, spaces → `_`.
- `tools/` code is not ruff-clean by design; match surrounding style. CI runs `python -m py_compile tools/*.py` and `python -m unittest discover -s tests -v`.
- Never `git add -A` / `git add .`: add named paths only (gitignored and scratch files must never be staged).
- Shell: run `rg`/`grep` checks whose pattern starts with `/` in PowerShell, or Bash with `MSYS_NO_PATHCONV=1`.

## Review Focus

- A profile whose `Preferred first name` carries a trailing note ("Jordan (on forms)") must sign off as "Jordan". Test `test_signoff_name_drops_trailing_note` in Task 3.
- A profile with no `Preferred first name` line must fall back to the first word of `Full name`, not crash. Test `test_signoff_name_falls_back_to_full_name` in Task 3.
- `--profile` given before the `.md` argument must still treat the `.md` as the letter. Test `test_profile_flag_before_md` in Task 3.
- A personal term glued to `_` or `.` (as in `<Name>_Resume_Acme.tex` or `<name>.md`) must be caught, while the same letters inside a longer word must not. Tests `test_term_matches_next_to_underscore` / `test_term_ignores_inside_word` in Task 9.
- A `.personal-terms` file with blank lines, `#` comments or Windows line endings must not turn into an empty term that matches everything. Test `test_load_terms_skips_blank_and_comments` in Task 9.

---

### Task 1: Baseline capture (before any change)

**Files:** none (scratch only, outside the repo: `<S>/before/` holds sources copies, the letter run and JSON captures; nothing to commit)

**Depends on:** none

**Interfaces:**
- Produces: `<S>/before/sources/<six files>`, `<S>/before/letter/<dir>/` (the `.tex`), `<S>/before/letter/check.json`, `<S>/before/latest.json`, `<S>/before/resolved.json`, `<S>/before/grep-typed.txt`, `<S>/before/grep-questions.txt`. Task 10 compares against these.

Run in the main session (it needs the Claude Docs and Artifact tools), from `<worktree>`, on the same day as Task 10 and not on a Saturday (the weekly run). Nothing in the repo changes.

- [ ] **Step 1: Pull the sources with today's procedure.** Follow `.claude/skills/pull-sources.md` as it stands (it reads `sources.json`) from `<worktree>`, so the files land in `<worktree>/sources/` (gitignored). Copy the six files to `<S>/before/sources/`. Expected: six files, the procedure's one-line report.
- [ ] **Step 2: Cover letter.** Pick one `<main-checkout>/postings/<dir>/cover_letter.md` (any posting that has one). Copy it to `<S>/before/letter/<dir>/cover_letter.md` (keep `<dir>`; the tool takes the company from it). Run `python tools/build_cover_letter.py <S>/before/letter/<dir>/cover_letter.md --check > <S>/before/letter/check.json`, then `python tools/build_cover_letter.py <S>/before/letter/<dir>/cover_letter.md`. Record the `.tex` file name it wrote. Expected: a `*_Cover_Letter_<Company>.tex` next to the copy.
- [ ] **Step 3: Shortlist.** From today's `.claude/skills/job-shortlist/SKILL.md` "Constants", note the artifact URL and title; Artifact `read` that URL with `path: data/latest.json`; copy the saved file to `<S>/before/latest.json`.
- [ ] **Step 4: Resolved values.** Write `<S>/before/resolved.json` with the literal values today's skill text uses: `shortlist_url`, `shortlist_title` (Step 3); `career_ops_dir` and `discover_locations` (the path and `--location` list in `discover/SKILL.md` step 1, as a JSON list in order); `resume_tex` (the name `resume/SKILL.md` step 3 writes, with `<Company>` taken from Step 2's `<dir>`); `cover_letter_tex` (Step 2); `eligible_regions` (`["Canada", "Quebec"]` per spec §2), `home_city` (the city `outreach/SKILL.md` and `batch/scoring.md` name), `currency` (`CAD`), `phone_country` (`Canada (+1)` from `apply/workday.md`); `linkedin_premium` (`true`).
- [ ] **Step 5: Parse-only greps.** Run, with the maintainer's first name for `<First>`:
  `grep -E -h "typed, <First> to send" <main-checkout>/postings/*/outreach.md > <S>/before/grep-typed.txt` and
  `grep -E -h "Questions for <First>" <main-checkout>/postings/*/changelog.md > <S>/before/grep-questions.txt` (an empty file is a valid result).

### Task 2: Config files and maintainer migration

**Files:**
- Create: `config.example.json`
- Modify: `.gitignore`
- Remove from tracking: `sources.json` (`git rm --cached`)
- Create (gitignored, local only): `<worktree>/config.local.json`, `<worktree>/.personal-terms`

**Depends on:** Task 1

**Interfaces:**
- Produces: the config shape of spec §1 with the maintainer's values in `config.local.json`; `.personal-terms` (one term per line; blank lines and `#` lines ignored; Task 9 reads it).

- [ ] **Step 1: `.gitignore`.** Add, under the first block, the lines `/config.local.json`, `/.personal-terms`, `/sources.json` with a one-line comment `# Personal settings (README "Setup")`.
- [ ] **Step 2: `config.example.json`.** Spec §1 shape: `"_comment": "Copy to config.local.json and fill it in: see README \"Setup\". config.local.json is gitignored."` first; six `sources` entries with today's six `path`s and placeholder values `"https://claude.ai/code/artifact/<doc-id>"`, `"<tab-id>"`; the `sources/profile.md` entry also has `"node_id": "<node-id>"`, `"writable": true`; `"shortlist": {"artifact_url": "https://claude.ai/artifact/<artifact-id>", "title": "<shortlist title>"}`, `"career_ops_dir": "<path to your career-ops checkout>"`, `"discover_locations": ["<city or country>"]`, `"linkedin_premium": false`, `"targeting": {"eligible_regions": ["<country>", "<region>"], "home_city": "<city>", "currency": "USD", "phone_country": "<Country (+code)>"}`. Check: `python -c "import json; json.load(open('config.example.json', encoding='utf-8'))"` exits 0.
- [ ] **Step 3: `config.local.json` (spec §4).** Write it from Task 1's `resolved.json` and today's `sources.json` (all six entries copied verbatim, field for field): `sources`, `shortlist` `{artifact_url, title}`, `career_ops_dir`, `discover_locations`, `linkedin_premium: true`, `targeting` `{eligible_regions, home_city, currency, phone_country}`. Check with a Python one-liner that `config.local.json["sources"] == json.load(open("sources.json"))["sources"]`.
- [ ] **Step 4: `.personal-terms`** (answers gate plan question "every handle variant?": yes). One term per line: each word of `Full name` and the whole full name, `Preferred first name`, the OS username, the GitHub handle (owner part of `git remote get-url origin`), the LinkedIn vanity (last path part of the profile's `LinkedIn`), the GitHub URL's handle if different, the email (whole address and local part), the phone (as written in the profile and digits only), the `Street address` value from `sources/profile.md` (whichever section holds it), and every id in `config.local.json` (each doc UUID at the end of a `doc_url`, each `tab_id`, the `node_id`, the shortlist artifact id). Values come from `<worktree>/sources/profile.md` `## Contact` and `config.local.json`. Do not print them in chat. Write the file with LF line endings and no blank or comment lines, so the interim `git grep -n -i -w -F -f .personal-terms` checks in Tasks 4-8 (fixed strings, one per line) are safe; those checks miss `_`-glued forms such as `<Name>_Resume`, which Task 9's test catches (it is the authoritative check).
- [ ] **Step 5: Stop tracking `sources.json`.** `git rm --cached sources.json`, then delete the untracked `<worktree>/sources.json`. Run: `git status --short`. Expected: it shows `D  sources.json`, `M .gitignore`, `?? config.example.json` (plus this plan, its gate record and `docs/superpowers/README.md` if the caller has not committed them yet; they are committed with the plan, not in this task) and nothing for `config.local.json` / `.personal-terms`.
- [ ] **Step 6: Commit.** `git add .gitignore config.example.json` and `git commit -m "Local config: config.example.json, sources.json untracked"`.

(Gate plan question "does the worktree get a copy of `config.local.json`?": yes. The worktree copy is written here and used for Task 10's after capture; `<main-checkout>` gets its copy only after merge, Task 10 Step 7, because its skills read `sources.json` until then.)

### Task 3: Cover-letter tool reads the name from the profile; tool and test text made neutral

**Files:**
- Modify: `tools/build_cover_letter.py`, `tools/shortlist.py` (docstring line 1), `tests/fixtures/decision_keys.py` (docstring line 1)
- Create: `tests/fixtures/profile.md`
- Test: `tests/test_build_cover_letter.py`, `tests/test_shortlist.py` (`FIXTURE_SHA256`, decision `source` value), `tests/test_build_resume.py` (lines 23-26), `tests/test_pull_sources.py` (line 36)

**Depends on:** Task 1

**Interfaces:**
- Produces (in `tools/build_cover_letter.py`):
  - `PROFILE: Path` unchanged (default `<repo>/sources/profile.md`); `MISSING_PROFILE` unchanged.
  - `FORMS: dict[str, str]` greeting → closing word: `"Dear hiring team," → "Best,"`, `"Bonjour à l'équipe de recrutement," → "Cordialement,"`.
  - `contact_fields(profile: Path) -> dict[str, str]`: every `## Contact` bullet, trailing parenthetical note stripped (today's regex in `contact()`).
  - `contact(profile: Path) -> dict` (today's header dict, now from `contact_fields`).
  - `signoff_name(profile: Path) -> str`: `Preferred first name`, else first word of `Full name`.
  - `letter_tex_path(md: Path, profile: Path) -> Path`: `md.with_name(f"{Full name with spaces→_}_Cover_Letter_{company}.tex")`, company as today (`md.parent.name.split("-")[0]`).
  - `preamble(profile: Path) -> str` and `to_tex(text: str, profile: Path) -> str`: as today, passing `profile` to `contact`.
  - `check(lines: list[str], name: str) -> dict`: `signoff_ok` = greeting known and `lines[-2:] == [FORMS[greeting], name]`.
  - `main(argv)`: positional `.md` = first argument that is not `--check`, not `--profile`, and not the value after `--profile`; `--profile <path>` (default `PROFILE`) for sign-off check, header and file name; missing profile in either mode → `ok: false`, `error: MISSING_PROFILE`, report still has `words`, `greeting_ok`, `signoff_ok: false`, exit 1, no `.tex` written.
- Task 6 (apply/resume text) relies on the file-name rule.

- [ ] **Step 1: Fixture `tests/fixtures/profile.md`.** A fictional person: `# Application profile`, `## Contact` with `- Full name: Jordan Avery Lee`, `- Preferred first name: Jordan`, `- Phone: 555-0100`, `- Email: jordan@example.com`, `- Location: Springfield, QC, Canada`, `- LinkedIn: https://www.linkedin.com/in/jordan-example`, `- GitHub: https://github.com/jordan-example`; then `## Eligibility` with one bullet.
- [ ] **Step 2: Write the failing tests** in `tests/test_build_cover_letter.py`. `FIXTURE = Path(__file__).parent / "fixtures" / "profile.md"`; `LETTER` ends `"\n\nBest,\nJordan\n"`. Replace `mock.patch.object(... "PROFILE" ...)` uses with explicit `profile` arguments / `--profile`. Tests (assertions):
  - `test_contact_reads_contact_section`: `contact(FIXTURE)` equals the header dict (`name "Jordan Avery Lee"`, `city "Springfield"`, `linkedin_bare "linkedin.com/in/jordan-example"`, …); keep `test_contact_drops_trailing_notes` and `test_contact_keeps_inner_parentheses` on a temp copy of the fixture.
  - `test_signoff_name_prefers_preferred_first_name`: `signoff_name(FIXTURE) == "Jordan"`.
  - `test_signoff_name_drops_trailing_note`: temp profile with `- Preferred first name: Jordan (on forms)` → `"Jordan"`.
  - `test_signoff_name_falls_back_to_full_name`: temp profile without the `Preferred first name` line → `"Jordan"`.
  - `test_check_signoff_uses_profile_name`: `run_main([str(letter), "--check", "--profile", str(FIXTURE)])` → code 0, `signoff_ok` true; the same letter ending `Best,\nSam` → `signoff_ok` false, code 1.
  - `test_check_french_form`: greeting `Bonjour à l'équipe de recrutement,`, ending `Cordialement,\nJordan` → `greeting_ok` and `signoff_ok` true.
  - `test_profile_flag_before_md`: `run_main(["--profile", str(FIXTURE), str(letter), "--check"])` → code 0, `report["md"]` is the letter path.
  - `test_check_requires_profile` (replaces `test_check_needs_no_profile`): `--check --profile <missing>` → code 1, `ok` false, `error == MISSING_PROFILE`, `"words"` in report.
  - `test_missing_profile_is_json_error`: as today but via `--profile <missing>`; still no `.tex` written.
  - `test_default_profile_used_without_flag`: with `mock.patch.object(bcl, "PROFILE", FIXTURE)`, `run_main([letter, "--check"])` → code 0.
  - `test_letter_tex_path_from_full_name`: `letter_tex_path(<tmp>/Acme-1/cover_letter.md, FIXTURE).name == "Jordan_Avery_Lee_Cover_Letter_Acme.tex"`.
  - keep `test_profile_path`.
- [ ] **Step 3: Run, expect failures.** `python -m unittest tests.test_build_cover_letter -v` → errors on `signoff_name` / `letter_tex_path` / `--profile`.
- [ ] **Step 4: Implement** the Interfaces above in `tools/build_cover_letter.py`. Rewrite the module docstring: usage `python tools/build_cover_letter.py <postings/<dir>/cover_letter.md> [--check] [--profile <path>]`; `signoff_ok` "last two lines are the closing word for that greeting and the profile's `Preferred first name` (else first word of `Full name`)"; `pdf` `<Full_Name>_Cover_Letter_<Company>.pdf`; `error` "sources/profile.md (or --profile) is missing, in either mode". The line-92 comment says "a trailing note for the user".
- [ ] **Step 5: Run, expect pass.** `python -m unittest tests.test_build_cover_letter -v` → OK (skips only when PyMuPDF is absent).
- [ ] **Step 6: Neutral text elsewhere.** `tools/shortlist.py` docstring line 1 → "Helper for the job-shortlist skill: the user's weekly shortlist artifact and its `decisions`." `tests/fixtures/decision_keys.py` line 1 → "Reference key functions for the Job Shortlist decisions. Must match the page's JS exactly." (key functions untouched; keep its `-text` byte form: edit with Python `bytes.replace`, not an editor that rewrites line endings), then set `FIXTURE_SHA256` in `tests/test_shortlist.py` to `python -c "import hashlib;print(hashlib.sha256(open('tests/fixtures/decision_keys.py','rb').read()).hexdigest())"`. In `tests/test_shortlist.py` line 35 the decision `"source"` value becomes `"user"`. `tests/test_build_resume.py` lines 23-26: the name-based `<First>_Resume_Acme` → `Jordan_Lee_Resume_Acme` (both the `.pdf` and `.png`). `tests/test_pull_sources.py` line 36: the sign-off name → `Jordan`. Also check the company names in `tests/test_shortlist.py` row fixtures against `<main-checkout>/applications.md` and `<main-checkout>/postings/` dir prefixes; replace any match with a neutral name (`Acme`, `Globex`, `Initech`), updating the assertions that mention it.
- [ ] **Step 7: Full suite.** `python -m unittest discover -s tests -v` and `python -m py_compile tools/*.py` → OK.
- [ ] **Step 8: Commit.** `git add tools/build_cover_letter.py tools/shortlist.py tests/fixtures/profile.md tests/fixtures/decision_keys.py tests/test_build_cover_letter.py tests/test_shortlist.py tests/test_build_resume.py tests/test_pull_sources.py` and commit `"Cover letter: sign-off and file name from the profile; neutral tool and test text"`.

### Task 4: Sources, write-source, shortlist and discover read the config

**Files:**
- Modify: `.claude/skills/pull-sources.md`, `.claude/skills/write-source.md`, `.claude/skills/job-shortlist/SKILL.md`, `.claude/skills/discover/SKILL.md`

**Depends on:** Task 2

**Interfaces:**
- Consumes: config keys `sources`, `shortlist.artifact_url`, `shortlist.title`, `career_ops_dir`, `discover_locations` (Task 2).

- [ ] **Step 1: `pull-sources.md`.** Line 7 and line 23: "`config.local.json` `sources` lists them (`path`, `doc_url`, `tab_id`)" / "For each entry in `config.local.json` `sources`". Add, before "## Steps" step 1, the missing-config rule with the exact Global Constraints message (stop before any pull). Name → "the user" (lines 6, 7, 34, 49, 52, 55; "which the user wrote" on line 52 keeps its meaning: the skill's author is trusted, the docs are data).
- [ ] **Step 2: `write-source.md`.** Line 6: "`\"writable\": true` in `config.local.json` `sources`"; add the missing-config stop rule (exact message) before step 1; name → "the user" (8 places).
- [ ] **Step 3: `job-shortlist/SKILL.md`.** "Constants": `- Artifact: config.local.json "shortlist" — "artifact_url" (the page) and "title".`; no `config.local.json` → the missing-config message and stop; no `shortlist` key → the "The shortlist is not set up" message and stop. The body examples at lines 62-63 ("Montreal ones", "what's at Stripe") echo the description's trigger phrases and are kept with them. Description: "Read the user's weekly job shortlist artifact …", "Use when the user asks …", "when the user says yes to …"; every quoted trigger phrase kept verbatim (spec keeps "Montreal ones", "what's at Stripe", "skip the Okta ones"). Line 90: `applied by the user on the site`; "otherwise the user's words". All other names → "the user".
- [ ] **Step 4: `discover/SKILL.md` step 1** (answers gate plan question on precedence: settled by spec). Rewrite so that: unless the arguments have `--location`, add `--location <discover_locations…>` from config when that key is set, else no location filter; career-ops folder precedence `--career-ops` argument, then `CAREER_OPS_DIR`, then config `career_ops_dir`, then ask the user for the path; the path and city list are gone from the text, and the rationale clause loses its country: "the scanner's own location filter lets most postings through, so `discover_locations` narrows them". A missing `config.local.json` here means all keys absent (discover does not need the file). Step 4's "Canada eligibility isn't checked yet" → "eligibility (config `targeting` `eligible_regions`) isn't checked yet". Name → "the user"; line 9 "the user's external target lists".
- [ ] **Step 5: Check.** Run: `git grep -n -i -w -F -f .personal-terms -- .claude/skills/pull-sources.md .claude/skills/write-source.md .claude/skills/job-shortlist .claude/skills/discover` → no output; `git grep -n "sources.json" -- .claude` → no output; `git grep -n -F "applied by the user on the site" -- .claude/skills/job-shortlist/SKILL.md` → one hit; `git grep -n -E "Canad|Quebec|Users" -- .claude/skills/discover` → no output, and `git grep -n "Montreal" -- .claude/skills/discover` → no output.
- [ ] **Step 6: Commit** the four files: `"Skills read config.local.json: sources, shortlist, discover"`.

### Task 5: LinkedIn skills: plan fallback, heading rename, region rule

**Files:**
- Modify: `.claude/skills/linkedin-tab.md`, `.claude/skills/outreach/SKILL.md`, `.claude/skills/followup/SKILL.md`

**Depends on:** Task 2

**Interfaces:**
- Consumes: config `linkedin_premium`, `targeting.eligible_regions`, `targeting.home_city`.

- [ ] **Step 1: `linkedin-tab.md`.** Heading line 27 → `## The user's plan and each person's message route`; line 31 bullet → "**The user's plan (once per run, …)**"; line 34's last sentence → "If none of these settles it, use `linkedin_premium` from `config.local.json` if set (true = Premium, false = free), else ask the user." Nothing else in the check changes. Other names → "the user".
- [ ] **Step 2: `outreach/SKILL.md`.** Lines 101-102 cross-reference → the new heading and "check the user's plan". Line 62 "**The user's connections first**". Line 87 "Never say he applied, even when he has" → "Never say the user applied, even when they have". Lines 67-69: "preferring ones covering the posting's location or `<eligible_regions>` (config `targeting`)"; "in the posting's location, or the user's `<home_city>` (config `targeting`) if the posting names several"; with no `targeting`: only the posting's location. Line 119: "(Older logs may carry `InMail` or `typed, <word> to send` (any single word); …". `NEEDS <NAME>` → `NEEDS USER` (line 186). All other names → "the user"; description keeps its trigger phrases.
- [ ] **Step 3: `followup/SKILL.md`.** Line 12 "his plan" → "the user's plan"; line 13 cross-reference → the new heading. Lines 51-52 and 236: `typed, <word> to send` (any single word), still parse-only, never written. Other names → "the user"; description trigger phrases kept.
- [ ] **Step 4: Check.** Run: `git grep -n -i -w -F -f .personal-terms -- .claude/skills/linkedin-tab.md .claude/skills/outreach .claude/skills/followup` → none; `git grep -n -F "The user's plan and each person's message route" -- .claude` → 3 hits (one per file); `git grep -n -E "Canada|Montreal|North America" -- .claude/skills/outreach .claude/skills/linkedin-tab.md .claude/skills/followup` → none.
- [ ] **Step 5: Commit** the three files: `"LinkedIn skills: the user, Premium fallback from config, regions from targeting"`.

### Task 6: Resume, apply, Workday and cover-letter skills

**Files:**
- Modify: `.claude/skills/resume/SKILL.md`, `.claude/skills/apply/SKILL.md`, `.claude/skills/apply/workday.md`, `.claude/skills/cover-letter/SKILL.md`

**Depends on:** Task 2, Task 3

**Interfaces:**
- Consumes: file-name rule of Task 3; config `targeting.eligible_regions`, `targeting.phone_country`.

- [ ] **Step 1: `resume/SKILL.md`.** Step 3 file name → `postings/<dir>/<Full_Name>_Resume_<Company>.tex` with one clause defining `<Full_Name>` (Global Constraints). Line 63: "if it excludes candidates based in any of `<eligible_regions>` (config `targeting`; skip this check when `targeting` is absent)"; changelog section `Questions for the user`. Line 68: "excludes a region in `<eligible_regions>`". Names → "the user".
- [ ] **Step 2: `apply/SKILL.md`.** Line 38: upload `<Full_Name>_Cover_Letter_<Company>.pdf` (the name `tools/build_cover_letter.py` prints as `pdf`). `NEEDS <NAME>` → `NEEDS USER` (lines 120, 124). Keep the 2026-10-04 Enter-key incident sentence (line 53) verbatim, company name included (spec exception). Names → "the user"; description trigger phrases kept.
- [ ] **Step 3: `apply/workday.md`.** Line 116: country code `<phone_country>` from config `targeting`; when absent, mark the field `ASK` (the user is asked with the step's other `ASK`s). `NEEDS <NAME>` → `NEEDS USER` (line 104). Names → "the user".
- [ ] **Step 4: `cover-letter/SKILL.md`.** Names → "the user" (2 places).
- [ ] **Step 5: Check.** Run: `git grep -n -i -w -F -f .personal-terms -- .claude/skills/resume .claude/skills/apply .claude/skills/cover-letter` → none; `git grep -n -E "Canada|Quebec" -- .claude/skills/resume .claude/skills/apply` → only `workday.md` line 114's `QC` → `Quebec` province-dropdown example (it maps the profile's address, not targeting; leave it).
- [ ] **Step 6: Commit** the four files: `"Resume and apply skills: the user, file names from the profile, targeting from config"`.

### Task 7: Batch skill and scoring

**Files:**
- Modify: `.claude/skills/batch/SKILL.md`, `.claude/skills/batch/scoring.md`

**Depends on:** Task 2

**Interfaces:**
- Consumes: config `targeting` (all four keys).
- Produces: prompt placeholders `<repo-root>` and `<eligible_regions>` that the orchestrator substitutes at launch.

- [ ] **Step 1: Repo path.** Each of the 6 prompts (lines 80, 104, 143, 169, 193, 289): "in the repo root `<repo-root>`". Add one sentence before the first prompt: "In every subagent prompt below, replace `<repo-root>` with the output of `git rev-parse --show-toplevel` , `<eligible_regions>` with config `targeting.eligible_regions` joined by ` or `, and `<currency>` with config `targeting.currency` (`USD` when absent)."
- [ ] **Step 2: Pre-screen (lines 20, 57, 85).** Table row: "live? eligible for `<eligible_regions>`?"; line 57 "unverified eligibility"; INELIGIBLE: "the text excludes candidates based in any of `<eligible_regions>`; quote it"; with no `targeting`, the orchestrator drops the INELIGIBLE clause from the prompt. Line 85's example posting dir (a real company) → "in the format of `posting.md` in `.claude/skills/resume/SKILL.md` step 2".
- [ ] **Step 3: Currency.** Lines 67-68 targeting keys: "`Pay floor: skip when the top of the posted range is below <amount> <currency>`, `USD to <currency> rate`" (no `targeting`: `USD` and no rate key). Lines 111, 122, 238: `CAD` → `<currency>`.
- [ ] **Step 4: Literals.** Line 147: the changelog's `Questions for <…>` section (any heading of that form), or none. `NEEDS <NAME>` → `NEEDS USER` (lines 32, 287, 295, 305, 307). Remaining names → "the user" (description trigger phrases kept).
- [ ] **Step 5: `scoring.md`.** Line 11 "evidence about the user". Line 12 profile key `USD to <currency> rate`. Line 42: "Convert to annual `<currency>` (config `targeting`): USD × `USD to <currency> rate`" (no `targeting`: amounts in USD, no conversion). Lines 44-45: "else from the posting's location (a location in `<eligible_regions>` → `<currency>`, a United States location → USD), else counts as USD". Lines 46-47: "use the one for a posting location in `<eligible_regions>` (`<home_city>` first when several apply), else any range in `<eligible_regions>`, else the first listed" (no `targeting`: the first listed). Lines 51, 87, 117: `CAD` → `<currency>`; band amounts unchanged. Say once near the top: "`<currency>`, `<eligible_regions>`, `<home_city>`: from `config.local.json` `targeting` at the repo root."
- [ ] **Step 6: Check.** Run: `git grep -n -i -w -F -f .personal-terms -- .claude/skills/batch` → none; `git grep -n -E "\bCAD\b|Canad|Quebec|Montreal|Users" -- .claude/skills/batch` → only the explicit-label list on scoring line 44 (`CAD`, `USD`, `CA$`: currency labels read from posting text, kept).
- [ ] **Step 7: Commit** the two files: `"Batch: <repo-root>, targeting and currency from config, name-free literals"`.

### Task 8: Docs: CLAUDE.md, README Setup, ADR 0009, knowledge and design-doc scrub

**Files:**
- Modify: `CLAUDE.md`, `README.md`, `knowledge/README.md`, `knowledge/decisions/README.md`, `knowledge/decisions/0001`–`0008` (substitutions only), `docs/superpowers/README.md`, every file under `docs/superpowers/specs/`, `docs/superpowers/plans/`, `docs/superpowers/gates/` (including this plan; this spec and its gate record are already clean), `.github/*` if anything hits
- Create: `knowledge/decisions/0009-shared-repo-and-local-config.md`

**Depends on:** Task 2

- [ ] **Step 1: `CLAUDE.md`.** Setup bullet: "signed in to the user's account; skills pull the sources listed in `config.local.json` (README "Setup")". Architecture line 30: "listed in `config.local.json` `sources`". Conventions: "the user" (approval rules unchanged in meaning). Gotcha on `tests/fixtures/decision_keys.py`: "the key functions match the shortlist artifact's keys file; the docstring is neutral, so the file is not byte-identical to it; refreshing the functions also means updating `FIXTURE_SHA256`". Add one gotcha: "`tests/test_no_personal_data.py` scans every tracked file; on the maintainer's machine it also checks the gitignored `.personal-terms`." Add `config.local.json` and `.personal-terms` to the local-only list.
- [ ] **Step 2: `README.md`.** Line 3 "A job-search workspace: …". New `## Setup` section per spec §2 "README Setup": prerequisites (Python 3, `pdflatex` or MiKTeX, Chrome with Claude in Chrome, the Claude Docs connector), create your six source Docs (one fenced code block each, names as in `config.example.json` `sources`), copy `config.example.json` to `config.local.json` and fill it (one line per key, optional keys and what their absence means, from spec §1/§2), optionally career-ops and the shortlist; then the note: "Git history predates this cleanup and still holds the maintainer's earlier details."
- [ ] **Step 3: ADR 0009** in the template's format (`knowledge/decisions/0000-template.md`), content per spec §5, status Accepted, date 2026-10-28; add its row to `knowledge/decisions/README.md`.
- [ ] **Step 4: Scrub** (substitution only, meaning kept; ADR decisions not changed): name → "the user" (or "the maintainer" where it records history); absolute paths → `<repo-root>` / `<career-ops-dir>` / `%USERPROFILE%`; the GitHub remote → "the GitHub remote"; Docs / artifact URLs → a description ("the Mega resume Doc", "the shortlist artifact"); `tab_id` / `node_id` values → `<tab_id>` / `<node_id>`; company names from the maintainer's applications → "a company". Gate records: scrub text only and leave every recorded `SHA-256` line as its historical value (answers gate plan question 4). For company names, build `<S>/companies.txt` from the Company column of `<main-checkout>/applications.md` and the `postings/` dir prefixes, then `git grep -n -i -w -F -f <S>/companies.txt` over the whole tree and review each hit (hits under `.claude/skills` or `tests/` are fixed here too and committed by path in Step 6); keep only the spec's exceptions (`apply/SKILL.md` line 53 incident; job-shortlist description phrases and their echoes at body lines 62-63, and the quotations of those phrases in this spec and this plan) and generic words that are not a reference to the application.
- [ ] **Step 5: Check** (this task's paths only: `CLAUDE.md README.md knowledge docs/superpowers .github`). Run: `git grep -n -i -w -F -f .personal-terms -- <those paths>` → no output; `git grep -n -I -E "claude\.ai/(code/)?artifact/[0-9A-Za-z-]{10,}|[A-Za-z]:[\\/]Users[\\/][^<%[:space:]]|github\.com/[^/ ]+/jobapps"` → no output; the companies grep → only the kept exceptions.
- [ ] **Step 6: Commit** the changed docs by path (`git add CLAUDE.md README.md knowledge docs/superpowers .github`, plus any skill or test file fixed in Step 4): `"Docs: scrub personal data, README Setup, ADR 0009"`.

### Task 9: Personal-data test

**Files:**
- Create: `tests/test_no_personal_data.py`

**Depends on:** Task 3, Task 4, Task 5, Task 6, Task 7, Task 8

**Interfaces:**
- Produces (module-level in the test file): `ROOT: Path`; `GENERIC: list[tuple[str, re.Pattern]]` named `artifact_url`, `routine_id`, `windows_user_path`, `home_path`, `mac_user_path`, `email`, `phone` with the regexes of spec §3; `ALLOWLIST: list[tuple[str, str, str]]` (path glob, regex, reason); `load_terms(path: Path) -> list[str]`; `term_pattern(term: str) -> re.Pattern` = `(?:(?<![A-Za-z0-9])|(?<=\\[ntr]))` + `re.escape(term)` + `(?![A-Za-z0-9])`, `re.IGNORECASE` (so `_`, `.`, `-` and a preceding literal `\n` / `\t` / `\r` escape count as boundaries); `scan(path: str, text: str, patterns: list[tuple[str, re.Pattern]]) -> list[str]` returning `"<path>:<line>: <pattern name>"` for each hit not allowlisted; `is_binary(data: bytes) -> bool` (`b"\0" in data[:8192]`); `tracked_files() -> list[str]` (`git ls-files -z` in `ROOT`).
- Email rule: `[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}`, a hit unless the domain is `example.com`/`example.org` or the local part is `noreply`.

- [ ] **Step 1: Write the tests.** Build every positive sample at runtime by concatenation (`"C:" + "\\" + "Users" + "\\" + "bob"`, `"bob" + "@" + "corp.io"`, `"514" + "-555-" + "0199"`, `"claude.ai/artifact/" + "A" * 12`, `"trig_" + "B" * 12`) so the file's own text never matches. `ScannerTest`:
  - `test_generic_patterns_hit`: each sample yields its pattern name from `scan`.
  - `test_generic_patterns_skip_placeholders`: `<repo-root>`, `%USERPROFILE%\x`, `C:\Users\<name>` (built by concatenation), `x@example.com`, `noreply@anthropic.com` (concatenated), `a@b.c`, `https://claude.ai/artifact/<artifact-id>` → no hit.
  - `test_term_matches_next_to_underscore`: `term_pattern("Zed")` matches `Zed_Resume_Acme.tex`, `zed.md`, `ZED's`, and the text `Best,\nZed` (backslash and `n` as literal characters, i.e. the Python string `"Best,\\nZed"`).
  - `test_term_ignores_inside_word`: no match in `Zedekiah` or `aZed`.
  - `test_load_terms_skips_blank_and_comments`: a temp file `"Zed\r\n\r\n# note\n  Qux  \n"` → `["Zed", "Qux"]`.
  - `test_binary_detection`: `is_binary(b"a\0b")` true, `is_binary(b"abc")` false.
  - `test_allowlist_suppresses_hit`: with a temporary `ALLOWLIST` entry (`mock.patch`), the matching path/regex hit is dropped.
  `RepoScanTest`:
  - `test_tracked_files_have_no_generic_hits`: for each tracked non-binary file (read as UTF-8, `errors="replace"`), `scan(...)` with `GENERIC` is empty; failure message lists the hits.
  - `test_tracked_files_have_no_personal_terms`: `skipTest` when `ROOT / ".personal-terms"` is absent; else scan with `[(f"term {i}", term_pattern(t)) ...]` (report the term's index, never its text) → empty.
- [ ] **Step 2: Run, expect failure** before the helpers exist: `python -m unittest tests.test_no_personal_data -v` → `NameError`/`AttributeError` failures.
- [ ] **Step 3: Implement** the helpers in the test module with `ALLOWLIST = []`.
- [ ] **Step 4: Run on the scrubbed tree; settle the allowlist** (answers gate plan question 2). `python -m unittest tests.test_no_personal_data -v`. For each hit: if it is personal data, fix the file (back to the owning task's rule); only a verified non-personal hit gets an `ALLOWLIST` entry (narrowest glob and regex, a one-line reason). Expected end state: all tests pass, `test_tracked_files_have_no_personal_terms` runs (not skipped) because `<worktree>/.personal-terms` exists. Then rename `.personal-terms` aside and rerun: that test is skipped and the rest pass (the CI view); rename it back.
- [ ] **Step 5: Full suite.** `python -m unittest discover -s tests -v` and `python -m py_compile tools/*.py` → OK.
- [ ] **Step 6: Commit** `tests/test_no_personal_data.py` (plus any file fixed in Step 4, by path): `"Test: no personal data in tracked files"`.

### Task 10: After capture, comparison, and maintainer migration on main

**Files:** none tracked (nothing to commit). Scratch: `<S>/after/` mirroring `<S>/before/`. Post-merge, local only (gitignored): `<main-checkout>/config.local.json`, `<main-checkout>/.personal-terms`.

**Depends on:** Task 1, Task 2, Task 3, Task 4, Task 5, Task 6, Task 7, Task 9

**Interfaces:**
- Consumes: Task 1's captures; the changed skills and tool.

Same day as Task 1, main session, from `<worktree>` (which holds `config.local.json`).

- [ ] **Step 1: Sources.** Follow the changed `.claude/skills/pull-sources.md` (it reads `config.local.json`); compare the six `<worktree>/sources/` files with `<S>/before/sources/` byte for byte in one Python script. Expected: all six identical.
- [ ] **Step 2: Cover letter.** Copy the same `cover_letter.md` to `<S>/after/letter/<dir>/`; run the changed tool with `--check` and without (default profile `<worktree>/sources/profile.md`). Expected: same `.tex` file name; `.tex` byte-identical to Task 1's; `check.json` equal to Task 1's as JSON with the `md`, `pdf`, `png` keys removed.
- [ ] **Step 3: Shortlist and resolved values.** Artifact `read` the URL from `config.local.json` `shortlist` with `path: data/latest.json`; compare to `<S>/before/latest.json` as JSON → equal. Write `<S>/after/resolved.json` from what the changed skills resolve: shortlist URL/title from config; discover's `career_ops_dir` and `--location` list per the changed step 1 with no arguments and no `CAREER_OPS_DIR`; `resume_tex` per the changed resume step 3 from `sources/profile.md` `Full name`; `cover_letter_tex` from Step 2; targeting values and `linkedin_premium` from config. Compare with `<S>/before/resolved.json` → equal.
- [ ] **Step 4: Parse-only greps.** `grep -E -h "typed, \S+ to send" <main-checkout>/postings/*/outreach.md` and `grep -E -h "Questions for .+" <main-checkout>/postings/*/changelog.md`; each output equals its Task 1 file. Confirm the patterns are the ones `followup/SKILL.md`, `outreach/SKILL.md` (`typed, <word> to send`) and `batch/SKILL.md` (`Questions for <…>`) name.
- [ ] **Step 5: Triggers.** For each `.claude/skills/*/SKILL.md`, compare `git show main:<file>` with the working file: every double-quoted phrase and `/command` in the old `description` that does not contain a `.personal-terms` term is still in the new one (a short Python script). Expected: no missing phrase.
- [ ] **Step 6: CI (criteria 1 and 3, CI half).** Push the branch and open the PR (under `/ship` this is its PR step; otherwise `gh pr create`). Run: `gh pr checks --watch` → `check-tools` passes. Then read the `check-tools` log (`gh run view --log` for that run). Expected: `py_compile` succeeded; the unittest run ends `OK` (skips allowed); `test_tracked_files_have_no_personal_terms ... skipped` and the other `test_no_personal_data` tests `ok`. Keep the run link and those log lines.
- [ ] **Step 6b: Evidence.** Put the results of Steps 1-5, Task 9 Step 4 (both local runs) and Step 6 (CI run link and log lines) in the PR body as a table (criterion → evidence).
- [ ] **Step 7: After merge, migrate `<main-checkout>`.** Once `main` is pulled in `<main-checkout>`: confirm `sources.json` is gone there (the pull deletes the formerly tracked file); copy `<worktree>/config.local.json` and `<worktree>/.personal-terms` into `<main-checkout>` before the worktree is removed. Run: `python -m unittest tests.test_no_personal_data -v` in `<main-checkout>` → pass with the terms test not skipped; `git status --short` there shows neither file.
- [ ] **Step 8: Maintainer sign-off (criterion 2, last part).** Ask the maintainer to run `/resume` on a posting that already has a pre-change resume and compare the two PDFs side by side; record their answer in the handoff / PR comment. This is the maintainer's step; nothing else waits on it.
