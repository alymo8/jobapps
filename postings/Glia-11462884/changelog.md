# Changelog: Glia, Senior Software Engineer - Conversational AI (Python)

Resume: `Aly_Mohamed_Hussein_Resume_Glia.tex` / `.pdf` (source: `mega-resume-v1.5.tex`)

## Emphasis
- Summary leads with production LLM agents in Python for major U.S. banks (Glia sells to banks and credit unions),
  real-time call pipelines, RAG and LLM-as-a-judge evals.
- Accenture AI Engineer (5 bullets), ordered for a real-time voice/conversational banking agent: the real-time
  transcript pipeline (Kinesis/Flink) call-summary service for a U.S. bank; the Gemini 2.5 Pro + text-to-speech
  conversational support-agent PoC (closest thing to voice AI); the LLM-as-a-judge hallucination eval framework
  (harness/evaluation); the fraud agent grounded via RAG (grounding, banking); the router/subagent billing system with
  production ownership and Langfuse benchmark (agentic flows, reliability).
- Clinic Ops (3 bullets): maps to "guardrails, grounding, policy enforcement": hallucination/prompt-injection
  controls, strict schemas, human-in-the-loop gate, AI gateway, MCP tools, provider-failure taxonomy, prompt caching.
- claude-kit (1 bullet): "AI-assisted development daily, standards for verifying agent-generated code".
- Skills: 5 lines; LLMs & Agents mirrors the posting (tool use, RAG, structured outputs, evals, Claude Code).

## Close-call cuts and overrides
- **Age-rule override: Vodafone included** (1 bullet). The posting is explicitly a Conversational AI role, and the
  Vodafone chatbot (NLU with LUIS, 43M customers) is the prompt's own named example of a valid override.
- **Safi cut** for space, though it fits "tradeoffs between latency, cost, and quality" and evals (judge 77% to 96%).
  Swap it in for claude-kit or Vodafone if you prefer.
- **Leagueware cut** (default-eligible): no room and no fit with conversational AI.
- Research section dropped for space; Cold-Chain Dispatch cut (no LLM work; its "agent output treated as untrusted"
  bullet would also fit the verify-agent-code ask). Accenture monitoring/alerting bullet cut for space.
- claude-kit's second bullet (agent constraints, 64 tests) cut; its git-worktree isolation folded into bullet 1.

## Gaps vs. posting
- **Senior / tech-lead or mentorship experience:** about 3 years full-time; "Led" microservices work at Accenture but
  no formal tech-lead or mentoring role in the mega resume.
- **Real-time voice AI latency work:** no ASR/STT, voice latency profiling or millisecond-level pipeline optimization;
  the closest are the TTS conversational PoC and the real-time transcript streaming pipeline.
- **Agent SDKs** (Claude Agent SDK / OpenAI Agents SDK) not explicitly in the mega resume (LangGraph, Anthropic API,
  OpenAI/Gemini SDKs are).
- Stack: no Elixir, DataDog, Argo CD, Terraform or Kafka (has Kinesis, Jenkins, CloudFormation/CDK/Bicep, Kubernetes).
- Posting requires 2 h/day overlap with Pacific Time (9-11 AM PT = 12-2 PM ET from Montreal): not a gap.

## Accuracy check requests
- Call-summary bullet: "live agent recommendations" condenses "real-time recommendations to customer support associates".
- Fraud bullet: "grounding fraud alerts via RAG" rephrases "augmenting fraud alerts via RAG".
- Clinic bullet 2: "regulated clinical setting" (source says "clinical setting"; regulation inferred from PDPL data residency).
- claude-kit: "a Claude Code plugin for verifying agent output" is my framing of "agent constraints for reliability
  over autonomy" plus the test-first merge gate / AI review / human approval flow.
- Vodafone: "extending its journey by 50%" is from "extended the internal cognitive chatbot journey by 50%".

## Build
- fill: 0.961, skills_lines: 5, pages: 1, no errors (only 0.56pt overfull warnings, not visible)

## Questions for Aly
- none (note: the real apply URL was not found; posting.md has the BuiltIn Ottawa link only)
