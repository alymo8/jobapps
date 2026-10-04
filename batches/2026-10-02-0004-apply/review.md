# Review: batch 2026-10-02-0004-apply (target list rows 13-20)

**Reply format** (one line; nothing is submitted without it):

```
answers: auth=yes, sponsor=no, salary=<CAD>, loom=<url>, portfolio=<url|none>, eeo=decline, referral=no, gfiles=<swap|keep>, gcover=<remove|keep|draft> | approve: all | except: 7 | edit 5: <text>
```

Ready for approval: **#2 Spellbook, #3 DeepMind, #5 Durable, #7 Xsolla** (forms filled in their own Chrome tabs, not submitted).
Dead-lettered: #1 US Mobile, #6 Dialpad, #8 Autodesk (closed), #4 EY (blocked, account).

## 1. Questions (deduplicated)

| Key | Question | Asked by |
|-----|----------|----------|
| `auth` | Legally entitled to work in Canada? (Spellbook: yes / no / no, but permit in process; Spellbook offers no sponsorship) | #2 (required), #3 (required); #5 requires Canada-based |
| `sponsor` | Need work-authorization sponsorship now or in the future? | #3 (required) |
| `salary` | Salary expectation (CAD)? Posting: $180k-$225k CAD base + equity | #5 (required) |
| `loom` | Loom video link (2-3 min, unscripted: who you are, what you're building, how AI is core to how you work) | #5 (required) |
| `portfolio` | Portfolio / website URL, or none | #7 (optional); #5 work-sample uses Safi (draft) |
| `eeo` | Gender, race, veteran status, age range (all voluntary); "decline" is fine | #7 |
| `referral` | Referred by a Spellbook employee? | #2 (optional) |
| `gfiles` | Replace the Google Careers **profile** resume (old Google Cloud PDF) with the DeepMind PDF? Edits the shared profile | #3 |
| `gcover` | Profile cover letter is addressed to the Google Cloud FDE role: remove / keep / draft a DeepMind one | #3 |

Reusable answers (`auth`, `sponsor`, `portfolio`, `eeo`) will be saved to `profile.md`.

## 2. Per posting

### #2 Spellbook: Forward Deployed Engineer (Remote, Canada; CA$170-213K + equity)
- Resume: `postings/Spellbook-d92285f3/Aly_Mohamed_Hussein_Resume_Spellbook.pdf`, fill 0.969
- Gaps: no legal-tech/DMS (iManage, NetDocuments) or SSO; no tRPC (Express/Node only in skills); no SOC2 (closest: PDPL residency, audit logs, tenant isolation); ~3 yrs, bottom of their 3-7 range.
- Sanity-check: SWE bullet merges three bullets ("Led" Jenkins microservices 33%, Spring Boot on Fargate, Python Lambda for SQS).
- Sanity-check: Accenture bullet 1 says "enterprise client stakeholders" (source: "enterprise stakeholders").
- Sanity-check: summary "enterprise AI systems from ambiguous client requirements to production on AWS and Azure" is a synthesis.
- ASKs: `auth`, `referral`. Blockers: none.

### #3 Google DeepMind: Research Developer, Frontier AI Incubation (Montreal; $185-190k CAD + 15% bonus + equity)
- Resume: `postings/GoogleDeepMind-115400405273191110/Aly_Mohamed_Hussein_Resume_GoogleDeepMind.pdf`, fill 0.965 (not uploaded yet; depends on `gfiles`)
- Gaps: no foundation-model training/fine-tuning (RLHF, SFT, PEFT), the largest one; no large-scale training infra (TPU/JAX); no C++; no personalization/agentic memory/multimodal; no papers.
- Sanity-check: eval bullet appends "turning ambiguous stakeholder requirements into measurable success criteria" from another bullet.
- Sanity-check: summary "LLM agents, RAG, and evaluation frameworks from prototype to production in Python" is a synthesis.
- Sanity-check: Clinic Ops "four production LLM workflows ... live with a Cairo surgeon" merges two bullets.
- ASKs: `auth`, `sponsor`, `gfiles`, `gcover`. Note: Google caps applications at **3 per 30 days**.
- Blockers: none (Chrome signed in to the existing Careers profile; self-ID already complete).

### #5 Durable: AI Engineer (Remote Canada, quarterly Vancouver travel; $180-225k CAD + equity)
- Resume: `postings/Durable-5156304008/Aly_Mohamed_Hussein_Resume_Durable.pdf` (built 2026-10-01, uploaded)
- Gaps: frontend depth (no design systems, motion, TanStack Query, tRPC); not their stack (Cloudflare Workers, LangSmith, Inngest, Drizzle); no high-traffic product scale.
- Sanity-check: SWE bullet merges two microservices bullets under "Led".
- Sanity-check: AI Engineer title line adds React and TypeScript.
- Sanity-check: summary "full-stack LLM products in TypeScript, Next.js, and Python" is a synthesis.
- Draft, work sample link: `https://alymo8.github.io/safi-ai/` (alternative: `https://github.com/alymo8/claude-kit`)
- Draft, "Why Durable?":

  > I build AI products end to end in TypeScript and Next.js, and the part I care most about is the one
  > Durable describes: keeping a system reliable when the model is unpredictable. On a clinic platform I
  > run solo for a paying client, every LLM output is a strict-schema draft with illegible fields flagged
  > rather than inferred, and on Safi, my LLM cost optimizer, I lift quality with evals rather than
  > guesswork (a revised judge took agreement from 77% to 96%). Durable is a product where AI does most of
  > the heavy lifting and the interface is where trust is won, and that is the kind of problem I want to
  > work on.

- ASKs: `loom`, `salary` (both required); Preferred First Name (optional, leave empty unless told).
- Blockers: none, but it **cannot be submitted without the Loom link**.

### #7 Xsolla: Full Stack AI Engineer / Applied AI Engineer (Montreal, onsite)
- Resume: `postings/Xsolla-ebb74747/Aly_Mohamed_Hussein_Resume_Xsolla.pdf`, fill 0.970 (uploaded)
- **Fit flag: posting asks 1-3 years and pays $50k-$70k USD.** Likely well below your level; confirm or `except: 7`.
- Gaps: no Tailwind/Shadcn, MCP, Hugging Face; vector DB only pgvector.
- Sanity-check: summary "full-stack GenAI products and agentic systems in Python, TypeScript, and Next.js" is a synthesis.
- Sanity-check: AI Engineer title line adds React and TypeScript.
- Sanity-check: billing bullet drops "engineering consulting client" and Azure ML/Containers.
- ASKs: `portfolio`, `eeo` (all optional). Blockers: none.

## 3. Dead-lettered in this run

| # | Company | Title | Reason | Needs |
|---|---------|-------|--------|-------|
| 1 | US Mobile | AI/ML Engineer | CLOSED (Lever 404; no AI/ML role on board) | nothing |
| 6 | Dialpad | AI Engineer, Agentic Voice (TTS) | CLOSED (Greenhouse "Job not found") | nothing |
| 8 | Autodesk | Software Developer, MCP/AI | CLOSED (Workday 403, not in board search) | nothing; sibling "Software Development Manager, MCP/AI" (26WD98804-1) is live |
| 4 | EY Canada | AI and Data - Senior Consultant - AI/ML Engineer | BLOCKED (needs EY candidate account; FR/EN bilingual required) | sign in / create EY account in Chrome, or OK "apply with LinkedIn"; resume built at `postings/EY-1168571801/` |
