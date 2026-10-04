# Changelog: Shakudo, Senior Forward Deployed Engineer (Toronto, onsite)

Verification: 1 page, fill 0.965, skills_lines 5 (no category wraps), no LaTeX errors; only the
0.56pt overfulls the reference resume also has. PNG inspected (no orphan words, no collisions).

Source of facts: `mega_resume.tex` does not exist in the repo; used `mega-resume-v1.5.tex`.

## Emphasized
- What the posting asks for: production RAG, agents and evals, data pipelines, regulated industries, and
  deployments in difficult environments. The summary leads with "customer problems into production RAG,
  agentic, and streaming data systems in banking, healthcare, and enterprise settings".
- Customer embedding (ProServe): Accenture stakeholder bullet first; both client systems framed as
  "sole engineer for a paying client"; customer discovery; embedded with a non-technical owner.
- RAG/agents/evals: fraud agent (LangGraph plan-execute, RAG, 96%), router + parallel subagents on Azure
  AI Foundry, Langfuse eval framework, LLM-as-a-judge summary evals.
- Data engineering: the Kinesis/Flink real-time transcript streaming pipeline; Kinesis and Flink in Skills.
- Regulated / private deployments: U.S. bank work (fraud, call summaries, CI/CD); the Clinic Ops Azure
  UAE North PDPL data-residency deployment with private networking, Key Vault managed identity, IaC.
- Kubernetes / infrastructure: restored the Ericsson Kubernetes/Docker deployment bullet; IaC with
  CloudFormation, CDK and Bicep; production monitoring/alerting for the "production support" duty.
- Research section dropped (as in other FDE resumes) to make room for the client systems; Education
  compressed and placed before Projects.

## Close-call cuts
- claude-kit and Safi cut for space; the client systems are stronger evidence for a deployment role.
- Research (both MILA papers) cut, although the medical-LLM evaluation paper touches "evaluations".
- Accenture: Gemini dashboard chatbot, Langfuse observability bullet, Gemini TTS PoC. SWE: Step Functions,
  DynamoDB indexing. Clinic Ops: MCP server bullet, prompt-injection/hallucination mitigation (MCP kept in
  Skills and the project heading). Cold-Chain: user-centred design bullet, 116-test bullet.
- No age-rule override.

## Gaps vs the posting
- Seniority: posting asks for 8+ years in software/data/platform/AI engineering; Aly has about 3 years
  full time (plus internships). This is the main gap.
- 3+ years building LLM/AI applications: roughly 1.75 years at Accenture (AI Engineer since Jan 2025)
  plus M.Sc. research and solo projects.
- 5+ years Kubernetes: only the Ericsson internship (Kubernetes/Docker deployment) and Docker in projects;
  no production Kubernetes operation, no on-prem or air-gapped deployments.
- Data engineering: one streaming pipeline (Kinesis/Flink); no orchestration/transformation tooling
  (Airflow, dbt, Spark) in the mega resume.
- Go and Scala not in the mega resume (Python, Java, TypeScript cover the language requirement).
- Location: the role is onsite in Toronto; Aly is in Montreal (relocation/commute question).

## Please sanity-check
- Summary "in banking, healthcare, and enterprise settings" is a synthesis: banking = U.S. bank client,
  healthcare = Clinic Ops, enterprise = the engineering consulting billing client.
- Billing bullet now says subagents "automate manual billing verification steps" (source: "decide on and
  automate the previously manual billing verification steps").
- SWE bullet merges the CI/CD bullet with Fargate/Lambda deployment and CloudFormation/CDK provisioning
  (three separate source bullets).

## Questions for Aly
- The role is onsite in Toronto and asks for 8+ years; built the resume anyway. Confirm you are willing to
  relocate/work onsite in Toronto and want to apply despite the seniority gap.
