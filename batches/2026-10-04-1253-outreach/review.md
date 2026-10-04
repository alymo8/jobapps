# Review: outreach batch 2026-10-04 (ranks 3-40)

## How to reply

One line, any order, e.g.:

```
answers: salary=150k CAD, us_auth=No, sponsorship_us=Yes, eeo=decline, accommodations=No, start=4 weeks | approve: all | except: 14 | edit 13: <text> | outreach 5: crystal, lou, kelly | 20: skip | tr: wait | sb: wait
```
- `approve`: submit those applications (numbers = the `#` below). `outreach N: names` picks up to 3 people per posting; with no `outreach` line I send nothing on LinkedIn.
- Nothing is approved by silence. Answers marked reusable go to `profile.md`.

Batch: 24 postings in scope; **10 ready** below; 4 with LinkedIn drafts but no submittable application (section B2); 12 dead-lettered (section C); Cresta skipped (already applied 2026-10-02).

## A. Questions (deduplicated)

| Question | Asked by (#) |
|---|---|
| Salary / compensation expectation | 1, 12, 13, 19, 23 |
| US work authorization | 5 |
| Visa sponsorship (now or future) | 5, 14, 22 |
| EEO / voluntary self-identification (gender, race, veteran, disability) | 5, 14, 16 |
| Accommodations (AODA / interview) | 14, 19 |
| Years of experience | 1, 16 |
| Start date / availability | 1, 22 |
| Hybrid / in-person attendance | 13 |
| How did you hear about us | 13 |
| Background check consent | 22 |
| Employment restrictions / agreements | 16 |
| Loom / video | 12 |
| Ruby on Rails self-rating | 16 |
| Attestation | 13 |
| Preferred first name (Aly?) | 1, 12, 16, 19, 23 |

## B. Per posting (ready to submit after your answers)

### #1 (rank 3): Artefact, Senior AI & Agentic Engineer (8731948002)

- Resume: `postings/Artefact-8731948002/Aly_Mohamed_Hussein_Resume_Artefact.pdf`
- Fill: 0.963
- Form tab: https://job-boards.greenhouse.io/artefactnoram/jobs/8731948002 (filled, not submitted)
- **Gaps:**
  - Vector search / embeddings: only "RAG" (fraud agent) and pgvector in the mega skills list; no bullet on
    ingestion, chunking, embeddings or hybrid search.
  - No named agent SDK beyond LangGraph (no Google ADK, Claude Agent SDK, OpenAI Agents SDK); no Terraform
    (IaC is CloudFormation, CDK, Bicep); no LangSmith/promptfoo (Langfuse yes).
  - No warehouse/lakehouse experience; data pipeline evidence is the Kinesis/Flink stream.
  - No explicit mentoring, pre-sales or demo-building lines in the mega resume.
  - Years: about 3 years full time plus an internship, at the bottom of the 3-5 range.
- **Please sanity-check:**
  - Summary "shipping agentic systems, RAG, and LLM evaluations to production on Azure, GCP, and AWS" is a
    synthesis; the fraud RAG agent is not explicitly described as production in the mega resume.
  - Accenture bullet 4 merges three source bullets on the same summarization app (Llama FastAPI + Kinesis/
    Flink, Langfuse observability, LLM-as-a-judge eval).
  - SWE bullet merges the 33% Jenkins bullet with Fargate, Lambda and REST API bullets.
  - Cold-Chain bullet 2 shortens "check-then-insert race" to "a race".
- **ASK fields:** Preferred First Name (→ A: Preferred first name (Aly?)); Salary requirements (posting states no range) (→ A: Salary / compensation expectation); Years of relevant experience (→ A: Years of experience); Availability to start (textarea) (→ A: Start date / availability)

<details><summary>LinkedIn shortlist and drafts (verbatim)</summary>

| # | Name | Title | Location | Degree | Profile | Why |
|---|------|-------|----------|--------|---------|-----|
| 1 | Tom Consolin | Senior Manager, Consulting | AI Strategy @ Artefact | USA & Canada | Montreal, Quebec, Canada | 3rd+ | https://www.linkedin.com/in/tom-consolin-568ab6107/ | Closest to a North America hiring manager: leads AI consulting for USA & Canada, in Montreal. Verified from search headline |
| 2 | Ben Catchpole | Senior Manager Talent Acquisition at Artefact | United Kingdom | 3rd+ | https://www.linkedin.com/in/ben-catchpole/ | Senior TA leader at Artefact (global incl. US per his search blurb); only senior TA person found outside France. Verified from search blurb |
| 3 | Vasilis Christopoulos | Data and AI Consultant @ Artefact | Greater Montreal Metropolitan Area | 2nd | https://www.linkedin.com/in/vasilis-christopoulos-vc6/ | Montreal-based Artefact consultant (McGill MMA): peer / referral route; 7+ mutual connections. Verified from search headline |
| 4 | Pauline Chapelle | HR at Artefact (Talent Acquisition Specialist & HRBP, tech teams) | Paris, France | 2nd | https://www.linkedin.com/in/pauline-chapelle-75351214b/ | Recruits for Artefact tech teams since May 2025; Paris-based, may route to NA. Verified from search blurb |
| 5 | Gabriela Signeux Cucu | HRBP & Talent Acquisition at Artefact | Paris, France | 2nd | https://www.linkedin.com/in/gabriela-signeux-cucu-77414111b/ | Artefact TA/HRBP since 2022 (Greenhouse recruitment); Paris-based. Verified from search blurb |

No Montreal or North America recruiter surfaced (all recruiters found are in France, UK, Netherlands, Morocco). Maui Bar (Montreal engineering manager) did not show Artefact in his headline, so not shortlisted.
Not shortlisted (Artefact TA, other regions): Anouk Joubert, Rania Chouraqui, Chryzleine B., Luam Tesfamarian, Sofia Bennani, Anouar Lebbar, Clara Dolle Innocenti.

Suggested top 3: Tom Consolin, Vasilis Christopoulos, Ben Catchpole.

(a) = connection note, at most 300 characters including the posting link. (b) = follow-up after acceptance. Character counts in brackets.

#### 1. Tom Consolin (Senior Manager, Consulting | AI Strategy @ Artefact | USA & Canada, 3rd+)

(a) Connection note [251]:
> Hi Tom, I applied to Artefact's Senior AI & Agentic Engineer role (Montreal). AI engineer at Accenture, 3 yrs shipping production LLM/agent systems, M.Sc. ML McGill/MILA. Happy to connect. https://job-boards.greenhouse.io/artefactnoram/jobs/8731948002

(b) Follow-up [684]:
> Hi Tom,
>
> Thanks for connecting. I applied to Artefact's Senior AI & Agentic Engineer role in Montreal (https://job-boards.greenhouse.io/artefactnoram/jobs/8731948002). I'm an AI engineer at Accenture with 3 years taking production LLM systems from client goals to deployment, and I hold an M.Sc. in Machine Learning from McGill (MILA). I built a LangGraph fraud agent with RAG and a router agent running parallel subagents, an MCP server, and a Langfuse evaluation framework, with React/TypeScript and FastAPI on the full stack, and I'm a Claude Certified Architect. Could you tell me who is hiring for this role, or forward my application to the team?
>
> Thank you,
> Aly Mohamed Hussein

#### 2. Ben Catchpole (Senior Manager Talent Acquisition at Artefact, 3rd+)

(a) Connection note [251]:
> Hi Ben, I applied to Artefact's Senior AI & Agentic Engineer role (Montreal). AI engineer at Accenture, 3 yrs shipping production LLM/agent systems, M.Sc. ML McGill/MILA. Happy to connect. https://job-boards.greenhouse.io/artefactnoram/jobs/8731948002

(b) Follow-up [659]:
> Hi Ben,
>
> Thanks for connecting. I applied to Artefact's Senior AI & Agentic Engineer role in Montreal (https://job-boards.greenhouse.io/artefactnoram/jobs/8731948002). I'm an AI engineer at Accenture with 3 years taking production LLM systems from client goals to deployment, and I hold an M.Sc. in Machine Learning from McGill (MILA). I own agentic and RAG systems end to end (React/TypeScript front end, FastAPI services, Langfuse evaluation, an MCP server), shipped for paying clients, and I'm a Claude Certified Architect. Could you tell me whether you cover this role for North America, or point me to the right recruiter?
>
> Thank you,
> Aly Mohamed Hussein

#### 3. Vasilis Christopoulos (Data and AI Consultant @ Artefact, 2nd)

(a) Connection note [255]:
> Hi Vasilis, I applied to Artefact's Senior AI & Agentic Engineer role (Montreal). AI engineer at Accenture, 3 yrs shipping production LLM/agent systems, M.Sc. ML McGill/MILA. Happy to connect. https://job-boards.greenhouse.io/artefactnoram/jobs/8731948002

(b) Follow-up [688]:
> Hi Vasilis,
>
> Thanks for connecting. I applied to Artefact's Senior AI & Agentic Engineer role in Montreal (https://job-boards.greenhouse.io/artefactnoram/jobs/8731948002). I'm an AI engineer at Accenture with 3 years taking production LLM systems from client goals to deployment, and I hold an M.Sc. in Machine Learning from McGill (MILA). I built a LangGraph fraud agent with RAG and a router agent running parallel subagents, an MCP server, and a Langfuse evaluation framework, with React/TypeScript and FastAPI on the full stack, and I'm a Claude Certified Architect. Could you tell me who is hiring for this role, or forward my application to the team?
>
> Thank you,
> Aly Mohamed Hussein

#### 4. Pauline Chapelle (HR at Artefact (Talent Acquisition Specialist & HRBP, tech teams), 2nd)

(a) Connection note [255]:
> Hi Pauline, I applied to Artefact's Senior AI & Agentic Engineer role (Montreal). AI engineer at Accenture, 3 yrs shipping production LLM/agent systems, M.Sc. ML McGill/MILA. Happy to connect. https://job-boards.greenhouse.io/artefactnoram/jobs/8731948002

(b) Follow-up [663]:
> Hi Pauline,
>
> Thanks for connecting. I applied to Artefact's Senior AI & Agentic Engineer role in Montreal (https://job-boards.greenhouse.io/artefactnoram/jobs/8731948002). I'm an AI engineer at Accenture with 3 years taking production LLM systems from client goals to deployment, and I hold an M.Sc. in Machine Learning from McGill (MILA). I own agentic and RAG systems end to end (React/TypeScript front end, FastAPI services, Langfuse evaluation, an MCP server), shipped for paying clients, and I'm a Claude Certified Architect. Could you tell me whether you cover this role for North America, or point me to the right recruiter?
>
> Thank you,
> Aly Mohamed Hussein

#### 5. Gabriela Signeux Cucu (HRBP & Talent Acquisition at Artefact, 2nd)

(a) Connection note [256]:
> Hi Gabriela, I applied to Artefact's Senior AI & Agentic Engineer role (Montreal). AI engineer at Accenture, 3 yrs shipping production LLM/agent systems, M.Sc. ML McGill/MILA. Happy to connect. https://job-boards.greenhouse.io/artefactnoram/jobs/8731948002

(b) Follow-up [664]:
> Hi Gabriela,
>
> Thanks for connecting. I applied to Artefact's Senior AI & Agentic Engineer role in Montreal (https://job-boards.greenhouse.io/artefactnoram/jobs/8731948002). I'm an AI engineer at Accenture with 3 years taking production LLM systems from client goals to deployment, and I hold an M.Sc. in Machine Learning from McGill (MILA). I own agentic and RAG systems end to end (React/TypeScript front end, FastAPI services, Langfuse evaluation, an MCP server), shipped for paying clients, and I'm a Claude Certified Architect. Could you tell me whether you cover this role for North America, or point me to the right recruiter?
>
> Thank you,
> Aly Mohamed Hussein

</details>


### #5 (rank 9): Baseten, Forward Deployed Engineer

- Resume: `postings/Baseten-84c1801c/Aly_Mohamed_Hussein_Resume_Baseten.pdf`
- Fill: 0.962
- Form tab: https://jobs.ashbyhq.com/baseten/84c1801c-1a65-49fb-aaaa-beeafd530e7e/application (filled, not submitted)
- **Gaps:**
  - No model-serving / inference-optimization work (GPU serving, TensorRT, vLLM, latency tuning of
    model servers), which is Baseten's core; the closest is LLM cost optimization (Safi) and
    autoscaling of production workloads at Accenture.
  - No model training or fine-tuning in production; ML-lifecycle familiarity is M.Sc. coursework/research.
  - No formal pre-sales / solution engineering experience; client-facing work is stakeholder
    requirements at Accenture and the two paying-client projects.
- **Please sanity-check:**
  - Summary "taking production LLM systems in Python from ambiguous client goals through evaluation,
    deployment, and monitoring" is a synthesis of the Accenture bullets, not a mega-resume line.
  - Safi: "written solo" compresses the source's "wrote essentially all of it solo".
  - Accenture bullet 1 says "client stakeholders"; source says "enterprise stakeholders" on the client
    billing engagement.
  - PyTorch stays in skills without a bullet behind it on this page (Research section dropped).
- **ASK fields:** Unrestricted US work authorization? (Yes/No) (→ A: US work authorization); Require visa sponsorship now or future? (Yes/No) (→ A: Visa sponsorship (now or future)); EEO block (gender, race, veteran, disability; voluntary) (→ A: EEO / voluntary self-identification (gender, race, veteran, disability))

<details><summary>LinkedIn shortlist and drafts (verbatim)</summary>

| # | Name | Title | Location | Degree | Profile | Why |
|---|------|-------|----------|--------|---------|-----|
| 1 | Crystal Warmington-North | Tech Talent Leader (Baseten) | Greater Seattle Area | 2nd | https://www.linkedin.com/in/cwarmingtonnorth/ | Leads tech talent; current Baseten role verified on her profile. Her profile shows a connection request already 'Pending' (not sent by this run) |
| 2 | Lou Zumpano | Talent (Baseten) | San Jose, California | 1st | https://www.linkedin.com/in/louzumpano/ | Talent at Baseten, already 1st degree: regular message with resume attached; verified from search headline |
| 3 | Kelly Hall (Butler) | Talent (Baseten) | Greater Seattle Area | 1st | https://www.linkedin.com/in/kellyebutler/ | Talent at Baseten, already 1st degree; verified from search headline |
| 4 | Julia Cozzette | Talent (Baseten) | New York City Metropolitan Area | 2nd | https://www.linkedin.com/in/julia-cozzette-691777106/ | Talent recruiter (New York is a listed location); verified from search headline |
| 5 | Daniel Sarfati | Forward Deployed Engineering (Baseten) | Sandy, Utah | 2nd | https://www.linkedin.com/in/sarfati/ | FDE teammate: peer / referral route; verified from search headline |

No Canada-based Baseten recruiter surfaced, and no clearly identified FDE hiring manager (searches for FDE manager and head of FDE returned
only FDEs and non-FDE leads). Not shortlisted: Megan Cardiff, Corina Fitzgerald Wagle, Grace Schaefer, Olivia Jamison (all SF-based recruiting/sourcing),
Colin McGrath (Head of Infrastructure), Dhruv Singal (FDE; profile says no headhunters).

Suggested top 3: Lou Zumpano, Kelly Hall (both 1st degree, resume can be attached), Crystal Warmington-North.

(a) = connection note, at most 300 characters including the posting link. (b) = message / follow-up. Character counts in brackets.

#### 1. Crystal Warmington-North (Tech Talent Leader (Baseten), 2nd)

(a) Connection note [277]:
> Hi Crystal, I applied to Baseten's Forward Deployed Engineer role (Montreal/Toronto eligible). AI engineer at Accenture, 3 yrs taking production LLM systems from client goals to deployment. Happy to connect. https://jobs.ashbyhq.com/baseten/84c1801c-1a65-49fb-aaaa-beeafd530e7e

(b) Follow-up [700]:
> Hi Crystal,
>
> Thanks for connecting. I applied to Baseten's Forward Deployed Engineer role (Montreal and Toronto are listed locations; I'm based in Montreal). I'm an AI engineer at Accenture with 3 years of experience taking production LLM systems in Python from ambiguous client goals through evaluation, deployment and monitoring, and I hold an M.Sc. in Machine Learning from McGill (MILA). I owned an agentic system's Azure production deployment for a client, built a Langfuse evaluation framework, and shipped two revenue-generating systems solo. Could you tell me whether you cover this role, or forward my application to the hiring team? Happy to share my resume.
>
> Thank you,
> Aly Mohamed Hussein

#### 2. Lou Zumpano (Talent (Baseten), 1st)

(a) not needed (already 1st degree).

(b) Message [709]:
> Hi Lou,
>
> I applied to Baseten's Forward Deployed Engineer role (Montreal and Toronto are listed locations; I'm in Montreal): https://jobs.ashbyhq.com/baseten/84c1801c-1a65-49fb-aaaa-beeafd530e7e
>
> I'm an AI engineer at Accenture with 3 years of experience taking production LLM systems in Python from ambiguous client goals through evaluation, deployment and monitoring, and I hold an M.Sc. in Machine Learning from McGill (MILA). I owned an agentic system's production deployment on Azure, built a Langfuse evaluation framework, and shipped two revenue-generating systems solo. Could you tell me whether you cover this role, or point me to the right recruiter? Resume attached.
>
> Thank you,
> Aly Mohamed Hussein

#### 3. Kelly Hall (Butler) (Talent (Baseten), 1st)

(a) not needed (already 1st degree).

(b) Message [688]:
> Hi Kelly,
>
> I applied to Baseten's Forward Deployed Engineer role (Montreal and Toronto are listed locations; I'm in Montreal): https://jobs.ashbyhq.com/baseten/84c1801c-1a65-49fb-aaaa-beeafd530e7e
>
> I'm an AI engineer at Accenture with 3 years of experience in production LLM systems in Python, from ambiguous client requirements through evaluation, deployment and monitoring, with an M.Sc. in Machine Learning from McGill (MILA). I built a Langfuse evaluation framework for an agentic system and owned its Azure deployment. If you cover this role, I'd appreciate any update on next steps; if not, could you point me to the right recruiter? Resume attached.
>
> Thank you,
> Aly Mohamed Hussein

#### 4. Julia Cozzette (Talent (Baseten), 2nd)

(a) Connection note [275]:
> Hi Julia, I applied to Baseten's Forward Deployed Engineer role (Montreal/Toronto eligible). AI engineer at Accenture, 3 yrs taking production LLM systems from client goals to deployment. Happy to connect. https://jobs.ashbyhq.com/baseten/84c1801c-1a65-49fb-aaaa-beeafd530e7e

(b) Follow-up [627]:
> Hi Julia,
>
> Thanks for connecting. I applied to Baseten's Forward Deployed Engineer role (Montreal and Toronto are listed locations; I'm based in Montreal). I'm an AI engineer at Accenture with 3 years of experience in production LLM systems in Python, from ambiguous client goals through evaluation, deployment and monitoring, with an M.Sc. in Machine Learning from McGill (MILA). I owned an agentic system's Azure production deployment and built its Langfuse evaluation framework. Could you tell me whether you support this role, or point me to the recruiter who does? Happy to share my resume.
>
> Thank you,
> Aly Mohamed Hussein

#### 5. Daniel Sarfati (Forward Deployed Engineering (Baseten), 2nd)

(a) Connection note [292]:
> Hi Daniel, I applied to Baseten's Forward Deployed Engineer role. I'm an AI engineer at Accenture (Montreal) who takes production LLM systems from client goals to deployment. Would love to connect and hear about your work. https://jobs.ashbyhq.com/baseten/84c1801c-1a65-49fb-aaaa-beeafd530e7e

(b) Follow-up [623]:
> Hi Daniel,
>
> Thanks for connecting. I applied to Baseten's Forward Deployed Engineer role and wanted to reach out to someone on the team. I'm an AI engineer at Accenture in Montreal (3 years), working in Python: I partnered with client stakeholders to turn ambiguous requirements into success criteria, owned an agentic system's Azure deployment, and built its Langfuse evaluation and monitoring. I'd love to hear what FDE work looks like day to day and how the team works with customers. Would you have 15 minutes for a quick chat? Any pointer to the hiring team would also be much appreciated.
>
> Thanks,
> Aly Mohamed Hussein

</details>


### #6 (rank 11): 11x, Forward Deployed Engineer [REMOTE - Canada]

- Resume: `postings/11x-FDE-Canada/Aly_Mohamed_Hussein_Resume_11x.pdf`
- Fill: 0.964
- Form tab: https://jobs.gem.com/11x-ai/am9icG9zdDo7tWh-PewL-ku53L0cC2FB (filled, not submitted)
- **Gaps:**
  - Node.js appears only in Skills (no bullet behind it); no explicit Node.js backend work in the mega
    resume beyond Vodafone (cut by the age rule).
  - No production voice system: the voice work is a proof of concept (Gemini 2.5 Pro + text-to-speech).
  - No startup employment apart from Leagueware co-founding and the solo client work.
  - Years: about 3 years full time, right at their 3+ floor.
- **Please sanity-check:**
  - Summary: "building fullstack AI agent systems (TypeScript, React, Next.js, Python) from client
    requirements to live deployment; shipped two paid systems solo" is a synthesis; "paid" stands for
    the mega resume's "revenue-generating".
  - TTS bullet says "proof of concept of the support call"; the source says "of the call summarization
    process ... using Gemini 2.5 Pro as the support agent".
  - Accenture bullet 2 says the system was built "on Azure AI Foundry, Azure ML, and Azure Containers",
    as in the source; the stakeholder bullet keeps "enterprise stakeholders".

<details><summary>LinkedIn shortlist and drafts (verbatim)</summary>

| # | Name | Title | Location | Degree | Profile | Why |
|---|------|-------|----------|--------|---------|-----|
| 1 | Lily Chan | Talent @ 11x | San Francisco Bay Area | 3rd | https://www.linkedin.com/in/lilychan4/ | Only 11x recruiter surfaced; profile verified (11x, Talent) |
| 2 | Evan Timms | Member of Technical Staff @ 11x | Vancouver, BC, Canada | 2nd | https://www.linkedin.com/in/evanperretimms/ | Canada-based engineer at 11x: peer / referral route |
| 3 | Olivia Naidu | Engineering @11x | San Francisco, CA | 2nd | https://www.linkedin.com/in/olivia-naidu-230b01167/ | 11x engineer: peer / referral route |

No 11x engineering manager or Canada-based recruiter surfaced. Not shortlisted: Jack Gardner (ex-11x), Justin Swisher (title "Growing at 11x!", unclear role).
Suggested top 2: Lily Chan, Evan Timms.

(a) = connection note, at most 300 characters including the posting link. (b) = follow-up message. Character counts in brackets (approx.).

#### 1. Lily Chan (Talent @ 11x, 3rd)

(a) Connection note [~270]:
> Hi Lily, I applied to 11x's Forward Deployed Engineer (Canada remote) role. AI engineer at Accenture, 3 yrs building fullstack agent systems in TypeScript/React/Python. Happy to connect. https://jobs.gem.com/11x-ai/am9icG9zdDo7tWh-PewL-ku53L0cC2FB

(b) Follow-up [~690]:
> Hi Lily,
>
> Thanks for connecting. I applied to 11x's Forward Deployed Engineer role (remote, Canada; I'm based in Montreal). I'm an AI engineer at Accenture with 3 years of experience building fullstack AI agent systems in TypeScript, React and Python, and I hold an M.Sc. in Machine Learning from McGill (MILA). I owned an agentic system's production deployment on Azure with a React/TypeScript operator frontend, and I built a prototype that turns an LLM into a fully conversational voice support agent (Gemini plus text-to-speech). Could you tell me whether you cover this role, or forward my application to the hiring team? Happy to share my resume.
>
> Thank you,
> Aly Mohamed Hussein

#### 2. Evan Timms (Member of Technical Staff @ 11x, 2nd)

(a) Connection note [~285]:
> Hi Evan, I applied to 11x's Forward Deployed Engineer (Canada remote) role. I'm an AI engineer at Accenture (Montreal) building fullstack agent systems in TypeScript/React. Would love to connect and hear about your work. https://jobs.gem.com/11x-ai/am9icG9zdDo7tWh-PewL-ku53L0cC2FB

(b) Follow-up [~640]:
> Hi Evan,
>
> Thanks for connecting. I applied to 11x's Forward Deployed Engineer role and wanted to reach out to someone on the engineering team in Canada. I'm an AI engineer at Accenture in Montreal (3 years): I built a router-plus-subagents agentic system on Azure with a React/TypeScript frontend, owned its production deployment, and prototyped an LLM-powered conversational voice support agent. I'd love to hear what the work looks like day to day on the voice team. Would you have 15 minutes for a quick chat? Any pointer to the hiring team would also be much appreciated.
>
> Thanks,
> Aly Mohamed Hussein

#### 3. Olivia Naidu (Engineering @11x, 2nd)

(a) Connection note [~280]:
> Hi Olivia, I applied to 11x's Forward Deployed Engineer (Canada remote) role. I'm an AI engineer at Accenture (Montreal) taking agentic systems from client requirements to production. Would love to connect. https://jobs.gem.com/11x-ai/am9icG9zdDo7tWh-PewL-ku53L0cC2FB

(b) Follow-up [~600]:
> Hi Olivia,
>
> Thanks for connecting. I applied to 11x's Forward Deployed Engineer role. I'm an AI engineer at Accenture in Montreal with 3 years of experience building fullstack AI agent systems in TypeScript, React and Python, including an Azure production deployment and a Langfuse evaluation framework. I'd love to hear how engineers at 11x work with customers on live deployments. Would you have 15 minutes for a quick chat, or be able to point me to the hiring team?
>
> Thanks,
> Aly Mohamed Hussein

</details>


### #12 (rank 21): Durable, AI Engineer

- Resume: `postings/Durable-5156304008/Aly_Mohamed_Hussein_Resume_Durable.pdf`
- Fill: 0.969
- Form tab: https://job-boards.greenhouse.io/durable/jobs/5156304008 (filled, not submitted)
- **Gaps:**
  - Frontend depth: no design systems, motion/animation, TanStack Query or tRPC in the mega resume.
    Apply on the **full-stack track**.
  - Their stack: no Cloudflare Workers/Durable Objects, LangSmith, Inngest or Drizzle experience.
    pgvector appears only in the skills list.
  - "Scaling under real load": the backend evidence is enterprise microservices and streaming, not
    high-traffic product scale.
  - The application **requires a Loom video** (2 to 3 min) and asks for salary expectations
    (posted range: $180k to $225k CAD base + equity).
- **Please sanity-check:**
  - SWE bullet merges two mega-resume bullets: "Led development of synchronous and asynchronous
    microservices ... 33% ... and ~15 min per run". The source says "Led" for the pipeline-integration
    microservices and lists the sync/async ones separately.
  - AI Engineer title line adds React and TypeScript (taken from the billing bullet's operator frontend).
  - Summary: "full-stack LLM products in TypeScript, Next.js, and Python" is a synthesis of the client
    projects and Accenture work, not a mega-resume line.
- **ASK fields:** Preferred First Name (→ A: Preferred first name (Aly?)); Loom link* (→ A: Loom / video); What is your salary expectation?* (→ A: Salary / compensation expectation); Loom link* (→ A: Loom / video)
- **Why Durable? (draft)** (verbatim):

  > I build AI products end to end in TypeScript and Next.js, and the part I care most about is the one
  > Durable describes: keeping a system reliable when the model is unpredictable. On a clinic platform I
  > run solo for a paying client, every LLM output is a strict-schema draft with illegible fields flagged
  > rather than inferred, and on Safi, my LLM cost optimizer, I lift quality with evals rather than
  > guesswork (a revised judge took agreement from 77% to 96%). Durable is a product where AI does most of
  > the heavy lifting and the interface is where trust is won, and that is the kind of problem I want to
  > work on.
- **Draft answers in the form:**
  Link to work sample, portfolio, or demo | https://alymo8.github.io/safi-ai/ | mega_resume, **draft** (posting wants one strong example; alternative: https://github.com/alymo8/claude-kit)
  Why Durable?* | see below | posting + mega_resume, **draft**

<details><summary>LinkedIn shortlist and drafts (verbatim)</summary>

| # | Name | Title | Location | Degree | Profile | Why |
|---|------|-------|----------|--------|---------|-----|
| 1 | Mohammad Zeinalizadeh | Senior Product Manager @ Durable, AI | Vancouver | 2nd | https://www.linkedin.com/in/mozadeh/ | AI product lead at Durable; likely works closely with the AI engineering hiring team |
| 2 | Billy Lam | Senior AI Engineer at Durable | Greater Vancouver | 3rd+ | https://www.linkedin.com/in/billylam12/ | Peer on the AI engineering team: referral / team-insight route |
| 3 | James Clift | Founder at Durable.com | Canada | 2nd | https://www.linkedin.com/in/jclift/ | Founder; a short forward to the hiring team is plausible, lower odds of a reply |

No Durable recruiter / talent person surfaced, and no engineering manager was identified (searches: "Durable recruiter" returned only unrelated
companies such as Duravent/Duravant/Duratec; "Durable engineering manager website builder" returned nothing relevant).
Not shortlisted: Gavin Dove and Ara Ghougassian (Growth @ Durable, not hiring-related), Anfal Mushtaq (headline describes Durable-like work but
does not name the company; not verified), Peter Gassiraro (Durable Digital, a different company).

Suggested top 3: Mohammad Zeinalizadeh, Billy Lam, James Clift.

(a) = connection note, at most 300 characters including the posting link. (b) = follow-up message after acceptance. Character counts in brackets.

#### 1. Mohammad Zeinalizadeh (Senior Product Manager @ Durable, 2nd)

(a) Connection note [242]:
> Hi Mohammad, I applied to Durable's AI Engineer role (Vancouver). I build AI products in TypeScript/Next.js and ship LLM features with evals and strict-schema outputs. Happy to connect. https://job-boards.greenhouse.io/durable/jobs/5156304008

(b) Follow-up [647]:
> Hi Mohammad,
>
> Thanks for connecting. I applied to Durable's AI Engineer role in Vancouver (I'm based in Montreal, Canada). I build AI products end to end in TypeScript and Next.js: on a clinic platform I run solo for a paying client, every LLM output is a strict-schema draft with unclear fields flagged rather than inferred, and on Safi, my LLM cost optimizer, a revised judge took eval agreement from 77% to 96%. I'm an AI engineer at Accenture with 3 years of production LLM experience. Could you point me to whoever is hiring for this role, or share how the AI team works with product? Happy to share my resume.
>
> Thank you,
> Aly Mohamed Hussein

#### 2. Billy Lam (Senior AI Engineer at Durable, 3rd+)

(a) Connection note [235]:
> Hi Billy, I applied to Durable's AI Engineer role. I build full-stack AI products in TypeScript/Next.js with evals-driven quality. Would love to connect and hear about your work. https://job-boards.greenhouse.io/durable/jobs/5156304008

(b) Follow-up [604]:
> Hi Billy,
>
> Thanks for connecting. I applied to Durable's AI Engineer role. I build AI products end to end in TypeScript and Next.js and care most about keeping systems reliable when the model is unpredictable: strict-schema LLM outputs on a clinic platform I run solo for a client, and on Safi, my LLM cost optimizer, evals that took judge agreement from 77% to 96%. I'm an AI engineer at Accenture (3 years, Montreal). I'd love to hear what the AI engineering work looks like day to day. Would you have 15 minutes for a quick chat, or be able to point me to the hiring team?
>
> Thanks,
> Aly Mohamed Hussein

#### 3. James Clift (Founder at Durable.com, 2nd)

(a) Connection note [236]:
> Hi James, I applied to Durable's AI Engineer role. I build AI products end to end in TypeScript/Next.js and care about reliability when models are unpredictable. Happy to connect. https://job-boards.greenhouse.io/durable/jobs/5156304008

(b) Follow-up [569]:
> Hi James,
>
> Thanks for connecting. I applied to Durable's AI Engineer role in Vancouver (I'm in Montreal, Canada, and open to the quarterly Vancouver travel). I build AI products end to end in TypeScript and Next.js, and the part I care about most is reliability when the model is unpredictable: strict-schema LLM outputs on a clinic platform I run solo for a paying client, and evals on my LLM cost optimizer Safi that raised judge agreement from 77% to 96%. Could you forward my application to the hiring team? Happy to share my resume.
>
> Thank you,
> Aly Mohamed Hussein

</details>


### #13 (rank 25): Guidepoint AI Engineer (8635707002)

- Resume: `postings/Guidepoint-8635707002/Aly_Mohamed_Hussein_Resume_Guidepoint.pdf`
- Fill: 0.962
- Form tab: https://job-boards.greenhouse.io/guidepoint/jobs/8635707002 (filled, not submitted)
- **ASK fields:** How did you hear about this job? (optional) (→ A: How did you hear about us); Desired compensation? (required, free text) (→ A: Salary / compensation expectation); Comfortable with in-office/hybrid at Toronto office? (Yes/No, required) (→ A: Hybrid / in-person attendance); Attestation checkbox (true and complete information, reference checks; option Yes; required) (→ A: Attestation)

<details><summary>LinkedIn shortlist and drafts (verbatim)</summary>

| # | Name | Title | Location | Degree | Profile | Why |
|---|------|-------|----------|--------|---------|-----|
| 1 | Aniketh Pradhan | Senior Recruiter @ Guidepoint | Toronto, Ontario, Canada | 2nd | https://www.linkedin.com/in/anikethpradhan/ | Senior recruiter based in Toronto, where the role sits; headline lists AI and global hiring; verified from search headline |
| 2 | Megha Garg, CHRP, BSc | AI/ML Hiring | Technical Recruitment @ Guidepoint | Toronto, Ontario, Canada | 3rd+ | https://www.linkedin.com/in/meghagarg25/ | Headline says AI/ML hiring and technical recruitment at Guidepoint, Toronto; most likely the recruiter for this role; verified from search headline |
| 3 | Saarthak Sangamnerkar | AI Lead @ Guidepoint | Toronto, Ontario, Canada | 3rd+ | https://www.linkedin.com/in/saarthaksangam/ | AI Lead at Guidepoint in Toronto, likely on the hiring team for this role (hiring manager is not named in the posting); verified from search headline |
| 4 | Ying Zhou | AI Engineer @ Guidepoint | Toronto, Ontario, Canada | 2nd | https://www.linkedin.com/in/yzhouu/ | Current AI engineer at Guidepoint in Toronto (teammate: peer / referral route); 50+ mutual connections; verified from search headline |
| 5 | Krishna M. | Engineering Manager @ Guidepoint | New York, New York, United States | 3rd+ | https://www.linkedin.com/in/krishna-m-206546141/ | Engineering Manager at Guidepoint working on Databricks, OpenAI and LLM systems (same stack as the posting); New York based, so not confirmed as this team's manager; verified from search headline |

Not shortlisted: Dhara Rijhsinghani and Richard Ginsberg (New York engineering leaders, no Toronto tie), Constantine Baranau (Talent Acquisition, New York), Louis Luo (AI at Guidepoint, Toronto; junior peer), Jaspreet S. (Toronto engineering leader, headline does not name Guidepoint, so employer unverified).
No hiring manager is named in the posting; Saarthak (AI Lead, Toronto) is the best proxy.

Suggested top 3: Aniketh Pradhan, Megha Garg, Saarthak Sangamnerkar.

(a) = connection note, at most 300 characters including the posting link. (b) = follow-up message after acceptance. Character counts in brackets.

#### 1. Aniketh Pradhan (Senior Recruiter @ Guidepoint, 2nd)

(a) Connection note [240]:
> Hi Aniketh, I applied to Guidepoint's AI Engineer role (Toronto, hybrid). AI engineer at Accenture, 3 yrs shipping RAG and agentic systems to production on Azure. Happy to connect. https://job-boards.greenhouse.io/guidepoint/jobs/8635707002

(b) Follow-up [617]:
> Hi Aniketh,
>
> Thanks for connecting. I applied to Guidepoint's AI Engineer role on the Toronto AI team (https://job-boards.greenhouse.io/guidepoint/jobs/8635707002). I'm an AI engineer at Accenture with 3 years of experience shipping RAG pipelines, multi-agent systems (LangGraph) and LLM evals (LLM-as-a-judge, Langfuse) to production on Azure, and I hold an M.Sc. in Machine Learning from McGill (MILA). I also build FastAPI backend services for U.S. bank clients. Could you tell me whether you handle this role, or forward my application to the hiring team? Happy to share my resume.
>
> Thank you,
> Aly Mohamed Hussein

#### 2. Megha Garg, CHRP, BSc (AI/ML Hiring | Technical Recruitment @ Guidepoint, 3rd+)

(a) Connection note [250]:
> Hi Megha, I applied to Guidepoint's AI Engineer role (Toronto). AI engineer at Accenture, 3 yrs shipping RAG, LangGraph agents and LLM evals to production on Azure. Would be glad to connect. https://job-boards.greenhouse.io/guidepoint/jobs/8635707002

(b) Follow-up [674]:
> Hi Megha,
>
> Thanks for connecting. I applied to Guidepoint's AI Engineer role in Toronto (https://job-boards.greenhouse.io/guidepoint/jobs/8635707002). I'm an AI engineer at Accenture with 3 years of experience: I built an agentic system on Azure AI Foundry that automates a client's billing and owned its production deployment, designed a LangGraph fraud-detection agent with RAG for a U.S. bank (96% accuracy on 500 transactions), and delivered LLM-as-a-judge evals with Langfuse monitoring. M.Sc. in Machine Learning from McGill (MILA). Could you let me know if you cover this role, or point me to the right person? Happy to send my resume.
>
> Thank you,
> Aly Mohamed Hussein

#### 3. Saarthak Sangamnerkar (AI Lead @ Guidepoint, 3rd+)

(a) Connection note [247]:
> Hi Saarthak, I applied to Guidepoint's AI Engineer role in Toronto. AI engineer at Accenture (RAG, LangGraph agents, LLM evals on Azure). I'd value connecting and hearing about your team. https://job-boards.greenhouse.io/guidepoint/jobs/8635707002

(b) Follow-up [680]:
> Hi Saarthak,
>
> Thanks for connecting. I applied to Guidepoint's AI Engineer role in Toronto (https://job-boards.greenhouse.io/guidepoint/jobs/8635707002). I'm an AI engineer at Accenture with 3 years of experience. Most relevant to your stack: a multi-agent billing system on Azure AI Foundry that I took to production, a LangGraph plan-and-execute agent with RAG over customer and transaction history (96% accuracy on 500 transactions), and LLM-as-a-judge evals with Langfuse tracing and monitoring. I'd love to hear how your team approaches RAG quality and LLMOps. Would you have 15 minutes for a quick chat, or could you point me to the hiring team?
>
> Thanks,
> Aly Mohamed Hussein

#### 4. Ying Zhou (AI Engineer @ Guidepoint, 2nd)

(a) Connection note [252]:
> Hi Ying, I applied to Guidepoint's AI Engineer role in Toronto. I'm an AI engineer at Accenture building production multi-agent and RAG systems. Would love to connect and hear about your work. https://job-boards.greenhouse.io/guidepoint/jobs/8635707002

(b) Follow-up [648]:
> Hi Ying,
>
> Thanks for connecting. I applied to Guidepoint's AI Engineer role in Toronto (https://job-boards.greenhouse.io/guidepoint/jobs/8635707002) and wanted to hear from someone on the team. I'm an AI engineer at Accenture (3 years) building production multi-agent and RAG systems in Python on Azure, with LangGraph agents, Langfuse evals and FastAPI services, plus an M.Sc. in Machine Learning from McGill (MILA). I'd love to learn what the work looks like day to day and how the team handles LLM evaluation. Would you have 15 minutes for a quick chat? Any pointer to the hiring team would also be much appreciated.
>
> Thanks,
> Aly Mohamed Hussein

#### 5. Krishna M. (Engineering Manager @ Guidepoint, 3rd+)

(a) Connection note [221]:
> Hi Krishna, I applied to Guidepoint's AI Engineer role (Toronto). AI engineer at Accenture shipping RAG, agents and LLM evals on Azure. Would be glad to connect. https://job-boards.greenhouse.io/guidepoint/jobs/8635707002

(b) Follow-up [584]:
> Hi Krishna,
>
> Thanks for connecting. I applied to Guidepoint's AI Engineer role on the Toronto AI team (https://job-boards.greenhouse.io/guidepoint/jobs/8635707002). Your work on LLM systems with Databricks and OpenAI is close to what I do: I'm an AI engineer at Accenture with 3 years of experience shipping RAG, LangGraph multi-agent systems and LLM-as-a-judge evals (Langfuse) to production on Azure, and I hold an M.Sc. in Machine Learning from McGill (MILA). Would you be open to a short chat, or to pointing me to the hiring manager for this role?
>
> Thank you,
> Aly Mohamed Hussein

</details>


### #14 (rank 26): Censys, Senior AI/LLM Engineer (SOC/TH team)

- Resume: `postings/Censys-8540995002/Aly_Mohamed_Hussein_Resume_Censys.pdf`
- Fill: 0.967
- Form tab: https://job-boards.greenhouse.io/censys/jobs/8540995002 (filled, not submitted)
- **Gaps:**
  - Posting asks for 5+ years of SWE experience including 2+ years on AI features. You have about 3 years full-time
    (since September 2023) plus the Ericsson internship, and about 1.75 years in the AI Engineer role.
  - RAGAS and LangSmith are not in the mega resume. Your eval experience is Langfuse plus custom LLM-as-a-judge.
  - No LLM fine-tuning, embedding-model, or vector-search work beyond RAG (pgvector appears only in the mega
    skills list).
  - No cybersecurity, SOC, or threat-intel domain experience. The closest are fraud detection for a bank and the
    clinical data-residency work.
  - No low-latency or in-browser model optimization.
- **ASK fields:** Sponsorship to work in the US now or in the future? (Yes/No, required) (→ A: Visa sponsorship (now or future)); Special accommodations during interview process? (free text, required) (→ A: Accommodations (AODA / interview)); Gender (voluntary) (→ A: EEO / voluntary self-identification (gender, race, veteran, disability)); Are you Hispanic/Latino? (voluntary) (→ A: EEO / voluntary self-identification (gender, race, veteran, disability)); Veteran Status (voluntary) (→ A: EEO / voluntary self-identification (gender, race, veteran, disability))
- **Draft answers in the form:**
  Example of an AI service taken to production (free text, required) | draft: Azure agentic billing-verification system (router agent + parallel subagents, owned production deployment, Langfuse evaluation framework), plus LangGraph fraud-detection RAG agent (96% on 500 transactions) and LLM-as-a-judge framework | draft (mega_resume / resume Accenture bullets)

<details><summary>LinkedIn shortlist and drafts (verbatim)</summary>

| # | Name | Title | Location | Degree | Profile | Why |
|---|------|-------|----------|--------|---------|-----|
| 1 | Melissa Kiriu | Sr. Manager, Talent Acquisition (Censys) | United States | 3rd+ | https://www.linkedin.com/in/melissa-kiriu-0b217b43/ | Leads talent acquisition; best route to whoever owns this req |
| 2 | Matt C. (Chiasson) | Senior Sourcing Recruiter (Censys) | San Jose, California | 3rd+ | https://www.linkedin.com/in/mattchiasson/ | Sourcing recruiter at Censys |
| 3 | Yana Tychynska | Recruiting (Censys) | San Francisco Bay Area | 3rd+ | https://www.linkedin.com/in/yanatychynska/ | Recruiter at Censys |
| 4 | Rohan Kanade | Senior AI/LLM Software Engineer (Censys) | Greater Montreal | 2nd (mutual: Jonathan Deguire) | https://www.linkedin.com/in/kanade/ | Same title family as this role and in Montreal: peer / referral route |
| 5 | Eirik Herskedal | Vice President of Engineering (Censys) | Nepean, Ontario, Canada | 3rd+ | https://www.linkedin.com/in/eirik-herskedal-016475/ | Canada-based engineering VP (senior; hiring-manager chain) |

No clearly identified SOC/TH AI hiring manager surfaced. Not shortlisted: Andrew Spacewalz (Engineering Manager, Michigan), Matthew Ellison (Engineering Leadership, Michigan), Kenny Massie (AI engineer, Detroit), Jasmine Burns (Chief People Officer), Marcy Stanley (People Ops).

Suggested top 3: Rohan Kanade, Melissa Kiriu, Eirik Herskedal.

(a) = connection note, at most 300 characters including the posting link. (b) = follow-up message. Character counts in brackets.

#### 1. Melissa Kiriu (Sr. Manager, Talent Acquisition, 3rd+)

(a) Connection note [252]:
> Hi Melissa, I applied to Censys' Senior AI/LLM Engineer role (remote, Canada). AI engineer at Accenture, 3 yrs building production LLM/RAG systems in Python with eval frameworks. Happy to connect. https://job-boards.greenhouse.io/censys/jobs/8540995002

(b) Follow-up:
> Hi Melissa,
>
> Thanks for connecting. I applied to Censys' Senior AI/LLM Engineer role on the SOC/TH team (remote, and I'm based in Montreal): https://job-boards.greenhouse.io/censys/jobs/8540995002
>
> I'm an AI engineer at Accenture with 3 years of experience building production LLM and RAG systems in Python. I built a LangGraph fraud-detection agent with RAG for a major U.S. bank, an LLM-as-a-judge framework that catches summary degradation early, and a Langfuse evaluation framework for an agentic system whose Azure production deployment I owned. I also hold an M.Sc. in Machine Learning from McGill (MILA). Could you tell me whether you cover this role, or point me to the right recruiter? Resume attached.
>
> Thank you,
> Aly Mohamed Hussein

#### 2. Matt C. (Senior Sourcing Recruiter, 3rd+)

(a) Connection note [249]:
> Hi Matt, I applied to Censys' Senior AI/LLM Engineer role (remote, Canada). AI engineer at Accenture, 3 yrs building production LLM/RAG systems in Python with eval frameworks. Happy to connect. https://job-boards.greenhouse.io/censys/jobs/8540995002

(b) Follow-up:
> Hi Matt,
>
> Thanks for connecting. I applied to Censys' Senior AI/LLM Engineer role (remote; I'm in Montreal): https://job-boards.greenhouse.io/censys/jobs/8540995002
>
> I'm an AI engineer at Accenture with 3 years of experience in production LLM and RAG systems in Python, including a LangGraph fraud-detection agent for a major U.S. bank and an LLM-as-a-judge framework for automated regression-style evaluation, with an M.Sc. in Machine Learning from McGill (MILA). If you source for this role, I'd appreciate any update on next steps; if not, could you point me to the right recruiter? Resume attached.
>
> Thank you,
> Aly Mohamed Hussein

#### 3. Yana Tychynska (Recruiting, 3rd+)

(a) Connection note [249]:
> Hi Yana, I applied to Censys' Senior AI/LLM Engineer role (remote, Canada). AI engineer at Accenture, 3 yrs building production LLM/RAG systems in Python with eval frameworks. Happy to connect. https://job-boards.greenhouse.io/censys/jobs/8540995002

(b) Follow-up:
> Hi Yana,
>
> Thanks for connecting. I applied to Censys' Senior AI/LLM Engineer role (remote; I'm based in Montreal): https://job-boards.greenhouse.io/censys/jobs/8540995002
>
> I'm an AI engineer at Accenture with 3 years of experience building production LLM and RAG systems in Python, with Langfuse tracing and evaluation, and an M.Sc. in Machine Learning from McGill (MILA). Could you tell me whether you recruit for this role, or point me to the recruiter who does? Happy to share my resume.
>
> Thank you,
> Aly Mohamed Hussein

#### 4. Rohan Kanade (Senior AI/LLM Software Engineer, 2nd)

(a) Connection note [251]:
> Hi Rohan, I applied to Censys' Senior AI/LLM Engineer role (SOC/TH team) and I'm also in Montreal. I build production LLM/RAG systems at Accenture. Would love to connect and hear about your work. https://job-boards.greenhouse.io/censys/jobs/8540995002

(b) Follow-up:
> Hi Rohan,
>
> Thanks for connecting. I applied to Censys' Senior AI/LLM Engineer role and wanted to reach out to someone on the team, especially someone in Montreal. I'm an AI engineer at Accenture (3 years), working in Python on RAG and agent systems: a LangGraph fraud-detection agent for a major U.S. bank, and an LLM-as-a-judge framework plus Langfuse evaluation for an agentic system I took to production on Azure. I'd love to hear what the team's AI work looks like day to day. Would you have 15 minutes for a quick chat? Any pointer to the hiring team would also be much appreciated.
>
> Thanks,
> Aly Mohamed Hussein

#### 5. Eirik Herskedal (Vice President of Engineering, 3rd+)

(a) Connection note [235]:
> Hi Eirik, I applied to Censys' Senior AI/LLM Engineer role (SOC/TH team, remote Canada). AI engineer at Accenture shipping production LLM/RAG systems with evals. Happy to connect. https://job-boards.greenhouse.io/censys/jobs/8540995002

(b) Follow-up:
> Hi Eirik,
>
> Thanks for connecting. I applied to Censys' Senior AI/LLM Engineer role on the SOC/TH team (remote, Canada): https://job-boards.greenhouse.io/censys/jobs/8540995002
>
> I'm an AI engineer at Accenture with 3 years of experience in production LLM and RAG systems in Python. I built a LangGraph fraud-detection agent with RAG for a major U.S. bank (96% accuracy across 500 transactions) and a Langfuse evaluation framework for an agentic system whose production deployment I owned. If it's useful, I'd be glad to share my resume or have a short chat about the team's AI roadmap.
>
> Thank you,
> Aly Mohamed Hussein

</details>


### #16 (rank 29): GitLab Backend Engineer, AI Engineering: Duo Chat (8698314002)

- Resume: `postings/GitLab-8698314002/Aly_Mohamed_Hussein_Resume_GitLab.pdf`
- Fill: 0.965
- Form tab: https://job-boards.greenhouse.io/gitlab/jobs/8698314002 (filled, not submitted)
- **ASK fields:** Preferred First Name (required) (→ A: Preferred first name (Aly?)); Over 3 years professional software engineering experience? (Yes/No) (→ A: Years of experience); Ruby on Rails 0-5 (→ A: Ruby on Rails self-rating); Subject to employment agreements / post-employment restrictions? (Yes/No) (→ A: Employment restrictions / agreements); EEO block (gender, Hispanic/Latino, veteran; voluntary) (→ A: EEO / voluntary self-identification (gender, race, veteran, disability))
- **Draft answers in the form:**
  Preferred First Name (required) | Aly | draft (profile has ASK; set to first name, Aly to confirm)
  Python 0-5 | 4 (advanced) | draft from mega_resume (Python is the core stack); Aly to confirm

<details><summary>LinkedIn shortlist and drafts (verbatim)</summary>

| # | Name | Title | Location | Degree | Profile | Why |
|---|------|-------|----------|--------|---------|-----|
| 1 | Jessica Lacey | Senior GTM/Professional Services/FDE Recruiter - GitLab | Lincoln, California, United States | 3rd+ | https://www.linkedin.com/in/jessica-lacey-1578072/ | GitLab recruiter with an AI/FDE focus; verified from search headline. Not Canada-based, so a referral route to the right recruiter |
| 2 | Joyce Wang, SHRM-CP | Senior Talent Partner (Via Talentful) at GitLab | United States | 2nd | https://www.linkedin.com/in/joyce-wx/ | Recruiter for GitLab (contract via Talentful); verified from search headline |
| 3 | Christopher Fraser | Engineering Manager @ GitLab | Toronto, Ontario, Canada | 3rd+ | https://www.linkedin.com/in/christopher-fraser-61920a27/ | Engineering Manager at GitLab in Canada; team not confirmed (may not be Duo Chat); verified from search headline |
| 4 | Annie Ying, PhD | Engineering Manager at GitLab | Vancouver, British Columbia, Canada | 3rd+ | https://www.linkedin.com/in/annieying/ | Engineering Manager at GitLab in Canada; team not confirmed; verified from search headline |
| 5 | Donald Cook | Engineering Leader @ GitLab, AI Clients (7 teams, 20+ engineers) | Los Angeles Metropolitan Area | 3rd+ | https://www.linkedin.com/in/donaldpcook/ | Leads AI engineering teams at GitLab (AI Clients), near the AI Engineering org that owns Duo Chat; verified from search headline |

No Canada-based GitLab recruiter surfaced (recruiters shown are US-based, two via Talentful). Not shortlisted: Albert Borja (Senior Technical Recruiter via Talentful, US; https://www.linkedin.com/in/albert-borja-16169840/),
Juan Silva (headline says he led Duo Chat but is open to EM roles, so likely no longer at GitLab), Mohamed Hamda (Acting EM, Custom Models, Berlin), Matthew Nohr (EM AI, Minneapolis), other EMs in Europe/China.
No individual was confirmed to be on the Chat Engine team.

Suggested top 3: Jessica Lacey, Joyce Wang, Christopher Fraser.

(a) = connection note, at most 300 characters including the posting link. (b) = follow-up message after acceptance. Character counts in brackets.

#### 1. Jessica Lacey (Senior GTM/Professional Services/FDE Recruiter - GitLab, 3rd+)

(a) Connection note [271]:
> Hi Jessica, I applied to GitLab's Duo Chat Backend Engineer role (Remote, Canada). I build Python LangGraph agents with LLM evals at Accenture and live in Montreal. Could you point me to the recruiter for this role? https://job-boards.greenhouse.io/gitlab/jobs/8698314002

(b) Follow-up [603]:
> Hi Jessica,
>
> Thanks for connecting. I applied to GitLab's Backend Engineer, AI Engineering: Duo Chat role (Remote, Canada; I'm in Montreal), and I'd like to make sure it reaches the right recruiter. I'm an AI engineer at Accenture with 3 years of experience in Python, building LangGraph agents (a router/subagent billing system and a plan-execute fraud agent with RAG), a FastAPI service, and LLM-as-a-judge evaluation with Langfuse tracing. I hold an M.Sc. in Machine Learning from McGill (MILA). Do you cover this role, or could you point me to the recruiter who does?
>
> Thank you,
> Aly Mohamed Hussein

#### 2. Joyce Wang, SHRM-CP (Senior Talent Partner (Via Talentful) at GitLab, 2nd)

(a) Connection note [269]:
> Hi Joyce, I applied to GitLab's Duo Chat Backend Engineer role (Remote, Canada). I build Python LangGraph agents with LLM evals at Accenture and live in Montreal. Could you point me to the recruiter for this role? https://job-boards.greenhouse.io/gitlab/jobs/8698314002

(b) Follow-up [577]:
> Hi Joyce,
>
> Thanks for connecting. I applied to GitLab's Backend Engineer, AI Engineering: Duo Chat role (Remote, Canada; I'm in Montreal). I'm an AI engineer at Accenture with 3 years of experience in Python, building LangGraph agents (a router/subagent billing system and a plan-execute fraud agent with RAG), a FastAPI service, and LLM-as-a-judge evaluation with Langfuse tracing, plus an M.Sc. in Machine Learning from McGill (MILA). Could you tell me whether you cover this role, or point me to the right recruiter? Happy to share my resume.
>
> Thank you,
> Aly Mohamed Hussein

#### 3. Christopher Fraser (Engineering Manager @ GitLab, 3rd+)

(a) Connection note [276]:
> Hi Christopher, I applied to GitLab's Duo Chat Backend Engineer role (Remote, Canada). I build Python LangGraph agents with LLM evals at Accenture and live in Montreal. Would love to connect and hear how your team works. https://job-boards.greenhouse.io/gitlab/jobs/8698314002

(b) Follow-up [585]:
> Hi Christopher,
>
> Thanks for connecting. I applied to GitLab's Backend Engineer, AI Engineering: Duo Chat role (Remote, Canada; I'm in Montreal) and wanted to reach out to an engineering manager. At Accenture I built Python LangGraph agents (a router/subagent billing system, a plan-execute fraud agent with RAG) and LLM-as-a-judge evals with Langfuse tracing, and in a personal project I built an MCP server with a 584-test CI suite. Would you have 15 minutes to share how your team works, or could you point me to the Chat Engine team's hiring manager?
>
> Thank you,
> Aly Mohamed Hussein

#### 4. Annie Ying, PhD (Engineering Manager at GitLab, 3rd+)

(a) Connection note [270]:
> Hi Annie, I applied to GitLab's Duo Chat Backend Engineer role (Remote, Canada). I build Python LangGraph agents with LLM evals at Accenture and live in Montreal. Would love to connect and hear how your team works. https://job-boards.greenhouse.io/gitlab/jobs/8698314002

(b) Follow-up [565]:
> Hi Annie,
>
> Thanks for connecting. I applied to GitLab's Backend Engineer, AI Engineering: Duo Chat role (Remote, Canada; I'm in Montreal) and wanted to reach out to an engineering manager. At Accenture I built Python LangGraph agents (a router/subagent billing system, a plan-execute fraud agent with RAG) and LLM-as-a-judge evals with Langfuse tracing, and I hold an M.Sc. in Machine Learning from McGill (MILA). Would you have 15 minutes to share how your team works, or could you point me to the Chat Engine team's hiring manager?
>
> Thank you,
> Aly Mohamed Hussein

#### 5. Donald Cook (Engineering Leader @ GitLab, AI Clients (7 teams, 20+ engineers), 3rd+)

(a) Connection note [252]:
> Hi Donald, I applied to GitLab's Duo Chat Backend Engineer role (Remote, Canada). I build Python LangGraph agents with LLM evals at Accenture and live in Montreal. Would value connecting with you. https://job-boards.greenhouse.io/gitlab/jobs/8698314002

(b) Follow-up [541]:
> Hi Donald,
>
> Thanks for connecting. I applied to GitLab's Backend Engineer, AI Engineering: Duo Chat role (Remote, Canada; I'm in Montreal). I'm an AI engineer at Accenture with 3 years of experience in Python, building LangGraph agents (a router/subagent billing system and a plan-execute fraud agent with RAG) and LLM-as-a-judge evaluation with Langfuse tracing. I'd appreciate a pointer to the right person on the Chat Engine team, or any advice on how the AI Engineering org hires. Thank you for your time.
>
> Thank you,
> Aly Mohamed Hussein

</details>


### #19 (rank 33): Knak, Senior Software Developer, AI Agents

- Resume: `postings/Knak-4732794005/Aly_Mohamed_Hussein_Resume_Knak.pdf`
- Fill: 0.965
- Form tab: https://job-boards.greenhouse.io/knak/jobs/4732794005 (filled, not submitted)
- **Gaps:**
  - 6+ years required: about 3 years full-time plus an internship.
  - No PHP/Laravel, no MySQL (PostgreSQL and DynamoDB instead), no LangSmith (Langfuse instead), no
    AWS Bedrock in the mega resume.
  - Node.js: listed in skills only; no Node.js bullet on this page (the only Node.js work is the cut
    Vodafone internship).
  - Mentoring / leading code reviews: nothing explicit in the mega resume beyond "led" microservices
    and the Leagueware back end.
- **Please sanity-check:**
  - Summary "building production LLM agents in Python and the evals that measure them" is a synthesis
    of the Accenture and project bullets, not a mega-resume line.
  - Clinic Ops bullet 1 merges the live-deployment, four-workflows and MCP-server bullets; bullet 2
    merges guardrails, failure taxonomy, smoke harness and the 584-test TDD line.
  - React stays in skills though its bullet detail (billing operator frontend) was trimmed.
- **ASK fields:** Preferred First Name (→ A: Preferred first name (Aly?)); What is your desired salary? (→ A: Salary / compensation expectation); AODA: would you require any accommodations if selected for an interview? (Yes/No) (→ A: Accommodations (AODA / interview))

<details><summary>LinkedIn shortlist and drafts (verbatim)</summary>

| # | Name | Title | Location | Degree | Profile | Why |
|---|------|-------|----------|--------|---------|-----|
| 1 | Zak Michalyshyn | Senior Talent Acquisition Lead (Knak) | Ottawa, Ontario | 2nd | https://www.linkedin.com/in/zakmichalyshyn/ | Only Knak recruiter surfaced; Canada-based; mutual connection Saifullah Elsayed |
| 2 | Joel Chretien | VP of Engineering (Knak) | Greater Sudbury, Ontario | 3rd+ | https://www.linkedin.com/in/jchretien/ | Head of engineering; ultimate owner of the AI agents team |
| 3 | Scott Broschell | Senior Engineering Manager (Knak) | Greater Ottawa | 3rd+ | https://www.linkedin.com/in/scottbroschell/ | Likely hiring manager level for a senior developer role |
| 4 | Calvin Smith | Engineering Manager (Knak) | Greater Toronto Area | 2nd | https://www.linkedin.com/in/calvinrosssmith/ | Engineering manager; 2nd degree with mutual connections (Marylou Cormier, Ibrahim Younas +1) |

Not shortlisted: Brady Riordan (headline "Engineering Team Lead | AI-Ready Platforms", Ottawa, 3rd+; Knak not named in search headline, unverified), Shyley Engstrom and James K Abell (team leads, 3rd+, not AI-specific). No AI-agents-specific manager was identifiable from headlines.

Suggested top 3: Zak Michalyshyn, Scott Broschell, Calvin Smith.

(a) = connection note, at most 300 characters including the posting link. (b) = follow-up message after acceptance. Character counts approximate.

#### 1. Zak Michalyshyn (Senior Talent Acquisition Lead (Knak), 2nd)

(a) Connection note [~285]:
> Hi Zak, I applied to Knak's Senior Software Developer, AI Agents role (Remote - Canada). AI engineer at Accenture, 3 yrs building production LLM agents in Python with evaluation in Langfuse. Happy to connect. https://job-boards.greenhouse.io/knak/jobs/4732794005

(b) Follow-up [~680]:
> Hi Zak,
>
> Thanks for connecting. I applied to Knak's Senior Software Developer, AI Agents role (Remote - Canada; I'm based in Montreal). I'm an AI engineer at Accenture with 3 years of experience building LLM agents in Python, including tool calling and orchestration, and I hold an M.Sc. in Machine Learning from McGill (MILA). I built a Langfuse evaluation and monitoring framework for an agentic system, owned its production deployment on Azure, and shipped two revenue-generating systems solo. Could you tell me where my application stands, or forward it to the hiring team? Happy to share my resume.
>
> Thank you,
> Aly Mohamed Hussein

#### 2. Joel Chretien (VP of Engineering (Knak), 3rd+)

(a) Connection note [~290]:
> Hi Joel, I applied to Knak's Senior Software Developer, AI Agents role. I'm an AI engineer at Accenture (Montreal) who builds production LLM agents in Python, with evals and tracing in Langfuse. Would love to connect. https://job-boards.greenhouse.io/knak/jobs/4732794005

(b) Follow-up [~640]:
> Hi Joel,
>
> Thanks for connecting. I applied to Knak's Senior Software Developer, AI Agents role. I'm an AI engineer at Accenture in Montreal (3 years, M.Sc. in Machine Learning from McGill/MILA). The closest match to what you describe is an agentic system I worked on: I partnered with client stakeholders to turn ambiguous requirements into success criteria, built its Langfuse evaluation and monitoring framework, and owned its Azure production deployment. I'd welcome 15 minutes to hear how the agent harness and evals are evolving at Knak, or a pointer to the right person on the team.
>
> Thanks,
> Aly Mohamed Hussein

#### 3. Scott Broschell (Senior Engineering Manager (Knak), 3rd+)

(a) Connection note [~280]:
> Hi Scott, I applied to Knak's Senior Software Developer, AI Agents role. AI engineer at Accenture (Montreal), 3 yrs shipping production LLM agents in Python with an evaluation framework in Langfuse. Would love to connect. https://job-boards.greenhouse.io/knak/jobs/4732794005

(b) Follow-up [~640]:
> Hi Scott,
>
> Thanks for connecting. I applied to Knak's Senior Software Developer, AI Agents role. I'm an AI engineer at Accenture (3 years) working in Python on LLM agents in production. For an agentic system I built the Langfuse evaluation and monitoring framework, so changes were measured instead of guessed at, and owned its Azure deployment. I also hold an M.Sc. in Machine Learning from McGill (MILA). If you are involved in hiring for this role, I'd appreciate any update on next steps, or a short chat about how the team approaches agent evals.
>
> Thanks,
> Aly Mohamed Hussein

#### 4. Calvin Smith (Engineering Manager (Knak), 2nd)

(a) Connection note [~285]:
> Hi Calvin, I applied to Knak's Senior Software Developer, AI Agents role. AI engineer at Accenture (Montreal), 3 yrs building production LLM agents in Python, with evals and monitoring in Langfuse. Happy to connect. https://job-boards.greenhouse.io/knak/jobs/4732794005

(b) Follow-up [~620]:
> Hi Calvin,
>
> Thanks for connecting. I applied to Knak's Senior Software Developer, AI Agents role. I'm an AI engineer at Accenture in Montreal with 3 years of experience in Python, building LLM-powered systems from ambiguous client requirements through evaluation, deployment and monitoring (Langfuse, Azure). I also hold an M.Sc. in Machine Learning from McGill (MILA). Would you have 15 minutes to share what the team looks for, or could you point me to the hiring team?
>
> Thanks,
> Aly Mohamed Hussein

</details>


### #22 (rank 38): Sardine, Forward Deployed AI Engineer

- Resume: `postings/Sardine-4ff32b5d/Aly_Mohamed_Hussein_Resume_Sardine.pdf`
- Fill: 0.968
- Form tab: https://jobs.ashbyhq.com/sardine/4ff32b5d-13c6-4024-826c-04ed2881d688/application (filled, not submitted)
- **Gaps:**
  - Posting asks for 5+ years in Data Science or Applied AI. You have about 3 years full-time (since Sept 2023),
    of which about 1.75 years are in the AI Engineer role, plus the M.Sc.
  - No model fine-tuning or training of custom models in the mega resume. Your agent work is prompt/orchestration,
    RAG, and evaluation.
  - No causal-impact measurement or experiment design (A/B testing) experience on record. The closest is the
    Langfuse benchmark against the manual process.
  - SQL is listed but no bullet shows complex SQL data manipulation; it is backed only by Postgres work in projects.
  - Fincrime domain experience is limited to the one fraud detection agent; no AML or compliance work.
- **ASK fields:** Will you now or in the future require sponsorship for employment visa status (Yes/No) (→ A: Visa sponsorship (now or future)); Available to attend an in-person interview if requested? (Yes/No) (→ A: Start date / availability); Background check consent (Yes/No) (→ A: Background check consent)
- **Draft answers in the form:**
  What excites you about the opportunity to join Sardine? (max 3 sentences) | draft: "Sardine's focus on deploying custom AI agents into real fraud and AML workflows is exactly the client-embedded, production-first work I do as an AI engineer at Accenture, where I took LLM agent systems from ambiguous client goals to Azure production with Langfuse evaluation. I am drawn to the emphasis on rigorous evaluation and measuring the causal impact of deployed agents. The chance to own solutions end to end for fintech clients at this scale is what excites me." | draft (mega_resume + posting)

<details><summary>LinkedIn shortlist and drafts (verbatim)</summary>

| # | Name | Title | Location | Degree | Profile | Why |
|---|------|-------|----------|--------|---------|-----|
| 1 | George Cave | Talent Lead - Tech (Sardine) | Victoria, BC, Canada | 2nd | https://www.linkedin.com/in/george-cave-77652a101/ | Tech recruiting lead, Canada-based; mutual connection Zach Peterson |
| 2 | Chandni Raja | Global Head of Talent and People (Sardine) | Toronto, ON, Canada | 3rd+ | https://www.linkedin.com/in/chandniraja/ | Heads talent globally, Canada-based; route to the right recruiter |
| 3 | Andrew Hennessy | Senior Recruiter (Sardine) | New York, NY, United States | 3rd+ | https://www.linkedin.com/in/andrewhennessy1/ | Senior recruiter at Sardine; US coverage of the remote US/Canada role |
| 4 | Zhiheng Yi | Tech Lead (Sardine) | Ottawa, ON, Canada | 2nd | https://www.linkedin.com/in/zhihengyi/ | Engineering lead in Canada; mutual connection Nurudeen Esivue; possible hiring-team contact |
| 5 | Kartik Agarwal | Enterprise Solutions Engineer (Sardine) | Canada | 2nd | https://www.linkedin.com/in/kartik-agarwal-97a2789b/ | Client-facing technical role close to forward deployed work: peer / referral route |

No FDE hiring manager surfaced by name. Not shortlisted: Lindsay Bogue (GTM/corporate recruiter), Angel O'Hara (Brazil), Saran Jha (Integrations, Vancouver), Nabil Khaja and Sherif Mostafa (software engineers), Kazuki Nishiura (CTO), Sebastian Glenn-Anderson (headline does not name Sardine).

Suggested top 3: George Cave, Chandni Raja, Zhiheng Yi.

(a) = connection note, at most 300 characters including the posting link. (b) = follow-up after acceptance.

#### 1. George Cave (Talent Lead - Tech, 2nd)

(a) Connection note:
> Hi George, I applied to Sardine's Forward Deployed AI Engineer role (Canada remote). AI engineer at Accenture, 3 yrs taking production LLM agents from client goals to deployment. Happy to connect. https://jobs.ashbyhq.com/sardine/4ff32b5d-13c6-4024-826c-04ed2881d688

(b) Follow-up:
> Hi George,
>
> Thanks for connecting. I applied to Sardine's Forward Deployed AI Engineer role (remote, Canada; I'm based in Montreal). I'm an AI engineer at Accenture with 3 years of experience taking production LLM agent systems in Python from ambiguous client goals through evaluation, deployment and monitoring, and I hold an M.Sc. in Machine Learning from McGill (MILA). I owned an agentic system's Azure production deployment for a client and built its Langfuse evaluation framework. Could you tell me whether you cover this role, or forward my application to the hiring team? Happy to share my resume.
>
> Thank you,
> Aly Mohamed Hussein

#### 2. Chandni Raja (Global Head of Talent and People, 3rd+)

(a) Connection note:
> Hi Chandni, I applied to Sardine's Forward Deployed AI Engineer role (Canada remote). AI engineer at Accenture (Montreal), 3 yrs shipping production LLM agents for clients, M.Sc. ML from McGill. Would love to connect. https://jobs.ashbyhq.com/sardine/4ff32b5d-13c6-4024-826c-04ed2881d688

(b) Follow-up:
> Hi Chandni,
>
> Thanks for connecting. I applied to Sardine's Forward Deployed AI Engineer role. I'm an AI engineer at Accenture in Montreal with 3 years in production LLM systems in Python, working directly with client stakeholders to turn ambiguous requirements into success criteria, then owning evaluation (Langfuse) and Azure deployment. The emphasis on evaluating the impact of deployed agents is what drew me to the role. If you could point me to the recruiter covering it, or pass my application to the hiring team, I'd be grateful. Happy to share my resume.
>
> Thank you,
> Aly Mohamed Hussein

#### 3. Andrew Hennessy (Senior Recruiter, 3rd+)

(a) Connection note:
> Hi Andrew, I applied to Sardine's Forward Deployed AI Engineer role (US/Canada remote). AI engineer at Accenture, 3 yrs taking production LLM agents from client goals to deployment. Happy to connect. https://jobs.ashbyhq.com/sardine/4ff32b5d-13c6-4024-826c-04ed2881d688

(b) Follow-up:
> Hi Andrew,
>
> Thanks for connecting. I applied to Sardine's Forward Deployed AI Engineer role (I'm in Montreal, Canada). I'm an AI engineer at Accenture with 3 years of experience in production LLM systems in Python, from ambiguous client requirements through evaluation, deployment and monitoring, with an M.Sc. in Machine Learning from McGill (MILA). I built a Langfuse evaluation framework for an agentic system and owned its Azure deployment. Could you tell me whether you cover this role, or point me to the right recruiter? Happy to share my resume.
>
> Thank you,
> Aly Mohamed Hussein

#### 4. Zhiheng Yi (Tech Lead, 2nd)

(a) Connection note:
> Hi Zhiheng, I applied to Sardine's Forward Deployed AI Engineer role. I'm an AI engineer at Accenture (Montreal) taking production LLM agents from client goals to deployment. Would love to connect and hear about your work. https://jobs.ashbyhq.com/sardine/4ff32b5d-13c6-4024-826c-04ed2881d688

(b) Follow-up:
> Hi Zhiheng,
>
> Thanks for connecting. I applied to Sardine's Forward Deployed AI Engineer role and wanted to reach out to someone on the engineering side. I'm an AI engineer at Accenture in Montreal (3 years), working in Python: I partnered with client stakeholders to turn ambiguous requirements into success criteria, owned an agentic system's Azure deployment, and built its Langfuse evaluation and monitoring. I'd love to hear how engineering and client-facing AI work fit together at Sardine. Would you have 15 minutes for a quick chat? Any pointer to the hiring team would also be much appreciated.
>
> Thanks,
> Aly Mohamed Hussein

#### 5. Kartik Agarwal (Enterprise Solutions Engineer, 2nd)

(a) Connection note:
> Hi Kartik, I applied to Sardine's Forward Deployed AI Engineer role. I'm an AI engineer at Accenture (Montreal) who takes production LLM systems from client goals to deployment. Would love to connect. https://jobs.ashbyhq.com/sardine/4ff32b5d-13c6-4024-826c-04ed2881d688

(b) Follow-up:
> Hi Kartik,
>
> Thanks for connecting. I applied to Sardine's Forward Deployed AI Engineer role and wanted to hear from someone working with clients. I'm an AI engineer at Accenture in Montreal (3 years), working in Python: I turned ambiguous client requirements into success criteria, owned an agentic system's Azure deployment, and built its Langfuse evaluation. I'd love to hear what client-embedded work looks like day to day at Sardine. Would you have 15 minutes for a quick chat?
>
> Thanks,
> Aly Mohamed Hussein

</details>


### #23 (rank 39): Banyan Software, Forward Deployed AI Engineer (Toronto, hybrid 3 days/week)

- Resume: `postings/BanyanSoftware-5240690007/Aly_Mohamed_Hussein_Resume_BanyanSoftware.pdf`
- Fill: 0.966
- Form tab: https://job-boards.greenhouse.io/banyansoftware/jobs/5240690007 (filled, not submitted)
- **Gaps:**
  - **n8n / automation-orchestration platforms**: nothing in the mega resume (closest: AWS Step Functions
    PoC, not listed). No explicit build-vs-buy decision on record.
  - **Excel and BI tools (Looker, Power BI, Tableau)**: not in the mega resume. SQL is only in the skills
    list (Postgres work backs it); no dedicated data-modelling or analytics bullet.
  - **Years**: posting asks 6 to 10 years total with 3+ in AI; Aly has about 3 years full time
    (plus internships), so it is below the floor on total experience.
  - Staged rollout / rollback: not explicitly shown.
  - Financial/commercial acumen, training teams and driving adoption: only indirectly (customer
    discovery, runbooks for the customer).
- **Please sanity-check:**
  - Summary: "embedding with business teams to turn manual workflows into production LLM, retrieval, and
    agentic tools ... built with Claude Code" is a synthesis of the Accenture stakeholder work, the
    Cold-Chain embedding, and claude-kit; "built with Claude Code" assumes Claude Code is your day-to-day
    agentic tool on these builds.
  - Accenture billing bullet: "Automated a consulting client's manual billing verification" (source: "to
    automate the billing process of an engineering consulting client ... previously manual billing
    verification steps").
  - SWE bullet says "deployed on AWS Fargate behind REST APIs" (Lambda dropped, since the Lambdas processed
    SQS events, not REST).
- **ASK fields:** Preferred First Name (→ A: Preferred first name (Aly?)); What are your salary expectations for this role? (optional) (→ A: Salary / compensation expectation)

<details><summary>LinkedIn shortlist and drafts (verbatim)</summary>

| # | Name | Title | Location | Degree | Profile | Why |
|---|------|-------|----------|--------|---------|-----|
| 1 | Charles Duckworth | Senior Director, Technology & Data Strategy at Banyan Software ("Building AI and data systems for vertical software M&A") | Toronto, Ontario | 2nd | https://www.linkedin.com/in/charles-duckworth-b385a411/ | Posting says the role shares work with the Technology & Data Strategy team: likely hiring manager |
| 2 | Trevor Rudd | Executive Talent Acquisition Partner @ Banyan Software | Toronto, Ontario | 2nd | https://www.linkedin.com/in/trevorrudd/ | Toronto-based Banyan recruiter |
| 3 | Tom Prendiville | Chief of Staff @ Banyan Software | Toronto, Ontario | 2nd | https://www.linkedin.com/in/thomas-prendiville/ | Toronto-based; internal functions are the role's stakeholders (referral route, weaker fit) |

Searches run: "Banyan Software recruiter", "Banyan Software AI Toronto", "Banyan Software talent acquisition". Not shortlisted: Aniket Singh (Sr Talent Acquisition Partner, GTA) and Karla Padilla (Talent Acquisition Leader, Canada), because their headlines do not name Banyan so current employer is unverified; Muhammed Samiullah Almuslim (Banyan Canopy Group, Pakistan), Arma Muksinovic (executive search, UK), Olivia Van Patter (finance), Caleb Williams, Ben Abnett and Patrick Egan (corporate development), Muhammad T. (employer not shown).

Suggested top 3: Charles Duckworth, Trevor Rudd, Tom Prendiville.

(a) = connection note, at most 300 characters including the posting link. (b) = follow-up message. Character counts in brackets.

#### 1. Charles Duckworth (Senior Director, Technology & Data Strategy, 2nd)

(a) Connection note [255]:
> Hi Charles, I applied to Banyan's Forward Deployed AI Engineer role. I'm an AI engineer (3 yrs) who builds agentic and RAG tools with business teams, using Claude Code. Would love to connect. https://job-boards.greenhouse.io/banyansoftware/jobs/5240690007

(b) Follow-up [~775]:
> Hi Charles,
>
> Thanks for connecting. I applied to Banyan's Forward Deployed AI Engineer role through the careers site (job 5240690007). I'm an AI engineer with 3 years of experience embedding with business teams to turn manual workflows into production LLM, retrieval and agentic tools in Python, TypeScript and AWS/Azure, built with Claude Code. At Accenture I partnered with stakeholders to turn ambiguous billing requirements into measurable success criteria, built a Langfuse evaluation framework against the manual process, and owned the Azure production deployment. I also shipped two revenue-generating systems solo, and I hold an M.Sc. in Machine Learning from McGill (MILA). Would you have 15 minutes to hear how your team approaches AI?
>
> Thank you,
> Aly Mohamed Hussein

#### 2. Trevor Rudd (Executive Talent Acquisition Partner, 2nd)

(a) Connection note [242]:
> Hi Trevor, I applied to Banyan's Forward Deployed AI Engineer role (Toronto, hybrid). AI engineer at Accenture, 3 yrs shipping production LLM and agentic tools. Happy to connect. https://job-boards.greenhouse.io/banyansoftware/jobs/5240690007

(b) Follow-up [601]:
> Hi Trevor,
>
> Thanks for connecting. I applied to Banyan's Forward Deployed AI Engineer role through the careers site (job 5240690007). I'm an AI engineer at Accenture with 3 years of experience shipping production LLM, retrieval and agentic tools (Python, TypeScript, AWS, Azure), including owning an agentic system's Azure deployment and its Langfuse evaluation framework. I'm based in Montreal and hold an M.Sc. in Machine Learning from McGill (MILA). Could you tell me whether you are covering this role, or point me to the recruiter who is? Happy to share my resume.
>
> Thank you,
> Aly Mohamed Hussein

#### 3. Tom Prendiville (Chief of Staff, 2nd)

(a) Connection note [279]:
> Hi Tom, I applied to Banyan's Forward Deployed AI Engineer role, which builds AI tools for internal functions. I'm an AI engineer (3 yrs) who works with business teams on production LLM tools. Would love to connect. https://job-boards.greenhouse.io/banyansoftware/jobs/5240690007

(b) Follow-up [634]:
> Hi Tom,
>
> Thanks for connecting. I applied to Banyan's Forward Deployed AI Engineer role through the careers site (job 5240690007). I'm an AI engineer with 3 years of experience working with business stakeholders to turn manual workflows into production LLM and agentic tools: at Accenture I automated a client's manual billing verification and built the evaluation framework that benchmarks it against the manual process. I also shipped two revenue-generating systems solo. If it is appropriate, could you point me to the right person on the hiring side for this role? Any pointer would be appreciated.
>
> Thank you,
> Aly Mohamed Hussein

</details>


## B2. LinkedIn drafts without a submittable application

### 20 (rank 36): Block-11452431

- DECISION: no Canada posting; the only posting is Greenhouse id 5434157008 (US - CA - Bay Area - Remote) whose data lists Canada pay ranges. Apply there (you fill it by hand or I prepare it in the next run), or skip?
- Resume: `postings/Block-11452431/Aly_Mohamed_Hussein_Resume_Block.pdf`

<details><summary>LinkedIn shortlist and drafts (verbatim)</summary>

| # | Name | Title | Location | Degree | Profile | Why |
|---|------|-------|----------|--------|---------|-----|
| 1 | Aaron Young | Engineering Manager at Cash App | Canada | 3rd | https://www.linkedin.com/in/aaron-young-6b52333/ | Canada-based Cash App eng manager; the posting is a Cash App role. Team unknown |
| 2 | Haroon Salimi | ML @ Cash App | Greater Toronto Area | 2nd | https://www.linkedin.com/in/haroonsalimi/ | Toronto Cash App ML engineer: peer / referral route |
| 3 | Shahzad Raza | Building ML-powered fraud prevention systems at CashApp | Canada | 3rd | https://www.linkedin.com/in/shahzadraza/ | Canada-based Cash App ML engineer |
| 4 | Jered Davis | Talent Acquisition, Block, Square, Cash App | Denver, Colorado | 2nd | https://www.linkedin.com/in/jered-davis-ba052951/ | Block/Cash App recruiter (US; no Canada recruiter surfaced) |
| 5 | Victor Borges | Technical Recruiter, Cash App @ Square | Brooklyn, New York | 3rd | https://www.linkedin.com/in/victor-borges-483b51bb/ | Cash App technical recruiter (US) |

Searches run: "Block technical recruiter Toronto", "Cash App Block recruiter Canada", "Block AI evaluation", "Cash App recruiter", "Cash App engineering manager Toronto". Most results were non-Block (Stripe, ex-Block, H&R Block). Not shortlisted: Kyle De Freitas (AI solutions across Block ecosystem, Etobicoke, 3rd, https://www.linkedin.com/in/kyledef/) and Keefer Kosciuch ("human @ block.xyz", Toronto, 2nd, https://www.linkedin.com/in/keeferrourke/): role unclear. No evaluation-team manager identified.

Suggested top 3: Haroon Salimi, Aaron Young, Jered Davis.

(a) = connection note, at most 300 characters including link. (b) = follow-up after acceptance.

#### 1. Aaron Young (Engineering Manager, Cash App, 3rd)

(a) Connection note:
> Hi Aaron, I'm interested in Cash App's AI Evaluation Infrastructure Engineer role. I'm an AI engineer at Accenture (Montreal) who built a Langfuse evaluation framework for a production agentic system. Would love to connect. https://block.xyz/careers/jobs/5434157008

(b) Follow-up:
> Hi Aaron,
>
> Thanks for connecting. I'm interested in Block's AI Evaluation Infrastructure Engineer role (https://block.xyz/careers/jobs/5434157008). I'm an AI engineer at Accenture in Montreal with 3 years in production LLM systems in Python, and an M.Sc. in Machine Learning from McGill (MILA). I built a Langfuse-based evaluation and monitoring framework for an agentic system and owned its Azure production deployment. The posting lists the role as remote; I'm in Canada. Would you be open to a 15-minute chat, or could you point me to the hiring team for this role?
>
> Thank you,
> Aly Mohamed Hussein

#### 2. Haroon Salimi (ML @ Cash App, 2nd)

(a) Connection note:
> Hi Haroon, I'm interested in Cash App's AI Evaluation Infrastructure Engineer role. I'm an AI engineer at Accenture (Montreal) and built a Langfuse evaluation framework for a production agentic system. Would love to connect and hear about ML work at Cash App. https://block.xyz/careers/jobs/5434157008

(b) Follow-up:
> Hi Haroon,
>
> Thanks for connecting. I'm interested in Block's AI Evaluation Infrastructure Engineer role (https://block.xyz/careers/jobs/5434157008) and wanted to hear from someone on the ML side. I'm an AI engineer at Accenture (Montreal, 3 years), working in Python on production LLM systems; I built a Langfuse evaluation and monitoring framework and owned an agentic system's Azure deployment, with an M.Sc. in Machine Learning from McGill (MILA). Would you have 15 minutes for a quick chat about how evaluation works at Cash App? A pointer to the right hiring contact would also help.
>
> Thanks,
> Aly Mohamed Hussein

#### 3. Shahzad Raza (ML fraud prevention, CashApp, 3rd)

(a) Connection note:
> Hi Shahzad, I'm interested in Cash App's AI Evaluation Infrastructure Engineer role. I'm an AI engineer at Accenture (Montreal) focused on production LLM systems and their evaluation. Would love to connect. https://block.xyz/careers/jobs/5434157008

(b) Follow-up:
> Hi Shahzad,
>
> Thanks for connecting. I'm interested in Block's AI Evaluation Infrastructure Engineer role (https://block.xyz/careers/jobs/5434157008). I'm an AI engineer at Accenture in Montreal with 3 years on production LLM systems in Python, an M.Sc. in Machine Learning from McGill (MILA), and a Langfuse evaluation framework I built for an agentic system. If you're close to the team, would you be open to a short chat about how evaluation is done at Cash App, or to pointing me to the hiring team?
>
> Thank you,
> Aly Mohamed Hussein

#### 4. Jered Davis (Talent Acquisition, Block/Square/Cash App, 2nd)

(a) Connection note:
> Hi Jered, I'm interested in Block's AI Evaluation Infrastructure Engineer role (Cash App). AI engineer at Accenture, 3 yrs taking production LLM systems to deployment; based in Canada. Happy to connect. https://block.xyz/careers/jobs/5434157008

(b) Follow-up:
> Hi Jered,
>
> Thanks for connecting. I'm interested in Block's AI Evaluation Infrastructure Engineer role (Req R0007124, https://block.xyz/careers/jobs/5434157008). I'm an AI engineer at Accenture in Montreal with 3 years in production LLM systems in Python, an M.Sc. in Machine Learning from McGill (MILA), and I built a Langfuse evaluation framework for an agentic system and owned its Azure deployment. The posting is listed as remote; could you tell me whether it is open to candidates in Canada, and whether you cover it or can point me to the recruiter who does? Happy to share my resume.
>
> Thank you,
> Aly Mohamed Hussein

#### 5. Victor Borges (Technical Recruiter, Cash App, 3rd)

(a) Connection note:
> Hi Victor, I'm interested in Cash App's AI Evaluation Infrastructure Engineer role. AI engineer at Accenture (Montreal), 3 yrs in production LLM systems and evaluation. Is the role open to Canada? Happy to connect. https://block.xyz/careers/jobs/5434157008

(b) Follow-up:
> Hi Victor,
>
> Thanks for connecting. I'm interested in Block's AI Evaluation Infrastructure Engineer role (https://block.xyz/careers/jobs/5434157008). I'm an AI engineer at Accenture in Montreal with 3 years in production LLM systems in Python and an M.Sc. in Machine Learning from McGill (MILA); I built a Langfuse evaluation framework for an agentic system. Could you confirm whether the role is open to candidates in Canada and, if so, how to apply? Happy to share my resume.
>
> Thank you,
> Aly Mohamed Hussein

**Warning: connection note(s) over 300 chars: [301]**

</details>


### 24 (rank 40): Velixo-10899199

- BLOCKED (DLQ): no web form; apply by emailing jobs@velixo.com with the built resume, or via a Built In account.
- Resume: `postings/Velixo-10899199/Aly_Mohamed_Hussein_Resume_Velixo.pdf`

<details><summary>LinkedIn shortlist and drafts (verbatim)</summary>

| # | Name | Title | Location | Degree | Profile | Why |
|---|------|-------|----------|--------|---------|-----|
| 1 | Anna Kosianenko | Human Resources Recruiter @ Velixo | Poland | 3rd+ | https://www.linkedin.com/in/anna-kosianenko/ | Only recruiter surfaced; right person for how to apply (no Velixo application form found) |
| 2 | Gabriel Michaud | Founder & CEO, Velixo | Montreal, QC | 3rd+ | https://www.linkedin.com/in/gabrielmichaud/ | Small company, Montreal founder; the role owns the numbers behind pricing, so he is plausibly the decision-maker |
| 3 | Philippe Bellefeuille | COO at Velixo | Montreal, QC | 3rd+ | https://www.linkedin.com/in/philippebellefeuille/ | Senior Montreal operator; likely knows who owns this hire |
| 4 | Anastasiya Babiy, CPA auditor | VP Finance at Velixo | Montreal, QC | 2nd | https://www.linkedin.com/in/anastasiyababiy/ | Posting says the role works alongside the VP Finance on pricing and margin |
| 5 | Aaron Solomon | ERP Data Analyst at Velixo | Montreal, QC | 2nd | https://www.linkedin.com/in/aaron-solomon-/ | Montreal peer on the data side; referral route / insight into the team |

No Velixo engineering or AI manager/CTO surfaced (the "Velixo CTO" search returned the CEO and unrelated people). Not shortlisted: Dominic Renda (Partnership
Development Rep), Markens Juste (Technical Support Specialist), Cyrille Lanctot (headline does not name Velixo), Layal Zok (company unverified).

Suggested top 3: Anna Kosianenko, Gabriel Michaud, Anastasiya Babiy.

(a) = connection note, at most 300 characters including the posting link. (b) = message / follow-up.

#### 1. Anna Kosianenko (Recruiter, 3rd+)

(a) Connection note:
> Hi Anna, I'm interested in Velixo's Applied AI Engineer role (Montreal). AI engineer at Accenture, built Langfuse evals and an LLM cost layer. Could you point me to how to apply? https://builtinmontreal.com/job/applied-ai-engineer/10899199

(b) Follow-up:
> Hi Anna,
>
> Thanks for connecting. I'm interested in Velixo's Applied AI Engineer role (https://builtinmontreal.com/job/applied-ai-engineer/10899199), and I'm based in Montreal, bilingual English/French. The application link on Built In goes to a generic feedback form, so I wanted to ask how candidates should apply.
>
> I'm an AI engineer at Accenture (3 years) and built a Langfuse evaluation framework with LLM-as-a-judge degradation detection for production LLM systems. On the cost side, I'm building Safi, a layer that cuts LLM token spend with prompt caching and model routing while evals guard quality (61.7% realized savings at 100% quality agreement on a live trace). Could you tell me where to send my resume?
>
> Thank you,
> Aly Mohamed Hussein

#### 2. Gabriel Michaud (Founder & CEO, 3rd+)

(a) Connection note:
> Hi Gabriel, I'm a Montreal AI engineer interested in Velixo's Applied AI Engineer role (evals and cost per action). I've built both: Langfuse evals and an LLM cost layer. https://builtinmontreal.com/job/applied-ai-engineer/10899199

(b) Follow-up:
> Hi Gabriel,
>
> Thanks for connecting. I'm an AI engineer at Accenture in Montreal, and the Applied AI Engineer role (evals plus cost per action for Velixo Intelligence) is close to what I've been building. At Accenture I built a Langfuse evaluation framework and LLM-as-a-judge degradation detection for production LLM systems. On my own, Safi cuts LLM token spend (prompt caching, model routing) with evals guarding quality: 61.7% realized savings at 100% quality agreement on a live trace, and when my first judge missed the thresholds I diagnosed it rather than tuned it. I'd welcome 15 minutes, or a pointer to the right person on your team.
>
> Thank you,
> Aly Mohamed Hussein

#### 3. Philippe Bellefeuille (COO, 3rd+)

(a) Connection note:
> Hi Philippe, I'm a Montreal AI engineer interested in Velixo's Applied AI Engineer role. I build LLM eval harnesses (Langfuse) and cost optimization (prompt caching, routing). https://builtinmontreal.com/job/applied-ai-engineer/10899199

(b) Follow-up:
> Hi Philippe,
>
> Thanks for connecting. I'm interested in Velixo's Applied AI Engineer role (https://builtinmontreal.com/job/applied-ai-engineer/10899199). I'm an AI engineer at Accenture in Montreal with 3 years in production LLM systems, including a Langfuse evaluation framework and LLM-as-a-judge monitoring, plus a project that cut LLM token spend with 100% quality agreement on a live trace. Could you tell me who is leading this hire, or the best way to get my resume to them?
>
> Thank you,
> Aly Mohamed Hussein

#### 4. Anastasiya Babiy (VP Finance, 2nd)

(a) Connection note:
> Hi Anastasiya, I'm interested in Velixo's Applied AI Engineer role, which supplies unit cost data for pricing. I build LLM cost tracking and evals (Langfuse). https://builtinmontreal.com/job/applied-ai-engineer/10899199

(b) Follow-up:
> Hi Anastasiya,
>
> Thanks for connecting. I'm interested in Velixo's Applied AI Engineer role, which partners with Finance on the unit cost behind credit pricing. I'm an AI engineer at Accenture in Montreal; I built a Langfuse evaluation framework for a production LLM system, and my project Safi reports cost, quality and harm separately while cutting token spend 61.7% at 100% quality agreement on a live trace. Could you tell me who is hiring for this role, or forward my resume to them? Happy to share it.
>
> Thank you,
> Aly Mohamed Hussein

#### 5. Aaron Solomon (ERP Data Analyst, 2nd)

(a) Connection note:
> Hi Aaron, I'm a Montreal AI engineer interested in Velixo's Applied AI Engineer role. Would love to connect and hear what working at Velixo is like. https://builtinmontreal.com/job/applied-ai-engineer/10899199

(b) Follow-up:
> Hi Aaron,
>
> Thanks for connecting. I'm interested in Velixo's Applied AI Engineer role (evals and cost per action for Velixo Intelligence), and I'm based in Montreal. I'm an AI engineer at Accenture who built a Langfuse evaluation framework and an LLM cost-optimization layer. Would you have 15 minutes to tell me how the team works with Velixo Intelligence day to day? A pointer to the hiring manager would also be much appreciated.
>
> Thanks,
> Aly Mohamed Hussein

</details>


### TR (rank 19+20): ThomsonReuters-combined

- Combined LinkedIn resume for both TR roles. Both applications are BLOCKED (DLQ: Workday account at thomsonreuters.wd5). Drafts say 'applying shortly'. Send now, or wait until you've applied?
- Resume: `postings/ThomsonReuters-combined/Aly_Mohamed_Hussein_Resume_ThomsonReuters.pdf`

<details><summary>LinkedIn shortlist and drafts (verbatim)</summary>

| # | Name | Title | Location | Degree | Profile | Roles | Why |
|---|------|-------|----------|--------|---------|-------|-----|
| 1 | Garima Kalra | Technical Talent Acquisition Lead @ Thomson Reuters (AI & ML engineering teams) | Greater Toronto Area | 2nd | https://www.linkedin.com/in/garima-kalra29/ | A + B | Tech recruiting lead for AI/ML in Toronto |
| 2 | Connor Quinn | Technical Recruiter at Thomson Reuters | Greater Toronto Area | 3rd+ | https://www.linkedin.com/in/connor-quinn-37076717a/ | A + B | Technical recruiter, Toronto |
| 3 | Mohammad Neisiani | Senior Software Development Manager at Thomson Reuters | Toronto | 2nd | https://www.linkedin.com/in/mohammad-neisiani-63203623/ | B (CoCounsel search hit; team not confirmed) | Toronto eng manager surfaced for CoCounsel FDE search |
| 4 | Elvis L. | AI Evaluation Product Manager @ Thomson Reuters (LLM & agent evaluation) | Toronto | 2nd | https://www.linkedin.com/in/shuchangl/ | A + B | Evaluation of LLM agents, matches the Langfuse / LLM-as-a-judge work |
| 5 | Kanish Goel | AI Enabled Software Engineering @ Thomson Reuters | Toronto | 2nd | https://www.linkedin.com/in/0xkgoel/ | A + B (peer) | Toronto AI engineering peer, referral route |

No clearly identified Product Analytics director or FDE hiring manager in Toronto surfaced. Not shortlisted: Ashish Verma (FDE leader, Dallas), Esmond Kim and Jeremy Tremblay (US CoCounsel engineers), Anthony Virgilio (Toronto recruiter, backup), Patricia Frutos (executive search).
Suggested top 3: Garima Kalra, Elvis L., Mohammad Neisiani.

(a) = connection note, at most 300 characters. (b) = message after connecting.

#### 1. Garima Kalra (Technical TA Lead, 2nd)

(a) Connection note:
> Hi Garima, I'm applying to Thomson Reuters' AI Engineer, Product Analytics (JREQ202780) and Software Engineer - AI, CoCounsel Forward Deployed Engineering (JREQ200166) roles in Toronto. AI engineer at Accenture, 3 yrs in production LLM agents and evals. Happy to connect.

(b) Follow-up:
> Hi Garima,
>
> Thanks for connecting. I'm applying shortly to two Toronto roles: AI Engineer, Product Analytics (JREQ202780) and Software Engineer - AI, CoCounsel Forward Deployed Engineering (JREQ200166). I'm an AI engineer at Accenture (3 years, Montreal) building LLM agents, RAG and evals in Python for regulated clients. I designed a LangGraph fraud-detection agent with RAG for a major U.S. bank (96% accuracy across 500 transactions), built a Langfuse evaluation framework, and delivered an LLM-as-a-judge framework checking summaries for hallucination. I hold an M.Sc. in Machine Learning from McGill (MILA). Could you tell me whether you recruit for these teams, or point me to the right person? Resume attached.
>
> Thank you,
> Aly Mohamed Hussein

#### 2. Connor Quinn (Technical Recruiter, 3rd+)

(a) Connection note:
> Hi Connor, I'm applying to Thomson Reuters' AI Engineer, Product Analytics (JREQ202780) and CoCounsel Forward Deployed Engineering (JREQ200166) roles in Toronto. AI engineer at Accenture, 3 yrs in production LLM agents, RAG and evals. Would be glad to connect.

(b) Follow-up:
> Hi Connor,
>
> Thanks for connecting. I'm applying shortly to AI Engineer, Product Analytics (JREQ202780) and Software Engineer - AI, CoCounsel Forward Deployed Engineering (JREQ200166), both Toronto hybrid. I'm an AI engineer at Accenture with 3 years in Python, owning an agentic billing system's Azure production deployment from ambiguous client requirements, with a Langfuse evaluation framework and a Llama call-summary app that saves 15 minutes per call for a major U.S. bank. M.Sc. in Machine Learning, McGill (MILA). Are you the recruiter for either role, or could you forward my application to the hiring team? Resume attached.
>
> Thank you,
> Aly Mohamed Hussein

#### 3. Mohammad Neisiani (Senior Software Development Manager, 2nd)

(a) Connection note:
> Hi Mohammad, I'm applying to Thomson Reuters' CoCounsel Forward Deployed Engineering (JREQ200166) and AI Engineer, Product Analytics (JREQ202780) roles in Toronto. AI engineer at Accenture shipping LLM agents to production for banking clients. Would love to connect.

(b) Follow-up:
> Hi Mohammad,
>
> Thanks for connecting. I'm applying shortly to Software Engineer - AI, CoCounsel Forward Deployed Engineering (JREQ200166) and AI Engineer, Product Analytics (JREQ202780) in Toronto. At Accenture I partnered with enterprise stakeholders to turn ambiguous requirements into success criteria, built a router/subagent agentic system on Azure and owned its production deployment, and designed a LangGraph fraud-detection agent with RAG (96% accuracy across 500 transactions). If your team touches either role, would you have 15 minutes for a quick chat, or could you point me to the hiring manager?
>
> Thanks,
> Aly Mohamed Hussein

#### 4. Elvis L. (AI Evaluation Product Manager, 2nd)

(a) Connection note:
> Hi Elvis, I'm applying to Thomson Reuters' AI Engineer, Product Analytics (JREQ202780) and CoCounsel Forward Deployed Engineering (JREQ200166) roles in Toronto. I build LLM agent evals (Langfuse, LLM-as-a-judge) at Accenture and would love to connect given your work in AI evaluation.

(b) Follow-up:
> Hi Elvis,
>
> Thanks for connecting. I'm applying shortly to AI Engineer, Product Analytics (JREQ202780) and Software Engineer - AI, CoCounsel Forward Deployed Engineering (JREQ200166). Evaluation is the part of my work I'd most like to talk about: I built a Langfuse framework benchmarking an agentic billing system against the manual process, and an LLM-as-a-judge framework scoring generated summaries for completeness, hallucination and readability, which caught degradation early. I'd value hearing how TR evaluates its agents and whether the teams hiring for these roles would be open to a short chat.
>
> Thanks,
> Aly Mohamed Hussein

#### 5. Kanish Goel (AI Enabled Software Engineering, 2nd)

(a) Connection note:
> Hi Kanish, I'm applying to Thomson Reuters' AI Engineer, Product Analytics (JREQ202780) and CoCounsel Forward Deployed Engineering (JREQ200166) roles in Toronto. AI engineer at Accenture (agents, RAG, MCP, evals). Would love to connect and hear about your work.

(b) Follow-up:
> Hi Kanish,
>
> Thanks for connecting. I'm applying shortly to two Toronto roles: AI Engineer, Product Analytics (JREQ202780) and Software Engineer - AI, CoCounsel Forward Deployed Engineering (JREQ200166). I'm an AI engineer at Accenture (3 years, Python) building LLM agents and RAG with Langfuse evals, plus an internal Gemini-on-Vertex-AI chatbot that generates dashboard visualizations from natural language. I'd love to hear what AI engineering looks like at TR day to day. Would you have 15 minutes, or any pointer to the hiring teams?
>
> Thanks,
> Aly Mohamed Hussein

</details>


### SB (rank 5+31): Scotiabank-combined

- Combined LinkedIn resume for both Scotiabank roles. Both applications are BLOCKED (DLQ: Scotiabank Talent Community account). Drafts say 'applying'. Send now, or wait until you've applied?
- Resume: `postings/Scotiabank-combined/Aly_Mohamed_Hussein_Resume_Scotiabank.pdf`

<details><summary>LinkedIn shortlist and drafts (verbatim)</summary>

| # | Name | Title | Location | Degree | Profile | Role | Why |
|---|------|-------|----------|--------|---------|------|-----|
| 1 | Margarita K. | Senior Talent Acquisition at Scotiabank | SME Digital and Technology Hiring | Canada | 2nd | https://www.linkedin.com/in/margaritalovestech/ | A + B | Technology recruiter at Scotiabank (current role in headline) |
| 2 | Sandra Jennings | Sr Consultant for Technology, Talent Acquisition at Scotiabank | Toronto, Ontario | 2nd | https://www.linkedin.com/in/jenningssandra/ | A + B | Technology talent acquisition at Scotiabank, Toronto |
| 3 | Claudia Jin | Manager, AI and Machine Learning @ Scotiabank | Toronto, Ontario | 2nd | https://www.linkedin.com/in/claudiajin-cx/ | A (B as context) | AI/ML manager at Scotiabank, Toronto: hiring-manager type for role A |
| 4 | Will Lau | AI @ Scotiabank | Toronto, Ontario | 1st | https://www.linkedin.com/in/yuenlau/ | A (B as context) | Scotiabank AI practitioner, already 1st degree: regular message with resume attached; peer / referral route for role A |
| 5 | Vipul Malhotra, MS | AI & Portfolio Analytics Leader @ Tangerine (Scotiabank) | Greater Toronto Area | 2nd | https://www.linkedin.com/in/vipul-malhotra-vp/ | B (A as context) | Tangerine AI/MLOps leader, GTA: closest Tangerine AI contact for role B |

Not shortlisted: Vishwa Tailor (Acting Senior Manager, Talent Acquisition, Scotiabank, Toronto, 2nd, https://www.linkedin.com/in/vishwatailor/; good backup recruiter), Chahana Dora - Rohan, Vikas Vats and Emma Hong (Toronto tech recruiters whose headlines do not name Scotiabank), Nikhita Gurwara (Scotiabank Retail Banking TA, less relevant), Zoey L. (Senior Manager, Data Science, Scotiabank), Emad Jabbar (Senior AI Engineer @ Tangerine, Calgary, 2nd, https://www.linkedin.com/in/emad-jabbar/; backup Tangerine peer). No Tangerine-specific recruiter surfaced in Toronto.

Suggested top 3: Margarita K. (technology recruiter), Claudia Jin (AI/ML manager), Vipul Malhotra (Tangerine AI).

(a) = connection note, at most 300 characters. (b) = message / follow-up. Character counts in brackets (with first name inserted).

#### 1. Margarita K. (Senior Talent Acquisition at Scotiabank | SME Digital and Technology Hiring, 2nd) - A + B

(a) Connection note [216]:
> Hi Margarita, I am applying to two Toronto roles: Software Engineer (AI Engineer) at Scotiabank and Senior AI Engineer at Tangerine. AI engineer (3 yrs, LangGraph/RAG, FastAPI) at Accenture. Would be glad to connect.

(b) Follow-up [879]:
> Hi Margarita,
>
> Thanks for connecting. I am applying (shortly) to two Toronto roles: Software Engineer (AI Engineer) at Scotiabank (req 270579) and Senior AI Engineer at Tangerine (req 274918). I am an AI engineer at Accenture with 3 years building production LLM agents (LangGraph, RAG) and Python microservices for major U.S. banks, including a fraud detection agent (96% accuracy across 500 transactions) and a call-summarization app that saved 15 minutes per call, with an M.Sc. in Machine Learning from McGill (MILA). Could you tell me whether you cover these roles, or point me to the recruiter who does? Happy to share my resume.
>
> Scotiabank: https://jobs.scotiabank.com/job/Toronto-Software-Engineer-%28AI-Engineer%29-ON-M5H-1H1/605446017/
> Tangerine: https://jobs.scotiabank.com/Tangerine/job/Toronto-Senior-AI-Engineer-ON-M2H0A1/606493117/
>
> Thank you,
> Aly Mohamed Hussein

#### 2. Sandra Jennings (Sr Consultant for Technology, Talent Acquisition at Scotiabank, 2nd) - A + B

(a) Connection note [232]:
> Hi Sandra, I am applying to Scotiabank's Software Engineer (AI Engineer) and Tangerine's Senior AI Engineer roles in Toronto. I build production LLM agents at Accenture for U.S. banks. Would love to connect and hear about your team.

(b) Follow-up [876]:
> Hi Sandra,
>
> Thanks for connecting. I am applying (shortly) to two Toronto roles: Software Engineer (AI Engineer) at Scotiabank (req 270579) and Senior AI Engineer at Tangerine (req 274918). I am an AI engineer at Accenture with 3 years building production LLM agents (LangGraph, RAG) and Python microservices for major U.S. banks, including a fraud detection agent (96% accuracy across 500 transactions) and a call-summarization app that saved 15 minutes per call, with an M.Sc. in Machine Learning from McGill (MILA). Could you tell me whether you cover these roles, or point me to the recruiter who does? Happy to share my resume.
>
> Scotiabank: https://jobs.scotiabank.com/job/Toronto-Software-Engineer-%28AI-Engineer%29-ON-M5H-1H1/605446017/
> Tangerine: https://jobs.scotiabank.com/Tangerine/job/Toronto-Senior-AI-Engineer-ON-M2H0A1/606493117/
>
> Thank you,
> Aly Mohamed Hussein

#### 3. Claudia Jin (Manager, AI and Machine Learning @ Scotiabank, 2nd) - A (B as context)

(a) Connection note [233]:
> Hi Claudia, I am applying to Scotiabank's Software Engineer (AI Engineer) and Tangerine's Senior AI Engineer roles in Toronto. I build production LLM agents at Accenture for U.S. banks. Would love to connect and hear about your team.

(b) Follow-up [869]:
> Hi Claudia,
>
> Thanks for connecting. I am applying (shortly) to two Toronto roles: Software Engineer (AI Engineer) at Scotiabank (AI Engineering and Labs) and Senior AI Engineer at Tangerine. I am an AI engineer at Accenture (3 years) building production LLM agents in Python for major U.S. banks: a LangGraph fraud detection agent with RAG (96% accuracy across 500 transactions), and an LLM-as-a-judge framework with Langfuse tracing for call summaries. I also built an MCP server with structured outputs and prompt-injection hardening. I would value 15 minutes to hear how your team works, or any pointer to the hiring team.
>
> Scotiabank: https://jobs.scotiabank.com/job/Toronto-Software-Engineer-%28AI-Engineer%29-ON-M5H-1H1/605446017/
> Tangerine: https://jobs.scotiabank.com/Tangerine/job/Toronto-Senior-AI-Engineer-ON-M2H0A1/606493117/
>
> Thank you,
> Aly Mohamed Hussein

#### 4. Will Lau (AI @ Scotiabank, 1st) - A (B as context)

(a) not needed (already 1st degree).

(b) Message [793]:
> Hi Will,
>
> I am applying (shortly) to two Toronto roles: Software Engineer (AI Engineer) at Scotiabank (req 270579) and Senior AI Engineer at Tangerine (req 274918). I am an AI engineer at Accenture with 3 years building production LLM agents (LangGraph, RAG, MCP) and FastAPI microservices on AWS, GCP and Azure for major U.S. banks, with an M.Sc. in Machine Learning from McGill (MILA). I would love to hear what the work looks like day to day. Would you have 15 minutes for a quick chat, or be able to point me to the hiring team? Resume attached.
>
> Scotiabank: https://jobs.scotiabank.com/job/Toronto-Software-Engineer-%28AI-Engineer%29-ON-M5H-1H1/605446017/
> Tangerine: https://jobs.scotiabank.com/Tangerine/job/Toronto-Senior-AI-Engineer-ON-M2H0A1/606493117/
>
> Thank you,
> Aly Mohamed Hussein

#### 5. Vipul Malhotra, MS (AI & Portfolio Analytics Leader @ Tangerine (Scotiabank), 2nd) - B (A as context)

(a) Connection note [220]:
> Hi Vipul, I am applying to Tangerine's Senior AI Engineer role (and Scotiabank's Software Engineer, AI Engineer). I build production LLM agents at Accenture for U.S. banks. Would love to connect and hear about your team.

(b) Follow-up [772]:
> Hi Vipul,
>
> Thanks for connecting. I am applying (shortly) to Tangerine's Senior AI Engineer role in Toronto, and to Scotiabank's Software Engineer (AI Engineer) role. I am an AI engineer at Accenture (3 years) building production LLM agents in Python for major U.S. banks: a LangGraph fraud detection agent with RAG (96% accuracy across 500 transactions), Langfuse-based evaluation, and a Vertex AI Gemini chatbot on GCP. I would value 15 minutes to hear how AI work is organized at Tangerine, or any pointer to the hiring team.
>
> Scotiabank: https://jobs.scotiabank.com/job/Toronto-Software-Engineer-%28AI-Engineer%29-ON-M5H-1H1/605446017/
> Tangerine: https://jobs.scotiabank.com/Tangerine/job/Toronto-Senior-AI-Engineer-ON-M2H0A1/606493117/
>
> Thank you,
> Aly Mohamed Hussein

</details>


## C. Dead-lettered in this run

| Rank | Company | Title | Reason | Needs |
|---|---|---|---|---|
| 10 | Affinity | AI Engineer, AI Platform | CLOSED | nothing, closed |
| 14 | Level Access | AI Engineer | CLOSED | nothing, closed |
| 27 | Mercury | Senior Software Engineer - AI Engineering | CLOSED | nothing, closed |
| 37 | Klue | Senior Software Engineer, Agents | CLOSED | nothing, closed; Aly may want the similar Klue role |
| 5 | Scotiabank | Software Engineer (AI Engineer) | BLOCKED | Aly signs in to or creates a Scotiabank Talent Community account in Chrome, then /batch apply dlq.md --reason BLOCKED |
| 31 | Scotiabank (Tangerine) | Senior AI Engineer | BLOCKED | Aly signs in to or creates a Scotiabank Talent Community account in Chrome, then /batch apply dlq.md --reason BLOCKED |
| 8 | Morgan Stanley | AI Development Solution Engineering Specialist (Hybrid) | BLOCKED | Aly creates a Workday candidate account at ms.wd5.myworkdayjobs.com (or applies by hand with the built resume), then /batch outreach dlq.md --reason BLOCKED |
| 13 | Manulife | Agentic Engineer, Innovation | BLOCKED | Aly creates a Workday candidate account at manulife.wd3.myworkdayjobs.com (or applies by hand with the built resume), then /batch outreach dlq.md --reason BLOCKED |
| 19 | Thomson Reuters | AI Engineer, Product Analytics | BLOCKED | Aly creates a Workday candidate account at thomsonreuters.wd5.myworkdayjobs.com (or applies by hand with the built resume), then /batch outreach dlq.md --reason BLOCKED |
| 32 | RBC | AI Engineer | BLOCKED | Aly creates a Workday candidate account at rbc.wd3.myworkdayjobs.com (or applies by hand with the built resume), then /batch outreach dlq.md --reason BLOCKED |
| 20 | Thomson Reuters | Software Engineer - AI – CoCounsel Forward Deployed Engineering | BLOCKED | Aly creates a Workday candidate account at thomsonreuters.wd5.myworkdayjobs.com (same account covers rank 19), then /batch outreach dlq.md --reason BLOCKED |
| 40 | Velixo | Applied AI Engineer | BLOCKED | Aly emails jobs@velixo.com with Aly_Mohamed_Hussein_Resume_Velixo.pdf (+ cover letter), or applies via a Built In account |

Not in this batch: Klue has a similar live role, "Senior Software Engineer, AI" (Ashby id 25683e0d), if you want it added.
