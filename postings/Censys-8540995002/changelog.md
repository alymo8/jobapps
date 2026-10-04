# Changelog: Censys, Senior AI/LLM Engineer (SOC/TH team)

Resume: `Aly_Mohamed_Hussein_Resume_Censys.tex` / `.pdf` (source: `mega-resume-v1.5.tex`)

## Emphasis
- Led with what the posting asks for: Python LLM/RAG services, evaluation and regression testing for LLM
  pipelines, prompt engineering, and guardrails and safety checks for sensitive data.
- Accenture AI Engineer (4 bullets): fraud-detection RAG agent for a U.S. bank (the closest thing to a security
  domain), the Llama FastAPI call-summary service with Langfuse tracing, the LLM-as-a-judge degradation framework
  (maps to "automated regression testing"), and the Azure agentic billing system with its Langfuse eval benchmark.
- Kept the Research section (privacy-preserving NLP) for "secure and responsible AI / prevent data exposure":
  PII leakage, membership-inference attacks, prompt engineering.
- Projects: Clinic Ops (production LLM workflows behind an AI gateway, prompt-injection and hallucination
  guardrails), Safi (evals as the honesty mechanism, LLM judge catching a regression), claude-kit (AI tools as
  a force multiplier, which is one of the posting's "sets you apart" items).
- Skills: 5 lines. Langfuse moved into Frameworks & Tools; added prompt-injection hardening.

## Close-call cuts
- **Leagueware cut** (the prompt keeps it by default). There was no room once Research and three AI projects were
  in, and it is the least relevant to an AI/LLM security role. Restore it in place of claude-kit if you prefer.
- Cold-Chain Dispatch cut: no LLM content, so it is weaker than Safi for this role.
- Medical LLM accuracy research cut: the privacy research fits the security angle better.
- Gemini Vertex AI dashboard chatbot cut, along with the Clinic Ops MCP server and Azure IaC bullets.
- No age-rule override.

## Gaps vs. posting
- Posting asks for 5+ years of SWE experience including 2+ years on AI features. You have about 3 years full-time
  (since September 2023) plus the Ericsson internship, and about 1.75 years in the AI Engineer role.
- RAGAS and LangSmith are not in the mega resume. Your eval experience is Langfuse plus custom LLM-as-a-judge.
- No LLM fine-tuning, embedding-model, or vector-search work beyond RAG (pgvector appears only in the mega
  skills list).
- No cybersecurity, SOC, or threat-intel domain experience. The closest are fraud detection for a bank and the
  clinical data-residency work.
- No low-latency or in-browser model optimization.

## Accuracy check requests
- Summary says "shipping production LLM, RAG, and agentic systems". The fraud RAG agent is not explicitly
  described as production in the mega resume. Production RAG/LLM is supported by the call-summary service and
  Clinic Ops; the agentic part is supported by the billing system.
- Billing bullet merges three source bullets (system, production ownership, Langfuse eval framework).
- Call-summary bullet merges the Llama FastAPI bullet with the Langfuse observability bullet.
- SWE bullet merges the 33% Jenkins bullet with the Fargate and Lambda bullets.

## Build
- fill: 0.967, skills_lines: 5, pages: 1, no errors (only sub-1pt overfull warnings, which are not visible)

## Questions for Aly
- none
