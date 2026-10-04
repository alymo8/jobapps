# Changelog: Morgan Stanley, AI Development Solution Engineering Specialist (Hybrid), PT-JR041698

Verification: 1 page, fill 0.966, skills_lines 5 (no category wraps), no LaTeX errors; only the
0.56pt overfulls the reference resume also has. PNG inspected.

Source of facts: `mega-resume-v1.5.tex` (stands in for `mega_resume.tex`).

Eligibility: Montreal, Quebec, hybrid; French and English required (both on the resume as bilingual).

## Emphasized
- Business partnership + agentic delivery (the role's core): summary and first Accenture bullet lead
  with translating stakeholder requirements into success criteria and owning production deployment.
- Orchestration: router agent with parallel subagents, LangGraph plan-execute fraud agent with RAG.
- Evaluation frameworks: Langfuse benchmark vs the manual process, LLM-as-a-judge summary evals
  (model-based assessment), Safi's judge revision that still caught a routing regression (regression testing).
- Governance/auditability (human approvals, audit records, privacy): Clinic Ops AI gateway with audit
  logging, human-in-the-loop approval of every draft, PDPL data residency.
- MCP + Claude Code: Clinic Ops MCP server; claude-kit (Claude Code plugin with human-approval and
  decision-verification gates) mirrors "reusable frameworks, best practices" and "agentic coding tools".
- Production ops and cost management: monitoring/alerting bullet, Langfuse tracing, Safi cost layer.
- Data engineering: SQL + PostgreSQL, and DynamoDB (non-relational) via the secondary-index bullet.
- Research section dropped; Education placed before Projects (as in other tailored versions).

## Close-call cuts
- **Cold-Chain Dispatch cut** (usual shortlist) for space; Clinic Ops, claude-kit and Safi map more
  directly to MCP, Claude Code, governance and cost management.
- Research (both MILA papers) cut; the medical-LLM evaluation paper would also support "evaluation".
- Accenture: Llama/Kinesis call-summary bullet (15 min/call), Gemini dashboard chatbot, Gemini TTS PoC.
  SWE: Step Functions PoC (workflow orchestration), CloudFormation, Fargate/Lambda.
- Leagueware kept at one bullet.

## Gaps vs the posting
- **Claude Agent SDK**: not in the mega resume (Anthropic API with tool use and structured outputs, and
  Claude Code plugins, are). Not claimed.
- Codex: no mention in the mega resume; only Claude Code.
- No financial-services employment beyond Accenture's work for major U.S. banks (stated as such).
- "Large-scale data store" beyond DynamoDB/Kinesis is thin; no data-warehouse experience listed.
- Years: about 3 years full time (Sept 2023 onward plus internship), right at the 3-year floor.

## Please sanity-check
- Summary "3 years partnering with business teams to design, deploy, and evaluate production agentic
  systems (Python, MCP, Claude Code)" is a synthesis; the MCP/Claude Code work is in projects, not at Accenture.
- Accenture bullet 2 merges the billing-system and Langfuse eval bullets; "Azure Containers" dropped.
- Accenture bullet 4 merges the LLM-as-a-judge bullet with the Langfuse observability bullet (both are
  the call-summarization app).
- Clinic Ops "prompt-injection isolation" stands for "clinic instructions isolated in the system channel".
- Safi "Cost-management layer ... gated by evals" stands for "cuts token spend ... with quality guaranteed by evals".

## Questions for Aly
- none
