# Changelog: EQ Bank, Forward Deployed AI Engineer (Staff-level), Toronto (Hybrid)

Verification: 1 page, fill 0.969, skills_lines 5 (no category wraps), no LaTeX errors; only the
0.56pt overfulls the reference resume also has. PNG inspected.

Source of facts: `mega_resume.tex` does not exist in the repo; used `mega-resume-v1.5.tex` (the only
mega resume present).

Eligibility: Toronto, hybrid. No Canada exclusion; Aly is Montreal-based, so a hybrid Toronto role
implies relocation or commuting (see Questions).

## Emphasized
- Azure (their preferred cloud): summary leads with Azure; Accenture Azure agentic billing system
  (AI Foundry, Azure ML, Containers) first; Clinic Ops Azure deployment (Bicep, Container Apps, Key
  Vault with managed identity, private networking) kept; Cloud skills line leads with Azure.
- Claude in production: Anthropic API (Claude) in Skills, Claude Certified Architect, and Clinic Ops'
  four production LLM workflows on Anthropic structured outputs.
- Governance (prompt safety, injection prevention, compliance): Clinic Ops prompt-injection and
  hallucination bullet, AI gateway with payload minimization and audit logging, PDPL data residency.
- Banking domain: fraud-detection agent and call-summary service, both for major U.S. banks; CI/CD
  microservices for a U.S. bank.
- Event-driven / API-first: Kinesis + Flink streaming, Lambda processing SQS events, REST APIs.
- Stakeholder work and fast delivery: stakeholder bullet at Accenture; both solo client systems
  (Cold-Chain built in about four weeks), customer discovery on Clinic Ops.
- Research section dropped (as in other FDE resumes) to fit the delivery evidence.

## Close-call cuts
- claude-kit and Safi cut (Safi's LLM cost work and evals are relevant, but space went to Azure and
  governance evidence).
- Research section (both MILA papers) cut.
- Accenture: Gemini dashboard chatbot, Gemini TTS PoC, Langfuse observability, monitoring/alerting
  bullet (cut for space). SWE: Step Functions, CDK/CloudFormation, DynamoDB indexes.
- Cold-Chain: agentic pipeline and 116-test bullets. Clinic Ops: caching, MCP-only bullet (merged),
  584-test bullet.

## Gaps vs the posting
- Staff-level: about 3 years full time; no formal tech-lead or staff title.
- "Ship production systems at scale": the strongest scale evidence is bank-wide (33% fewer failing
  pipelines) and bank call-center work; the solo systems are small in user count.
- Event-driven design is shown through AWS (Kinesis, SQS), not Azure-native eventing (Event Grid,
  Service Bus), which the mega resume does not mention.

## Please sanity-check
- Summary: "shipping production LLM applications and agent workflows on Azure and AWS, including for
  major U.S. banks" is a synthesis of the Accenture bullets; the fraud agent's production status is
  not stated in the source.
- Clinic Ops Azure bullet drops "azd" and "fail-closed multi-tenant isolation" for space; wording
  otherwise follows the source.
- SWE bullet 2 merges the Fargate/REST API and Lambda/SQS source bullets.

## Questions for Aly
- none (decided: applied despite Toronto hybrid; Aly is in Montreal, so confirm relocation/commute
  before submitting)
