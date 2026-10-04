# Changelog: Google DeepMind, Research Developer, Frontier AI Incubation

Verification: 1 page, fill 0.965, skills 5 lines (no category wraps), no LaTeX errors; only the
0.56pt overfulls the reference resume also has. PNG inspected (no orphans, dates aligned).

## Emphasized
- Research-engineer framing: Research section kept (both MILA projects, 2 bullets each) because the
  role is research-focused (publishing, partner universities, "scientific analysis").
- Evaluation methodology (their 4th responsibility): billing eval framework vs manual process,
  LLM-as-a-judge for summaries, Safi judge 77% to 96%, cross-language LLM eval research.
- Agentic workflows and RAG (preferred quals): router/parallel-subagent billing system, LangGraph
  plan-execute fraud agent with RAG.
- Inference optimization / serving: Safi (prompt caching, model routing, context compaction, 61.7%
  savings at 100% quality), Llama FastAPI service on a real-time Kinesis/Flink stream.
- Concept-to-deployment (min qual): "owned it end to end into production" on the billing system.

## Close-call cuts
- claude-kit cut (agentic-workflow signal, but no room). Cold-Chain cut (product/ops, weaker fit).
- **Leagueware cut** (default-eligible): no room, and least relevant to a frontier-AI research role.
- Accenture: Gemini 2.5 Pro conversational TTS prototype (closest thing to multimodal), Gemini
  dashboard chatbot, monitoring bullet. Clinic Ops compressed to 1 bullet.
- Education: "research areas: NLP, reinforcement learning" dropped (caused a date collision).
- Skills: Bash, C#, Spanish, IaC tooling, pgvector, AWS ML Engineer cert (in progress).
- No age-rule overrides.

## Gaps vs the posting
- No foundation-model training or fine-tuning (RLHF/RLAIF, SFT, PEFT) in the mega resume; RL only
  as M.Sc. coursework/research area. This is the largest gap for a role that "designs, trains".
- No large-scale training or serving infrastructure (TPU/GPU clusters, JAX); PyTorch only via research.
- No C++ (Python satisfies the min qual).
- Personalization, user modeling, agentic memory and multimodal reasoning: none directly.
- No published papers (research is project write-ups / a LinkedIn post).
- Comp posted: $185k-$190k CAD + 15% bonus + equity.

## Please sanity-check
- Eval bullet appends "turning ambiguous stakeholder requirements into measurable success criteria",
  taken from the separate "Partnered with enterprise stakeholders" bullet.
- Summary "taking LLM agents, RAG, and evaluation frameworks from prototype to production in Python"
  is a synthesis, not a mega-resume line.
- Clinic Ops: "took four production LLM workflows ... live with a Cairo surgeon" merges the
  workflows bullet with the live-deployment bullet.

## Questions for Aly
- None blocking. Consider whether to address the fine-tuning/training gap in the application
  (RL coursework at MILA is the only adjacent evidence).
