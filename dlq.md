# Dead-letter queue

Postings that couldn't be processed. Only the `batch` orchestrator (or a single `/resume`, `/apply`,
`/outreach` run in the main session) writes here, one row per posting; update the row in place
rather than adding a duplicate.

- **Reason**: `CLOSED` (404, "no longer available", expired), `UNREADABLE` (page or API returned no
  posting body), `FAILED` (resume build or form fill failed twice), `BLOCKED` (needs an account
  login/sign-up, CAPTCHA before the form, unsupported site), `INELIGIBLE` (posting excludes Canada
  or Quebec), `SKIPPED` (Aly chose to skip it at confirmation or review).
- **Needs**: what would unblock it (e.g. "Aly creates Workday account", "re-check next week").
- **Status**: `open` → `retried` (put back through a run) → `resolved` / `dropped`.

`read_postings.py` skips URLs with an `open` row here (and any `CLOSED`/`INELIGIBLE`/`dropped`
row) unless `--all` is given. Retry open entries with `/batch <mode> dlq.md` (add `--reason BLOCKED`
to retry only one kind).

| Date | Batch | Rank | Company | Title | URL | Stage | Reason | Detail | Needs | Status |
|------|-------|------|---------|-------|-----|-------|--------|--------|-------|--------|
| 2026-10-02 | 2026-10-02-0004-apply | 13 | US Mobile | AI/ML Engineer | https://jobs.lever.co/USMobile/7800a658-f3a0-4e5f-a023-4dcf23a6b449 | resume | CLOSED | Lever page 404 and API "Document not found"; the USMobile board (41 postings) has no AI/ML role | nothing, closed | open |
| 2026-10-02 | 2026-10-02-0004-apply | 18 | Dialpad | AI Engineer, Agentic Voice (TTS) | https://job-boards.greenhouse.io/dialpad/jobs/8597852002 | resume | CLOSED | Greenhouse API 404 "Job not found"; the URL redirects to the board with ?error=true; the role is not among the 60 live jobs | nothing, closed | open |
| 2026-10-02 | 2026-10-02-0004-apply | 20 | Autodesk | Software Developer, MCP/AI | https://autodesk.wd1.myworkdayjobs.com/en-US/Ext/job/Software-Developer--MCP-AI_26WD99364-1 | resume | CLOSED | Workday API 403 S22 for 26WD99364-1 while a sibling posting serves fine; not found by board search | nothing, closed (sibling: Software Development Manager, MCP/AI 26WD98804-1) | open |
| 2026-10-02 | 2026-10-02-0004-apply | 16 | EY Canada | AI and Data - Senior Consultant - AI/ML Engineer | https://careers.ey.com/ey/job/Montr%C3%A9al-AI-and-Data-Senior-Consultant-AIML-Engineer-Queb-H3A-0A8/1168571801/ | prepare | BLOCKED | Not signed in to careers.ey.com; Apply Now (/talentcommunity/apply/1168571801/) redirects to the home page; posting live, requires FR/EN bilingualism; resume built at postings/EY-1168571801 | Aly signs in to or creates an EY candidate account in Chrome (or OKs apply-with-LinkedIn), then /batch apply dlq.md --reason BLOCKED | open |
| 2026-10-02 | 2026-10-02-0004-apply | 15 | Google DeepMind | Research Developer, Frontier AI Incubation | https://www.google.com/about/careers/applications/jobs/results/115400405273191110-research-developer-frontier-ai-incubation-deepmind | review | SKIPPED | Aly skipped at review; resume built at postings/GoogleDeepMind-115400405273191110 | nothing | open |
| 2026-10-02 | 2026-10-02-0004-apply | 19 | Xsolla | Full Stack AI Engineer / Applied AI Engineer | https://jobs.lever.co/xsolla/ebb74747-c739-4247-bafc-a088c10fa643 | review | SKIPPED | Aly skipped at review (posting pays $50-70k USD, 1-3 yrs) | nothing | open |
| 2026-10-04 | 2026-10-04-1253-outreach | 10 | Affinity | AI Engineer, AI Platform | https://job-boards.greenhouse.io/affinity/jobs/7632052003 | prescreen | CLOSED | HTTP 404 on Greenhouse API and web page | nothing, closed | open |
| 2026-10-04 | 2026-10-04-1253-outreach | 14 | Level Access | AI Engineer | https://job-boards.greenhouse.io/levelaccess/jobs/8247559002 | prescreen | CLOSED | Job 8247559002 not on Level Access board (8 open roles, no AI Engineer) | nothing, closed | open |
| 2026-10-04 | 2026-10-04-1253-outreach | 27 | Mercury | Senior Software Engineer - AI Engineering | https://job-boards.greenhouse.io/mercury/jobs/5850044004 | prescreen | CLOSED | HTTP 404 on Greenhouse API boards/mercury/jobs/5850044004 | nothing, closed | open |
