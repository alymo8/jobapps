# Changelog: WorkOS, Applied AI Engineer (US & Canada, Remote)

Verification: 1 page, fill 0.969, skills_lines 5 (no category wraps), no LaTeX errors; only the
0.56pt overfulls the reference resume also has. PNG inspected (no orphans, no collisions, dates aligned).

Source of facts: `mega-resume-v1.5.tex`. Location: remote US/Canada; not a gap.

## Emphasized
- "Idea to production through an iteration cycle with real users": summary leads with it; Clinic Ops
  (customer discovery that repositioned v1, live with a surgeon reporting ~20 min saved per visit) and
  Cold-Chain (manual WhatsApp-and-paper process replaced, used daily, built in ~4 weeks).
- LLM APIs, tool-calling, MCP (nice-to-have): Anthropic structured outputs behind an AI gateway plus the
  MCP server; MCP and tool use in skills.
- Failure modes and observability ("not just whether the demo works"): Clinic Ops failure-modes bullet
  (provider-failure taxonomy, smoke harness, prompt-injection isolation, human-in-the-loop), Langfuse
  tracing + LLM-as-a-judge degradation detection, Cold-Chain "agent output as untrusted" bullet.
- Replacing multi-step manual processes with orchestrated agents: Accenture billing router/subagent
  system (owned production deployment), support-call summarization (customer support domain, maps to
  their AI support bots), internal Gemini chatbot (internal tooling).
- Sandboxed coding harness agent / internal AI infra: claude-kit (agent constraints, worktree isolation,
  spec-plan-build with gated merges). RAG: fraud agent bullet.
- Research section dropped (less relevant than shipped-product evidence for this role; M.Sc./MILA kept
  in summary and education).

## Close-call cuts
- Safi (multi-provider LLM layer, evals) cut for space; claude-kit and Cold-Chain fit "coding harness"
  and "replace manual workflows" better.
- Accenture: stakeholder/requirements bullet, Gemini TTS PoC, monitoring (Splunk/New Relic/CloudWatch).
  Billing Langfuse evaluation merged into the billing bullet. SWE: Fargate/Lambda/DynamoDB bullets.
- Leagueware kept at one bullet. No age-rule override.

## Gaps vs the posting
- No direct Slack/GitHub/CRM integration bots or GTM tooling in the mega resume.
- Customer-facing AI products: Clinic Ops is customer-facing but single-clinic scale; no large-user-base
  AI product.
- Embeddings: RAG appears (fraud agent, pgvector in mega skills) but no dedicated embeddings/retrieval
  architecture bullet.
- Sandboxed code execution specifically: claude-kit isolates via git worktrees, not a runtime sandbox.

## Please sanity-check
- Billing bullet: "built and owned the production deployment" merges "drove development end-to-end and
  owned its production deployment" with the Langfuse benchmark bullet.
- Clinic Ops: "prompt-injection isolation" compresses "clinic instructions isolated in the system channel";
  "SHA-256-keyed brief caching" for "caching AI briefs against a SHA-256 fingerprint of the prompt".
- SWE bullet merges the 33% failing-pipeline and ~15 min run-time bullets into one.

## Questions for Aly
- none
