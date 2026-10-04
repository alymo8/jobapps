# Changelog: Tali AI, Senior/Staff Applied AI Engineer (Toronto, Hybrid)

Verification: 1 page, fill 0.965, skills_lines 5 (no category wraps), no LaTeX errors; only the
0.56pt overfulls the reference resume also has. PNG inspected (no orphans, no collisions, dates aligned).

Source of facts: `mega-resume-v1.5.tex`. Location: Toronto hybrid; Aly will relocate / work hybrid
(profile.md), so not a gap.

## Emphasized
- Evaluation (their #1 theme): LLM-as-a-judge summary evals with a feedback loop leads Accenture;
  Langfuse tracing and the billing-agent evaluation benchmark; Safi's judge revision (77% to 96%
  agreement while still catching the real routing regression) answers "know when a judge is fooling you".
- Model routing / "which model serves which request": Safi planner over routing and caching across
  three providers, with cost/quality/harm scored separately.
- Clinical domain and agents: Clinic Ops (four production LLM workflows on Anthropic structured
  outputs, surgeon-reported 20 min saved per visit, hallucination/prompt-injection mitigation,
  human-in-the-loop, provider-failure taxonomy and smoke harness); router/subagent and LangGraph RAG agents.
- Audio-adjacent: real-time transcript streaming pipeline (Kinesis/Flink) for call summaries.
- Both MILA research entries kept (medical LLM evaluation; synthetic clinical data, which maps to
  "generate what you can" when ground truth is missing). Research placed as its own section after Projects.

## Close-call cuts
- claude-kit, Cold-Chain Dispatch and Leagueware cut for space (Leagueware cut flagged per the rule);
  the healthcare/eval items fit this posting better.
- Accenture: Gemini/Vertex AI dashboard chatbot (GCP still in skills/role line), stakeholder bullet,
  Gemini TTS conversational PoC, monitoring (Splunk/New Relic/CloudWatch). SWE: Fargate/Lambda/SQS bullet.
- Clinic Ops: MCP server bullet, Azure PDPL deployment, caching bullet. No age-rule override.

## Gaps vs the posting
- **5+ years in production ML/applied AI**: about 3 years full time (Sep 2023 on), AI-focused since
  Jan 2025; below the floor, and Senior/Staff levelling will weigh this.
- **Speech recognition / ASR, WER/speaker error rates, audio quality**: none. Closest is consuming a
  real-time transcript stream and a TTS PoC (not shown).
- **Fine-tuning, warehouse slicing, staged rollout / weighted routing in production**: no direct
  production evidence (Safi routing is a personal product, not at scale).
- **Human review / annotation programs**: only the human-in-the-loop draft gate in Clinic Ops.
- GCP Cloud Run: not in the mega resume (Vertex AI/Gemini is).

## Please sanity-check
- Accenture bullet 2 says "live agent recommendations" for "real-time recommendations to customer
  support associates" (agent = support agent) and attaches the Langfuse tracing to that service.
- Safi bullet 1 compresses the workload-aware planner bullet (profiler/detectors dropped).
- Accenture billing bullet merges the agentic system and its Langfuse evaluation framework.

## Questions for Aly
- none
