# Free-text answer bank

Answers Aly has written for past applications, in Aly's own voice. `/apply` starts from the closest
one when a posting asks a similar free-text question (cover letters: `/cover-letter`, rules in CoverLetter_prompt_v1.md), tailors
it to the posting, and marks the result `draft` for Aly's review. Reuse the facts and the voice;
don't paste an answer that doesn't fit the question. Behavioral "tell me about a time" questions use
[stories.md](stories.md).

## AI / LLM experience

### What's your most complex LLM project? (context: scale of data, technical complexities, fine-tuning; if few LLM experiments, present an AI project)

My most complex LLM project was a real-time fraud detection agent I designed professionally at Accenture. The system operated on live fraud alerts, pulled in relevant customer and transaction history through a RAG layer, and used LLM reasoning inside a LangGraph-based workflow to help determine whether a case looked genuinely fraudulent or needed deeper review. What made it complex was not just calling an LLM, but designing the decision flow around it so the model had the right context, structure, and constraints to make useful decisions in a real-time setting.

The technical challenge was making an agentic system work reliably across multiple moving parts: retrieval quality, prompt design, state management, tool usage, and orchestration logic. The LLM had to reason over non-trivial inputs rather than a single prompt, and the surrounding system had to support consistent behavior under production-style conditions. I did not fine-tune a base model for that project, but I spent a lot of time thinking about evaluation, failure modes, and how to make the overall system dependable enough for a high-stakes business use case. That same mindset also showed up in another project where I implemented an LLM-as-a-judge component to evaluate generated summaries for completeness, hallucinations, and readability.

What I liked most about that work was that it forced me to treat the LLM as one part of a larger system rather than the whole solution. It pushed me to think about orchestration, feedback loops, and how to build something that is not only intelligent, but also structured, observable, and useful in practice. That is the kind of complexity that excites me most.

### Tell us about a project where you worked with an LLM, either professionally or personally

Professionally, one project I'm proud of was building an LLM-powered decision layer for a fraud detection agent. The system used LLM reasoning to analyze customer and transaction history, decide what information mattered, and support downstream fraud-related actions in a more flexible way than traditional rule-based logic. What made it interesting was not just using an LLM, but designing how it fit into a larger agentic workflow, with the right context, structure, and safeguards so it could make useful decisions in a real business setting.

Outside of work, I use LLMs constantly in my day to day and I'm genuinely excited by how fast the space is moving. I'm a big Claude enthusiast, and I spend a lot of time keeping up with new ideas in AI-assisted programming, prompting patterns, agent design, feedback loops, and practical ways to automate complex workflows. I like thinking of LLMs not just as chat tools, but as systems that can plan, delegate, and execute tasks, with me acting as the orchestrator and supervisor to make sure the outcomes are reliable and actually useful.

### Please share any experience you have in building AI systems

I've been lucky to build AI systems in both production and project settings, and that's a huge part of why I'm excited about this role. At Accenture, I've worked on a real-time transcript streaming application that uses an LLM to generate customer support summaries and live recommendations, and I also built an LLM-as-a-judge component to evaluate generated summaries for completeness, hallucinations, and readability. I also designed a real-time fraud detection agent using LangGraph that combines RAG with GenAI reasoning over customer and transaction history. Outside of work, I've explored conversational AI more end-to-end through a chatbot project that included speech-to-text, text-to-speech, and LLM integration.

### Tell us about your experience in client-facing roles and/or with AI or agentic systems

My experience spans both, as every AI system I have built at Accenture has been delivered for an external client, in production, with stakeholders involved from the outset.

Over the past three years as a consultant, I have worked directly with enterprise clients in regulated industries, including a major U.S. bank, an engineering consulting firm, and telecom. In most engagements, the client understands their process deeply but has limited visibility into what an agentic system can realistically accomplish. On a recent billing automation project, the initial request was broad: whether AI could handle their billing verification. My role was to work with the client to translate that into measurable success criteria, then design, build, and deploy the resulting system. I owned it end to end, including the production deployment on Azure and the operator-facing React frontend, since the deliverable is not the agent itself but a system that operators rely on daily.

On the technical side, I designed a real-time fraud detection agent in LangGraph using a plan-and-execute pattern. The agent reasons over live fraud alerts and augments them with customer and transaction history retrieved through a RAG layer, achieving 96% precision across 500 transactions for the banking client. The billing system referenced above is built around a router agent that orchestrates parallel subagents and validates results before completing a request autonomously. I also built a Llama-based FastAPI service on top of a real-time transcript streaming pipeline (AWS Kinesis Data Analytics, Apache Flink) that generates call summaries and live recommendations for support associates, saving approximately 15 minutes per call.

Evaluation has been a consistent focus in this work, as anecdotal performance is not sufficient in a client setting. I built an LLM-as-a-judge pipeline that scores generated summaries for completeness, hallucination, and readability, with results feeding back into the system, along with a benchmark comparing the agentic billing workflow against the existing manual process in order to quantify the improvement.

The broader lesson from this work is that the model is rarely the most difficult component. The difficulty lies in the orchestration, the evaluation, the failure modes, and the alignment with the client on what a successful outcome actually means. That is the work I am most interested in continuing.

### Experience with the LLM inference ecosystem (e.g. vLLM, SGLang)

I've worked with vLLM in the context of building an LLM-as-a-judge system from scratch to evaluate GenAI-generated summaries. The goal was to score outputs on dimensions like quality, completeness, and potential hallucinations, which meant I had to work directly with inference infrastructure rather than just call a model API. Through that work, I dealt with vLLM as part of running evaluation workflows efficiently and understanding practical serving considerations like latency, throughput, and scaling. That exposure gave me a solid introduction to the LLM inference ecosystem, and it made me even more interested in learning more deeply about systems like vLLM and SGLang.

### What is the most interesting thing you've built?

The most interesting thing I've built was a proof of concept for an Accenture client that fully automated part of their order-to-cash process. I built an agentic system using LangGraph where the main agent could use tools, delegate work to sub-agents, and validate results before completing requests autonomously. What made it especially exciting was designing the orchestration logic so the system could reason through multi-step business workflows instead of just answering prompts. It was one of the first times I really felt I was building something that looked like the future of enterprise software.

### What's the hardest you've ever worked on something?

One of the hardest things I've worked on was building a chatbot from scratch end to end. I had to think through everything: the UI, the LLM behavior, speech-to-text, text-to-speech, and how all the pieces would work together in a way that actually felt smooth and conversational. It took time because every layer introduced its own challenges, and progress often meant debugging the interaction between components rather than just one model or one service. But that project taught me a lot about how AI systems really work in practice, and it made me even more excited about building thoughtful, high-quality AI products.

## About me

### What do you optimize for in life?

This question had me think for a bit. I think that my engineering mind tries to optimize everything, just for fun. Fun fact, I time myself while walking on different routes from a starting point to another to see if the way I think is quick is the fastest path.

Regarding my life goals, I would like to be impactful, even if not on a huge scale. I want that, people in my surrounding be able to benefit from their relationship with me, so I would always try to see how I can be a good influence/image, or a good help to those who are around.

On another hand, I always want to be around people who I can look up to. For example, at university I made friends with a lot of people who were playing high level sports, that pushed me to play squash at a high level, I improved a lot in 1 year and played with the McGill Varsity team and travelled with them, I have the same mentality in my professional and academic life.

### How intensely do you like working?

I can work well under high intensity, in fact I can enter a flow state that makes me fully focused for hours. I believe I am able to change my rhythm depending on the conditions around. I am able to rest when things are slow and adapt quickly when needed.

### What should we know about you?

- I am a sports enthusiast, I watch and play a lot of sports, mainly soccer and squash.
- I am good at math, had to study 2 degrees that were full of that!
- I like solving complex problems, and am good at it. I might not know the answer to every question on the top of my mind, but I am good at researching.
- I am pretty autonomous, I am able to get things done. I know when to check with my supervisors, but am not the type to need a lot of guidance to complete a task.
- I can lead people well, and have had great relationships with everyone I worked with.
