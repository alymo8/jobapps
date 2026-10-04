# Velixo: Applied AI Engineer

- URL: https://builtinmontreal.com/job/applied-ai-engineer/10899199
- Company: Velixo
- Title: Applied AI Engineer
- Location: Montreal, QC (listed In-Office on Built In; text says fully remote, priority to Quebec-based candidates, applications welcome from across Canada)
- Compensation: not listed
- Fetched: 2026-10-04

## Application form fields

Not available: no ATS API. Apply route: email jobs@velixo.com (velixo.com/careers lists no open roles) or Built In account apply. The Jotform linked from Built In (https://form.jotform.com/223044927257054) was inspected 2026-10-04: it is Built In's "Website Feedback & Suggestions" form, NOT a Velixo application, so no Apply URL is recorded. Real apply route unknown.

## Posting


## About Velixo

Velixo builds Excel-native reporting, planning, and automation for finance teams running Acumatica, Sage Intacct, Business Central, and MYOB. Founded in 2017 and headquartered in Montreal, we serve finance and accounting teams who live in spreadsheets and need their ERP data to be live, trustworthy, and writable.

Velixo is an equal opportunity employer. We celebrate diversity and are committed to creating an inclusive environment for all employees.

This is a fully remote position. While we welcome applications from across Canada, we are giving priority to candidates located in Quebec at this time.

## The role

You will own how well Velixo Intelligence works and what it costs us to run. That means building the evaluation infrastructure that tells us whether a model change made our product better or worse, and driving down the cost per action without degrading quality.

This is a measurement-first engineering role. Today we ship AI features and form opinions about quality from anecdotes. You will replace that with evidence.

## About Velixo Intelligence

Velixo Intelligence is our MCP-based gateway that lets finance teams query their ERP in natural language and perform governed writebacks from Claude, ChatGPT, and Copilot. Reads run through GIQL, our query language. Writes go through the ERP's own screen APIs so that every permission, validation, and audit rule still applies.

It launched in public preview this year. Usage is growing, the surface area is expanding, and our understanding of the unit economics has not kept pace. That gap is the reason this role exists.

## What you will own

### Evaluation

- Build and maintain regression suites for GIQL query generation, writeback correctness, and tool selection
- Define what "good" means for each action type and make it measurable
- Run structured evaluations before every model upgrade or prompt change, and produce a clear ship or no-ship recommendation
- Track quality over time so we notice degradation before customers do

### Cost engineering

- Instrument every Gateway action for tokens, cache behavior, model, latency, and tenant
- Establish and maintain the cost-per-action baseline that the rest of the company plans against
- Reduce cost through prompt compression, prompt caching, context pruning, and routing work to smaller models where evaluation shows quality holds
- Identify the expensive tail: which customers, which query shapes, which failure and retry loops

### Model strategy

- Track new model releases across providers and evaluate them against our workloads rather than published benchmarks
- Maintain a current view of the price and performance frontier for what we do
- Recommend when to migrate, when to wait, and when to run models in parallel

### Partnership with Finance

- Supply the unit cost data behind our credit pricing and plan allowances
- Model the margin impact of proposed pricing changes alongside our VP Finance
- Flag when product decisions will move the cost curve before they ship

You will not own pricing decisions. You will own the numbers those decisions depend on.

## First 90 days

- **Days 1 to 30:** Full instrumentation of the Gateway. A dashboard showing cost per action type, per tenant, and per model that the exec team checks weekly.
- **Days 31 to 60:** A working evaluation suite covering our highest-volume action types, with a documented baseline.
- **Days 61 to 90:** A prioritized cost reduction roadmap with sized estimates, and at least one shipped optimization with measured before-and-after quality.

## What we are looking for

- Substantial experience building on LLM APIs in production, not in demos or notebooks
- You have built an eval harness before and can explain why the naive version of it misleads you
- Hands-on with the current tooling landscape: tracing and observability platforms such as Langfuse, eval frameworks such as promptfoo. You have opinions about which of these earn their keep and which add ceremony without adding signal.
- Comfortable with token accounting, context window management, and caching strategies
- Strong analytical instincts and fluency with data. You reach for a query or a notebook before you reach for an opinion.
- Able to write clearly about tradeoffs for a non-technical audience, because your conclusions will land in board decks and pricing meetings
- Python or TypeScript proficiency

## Nice to have

- Experience with MCP or other tool-calling frameworks
- Background in ERP, accounting, or financial systems
- Prior exposure to usage-based or credit-based pricing models
- Experience at a small company where you set your own priorities

## Why this role is interesting

Most companies bolt a chat box onto their product and hope. We are building governed, auditable write access to financial systems of record, where a wrong answer has real consequences and a hallucinated journal entry is unacceptable. The evaluation problem here is genuinely hard and genuinely matters.

You will also have unusual visibility. The numbers you produce will directly shape what we charge and what we build.

