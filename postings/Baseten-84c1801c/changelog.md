# Changelog: Baseten, Forward Deployed Engineer

Verification: 1 page, fill 0.962, skills_lines 5 (no category wraps), no LaTeX errors; only the
0.56pt overfulls the reference resume also has. PNG inspected (no orphans, no collisions).

Eligibility: posting lists Toronto and Montreal among its locations, so Montreal is eligible.
Range $165K-$330K USD + equity. The form asks about US work authorization and sponsorship; with a
Montreal location these are about US roles, answer as appropriate at /apply.

## Emphasized
- The posting's lifecycle "problem framing -> evaluation -> production deployment -> monitoring":
  summary leads with it; Accenture bullets go stakeholder requirements -> agentic system -> owned
  Azure deployment, then Langfuse evaluation framework, LLM-as-a-judge degradation detection, and
  monitoring/alerting/autoscaling.
- Python strongly preferred: Python first in skills, FastAPI services (Llama call-summary service, Safi).
- "Quality, latency, and cost outcomes": added Safi (LLM cost layer; 61.7% savings at 100% quality
  agreement, evals as the quality guarantee) in place of claude-kit.
- Customer-facing FDE shape: Clinic Ops (customer discovery, live with a surgeon) and Cold-Chain
  (paying client, production cutover) as "sole engineer for a paying client".
- Education compressed to two lines; Research section dropped.

## Close-call cuts
- claude-kit cut (usual shortlist): internal dev tooling, less relevant than Safi's cost/quality story.
- Research section dropped (both MILA papers); M.Sc./MILA stays in summary and education. Familiarity
  with the ML lifecycle rests on the M.Sc. and the eval work rather than a research entry.
- Cold-Chain cut to 1 bullet; Clinic Ops caching/smoke-harness bullet and hallucination bullet cut;
  Safi's "revised LLM judge 77% -> 96%" bullet cut for space.
- Accenture: Gemini dashboard chatbot, Gemini TTS PoC, Langfuse observability bullet. SWE: reduced to
  one bullet (Fargate/Lambda, CDK, DynamoDB cut). Ericsson: one bullet.
- No age-rule overrides.

## Gaps vs the posting
- No model-serving / inference-optimization work (GPU serving, TensorRT, vLLM, latency tuning of
  model servers), which is Baseten's core; the closest is LLM cost optimization (Safi) and
  autoscaling of production workloads at Accenture.
- No model training or fine-tuning in production; ML-lifecycle familiarity is M.Sc. coursework/research.
- No formal pre-sales / solution engineering experience; client-facing work is stakeholder
  requirements at Accenture and the two paying-client projects.

## Please sanity-check
- Summary "taking production LLM systems in Python from ambiguous client goals through evaluation,
  deployment, and monitoring" is a synthesis of the Accenture bullets, not a mega-resume line.
- Safi: "written solo" compresses the source's "wrote essentially all of it solo".
- Accenture bullet 1 says "client stakeholders"; source says "enterprise stakeholders" on the client
  billing engagement.
- PyTorch stays in skills without a bullet behind it on this page (Research section dropped).

## Questions for Aly
- none
