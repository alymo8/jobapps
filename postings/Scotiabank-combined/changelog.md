# Changelog: Scotiabank (incl. Tangerine), combined resume for LinkedIn outreach

Covers Software Engineer (AI Engineer), Scotiabank, req 270579 and Senior AI Engineer, Tangerine, req 274918. This is not an application. The per-posting resumes in `postings/Scotiabank-605446017/` and `postings/Scotiabank-606493117/` are unchanged.

- **Emphasized:** what both roles want: Python microservices, REST APIs, and production LLM/agentic systems (LangGraph, RAG, structured outputs, MCP, evals), framed as banking AI engineering. The fraud detection agent comes first, then contact-center call summarization (both for major U.S. banks), then the LLM-as-a-judge/Langfuse evaluation work and the agentic billing system. GCP/Vertex AI and the text-to-speech support-agent prototype share one bullet. In Projects, Clinic Ops leads (MCP server, structured outputs, prompt-injection hardening). Cold-Chain shows testing, row-level security, and runbooks. Leagueware is kept.
- **Structure:** Summary, Skills, Experience, Education, Projects. Research is dropped, as in both per-posting resumes. Education is compressed. No age-rule override.
- **Differences from the 605446017 (Scotiabank SWE) resume:**
  - Added the MCP server and prompt-injection bullets from Clinic Ops, the Gemini text-to-speech prototype, the stakeholder/success-criteria content (merged into the billing bullet), and the 116-test line in Cold-Chain.
  - Dropped Node.js, Express.js, MongoDB, Linux, CloudFormation, and Bicep from Skills. Added Data & ML (NumPy, Pandas, PyTorch), Vertex AI, structured outputs, and prompt-injection hardening.
  - Dropped the Ericsson Kubernetes bullet and the Clinic Ops Azure deployment bullet.
  - Shortened the Cold-Chain and Leagueware wording.
- **Differences from the 606493117 (Tangerine Senior AI) resume:**
  - Restored Leagueware, which was cut there for space.
  - Merged the stakeholder bullet into the billing bullet. Merged the Gemini prototype into the Vertex AI chatbot bullet.
  - Dropped the Clinic Ops Azure deployment bullet and the Ericsson testing clause.
  - Added Jenkins to Skills. Dropped Azure Bicep and Langfuse from Skills to fit (Langfuse is still in the role title and bullets).
  - Used "customer support call summaries" (the source wording) instead of "contact-center".
- **Close-call cuts:** claude-kit, Safi, the Clinic Ops Azure/Bicep/managed-identity bullet (the closest thing to Tangerine's auth ask), the Accenture monitoring bullet, the DynamoDB index bullet, and Arabic/Spanish.
- **Gaps (union of both postings):** no OAuth 2.0 / OIDC / SAML (Tangerine says it is required), no Redis, no Kafka/RabbitMQ/Pub/Sub (closest are SQS and Kinesis), no Helm, Terraform, Ansible, or ArgoCD, no LangChain/LangSmith/ADK, no Angular, and no recent classical-ML or Scikit-learn work.
- **Sanity-check these:**
  - The billing bullet merges three source lines: the agentic system, the stakeholder/success-criteria work, and the Langfuse benchmark against the manual process.
  - The LLM-as-a-judge bullet merges in the Langfuse tracing bullet. Both come from the call-summarization app.
  - The Vertex AI bullet combines the internal Gemini chatbot with the Gemini 2.5 Pro text-to-speech proof of concept.
  - The summary's "for major U.S. banks" covers the bank work. The Azure billing system was for an engineering consulting client.
  - The certification is shortened to "AWS Solutions Architect - Associate".
- **Questions for Aly:** none.
- **Final build:** pages 1, fill 0.968, skills_lines 5, no errors. The only overfull boxes are the usual 0.56pt project-heading ones, which are invisible on the page.
