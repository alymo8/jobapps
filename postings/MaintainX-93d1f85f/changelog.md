# Changelog: MaintainX, Senior AI Platform Developer (Work Intelligence), Toronto / Montreal (Hybrid, remote-eligible)

Verification: 1 page, fill 0.965, skills_lines 5 (no category wraps), no LaTeX errors; only the
0.56pt overfulls the reference resume also has. PNG inspected (no collisions, dates and rules aligned).

Source of facts: `mega-resume-v1.5.tex` (the master resume).

## Emphasized
- Platform/backend framing: the posting wants shared AI-platform backend services, LLM integration into
  production workflows, observability/incident response, runtime cost optimization, and CI/CD/IaC.
  The summary leads with "Python backend services and LLM-integrated production systems ... observability,
  evals, and LLM cost optimization".
- Accenture AI Engineer: FastAPI LLM service on a Kinesis/Flink stream (async/distributed processing),
  Azure agentic billing system with production deployment ownership, Langfuse tracing + LLM-as-a-judge evals,
  Splunk/New Relic/CloudWatch monitoring, alerting and autoscaling (production reliability), fraud agent.
- Accenture SWE: sync/async microservices for the bank's CI/CD pipeline (shared infrastructure, CI/CD),
  Fargate/Lambda/SQS deployment provisioned with CloudFormation and CDK (IaC).
- Projects: Safi first (direct hit on "optimizing AI runtime performance and cost efficiency": caching, model
  routing, provider abstraction, FastAPI streaming recorder, 61.7% savings); Clinic Ops for the AI gateway
  (provider swap, audit logging) and Bicep IaC with CI; Leagueware kept.
- Research section dropped: a backend/platform role values the production systems more than the MILA papers.
  Education compressed and placed before Projects.

## Close-call cuts
- Cold-Chain Dispatch cut for space (its Postgres trigger/advisory-lock race fix and silent-backup hardening
  were relevant to reliability). claude-kit cut.
- Clinic Ops: SHA-256 brief caching and provider-failure taxonomy / smoke harness bullet (relevant to cost and
  reliability), MCP server bullet (MCP kept in heading/skills).
- Accenture: Gemini dashboard chatbot, Gemini TTS PoC, stakeholder bullet. SWE: DynamoDB indexing, Step Functions.
- No age-rule override.

## Gaps vs the posting
- 5+ years Python backend: Aly has about 3 years full time (Sept 2023 onward, plus the 2022 Ericsson
  internship), and the SWE role was mostly Java/Spring Boot with some Python Lambda. This is the main gap.
- Incident response: monitoring/alerting is on the resume, but no explicit on-call or incident-response
  ownership is in the mega resume.
- Terraform not in the mega resume (IaC is CloudFormation, CDK, Bicep).
- Location: none (Aly is Montreal-based and open to hybrid; Montreal is a listed location).

## Please sanity-check
- SWE first bullet merges two source bullets (33% fewer failing pipelines; sync/async microservices cutting
  ~15 minutes per run).
- SWE second bullet merges three source bullets (Fargate, Lambda/SQS, CloudFormation/CDK).
- Langfuse bullet merges the observability bullet with the LLM-as-a-judge summary-evaluation bullet.
- Safi "written solo" (source: "wrote essentially all of it solo").
- Summary "async pipelines" synthesizes the async microservices, SQS processing, and Kinesis/Flink stream.

## Questions for Aly
none
