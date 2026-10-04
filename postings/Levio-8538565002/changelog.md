# Changelog: Levio, Conseiller.ere ML/IA, Montreal

Verification: 1 page, fill 0.966, skills_lines 5 (no category wraps), no LaTeX errors; only the
0.56pt overfulls the reference resume also has. PNG inspected.

Source of facts: `mega-resume-v1.5.tex`. Language: the posting is in French; the resume skill has no
language rule, so the resume is in English (French bilingual listed under Languages).

## Emphasized
- Full ML lifecycle in production (design, deploy, operate): summary; Llama FastAPI inference service
  on Kinesis/Flink; billing system production deployment on Azure ML / AI Foundry.
- Monitoring of AI systems in production (posting: performance, drift, reliability): LLM-as-a-judge
  degradation detection, monitoring/alerting/autoscaling (Splunk, New Relic, CloudWatch) plus Langfuse
  tracing.
- RAG / LLM systems: fraud agent with RAG (LangGraph plan-execute).
- Cost and latency optimization of AI workloads: Safi (token spend cuts, 61.7% realized savings).
- Privacy, security, responsible AI: privacy-preserving NLP research (PyTorch, DistilBERT, PII
  leakage), Clinic Ops gateway (payload minimization, audit logging), PDPL data residency,
  prompt-injection/hallucination mitigation.
- PyTorch and scikit-learn in Skills (explicitly required by the posting).
- CI/CD: bank Jenkins CI/CD microservices (33% fewer failing pipelines); IaC with CloudFormation/CDK.

## Close-call cuts
- Research: medical LLM accuracy across languages (bias/responsible AI angle) cut for space.
- Leagueware cut for space (flagged per the prompt's named-exception rule); Cold-Chain and claude-kit
  cut in favour of Safi (cost optimization) and Clinic Ops (privacy/compliance).
- Accenture: Gemini dashboard chatbot, Gemini TTS PoC, stakeholder bullet. SWE: DynamoDB indexes,
  Step Functions.

## Gaps vs the posting
- 6+ years of engineering with 3+ in AI/ML: Aly has about 3 years full time (plus internships), about
  2 in a titled AI role.
- TensorFlow: not in the mega resume; left out.
- scikit-learn appears in the mega resume only in pre-2022 course projects (not on the page); it is
  listed in Skills because the posting requires it.
- Classical ML training pipelines, feature engineering, model versioning, drift/bias monitoring, and
  CI/CD with automated rollback for ML: no direct evidence beyond LLM eval/monitoring and general
  CI/CD.
- Mentoring junior ML engineers: no explicit evidence in the mega resume.

## Please sanity-check
- Summary "deploying and operating production ML and generative AI systems (LLM pipelines, RAG,
  agents, evals)" is a synthesis; the fraud agent's (RAG) production status is not stated in the
  source.
- "FastAPI inference service" rewords the source's "Llama-based LLM FastAPI application".
- Accenture monitoring bullet merges the monitoring/alerting/autoscaling bullet with the Langfuse
  observability bullet.
- SWE bullet 2 merges CloudFormation/CDK provisioning with the Lambda and Fargate deployment bullets.

## Questions for Aly
- none (decided: resume in English since the skill has no language rule; a French version could help
  for a French-language Quebec posting)
