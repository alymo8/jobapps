# Changelog: Scotiabank, Software Engineer (AI Engineer), req 270579

- **Emphasized:** Python microservices, REST APIs, async/event processing (SQS, Kinesis/Flink), IaC (CloudFormation, CDK, Bicep), Docker/Kubernetes, CI/CD, and LLM/agentic work (LangGraph, RAG, LLM-as-a-judge, Langfuse). Bank-domain work comes first (fraud agent, call summarization, CI/CD microservices, all for major U.S. banks). GCP shows up through the Vertex AI/Gemini chatbot. The posting asks for documented designs and runbooks, so the Cold-Chain bullet with the ADRs and 5 runbooks stays.
- **Structure:** Summary, Skills, Experience, Education, Projects. **The Research section is dropped** (close call): this is a software-engineering role, so the space went to the two client systems and Leagueware. Education is compressed to the degrees, GPAs, and MILA. No age-rule override.
- **Close-call cuts:** claude-kit (dropped for space), the third Cold-Chain bullet (116 tests, advisory-lock race fix), the Clinic Ops TDD/PR bullet, the Accenture monitoring bullet (Splunk/New Relic/CloudWatch), the DynamoDB index bullet, and Arabic/Spanish from Languages.
- **Gaps vs the posting:** no Redis, no RabbitMQ/Kafka/GCP Pub/Sub (closest are AWS SQS and Kinesis), no Helm, Terraform, or Ansible (closest are CloudFormation, CDK, and Bicep), no ArgoCD/ArgoWF, no LangChain/LangSmith/ADK (closest are LangGraph and Langfuse), no Webpack/Babel/Jest/Redux. GCP experience is limited to Vertex AI/Gemini.
- **Sanity-check these:**
  - The LLM-as-a-judge bullet merges the judge framework with the Langfuse tracing bullet. Both come from the same call-summarization app.
  - SWE bullet 2 combines three source bullets (Fargate REST microservices, Lambda SQS, CloudFormation/CDK).
  - The certification is shortened to "AWS Solutions Architect - Associate". The official name is "AWS Certified Solutions Architect - Associate".
  - Node.js and Express.js are in Skills only because the posting lists them. No bullet on the page backs them (the Node.js work is the cut Vodafone internship).
- **Questions for Aly:** none (all calls above made and noted).
- **Final build:** pages 1, fill 0.969, skills_lines 5, no errors. The only overfull boxes are 0.56pt ones from the project headings, which are invisible on the page.
