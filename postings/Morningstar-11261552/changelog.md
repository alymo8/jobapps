# Changelog: Morningstar, Senior Software Engineer - Applied AI

Resume: `Aly_Mohamed_Hussein_Resume_Morningstar.tex` / `.pdf` (source: `mega-resume-v1.5.tex`)

## Emphasis
- Summary leads with the posting's own list: MCP tools, RAG, structured outputs, evaluation frameworks, Python/FastAPI,
  TypeScript, AWS, and daily use of agentic coding tools.
- Accenture AI Engineer (5 bullets): the Kinesis/Flink FastAPI call-summary service (data pipelines + LLM inference),
  the LLM-as-a-judge eval framework and Langfuse benchmark (evaluation design), the billing agent with production
  ownership, the fraud RAG agent, and the monitoring/alerting/autoscaling bullet (operating production systems).
- Accenture SWE bullet 2 targets "AWS production deployment and infrastructure-as-code" (Fargate, Lambda/SQS,
  CloudFormation, CDK, DynamoDB indexing).
- Clinic Ops (3 bullets): production structured-output LLM workflows behind an AI gateway, the MCP server and tools,
  prompt-injection/hallucination mitigations (security/privacy judgment), Bicep IaC, and the SHA-256 brief cache (cost).
- claude-kit (2 bullets): evidence for "daily proficiency with agentic coding tools" (Claude Code skills/hooks).
- Skills: 5 lines; LLMs & Agents line mirrors the posting (MCP, RAG, structured outputs, tool use).

## Close-call cuts
- **Leagueware cut** (kept by default in the prompt): no room, and no fit with applied AI.
- **Safi cut** for space, though it fits "cost management" and "evaluation literacy" (LLM judge 77% to 96%). Swap it
  for claude-kit if you'd rather lead with cost/evals than agentic-coding tooling.
- Research section dropped entirely for space (both studies are eval-flavoured; the privacy one would support the
  "security/privacy judgment" line). Cold-Chain Dispatch cut (no LLM work).
- No age-rule override.

## Gaps vs. posting
- **5+ years:** you have about 3 years full-time (plus the Ericsson internship). Senior title; expect this to be the main objection.
- **GraphQL:** nothing in the mega resume. REST only.
- **TypeScript/Node.js:** backed by Clinic Ops / Cold-Chain (Next.js, TypeScript) and the billing React/TS frontend; no standalone Node.js backend service.
- No headless CMS, open-weight model benchmarking (beyond the Llama-based service), or Bedrock/Azure AI inference
  benchmarking. Regulated domain is partly covered (U.S. banks, clinical data under Egypt's PDPL).
- "Data pipeline patterns (idempotency, versioning, staged architectures)" are not shown explicitly.

## Accuracy check requests
- Summary "using agentic coding tools daily": inferred from claude-kit being the default setup across three active repos; the mega resume doesn't say "daily".
- Call-summary bullet merges the Llama FastAPI bullet with the Langfuse observability bullet.
- SWE bullet 1 merges the 33% Jenkins bullet with the roughly 15-minutes-per-run bullet; SWE bullet 2 merges the
  Fargate, Lambda/SQS, CloudFormation/CDK and DynamoDB-index bullets ("REST microservices" from "exposing functionality through REST APIs").
- Clinic bullet 1 "(e.g., extraction, report drafting)" abbreviates "handwritten document extraction" and "clinical report drafting".

## Build
- fill: 0.962, skills_lines: 5, pages: 1, no errors (only 0.56pt overfull warnings, not visible)

## Questions for Aly
- none
