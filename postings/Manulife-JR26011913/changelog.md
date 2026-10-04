# Changelog: Manulife, Applied AI Engineer – GenAI Systems (JR26011913)

Resume: `Aly_Mohamed_Hussein_Resume_Manulife.tex` / `.pdf` (1 page, fill 0.965, skills_lines 5, ok true; PNG visually checked). Only residual overfulls are the 0.56pt template-wide ones, which don't reach the margin.

## Emphasized
- The posting's GenAI patterns: RAG (fraud agent), agentic multi-step orchestration (LangGraph plan-execute, router agent with parallel subagents), structured extraction/summarization (Clinic Ops on Anthropic structured outputs, call summaries), tool use and MCP in Skills.
- The "high bar for evaluation" section: LLM-as-a-judge summary eval with degradation detection, Langfuse eval benchmarking the billing agent against the manual process, and Safi's eval-backed quality gate (judge agreement 77% to 96%, regression caught).
- Production readiness and governance: monitoring/alerting bullet, owned production deployment, guardrails (hallucination flags, strict schemas, human-in-the-loop review), payload minimization and audit logging, cost/latency trade-offs (Safi caching and routing), ADRs as the decision log.
- Privacy research kept (data minimization, PII leakage) since the posting stresses privacy and sensitive data. Finance link: two U.S. bank engagements.

## Cut (close calls)
- Medical-accuracy-across-languages research cut for space. It's relevant to GenAI evaluation, and Safi or Leagueware could be swapped out for it.
- Cold-Chain Dispatch cut for space (its runbooks, ADRs and production cutover match "contribute to runbooks"). claude-kit also cut.
- Leagueware kept at 1 bullet. No age-rule override.
- Accenture: the dashboard chatbot, Gemini voice PoC and Langfuse-tracing bullets were cut. SE role: DynamoDB, Step Functions and CDK bullets cut.

## Gaps (for a cover letter or interview)
- **4–7 years in applied DS/ML**: about 4 years professional in total, most of it engineering rather than classical data science.
- **Classical ML** (forecasting, classification, anomaly detection, optimization, backtesting/out-of-time testing, feature engineering at scale): nothing post-2022 in the mega resume. scikit-learn appears only in pre-age-rule course projects. The DistilBERT classifier from the research is the closest match.
- **Spark/Databricks, TensorFlow**: none. PyTorch is covered through the research.
- **Model risk governance, drift monitoring, model registry, automated retraining**: no explicit experience. The closest are operational monitoring and LLM degradation detection.
- **Finance/Treasury/Actuarial/IFRS-17 domain**: none. Banking exposure is fraud and call-centre, not finance or actuarial.
- **Vector DB / embedding strategy / Semantic Kernel**: only RAG (pgvector) and LangGraph.
- **Mentoring junior scientists**: no formal evidence.

## Sanity-check wording
- I merged the billing-agent bullet with the Langfuse benchmark bullet ("owned its production deployment and a Langfuse eval benchmarking it against the manual process").
- The summary now says "shipping production GenAI end to end". That rests on the billing system's production deployment and the Clinic Ops live deployment.
- Research bullet 1 now reads "synthetic clinical-text pipeline that prevents PII leakage", compressed from "preserves label distribution while preventing PII leakage".

## Questions for Aly
- none (gaps above are recorded, not blocking)
