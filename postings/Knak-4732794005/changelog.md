# Changelog: Knak, Senior Software Developer, AI Agents

Verification: 1 page, fill 0.965, skills_lines 5 (no category wraps), no LaTeX errors; only the
0.56pt overfulls the reference resume also has. PNG inspected (no orphans, no collisions).

Eligibility: Remote - Canada; base $135K-$170K CAD.

## Emphasized
- The two halves of the role, agent harness and evals: summary leads with "production LLM agents in
  Python and the evals that measure them". Accenture: router agent with parallel subagents (billing),
  Langfuse evaluation framework benchmarked against the manual process, LLM-as-a-judge degradation
  detection, LangGraph plan-execute fraud agent, Langfuse tracing.
- Tool calling, structured outputs, guardrails, failure handling: Clinic Ops (Anthropic structured
  outputs behind an AI gateway, MCP server/tools, hallucination and prompt-injection guardrails, typed
  provider-failure taxonomy, smoke harness, TDD).
- Regression tracking and model comparison: Safi (provider abstraction across Anthropic/OpenAI/Gemini,
  revised LLM judge 77% -> 96% agreement while catching a real routing regression).
- AWS Lambda, DB tuning: SWE role keeps the Python Lambda/SQS bullet and the DynamoDB secondary-index
  bullet (closest analogue to "tune MySQL queries and indexing").
- Vue (nice-to-have full-stack): Leagueware kept with 2 bullets; Vue.js and Node.js in skills.
- GitHub Actions / TDD / Docker / Kubernetes in skills, backed by projects and Ericsson.

## Close-call cuts
- Research section dropped (both MILA papers) for space; M.Sc./MILA stays in summary and education.
- Cold-Chain Dispatch cut entirely (strongest non-AI project, but less relevant to agent internals
  than Clinic Ops, Safi and claude-kit).
- Accenture: Gemini dashboard chatbot, Gemini TTS PoC, monitoring/autoscaling bullet, and the
  stakeholder bullet (folded "owned its production deployment" into bullet 1). React/TypeScript
  operator frontend detail removed from the billing bullet.
- SWE: the "15 minutes per pipeline run" detail, Step Functions, CDK. Ericsson: one bullet.
- No age-rule overrides (Vodafone Node.js chatbot work stays cut).

## Gaps vs the posting
- 6+ years required: about 3 years full-time plus an internship.
- No PHP/Laravel, no MySQL (PostgreSQL and DynamoDB instead), no LangSmith (Langfuse instead), no
  AWS Bedrock in the mega resume.
- Node.js: listed in skills only; no Node.js bullet on this page (the only Node.js work is the cut
  Vodafone internship).
- Mentoring / leading code reviews: nothing explicit in the mega resume beyond "led" microservices
  and the Leagueware back end.

## Please sanity-check
- Summary "building production LLM agents in Python and the evals that measure them" is a synthesis
  of the Accenture and project bullets, not a mega-resume line.
- Clinic Ops bullet 1 merges the live-deployment, four-workflows and MCP-server bullets; bullet 2
  merges guardrails, failure taxonomy, smoke harness and the 584-test TDD line.
- React stays in skills though its bullet detail (billing operator frontend) was trimmed.

## Questions for Aly
- none
