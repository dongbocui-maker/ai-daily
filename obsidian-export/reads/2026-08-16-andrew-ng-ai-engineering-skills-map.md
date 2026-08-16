---
title: "The AI Engineering Skills Map (The Batch #366)"
title_zh: "[待写]"
saved_date: 2026-08-16
original_url: "https://www.deeplearning.ai/the-batch/issue-366"
slug: "andrew-ng-ai-engineering-skills-map"
source: "manual"
fetch_status: "ok"
fetched_at: "2026-08-16T01:13:19.441Z"
fetch_type: "html"
content_length: 29418
tags: []
---
# The AI Engineering Skills Map from Andrew Ng
*Analytics DeepLearning.AI*
> 🔗 原文：[https://www.deeplearning.ai/the-batch/issue-366](https://www.deeplearning.ai/the-batch/issue-366)
---
Dear friends,

I am delighted to present The AI Engineering Skills Map. AI allows us to build software very differently today than in 2022, and everyone with the skills to take advantage of this shift has numerous exciting project and job opportunities. But with the noisy, hype-filled, information environment around AI, what are the most valuable skills for you to learn? I have been working with my team to synthesize a map of AI engineering skills in order to help (i) developers prioritize what to learn, and (ii) employers hire skilled developers.

Based on an analysis of over 10,000 job postings; carrying out dozens of structured interviews with AI experts, hiring managers, and recruiters; gathering data through surveys; and synthesizing other online data, here are the four most important AI engineering skills:

-   Building and deploying AI applications
-   Software engineering fundamentals
-   Using coding agents
-   Shaping the build

You can informally think of our process as akin to clustering on a massive dataset of jobs and expert interviews to identify the most important skills, not just today but also in the near future.

A note on terminology: I talk about AI Engineering skills rather than the “AI Engineer” role (someone whose job is to build AI systems), because the former is much broader. All developers today should know how to work with the cloud, and only a smaller number have a “Cloud engineer” title. Similarly, all developers — full-stack engineers, data engineers, DevOps engineers, machine learning engineers, and, yes, AI engineers — will need AI engineering skills.

![](https://charonhub.deeplearning.ai/content/images/2026/08/Skills-Map-2-2.webp)

**Building and deploying AI applications**. The key difference between AI and non-AI applications is that the former has unpredictable outputs. When you prompt an LLM, you don’t know what you’ll get back. When you train a deep learning algorithm, you don’t know what prediction it will make on new examples. In contrast, traditional software behaves more predictably.

People who are skilled at building and deploying AI applications understand the building blocks of AI (such as LLMs, context engineering, RAG, agentic workflows, machine learning and deep learning) and, importantly, how to use statistical techniques to measure, steer, and govern AI systems so that they behave more predictably. A core skill in doing so is knowing how to drive disciplined evals and error analysis loops. 

**Software engineering fundamentals.** When you deeply understand how software works, you can build much more effectively. Engineering software requires making tradeoffs between cost, scalability, reliability, speed, and more. Security and privacy add further complexity.

Understanding software fundamentals allows you to recognize what tradeoffs even exist. This leads to better decisions in choosing your software stack, designing system architecture, designing your data store, testing, and so on. It also leads to much better outcomes than those for an inexperienced developer who vibe codes a solution without knowing the tradeoffs their coding agent is making — which will often be poor ones, because they don’t know what context to give their coding agent. Understanding software engineering fundamentals lets you make good tradeoffs by steering coding agents using the precise language of software engineering.

**Using coding agents.** Using agentic coding effectively is now a key skill for every developer. When you have this skill, you have a good mental model for how agents work. You understand their limitations and how to work around them, and are able to quickly steer them — knowing how much to intervene and how much to leave them alone — to build robust software without wasting excessive time or [tokens](https://www.deeplearning.ai/the-batch/what-comes-after-tokenmaxxing-how-to-avoid-getting-locked-in-to-just-one-ai-provider).

This requires your knowing how to manage a coding agent’s context, make tradeoffs between planning and execution, and help the agent autonomously close loops by providing verifiers or evals. You also need to know how to work with a clear spec (and when not to bother doing so), orchestrate multiple agents that work together, and avoid pitfalls that risk an agent messing up your production database. Because agentic coding is evolving quickly, using coding agents skillfully means not only knowing cutting-edge practices, but also having routines to keep trying new tools and evolve your workflows as best practices change.

**Shaping the build.** Given a clear spec, coding agents are rapidly improving at delivering to it. Thus, our work as engineers is shifting toward deciding what should be in the spec. Engineers should no longer expect to be given a pixel-perfect design and asked only to implement it. Instead, effective AI engineering requires having product sense and understanding business context and customer goals, so you can participate in shaping and driving the build.  

AI also gives you the opportunity to take on greater ownership and agency than before. You can identify interesting problems and opportunities, and execute to take advantage of them in responsible ways. Taking advantage of this opportunity requires knowing how to drive projects forward. For example, knowing when to quickly build an MVP to take to users for testing, and when to slow down and take longer in order to build more carefully.

Underlying all these skills is a mindset of continuous learning. AI continues to change quickly, so we must all keep learning and evolving our skills to adopt emerging best practices.

DeepLearning.AI’s principal focus is to help developers gain these AI engineering skills. I have more to say about each of these four skills, and will flesh out each of them in my next few letters and share a more detailed AI Engineering Skills Map. As I look at where AI Engineering is going, I am incredibly excited about what all of us will be able to build. I hope you will play an exciting role in this future.

Keep building!

Andrew

P.S. As AI evolves, I will keep updating the AI Engineering Skills Map. If you are willing to contribute, please take a few minutes to complete our survey [here](https://8sijzx7m4dp.typeform.com/to/YHqoolF9). It takes around 5-7 minutes to complete, and it will help us to shape this for the community.

## A MESSAGE FROM [DEEPLEARNING.AI](http://deeplearning.ai/)

![Explore AI coding workflows in new course; control models, run in cloud or local. Enroll now with JetBrains.](https://charonhub.deeplearning.ai/content/images/2026/08/JetBrains_EndCard_02.webp)

Turn your AI coding defaults into choices. Rebuild the same app across cloud, hybrid, and fully local setups — from Claude Code to models running on your own machine. [Enroll for free](https://bit.ly/4qfoqXc)

## News

![Charts show Muse Spark 1.2 scoring lower but more cost-effective, supporting Meta’s low-cost coding model.](https://charonhub.deeplearning.ai/content/images/2026/08/MUSECODE--height-.webp)

## Muse Code Wants Your Data

Meta will cut coding bills from dollars to pennies for developers who let the company learn from their work.

**What’s new:** Meta [introduced](https://research.meta.ai/blog/introducing-muse-code-and-muse-spark-1-2) Muse Code, a command-line agentic coding harness, and Muse Spark 1.2, the capable, low cost-per-task model behind it.

-   **Input/output:** Text, images, video, and PDF in (up to 1,048,576 tokens), text out
-   **Features:** Adjustable reasoning levels (none, minimal, low, medium, high, xhigh), tool use, structured output, web search, context caching, background subagents that persist across a session
-   **Performance:** Achieved 57 points on Artificial Analysis’ Intelligence Index, first on Vals AI’s Finance Agent v2 and on Artificial Analysis’ AA-LCR
-   **Availability/price:** Muse Code in beta for macOS and Linux, Muse Spark 1.2 via Meta Model API. Standard tier $1.25/$0.15/$4.25 per million input/cached/output tokens (prompts and outputs not used for training); contributor tier $0.10/$0.002/$0.20 per million input/cached/output tokens (prompts and outputs used for training); web search $2.50 per thousand queries
-   **Undisclosed:** Parameter count, architecture, knowledge cutoff, training data, and method details

**How it works:** Muse Code runs in a terminal. Given a software task, it plans changes, writes code, and checks results at each step using Muse Spark 1.2. Meta trained the model to work with Muse Code, using data from Muse Spark 1.1. The company describes three design choices that distinguish the agent from a single loop that calls a model repeatedly.

-   A main agent delegates to a set of subagents that remain for the length of a session instead of being created and discarded for each task. Subagents edit in parallel inside isolated worktrees, separate working copies of a repository that keep simultaneous changes from conflicting, Mark Zuckerberg [wrote](https://x.com/finkd/status/2085080752098509124).
-   Because they persist, subagents retain context they have already learned about a repository rather than re-derive it. The subagents also determine when to report back to the main agent on their own.
-   The agent writes every model call, tool run, plan approval, and file edit to a log on the user’s machine. If the agent crashes, it reads the log and resumes from the step it reached rather than starting over, which helps agents to work on long-running tasks.
-   The agent ships with three default skills that users can call: /plan converts a request into a roadmap the user must approve, /grill probes that plan for weak points, and /goal drives work until an objective is met.

**Performance:** Independent evaluations place Muse Spark 1.2 a notch below the intelligence frontier, but at a lower cost per task than most models around or above its level.

-   On Artificial Analysis’ [Intelligence Index](https://artificialanalysis.ai/models/muse-spark-1-2), a composite of nine evaluations of economically useful tasks, Muse Spark 1.2 set to xhigh reasoning (57, $0.40 per task) ranked sixth, above Grok 4.5 set to high reasoning (56, $0.36 per task), and just behind Qwen3.8-Max set to reasoning (58, $1.13 per task). The new model’s Intelligence Index score was 4 points above last month’s Muse Spark 1.1 (53, $0.29 per task).
-   On Artificial Analysis’ AA-LCR, a test of reasoning across long documents, Muse Spark 1.2 set to xhigh reasoning (83.3 percent) outperformed all other models tested.
-   On the [Vals Index](https://www.vals.ai/models/meta_muse_spark_1_2), a composite of finance and coding tasks weighted by potential economic impact, Muse Spark 1.2 set to xhigh reasoning (71.88 percent, $0.70 per task) ranked fifth, ahead of Claude Opus 4.8 set to max reasoning (70.36 percent, $7.52 per task) and behind GPT-5.6 Sol set to max reasoning (73.12 percent, $7.46 per task) — less than one tenth of the cost per task.
-   On Vals AI’s [Finance Agent v2](https://www.vals.ai/benchmarks/fabv2), which assigns models the work of entry-level financial analysts, Muse Spark 1.2 set to xhigh reasoning (60.60 percent, $0.77 per task) ranked first of 45 models, significantly cheaper than second-place Claude Opus 5 set to max reasoning (58.63 percent, $5.12 per task) and taking roughly half the time per test.

**Behind the news:** Muse Spark 1.2 is already an inexpensive model, but if it catches on — [OpenAI](https://www.reddit.com/r/n8n/comments/1oa4kbp/openais_hidden_trick_get_up_to_10m_free_tokens/) and other companies have tried similar initiatives — a contributor discount for the model’s use in Muse Code is potentially a transformative one. Companies’ appetite for training data drives new policy pushes and business intiatives.

-   In a long essay, Mark Zuckerberg [argued](https://www.meta.com/thefutureisforeveryone/) that United States labs are disadvantaged by restrictions on training data.
-   Of all training data, high-quality code is a scarce commodity. Hugging Face published [The Stack v3](https://www.deeplearning.ai/the-batch/fresh-data-for-coding-models-hugging-face-updated-the-stack-the-largest-crawl-of-public-github-repositories) last week, a 4.9 trillion-token crawl of public GitHub assembled to replace its years-old predecessor. But a public repository shows only polished code, not all the reasoning, mistakes, and repairs that went into it. Sessions from a working coding harness capture that entire process.
-   The Muse Spark 1.2 discount lands in a price competition that has escalated over the summer: OpenAI cut GPT-5.6 Luna’s prices by 80 percent to $0.20/$1.20 per 1 million tokens of input/output, and DeepSeek-V4-Flash-0731 arrived at $0.14/$0.28 per 1 million tokens of input/output. Meta’s contributor tier undercuts them both and virtually everyone else selling high-performing models through an API.

**Why it matters:** The contributor tier buys Meta something its apps don’t supply. Facebook, Instagram, and WhatsApp generate enormous quantities of data, but not the kind of coding data required to train coding agents. Meta is short of such data and is willing to give away most of the price of the Muse Spark 1.2 to get it. Meta sells the same model at two prices, and the discount buys Meta the right to train on whatever passes through the agent. That trade requires no contract: A developer picks it by typing a different model name. The tier containing these data terms caps at 100 requests per minute per team versus 3,000 requests per minute for the standard tier, limits that make it practical mainly for individuals and small teams — the developers least likely to have a lawyer on retainer, and the ones whose entire product may sit in the repository the agent reads.

**We’re thinking:** No one is forced to give up their data to use Meta’s best model or agent. But developers weighing Muse Code’s discount are deciding, whether they think about it deliberately or not, what their own code and expertise are worth. Model builders have long trained on developers’ code by scraping it from public repositories and forums. Meta is trying to turn that knowledge transfer into a market. Like all markets, this one rewards the side that knows what its goods are worth, and the goods for sale here, both repositories (public or private) and a recording of how the work was done, lacked a clear price before. Meta has transparently priced the discount. Likewise, developers should price the value of their data before calling the trade a true bargain.

* * *

![Accuracy chart of robot tasks: screw bulb 36%, unscrew bulb 92%, tie trash bag 44%, dustpan 32%, ziplock 40%.](https://charonhub.deeplearning.ai/content/images/2026/08/GR2--1-.webp)

## Google’s Robotics Model Has Legs

Google’s latest vision-language-action model can walk a humanoid robot across a room, crouch to a low shelf, and close a five-fingered hand around a light bulb. Google says it’s the first model in its robotics family to run the legs and the hands from one set of weights, a breakthrough that simplifies model training and design.

**What’s new:** Google [released](https://deepmind.google/blog/gemini-robotics-2-brings-whole-body-intelligence-to-robots/) Gemini Robotics 2 (GR2), a model that turns camera images and typed instructions into commands for a robot's joints. Whereas earlier models in the Gemini Robotics family drove only the upper body for tabletop work, GR2 moves a humanoid’s legs, torso, arms, and hands together. One fixed set of the model’s trained weights runs three machine setups across two robot bodies.

-   **Input/output:** Camera images and text instructions (input) to joint commands (output), driving either a five-fingered hand with 22 degrees of freedom (Sharpa or Inspire hands) or a simple two-fingered gripper (Robotiq)
-   **Features:** Leg and hand control; multi-embodiment (one checkpoint runs Apptronik's Apollo 2 humanoid with Sharpa hands, the same Apollo 2 with Inspire hands, and a Franka Duo arm rig with a Robotiq gripper)
-   **Performance:** Self-reported success rates of 45.7 to 76.3 percent on whole-body pick-ups, 32 to 92 percent on multi-finger tasks, and 74.2 to 89.6 percent on gripper tasks
-   **Availability:** Early-access partners, with no public API
-   **Undisclosed:** Google published no model card for Gemini Robotics 2, and gave no base model, parameter count, training-data breakdown, or price

**How it works:** The release pairs Gemini Robotics 2 with Gemini Robotics ER 2, a separate reasoning model that breaks a job into steps and hands them to GR2 one at a time. Google published no model card or technical paper for GR2, so its [safety report](https://storage.googleapis.com/deepmind-media/gemini-robotics/Gemini-Robotics-2-Safety.pdf) and announcements provide what we know.

-   Google trained the model for each task in the demonstration videos using a mix of teleoperation, in which a person operates the robot remotely while the movements are recorded, plus video examples and simulation.
-   GR2 runs one set of trained weights across three machine setups; no version was trained per configuration. Motion transfer, introduced alongside [Gemini Robotics 1.5](https://arxiv.org/abs/2510.03342), trains a single model on data pooled from robots of different shapes, sensors, and joint counts. This makes data recorded on one machine setup valuable learning material for data on another.

**Performance:** Google ran every evaluation of GR2 on its own defined tasks and hardware, and no outside group has published tests of the model. Google reports the whole-body and gripper figures as averages over several tasks in a category and the finger figures as individual tasks. The nearest baseline is Google’s own first robotics model from March 2025, which was [adapted](https://arxiv.org/abs/2503.20020) to a two-armed Franka robot and averaged 63 percent across the tasks it was given.

-   An Apollo 2 robot with Inspire hands, trained to pick things up while using the legs, succeeded 76.3 percent of the time from a shelf, 68.4 percent from a table, and 45.7 percent from the floor. Google reports each as an average over several tasks in that category.
-   Fine finger work using Apollo 2 with Sharpa hands produced the lowest figures Google published: Tying a trash bag succeeded 44 percent of the time, sealing a zippered bag 40 percent, and sweeping with a dustpan 32 percent.
-   On the Franka robot, GR2 averaged 89.6 percent on precise insertion, 78.9 percent on tool kitting, and 74.2 percent on general pick and place. This task list differs slightly from that measured for Gemini Robotics 1.
-   Gemini Robotics ER 2’s judgment about whether a task was physically possible for the robot depended on being told what Gemini Robotics 2 had practiced. With no summary of that training it was right 62.0 percent of the time; with a highly detailed summary, 95.8 percent.
-   Google also introduced a safety benchmark, [ASIMOV-Agentic](https://huggingface.co/datasets/google/asimov_agentic). Google found that no system it tested, its own included, can both catch hazards to a person from a moving robot and avoid stopping for nothing. Holding needless stops under 5 percent meant missing more than 40 percent of the moments a person was too close. Consequently, Google recommends running these models alongside conventional physical safety equipment rather than in place of it.

**Screwing in a light bulb:** One pair of tasks in Google’s results illustrates how an apparently simple task, when reversed, can be a challenge in robotics. Unscrewing a bulb succeeded 92 percent of the time, the highest figure in Google’s finger-work set. Screwing one in succeeded 36 percent of the time. Unscrewing starts from a settled position (bulb already in the socket), so the hand needs only grip and rotation. Screwing one in has to establish bulb-in-socket alignment first, with the hand wrapped around the bulb.

**Behind the news:** An updated Gemini Robotics reasoning model called ER 2 is paired with this release. ER 2 plans steps, tracks progress from a video feed, and calls an action model as a tool. Another model, Gemini Robotics On-Device 2, runs on the robot’s own hardware without a network connection and adapts to an unfamiliar two-armed body in a few hours using typically fewer than 200 examples.

**Why it matters:** Many robotics models are trained for one task, one machine, and one environment at a time, and changing a single variable often means starting from scratch. There is also no corpus of robot motion at anything close to the scale of the text and images behind vision-language models. The latest Gemini Robotics models are an experiment in learning from more generalized training data than has been available for robots in the past. It shouldn’t matter if you change the type of hands, number of joints, or tasks performed: The goal of a true multi-embodied robotics model is to successfully transfer knowledge from one setup to another, as transformer-based language models have done so successfully with text.

**We’re thinking:** How many Gemini robots does it take to screw in a light bulb? At the current 36 percent success rate, just under three.

* * *

![Diagram shows Minimax H3's process from text prompt input to audiovisual output via a transformer.](https://charonhub.deeplearning.ai/content/images/2026/08/H3--1-.webp)

## MiniMax’s State-of-the-Art Video Model Is Only Minimally Open

A free-to-download model sets a new standard for video generation and editing, but its license comes with unexpected restrictions. 

**What’s new:** MiniMax [released H3](https://www.minimax.io/blog/minimax-h3), a high-definition video generation model that accepts a wide range of input media. But the model’s license requires users in the U.S., the UK, the European Union, and South Korea to submit an application to MiniMax to use it under the same terms as the rest of the world. Key components of the model also remain proprietary, at least for now.

-   **Input/output:** Up to twelve files including text (7000 characters), images (30 MB per file), audio (15 MB), and video (50 MB) in, video (up to 2000 pixels wide and 15 seconds long) with audio and text captions out
-   **Architecture:** Transformer, 33 billion parameters; separate text, audio, and video encoders, preprocessor, 2k video upscaler
-   **Features:** Video and audio editing, multi-shot output, six aspect ratios
-   **Performance:** First on Artificial Analysis’ video editing leaderboard, second (or tied for first, within the margin of error) in text-to-video and image-to-video
-   **Availability/price:** Weights [free](https://huggingface.co/MiniMaxAI/MiniMax-H3) for noncommercial and commercial uses under MiniMax H3 license; via MiniMax’s [API](https://platform.minimax.io/subscribe/token-plan?tab=api-enterprise) at $0.13 per second for 2K resolution, $0.08 per second for 768p resolution output, input costs vary from free for audio to $0.04 per image and $0.13 per second for high-definition video; prompt re-generation module costs $0.90 per million tokens of input and $3.60 per million tokens of output.
-   **Undisclosed:** Exact parameter count, training data, technical report

**How it works:** H3’s architecture consists of [three modules](https://huggingface.co/MiniMaxAI/MiniMax-H3) — a contextual processing system, a video/audio generation base model, and a high-definition upscaler. Only the base model is free to download, and it comes with restrictions.

-   MiniMax says it trained H3 on “real, natural data” to ensure data quality and scalability. Unlike MiniMax’s earlier video models, all audio types (voice, music, and sound effects) were trained together and are modeled through a single encoder. The team trained the model’s reference and editing functions using natural language rather than fixed presets. The team sought to combine different media types (sound, video, etc.) earlier in the process.
-   Supported generation modes include text-to-video, first- or last-frame image to video, and image, audio, and video references, plus any combination. For example, a user prompt might instruct the model to begin with a single still image, reference the camera movement in two videos, and the audio score from a third, with text instructions for how the scene should unfold.
-   Input is first processed by H3-Context-IR. This reasoning module interprets the prompts and input media and generates a new text prompt instructing the base model how to blend them together. Users of the base model alone need to be [explicit](https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/docs/VIDEO_PROMPT_WRITING_GUIDE_base_en.md) in their instructions for each media type, or use their own preprocessing system; users of the full API pipeline benefit from the Context-IR module doing most of that work.
-   The base module generates 768p video, that is, 1792 pixels by 768 pixels (given a maximum 21:9 aspect ratio). Three encoders process text, video, and audio, respectively; a separate variational autoencoder also encodes video.
-   A third module, H3-Regenerate-2K, instructs the base module to regenerate the 768p video in native 2K resolution (2000 pixels wide and up to 4667 pixels long). The optimized prompt also includes the original media references and user prompt as context, allowing the regenerated video to add missing details rather than only extrapolating from the source video.
-   The weights’ [license](https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/LICENSE) requires commercial users to prominently display the model name on any product using H3 and bars all users from distilling another model on H3’s output. It also prohibits use that may harm minors, interfere with elections, or violate local law. The license also identifies the United States, United Kingdom, European Union, and Republic of Korea as “excluded territories” and requires users of the weights in these territories to [apply](https://platform.minimax.io/h3-license) for a license “to ensure \[their\] usage is lawful, responsible, and without infringing any rights.”

**Behind the news:** MiniMax H3’s head-to-head human-preference [ELO scores](https://artificialanalysis.ai/video/leaderboard/text-to-video) put it squarely in a top three with Google’s [Gemini Omni Flash](https://www.deeplearning.ai/the-batch/google-pairs-nano-banana-update-with-video-api) and Bytedance’s [Dreamina Seedance 2.0](https://www.byteplus.com/en/blog/dreamina-seedance2-0). Black Forest Labs’ FLUX models have typically included an open weights release for developers, but its recent FLUX 3 model is proprietary and API-only. It’s yet to be independently tested, but Black Forest Labs’s tests suggest it would be a fourth model vying to be state-of-the-art. [Dreamina Seedance 2.5](https://dreamina.capcut.com/resource/seedance-2-5-launch) also awaits testing.

**Why it matters:** Despite the restrictive license and unusual territorial restrictions, MiniMax H3 is clearly a top video generation model, offering commercial users a strong and versatile set of tools for video generation on par with Google’s much more expensive competitor. We also get a glimpse of how a top video model works under the hood. It appears that MiniMax’s strategy of foregoing synthetic data — especially difficult when good video transcripts are hard to come by — and bundling prompt optimization into the pipeline is paying off. 

**We’re thinking:** Even in this paranoid period of AI development, it makes no sense to restrict use of weights by country beyond uses that would break that country or region’s laws. It violates the fundamental meaning of openness: the idea that anyone can download a model, see how it works, and put it to use. We hope these restrictions don’t become a trend. 

* * *

![Line graph showing Breakup Distress Scale decline over time for control and treatment groups.](https://charonhub.deeplearning.ai/content/images/2026/08/BREAKUP--1-.webp)

## AI Can Help Heal Romantic Distress

Chatbots that are designed to treat mental health issues typically require multiple sessions, posing a risk that users will drop out before they receive much benefit. Researchers showed that chatbots can provide relief in a single session.

**What’s new:** Thomas Menzel at Technical University of Munich and University of Cambridge, along with Michel Schimpf and Thomas Bohné at University of Cambridge, built [overit](https://arxiv.org/abs/2605.03261), a chatbot app designed to help users recover from romantic breakups. In a randomized, controlled trial, users felt substantially better after one conversation.

**Key insight:** Romantic breakups can continue to cause distress long after they occurred. Often, the former lovers are troubled by self-limiting beliefs about themselves (“I was abandoned because I am not enough”) or the world (“nobody could want me”). According to [memory reconsolidation theory](https://cshperspectives.cshlp.org/content/7/10/a021782), recalling a distressing memory, contemplating a self-limiting belief about it, and then presenting an interpretation that contradicts the earlier belief (“You did the best you could, but you were failed by someone you trusted”) can durably update the painful memory. If that’s true, a chatbot that elicits a self-limiting belief and guides the user toward a counterfactual interpretation could bring about a lasting reduction in distress.

**How it works:** Users filled out a survey that included a breakup distress score, breakup timing, and the ex-partner's name (along with follow-up surveys after the trial period). Then they discussed their breakups with a mobile app based on Claude Sonnet 4.5.

-   Given their survey responses, the app guided them through four phases of conversation. The app (i) asked open-ended questions about a breakup and its impact, (ii) elicited beliefs and identified at least one self-limiting belief, (iii) offered alternative perspectives, and (iv) asked users what they had learned from the conversation and how they felt now. It progressed from one phase to the next after a number of turns or reaching a certain milestone, capping conversations at 18 turns.
-   With each user input, the app asked Claude Sonnet 4.5 to assess the current phase by checking the last three turns against five milestones: (i) identifying a self-limiting belief, (ii) challenging it, (iii) steering the user toward a counterfactual interpretation, (iv) articulating a new insight, and (v) concluding the dialog.
-   Then the model considered the conversation history, instructions for the current phase (for example, to identify the core self-limiting belief in phase two), and survey data and generated a response.

**Results:** The authors ran a randomized, controlled trial with 171 participants in the U.S. and UK who had experienced a breakup within 18 months on average. Half of participants conversed with the app, via text or voice, in a single conversation of roughly 20 minutes; the other half did not interact with the app. The authors measured the participants’ distress via the [Breakup Distress Scale](https://psycnet.apa.org/doiLanding?doi=10.1037%2Ft66170-000), a 16-item questionnaire that yields scores between 16 and 64.

-   After 7 days, the group that used the app had experienced a large reduction in distress (from 35.3 to 26.6) relative to the control group (from 35.9 to 32.2).
-   After one month, the group that used the app showed lower distress (26.0) than the control group (29.0).
-   People who used the app were more likely to report a “sudden insight” about their breakup (such as “I had been carrying the blame for my failed relationship instead of recognizing that I did everything the best I could and I was failed by someone I trusted”): 61.7 percent versus 19.3 percent. Those who had such experience tended to report feeling better afterward.

**Why it matters:** Chatbots frequently sycophantically affirm a user’s expressions. This can be troublesome in therapeutic settings, where an analytical approach would be more helpful. This work addresses that issue by dividing each input into calls for evaluation and generation. Prompting the LLM first to evaluate the conversation’s state and then to generate a response separates the tasks of tracking therapeutic progress and expressing empathy to the user, which supports the LLM’s ability to provide helpful output. This approach offers a template for building goal-directed conversational agents that challenge users (in this case, to examine and reinterpret painful memories) rather than simply comforting them. 

**We’re thinking:** Any chatbot session is less expensive than a human therapist, but a single 20-minute conversation that can meaningfully improve a subject’s mood and attitude is truly favorable economics, even at Claude’s rates.