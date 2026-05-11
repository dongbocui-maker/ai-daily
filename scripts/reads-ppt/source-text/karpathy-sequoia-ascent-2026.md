# Sequoia Ascent 2026 summary — Andrej Karpathy

Source: https://karpathy.bearblog.dev/sequoia-ascent-2026/
Date: 30 Apr, 2026
Format: Fireside chat at Sequoia Ascent 2026, with Stephanie Zhan

## Sequoia Ascent 2026: Software 3.0, Agentic Engineering, and Jagged Intelligence

I recently joined Stephanie Zhan for a fireside chat at Sequoia Ascent 2026, speaking with founders about the recent shift in AI agents, what it means for software, and how I think about the next wave of AI-native companies.

The short version is that I think we have crossed a new threshold. LLMs are no longer just chatbots or autocomplete. They are becoming a new programmable layer for digital work.

## 1. December 2025 Was an Agentic Inflection Point

I said recently that I have never felt more behind as a programmer.

The reason is not that programming became harder in the old sense. It is that the default workflow changed. For much of 2025, tools like Claude Code, Codex, and Cursor-like agents were useful but still required frequent correction. **Around December 2025, I felt a step change: the generated chunks got larger, more coherent, and more reliable.** I started trusting the agents with more of the work.

The unit of programming changed from typing lines of code to delegating larger "macro actions":

- Implement this feature.
- Refactor this subsystem.
- Research this library.
- Set up this service.
- Write tests, run them, and fix failures.
- Compare approaches and propose a plan.

This is why I think the profession is being refactored. **The programmer is increasingly not just a code writer, but an orchestrator of agents.**

## 2. Software 3.0: The Context Window as the New Program

I think of this as the next step in a sequence:

- **Software 1.0**: humans write explicit code.
- **Software 2.0**: humans create datasets, objectives, and neural networks; the program is learned into weights.
- **Software 3.0**: humans program LLMs through prompts, context, tools, examples, memory, and instructions.

In Software 3.0, **the context window becomes the main lever.** The LLM is an interpreter over that context, performing computation over digital information.

One example is installation. In the old world, installing a complex tool across many environments required a brittle shell script full of conditionals. In the Software 3.0 world, the installer can be a block of instructions you paste into an agent. The agent reads the local environment, debugs errors, adapts to the machine, and completes the setup.

That is a different kind of program. It is less precise, but more adaptive.

## 3. MenuGen and the Moment Software Disappears

I used MenuGen as an example of a deeper shift.

MenuGen was a traditional web app: take a picture of a restaurant menu, OCR the dish names, generate images of the dishes, and render the result in a UI. It required frontend code, APIs, image generation, deployment, auth, payments, secrets, and infrastructure.

But later, I saw the Software 3.0 version: take a photo of the menu, give it to a multimodal model, and ask it to render dish images directly onto the menu image.

**In that version, much of the app disappears. The neural network directly transforms input media into output media. The old software stack was scaffolding around a transformation the model can now perform directly.**

This is one of the most important founder implications: AI is not just a faster way to build the old apps. **Some apps should stop existing as apps.**

## 4. The New Opportunity Is Not Just Faster Programming

The shift is broader than coding. LLMs automate forms of information processing that were not previously programmable.

My LLM Wiki pattern is the clearest example. Instead of using retrieval-augmented generation to answer questions from raw documents each time, an agent incrementally compiles raw sources into a persistent Markdown wiki: summaries, entity pages, concept pages, contradictions, cross-links, logs, and evolving synthesis.

No classical program could robustly maintain that kind of knowledge base across messy human documents. But an LLM can.

The lesson: do not only ask, "What existing workflow can AI speed up?" Also ask, **"What information transformation was impossible before, but is now natural?"**

## 5. Verifiability Explains Where AI Moves Fastest

My core automation framework is:

- **Traditional software automates what you can specify.**
- **LLMs and reinforcement learning automate what you can verify.**

If a task has an automatic reward or success signal, models can practice it. This is why math, coding, tests, benchmarks, games, and many engineering tasks improve so quickly. They are resettable, repeatable, and rewardable.

This also explains why coding agents feel dramatically better than many ordinary chatbot experiences. Coding gives the model feedback: tests pass or fail, programs run or crash, diffs can be inspected, benchmarks can be measured.

## 6. Jagged Intelligence Has Two Axes: Verifiability and Training Attention

The interview added an important refinement to the verifiability thesis.

Model capability is not only about whether a task is verifiable. It also depends on whether the task was emphasized by labs during training, post-training, synthetic data generation, and reinforcement learning.

A rough formula:

**capability spike ≈ verifiability × training attention × data coverage × economic value**

Chess is a good example. When GPT-4 improved at chess, that was not necessarily because general intelligence smoothly improved everywhere. It may also have been because much more chess data was included in the training mix.

This matters because frontier models do not come with a manual. They are artifacts of pretraining mixtures, RL environments, benchmark pressure, product priorities, and economic incentives. They spike in some places and behave strangely in others.

So the practical question for a founder is: **are you on the model's rails?**

If your task sits inside a region that is verifiable and heavily trained, the model may fly. If not, it may fail in surprisingly basic ways. You may need better context, tools, fine-tuning, your own evals, or your own reinforcement learning environment.

## 7. Vibe Coding vs. Agentic Engineering

I distinguish two related but different ideas:

- **Vibe coding raises the floor.** It lets almost anyone create software by describing what they want.
- **Agentic engineering raises the ceiling.** It is the professional discipline of coordinating fallible agents while preserving correctness, security, taste, and maintainability.

Vibe coding is fine for prototypes and personal tools. Agentic engineering is what serious teams need.

The agentic engineer does not blindly accept generated code. They design specs, supervise plans, inspect diffs, write tests, create evaluation loops, manage permissions, isolate worktrees, and preserve quality.

My MenuGen payment bug is a useful example. The agent tried to match Stripe purchases to Google accounts using email addresses. That is plausible code, but bad system design: the Stripe email and Google login email can differ. **A human needs enough product and engineering judgment to insist on persistent user IDs.**

The frontier skill is not memorizing every API detail. Agents can remember whether a tensor library uses dim, axis, keepdim, reshape, or permute. The human still needs to understand the underlying concepts: storage, views, memory copies, invariants, identity, security boundaries, and the shape of the system.

## 8. Hiring Should Change

If agentic engineering is the new professional skill, hiring should test it directly.

Traditional coding puzzles are increasingly mismatched. **A better interview might be: build a substantial project with agents, deploy it, make it secure, and then have adversarial agents try to break it.**

This tests the real skill:

- Can the candidate decompose work for agents?
- Can they write useful specs?
- Can they preserve quality while moving fast?
- Can they review generated work?
- Can they secure and harden a system?
- Can they use agents as leverage rather than produce slop?

**The old "10x engineer" idea may become much more extreme. People who master agentic workflows may outperform others by far more than 10x.**

## 9. Founders Should Look for Valuable Verifiable Environments

For founders, one important opportunity is finding domains that are **valuable, verifiable, and undertrained by frontier labs.**

If you can create a domain-specific environment where models can try actions and receive reliable rewards, you may be able to improve performance with fine-tuning or reinforcement learning even if the base model is not already excellent there.

The most obvious domains, like coding and math, are already heavily targeted by labs. But many economically important domains may have latent verifiable structure that has not yet been exploited.

**That is a startup wedge.**

## 10. Agent-Native Infrastructure: Build for the Agent, Not Just the Human

Most software is still built for humans clicking through screens.

Docs say things like "go to this URL, click this button, open this settings panel." But increasingly the user is not the human directly. **The user is the human's agent.**

This means products need agent-native surfaces:

- Markdown docs.
- CLIs.
- APIs.
- MCP servers.
- Structured logs.
- Machine-readable schemas.
- Copy-pasteable agent instructions.
- Safe permissioning.
- Auditable actions.
- Headless setup flows.

I think about this in terms of **sensors and actuators.** A sensor turns some state of the world into digital information. An actuator lets an agent change something. The future stack is agents using sensors and actuators on behalf of people and organizations.

The MenuGen deployment story remains a useful benchmark. Building the app was easy compared to wiring Vercel, auth, payments, DNS, secrets, and production settings. In a mature agent-native world, I should be able to say "build MenuGen" and have the agent deploy the whole thing without manual clicking.

## 11. Ghosts, Not Animals

My Animals vs. Ghosts framing is a way to avoid bad intuitions.

**LLMs are not animals.** They do not have biological drives, embodied survival pressure, curiosity, play, or intrinsic motivation in the animal sense. They are statistical simulations of human artifacts, shaped by pretraining, post-training, RL, product feedback, and economic incentives.

This matters because anthropomorphic expectations mislead us. These systems can be brilliant in one moment and bizarrely dumb in the next. **They are not smooth human minds. They are jagged, alien tools.**

The right posture is neither dismissal nor blind trust. It is empirical familiarity: learn where they work, where they fail, what they were trained for, and how to build guardrails around them.

## 12. Education: You Can Outsource Thinking, But Not Understanding

We ended on education. There is a line I keep returning to:

**You can outsource your thinking, but you can't outsource your understanding.**

Even if agents do more of the work, the human still needs understanding to direct them. You need to know what is worth building, what question matters, what result is suspicious, and what tradeoff is acceptable.

This is why I am interested in LLM knowledge bases. They are not just answer machines. They are tools for transforming information into understanding.

This also connects to my tiny microGPT project: a complete GPT training and inference implementation in a single dependency-free Python file. The educational artifact becomes small enough for both humans and agents to inspect. The human expert contributes the distilled artifact and the taste behind it; the agent can then explain it interactively to each learner.

## The Big Picture

The main thesis of the conversation is that **AI is becoming a new operating layer for digital work.**

The scarce thing is shifting:

- **Less scarce**: code generation, API recall, boilerplate, first drafts, repetitive setup, simple transformations.
- **More scarce**: understanding, taste, eval design, security, system boundaries, agent orchestration, domain-specific feedback loops, and knowing when the model is off the rails.

For founders, the most important questions are:

- What becomes possible when the primary user is an agent acting for a human?
- What workflows can be rebuilt around sensors, actuators, and verifiable loops?
- What software should disappear into direct model transformations?
- What domains are valuable and verifiable but not yet heavily trained by frontier labs?
- What human judgment must remain in the loop to preserve quality?

My current worldview is not that AI simply makes everyone faster at the old work. **It is that the work itself is being reorganized around agents.** Software, research, education, infrastructure, and knowledge work are all becoming variations of the same pattern:

```
define the context
define the tools
define the feedback loop
define the guardrails
let agents work
preserve human understanding
```

## Key quotes (for quote_pair)

- "I have never felt more behind as a programmer." — Karpathy
- "AI is becoming a new operating layer for digital work."
- "Some apps should stop existing as apps."
- "Traditional software automates what you can specify. LLMs and reinforcement learning automate what you can verify."
- "Capability spike ≈ verifiability × training attention × data coverage × economic value"
- "You can outsource your thinking, but you can't outsource your understanding."
- "LLMs are not animals. They are jagged, alien tools."

## Key timeline markers

- 2015–2020: Software 1.0 → 2.0 transition (deep learning)
- 2022–2024: Software 3.0 emerges (ChatGPT era)
- December 2025: Agentic inflection point (per Karpathy)
- April 2026: This Sequoia Ascent talk
