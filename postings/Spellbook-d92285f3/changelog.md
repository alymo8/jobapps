# Changelog: Spellbook, Forward Deployed Engineer

Verification: 1 page, fill 0.969, skills 5 lines (no category wraps), no LaTeX errors; only the
0.56pt overfulls the reference resume also has. PNG inspected.

Eligibility: posting location is "Remote - Canada" (Ashby API: workplaceType Remote, country Canada),
so Montreal is eligible. Posted range CA$170K-CA$213K base + equity.

## Emphasized
- Forward-deployed shape: the summary and the first Accenture bullet lead with taking enterprise
  client requirements from ambiguous to production and owning the deployment (the posting's "translate
  ambiguous requirements into production-ready systems").
- Customer-embedded delivery: both paying-client projects open with "sole engineer for a paying client",
  plus customer discovery (Clinic Ops) and embedding with the owner (Cold-Chain), mirroring "work directly
  with end users" and "drive adoption".
- Their workflow vocabulary: audit logging, human review loop (every output a draft the doctor accepts),
  multi-tenant isolation / RLS, data residency (Egypt PDPL), runbooks and handoff. These cover the
  posting's approvals, permissions, auditability and SOC2-style data handling.
- Their stack: TypeScript, Node.js, Express.js, MongoDB, Docker, AWS CDK (skills line plus a SWE bullet
  on provisioning with CloudFormation and CDK), Anthropic/OpenAI, RAG, evals.
- Education moved above Projects as in the reference; Research section dropped.

## Close-call cuts
- **claude-kit cut** (on the usual shortlist): internal dev tooling, and the posting says "not internal
  tooling". Cut to make room for Leagueware (MongoDB).
- **Safi cut**: an LLM cost layer is less relevant to enterprise deployment than the two client systems.
- **Research section dropped** (both MILA papers); M.Sc./MILA stays in the summary and education.
- Accenture: LLM-as-a-judge summary-eval bullet, Gemini dashboard chatbot, TTS PoC, monitoring bullet.
  SWE: DynamoDB index, Step Functions PoC, inner-source bullet. Cold-Chain: agentic pipeline, 116-test /
  advisory-lock bullet, DR backup bullet. Clinic Ops: hallucination/injection bullet, caching bullet,
  28-PR / 584-test bullet.
- No age-rule overrides.

## Gaps vs the posting
- No legal-tech or DMS integration experience (iManage, NetDocuments), and no identity-system / SSO
  integration work in the mega resume.
- No tRPC. Express.js and Node.js appear only in the skills list with no bullet behind them, and MongoDB
  only through Leagueware.
- No SOC2 experience; the closest is PDPL data residency, audit logging and tenant isolation on Clinic Ops.
- Years: about 3 years full time plus an internship, at the bottom of their 3-7 range.

## Please sanity-check
- The SWE bullet merges three mega-resume bullets: "Led" the Jenkins-pipeline microservices (33%), Spring
  Boot on Fargate behind REST APIs, and Python Lambda for SQS events.
- Accenture bullet 1 says "enterprise client stakeholders"; the source says "enterprise stakeholders"
  (on the client billing engagement).
- Summary: "taking enterprise AI systems from ambiguous client requirements to production on AWS and Azure"
  is a synthesis of the Accenture bullets, not a mega-resume line.

## Questions for Aly
- none
