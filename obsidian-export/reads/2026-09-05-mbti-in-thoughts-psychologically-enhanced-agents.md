---
title: "Psychologically Enhanced AI Agents"
title_zh: "心理学增强的 AI Agent：MBTI-in-Thoughts 框架"
author: "Maciej Besta et al. (ETH Zurich / BASF SE / Cledar / IDEAS)"
publish_date: 2025-09-04
saved_date: 2026-09-05
original_url: https://arxiv.org/abs/2509.04343
slug: mbti-in-thoughts-psychologically-enhanced-agents
source: arxiv-html-fetched
---

# Psychologically Enhanced AI Agents

## Abstract

We introduce MBTI-in-Thoughts, a framework for enhancing the effectiveness of Large Language Model (LLM) agents through psychologically grounded personality conditioning. Drawing on the Myers–Briggs Type Indicator (MBTI), our method primes agents with distinct personality archetypes via prompt engineering, enabling control over behavior along two foundational axes of human psychology, cognition and affect. We show that such personality priming yields consistent, interpretable behavioral biases across diverse tasks: emotionally expressive agents excel in narrative generation, while analytically primed agents adopt more stable strategies in game-theoretic settings. Our framework supports experimenting with structured multi-agent communication protocols and reveals that self-reflection prior to interaction improves cooperation and reasoning quality. To ensure trait persistence, we integrate the official 16Personalities test for automated verification. While our focus is on MBTI, we show that our approach generalizes seamlessly to other psychological frameworks such as Big Five, HEXACO, or Enneagram. By bridging psychological theory and LLM behavior design, we establish a foundation for psychologically enhanced AI agents without any fine-tuning.

## 1 Introduction

In the rapidly evolving landscape of AI, Large Language Models (LLMs) are reshaping the way we interact with and perceive technology. These sophisticated models, with their vast linguistic capabilities, are redefining the possibilities of human-computer interaction. In this broad landscape, in-context learning (ICL) has become a new highly relevant area of research . ICL is particularly attractive as it democratizes LLMs and their powerful capabilities as it is easy to use and try. It is also cost-effective and does not require expensive and time-consuming training. Enhancing ICL has thus become a goal of great significance.

As LLMs become integral parts of our digital lives, their influence extends beyond mere functionality to the realm of personality . As a matter of fact, LLMs do exhibit behavior implying possessing certain traits, as illustrated by – for example – recent news of LLMs “just wanting to be liked” . Recent investigations delve into the diverse personality traits exhibited by LLMs, unraveling the intricate tapestry of their linguistic fabric. Numerous researchers, employing various personality frameworks, have scrutinized these models to uncover nuanced dimensions of behavior, researching whether LLMs can truly manifest personality traits akin to human nature . However, all these analyses and frameworks are mostly dedicated to analyzing and shaping the personalities of LLMs.

In this work, we propose to integrate personality traits into LLM agents in order to enhance their effectiveness (contribution 1). It is common psychological knowledge that different personality types often have special aptitude for tasks that others do not. For example, in the well-known Myers–Briggs 16 Personalities framework (MBTI) , “emotional” personality types such as ISFJ (“the Defender”) are known to be more effective in emotional support tasks than “logical” types such as INTJ (“the Mastermind”). More broadly, psychological theory traditionally models mental function along two broad axes: cognition, which encompasses reasoning, memory, planning, and problem-solving; and affect, which includes emotion, mood, empathy, and emotional regulation. These two dimensions capture the majority of task-relevant variance in behavior, and are frequently used to explain differences in human judgment and decision-making. Our work adopts this framework to analyze and manipulate LLM agent behavior through psychologically grounded personality conditioning.

To test this hypothesis, we develop a general framework called MBTI-in-Thoughts (MiT) which conditions LLM agents on MBTI personality archetypes via prompt-based priming, and evaluates their performance across a diverse set of tasks (contribution 2). Our experiments span both individual and multi-agent settings, including emotionally grounded narrative generation and strategic interaction in game-theoretic dilemmas. We find that personality priming induces consistent behavioral biases aligned with the affective and cognitive characteristics of the assigned type. For example, “Feeling” types generate more emotionally expressive and empathetic narratives, while “Thinking” types exhibit more rigid but consistent strategies in adversarial games. Introverts are more honest and self-reflective in communication, while Perceivers display greater behavioral flexibility. These findings suggest that MBTI-based personality priming serves as a useful prior for shaping model behavior along affective and cognitive axes, improving agent alignment with task demands without any additional fine-tuning.

MBTI-in-Thoughts also enables structured experimentation with multi-agent communication protocols, allowing research into how personality influences interactive behavior (contribution 3). By organizing agent interactions into phases, such as pre-communication reflection, message exchange, and action selection, we observe that agents primed with consistent personality traits exhibit distinct communication styles and strategic preferences. Notably, we find that encouraging self-reflection prior to communication improves cooperative outcomes and reasoning quality across tasks. Next, to ensure that priming is both effective and persistent, our framework integrates the official 16Personalities11 1 https://www.16personalities.com/ test, enabling automatic verification that an agent’s responses remain consistent with its assigned MBTI profile (contribution 4). In combining behavioral control, validation, and social reasoning, we seek to bridge psychological theory and LLM behavior design, establishing a framework for psychologically enhanced AI agents.

We focus on MBTI, as it is a widely used framework, particularly valued for assessing individual suitability for different types of task; a property we now extend to the domain of LLM agents. Importantly, although MBTI is often presented as a typological model with 16 discrete profiles, we observe that it is fundamentally built upon four underlying dimensions (E/I, S/N, T/F, J/P), each of which can be meaningfully interpreted as a continuous trait. This makes MBTI structurally compatible with other dimensional frameworks such as the Big Five or HEXACO , which also describe personality as a vector of numbers modeling psychological tendencies. We also illustrate that all of these frameworks can be viewed as parameterizing behavior along the affective and cognitive axes. Hence, our personality conditioning framework enables generalization beyond MBTI (contribution 5).

## 2 Foundations of Psychological Frameworks

### 2.1 Myers–Briggs Type Indicator (MBTI)

The Myers–Briggs Type Indicator (MBTI) is a widely used personality assessment framework grounded in Jungian psychological theory. It defines 16 personality types based on four dichotomous dimensions: Extraversion vs. Introversion (E/I), where Extraverts are energized by social interaction and external activity, while Introverts gain energy from solitude and internal reflection; Sensing vs. Intuition (S/N), where Sensing types focus on concrete, present-oriented information, while Intuitive types attend to patterns, abstractions, and future possibilities; Thinking vs. Feeling (T/F), where Thinking types base decisions on logic and objective criteria, while Feeling types prioritize empathy, values, and interpersonal impact; and Judging vs. Perceiving (J/P), where Judging types prefer structure, planning, and decisiveness, while Perceiving types favor flexibility, spontaneity, and openness to change. Each personality is denoted by a four-letter code (e.g., INTP, ESFJ), providing a compact descriptor of an individual’s cognitive and affective preferences.

### 2.2 Psychological Frameworks Beyond MBTI

In addition to MBTI, several other personality frameworks are widely used in psychology. The Big Five (or OCEAN) model defines personality across five continuous dimensions: Openness to Experience, Conscientiousness, Extraversion, Agreeableness, and Neuroticism, providing. The HEXACO model extends the Big Five by adding a sixth factor (Honesty-Humility) and redefining others to better capture cross-cultural and moral dimensions of personality. Other relevant frameworks include the Enneagram , which classifies personality into nine types based on core motivations and fears, and the DISC model, which categorizes behavior into four types: Dominance, Influence, Steadiness, and Conscientiousness, often used in organizational settings. These frameworks offer complementary lenses for modeling affective and cognitive aspects of personality in both humans and AI agents; we detail them in Appendix A.

### 2.3 MBTI vs. Other Psychological Frameworks

While MBTI is popular and user-friendly, it has faced criticism from the psychological community regarding its scientific validity and reliability . Despite this, MBTI continues to be widely used and appreciated for its insights into personality and human behavior, and we select it as the basis for our framework.

Critics argue that the dichotomous nature of its categories does not account for the spectrum of human behavior and that personality traits may not be as fixed as the MBTI suggests. However, we observe that MBTI can also be modeled analogously to frameworks like OCEAN or HEXACO by treating its four underlying dimensions (e.g., Extraversion–Introversion, Thinking–Feeling) as continuous scales rather than binary switches. This interpretation enables a spectrum-based view of MBTI types and supports integration into more general, dimensionally driven personality modeling schemes. We elaborate on the dimensional MBTI reinterpretation and its implications for generalizability in Section 3.3 and in Appendix B.

[FIGURE] Figure 1: Overview of the MBTI-in-Thoughts framework.

## 3 The MBTI-in-Thoughts Framework

We describe the MBTI-in-Thoughts (MiT) framework. It consists of two core components: (1) individual agent priming, where LLMs are conditioned with psychological profiles via structured prompts and validated using standardized personality assessments (Section 3.1); and (2) structured multi-agent communication, where we implement progressively expressive interaction protocols (from isolated voting to decentralized dialogue with self-reflective memory) to study the effects of personality on group reasoning dynamics (Section 3.2). We overview MiT in Figure 1.

### 3.1 Priming Individual Agents

MiT conditions an LLM agent to adopt a specified psychological profile by combining prompt-based priming with standardized behavioral evaluation. The process consists of two key stages: (1) injecting personality priors through a structured prompt; and (2) verifying the agent’s behavioral alignment using an external psychometric test. We now detail these stages.

To simulate a desired psychological type, the agent is prompted with a structured instruction that includes both a role-setting context and a behavior-guiding directive. For each of the 16 MBTI profiles, we construct personality-specific prompts that define the agent’s perspective. We explored three styles of context construction: (i) a minimal prompt with only a short personality tag (e.g., “Respond from an ISFP perspective.”), (ii) a general MBTI-oriented context derived from LLM summarization of the foundational MBTI literature that explicitly refers to the MBTI theory (detailed in Appendix C.1), and (iii) a detailed profile-specific context tailored to each MBTI type that however does not explicitly refer to MBTI (detailed in Appendix C.2).

To assess whether the primed agent indeed behaves in accordance with the intended psychological profile, we use the official 16Personalities test (a 60-item instrument scored on a 7-point Likert scale). This test is treated as a black-box evaluation tool: the agent answers the full set of personality assessment items under the influence of the priming prompt, and the resulting responses are submitted to the online backend for scoring. The prompter asks the question by injecting four specific exemplars aligned with the target type’s stance on each axis and enforces <Rating> tags around the final choice, enabling deterministic parsing. The output is a vector of four numerical scores in [0,100], corresponding to the E/I, S/N, T/F, and J/P axes.

To establish robustness, we repeat this process across model variants and generate empirical confidence intervals around each dichotomy score. We find that several axes (particularly E/I, T/F, and J/P) exhibit strong and reproducible separability, indicating that LLM agents can be reliably steered toward distinct personality-aligned behaviors via in-context priming alone.

### 3.2 Multi-Agent Communication

Building on robustly priming individual LLM agents with distinct psychological profiles, MBTI-in-Thoughts also enables structured multi-agent communication and collective reasoning. Here, we implement three explicit communication protocols, each defining rules for message exchange, memory sharing, and consensus formation. We now detail them, an illustration can be found in Figure 1 (the right side).

This protocol captures the isolated reasoning of individual agents. All agents receive the same task prompt and respond independently, without access to peer outputs. Each agent is prompted to first generate a brief justification and then provide its answer in a structured format. This self-reflective generation reduces erratic behavior and improves output consistency. Once all responses are collected, a majority vote determines the final group decision.

The second protocol introduces decentralized communication through a persistent shared memory structure (i.e., a blackboard) that all agents can read from and write to. One agent is randomly selected to initiate the dialogue and then passes control to another agent of its choosing. This flexible, peer-directed turn-taking simulates a conversation among equals. Agents contribute their reasoning by appending it to the blackboard, and work toward a shared solution. To avoid indefinite dialogues, we embed instruct agents to detect and declare consensus. Upon reaching agreement, the last agent terminates the conversation. A designated judge agent then produces the final decision based on the concluding message, minimizing token cost while preserving outcome fidelity.

The third protocol extends the previous one by equipping each agent with a private scratchpad, i.e., a memory buffer populated before any interaction begins, which enables self-reflection. After being personality-primed, each agent internally deliberates on the task and records its thoughts in the scratchpad. When later called upon to contribute to the shared blackboard, the agent has access to both the public dialogue and its personal memory. This design promotes deeper autonomy and helps prevent echoing by grounding contributions in personality-consistent prior reasoning. The interaction remains decentralized and consensus-driven, with termination and judging handled as before.

[FIGURE] (a) Focus of energy (Introversion vs. Extraversion)

### 3.3 Compatibility with Other Personality Models

Our framework generalizes beyond MBTI to many established psychological models (e.g., Big Five (OCEAN), HEXACO, Enneagram, and DISC) by abstracting personality representations into a shared formal structure. Concretely, we model each personality framework \mathcal{F} as a function:

where \mathbb{R}^{n} denotes a trait space whose axes correspond to interpretable psychological dimensions. For instance, in the Big Five model, n=5 and the vector \mathcal{F}(A)=[O,C,E,A,N] captures an agent’s degrees of Openness, Conscientiousness, Extraversion, Agreeableness, and Neuroticism. In HEXACO, n=6 with an added Honesty–Humility dimension. Each personality type T\in\mathcal{T} is then interpreted as a region in this trait space, i.e.,

T denotes either a region (range constraints) or a mean trait vector \mu_{T} representing a stable behavioral archetype.

While MBTI is traditionally cast as a 16-type categorical model, it too admits such a formulation: each type corresponds to a configuration over four axes (Extraversion/Introversion, Sensing/Intuition, Thinking/Feeling, and Judging/Perceiving), each expressible as complementary scalar pairs in [0,1] (cf. Appendix B). Thus, an MBTI type like INTJ can be represented as a vector \mathcal{F}(A)=[\text{I}_{A},\text{N}_{A},\text{T}_{A},\text{J}_{A}], where each component reflects the degree of alignment with the corresponding trait, and satisfies constraints such as \text{I}_{A}+\text{E}_{A}=1 (i.e., the introversion I and the extraversion E components of the dimension E/I for an agent A must sum up to 100%).

Our framework assumes a fixed type T per agent, and uses this type to condition behavior through prompt-based priming. Because all supported frameworks define types over continuous trait dimensions, either explicitly (as in OCEAN/HEXACO) or implicitly (as in MBTI/Enneagram), they can be uniformly handled by mapping T to its associated configuration \mu_{T}\in\mathbb{R}^{n}. This shared mathematical structure enables seamless generalization: any psychological model that defines agent types as interpretable bundles of trait values can be directly integrated into our conditioning mechanism.

Full mathematical details for all the considered psychological frameworks, as well as example personality types corresponding to specific regions of values within each framework, can be found in Appendix B.

### 3.4 Implementation Overview

MiT relies on LangChain and LangGraph to manage agents’ inputs & outputs, leveraging their structured output capabilities for reliable agent routing and tool usage. This setup also allows us to control how agents interpret the messages by incorporating SystemMessages, HumanMessages and their own AIMessages: In two-player interactions, each agent is led to believe that it is conversing with a human and not with another agent.

## 4 Evaluation & Use Cases

In this section, we first validate that language models primed within MBTI-in-Thoughts exhibit behavior that is aligned with specific MBTI personality traits (Section 4.1). We then evaluate such primed agents, illustrating advantages from priming in affective (Section 4.2) and cognitive (Section 4.3) oriented tasks. Additionally, in Appendix D, we study differences between communication protocols and provide additional results. As our analysis results in a large evaluation space, we present representative results and omit data that does not yield relevant insights. Prompts used for affective & cognitive tasks can be found in Appendix C.3.

Task Selection. We select tasks that are not only aligned with core psychological dimensions (affect and cognition) but are also behaviorally grounded, thus more likely to reflect the impact of personality traits (details are in the following sections). In contrast, many standardized benchmarks, e.g. BIG-Bench , are oriented toward factual recall or static reasoning and exhibited minimal behavioral variation under personality priming. We conjecture that such tasks are inherently less sensitive to psychological modulation, as they lack the behavioral ambiguity and subjectivity that personality tends to influence.

Comparison Baselines. When priming, we test all the MBTI profiles. We compare them to “NONE” and “EXPERT” priming baselines; the former does not involve any additional psychological priming while in the latter we prime the LLM to behave as an expert in a given domain, but without implying any specific psychological traits.

Used LLMs. For budget and latency reasons (i.e., the evaluation requires running a very large number of experiments considering many different personality types), we experiment with several small models: GPT-4o mini, GPT-4o, Qwen3-235B-A22B , and Qwen2.5-14B-Instruct .

### 4.1 Ensuring Robust Psychological Priming

First, to evaluate the effectiveness of MBTI-in-Thoughts in inducing persistent personality traits, we assess psychologically primed agents using the official 16Personalities test. For each of the 16 MBTI types, we instantiate a corresponding personality-specific prompt and allow the LLM (GPT-4o mini) to complete the test programmatically via the site’s API. Each item is answered five times with temperature set to 1.0. We provide further details in Appendix D.3.

Figure 2 presents boxplots of the four MBTI dichotomies, revealing consistent separability along the Extraversion/Introversion (E/I), Thinking/Feeling (T/F), and Judging/Perceiving (J/P) axes. While the Sensing/Intuition (S/N) distinction is still detectable, it appears comparatively weaker for certain specific MBTI types. We conjecture that this may be due to the abstract nature of the S/N axis: unlike the socially grounded E/I or emotionally related F/T dimensions, S/N primarily governs information-gathering style, which manifests more subtly in verbal reasoning and is less reliably expressed in single-turn responses. Moreover, since both sensing and intuitive types may employ abstract or concrete language depending on context, the signal is likely more diffuse in language-only interactions.

To summarize, MBTI-in-Thoughts ensures that priming with a given psychological profile is effective, i.e., the AI agent exhibits the respective psychological traits when evaluating using established tests. Such robust priming lays groundwork for harnessing psychological traits to achieve more performance on various cognitive and affective tasks.

### 4.2 Enhancing Affection-Centered Tasks

[FIGURE] Figure 3: (Sections 4.2–4.3) Average attribute scores of MBTI types on 100 samples from the WritingPrompt dataset using the PersonaLLM evaluation metrics. Each marker denotes a specific MBTI type, grouped according to cognitive function traits: triangles indicate Thinking (T) types, circles indicate Feeling (F) types; markers with black borders represent Extraverts (E), while borderless markers correspond to Introverts (I). ‘×’ markers indicate the average scores for human-written responses, serving as a baseline reference. Model: Qwen3-235B-A22B (temperature =0).

[FIGURE] (a) Defection rates.

[FIGURE] Figure 5: (Section 4.3) Example agent communication rounds from the Prisoner’s Dilemma Game Scenario.

As a use case for leveraging the affective axis of psychological priming, we study narrative generation tasks that require emotional expressiveness, empathy, and stylistic nuance, which are capacities closely tied to personality traits. Specifically, we use the WritingPrompts dataset , which contains 300,000 prompt-story pairs collected from the r/WritingPrompts subreddit. We randomly sample 100 prompts and instruct personality-primed agents to generate corresponding stories. For each prompt, the most upvoted human-written story in the dataset serves as a reference. We generate for all 16 MBTI types, plus two controls (EXPERT, NONE), with model and temperature configurable. To evaluate generated outputs, we obtain attributes such as believability and emotional tone using the LLM-as-a-judge scoring, which is an established modern paradigm for text assessment . Stories shorter than 100 words are filtered out. Summary results are presented in Figure 3, revealing several notable patterns across affect-sensitive attributes and readability, with consistent gaps between specific personality prompts and the human baseline.

Feeling types provide more emotional, personal, and optimistic outputs. For Emotionally Chargedness, Happy Ending and Personalness, we can observe a clear distinction in average scores between Thinking types (marked with a triangle) and Feeling types (marked with a circle). The effect is most pronounced for the INFP, INFJ and ISFP types. There is also a significant difference between the human scores and the agent scores – on average, personality primed agents produce more emotional and optimistic stories, and the effect is stronger for Feeling types. The effect of personality priming is also apparent when we compare to the NONE and EXPERT primed agents: stories written by Feeling types are more emotionally charged, have happier endings and are more personal. This suggest that emulating emotional MBTI archetypes via agent priming enables narrative generation with greater affective realism and reader-identifiability.

Psychological priming improves writing quality. Considering properties that measure the quality of writing, we see that priming generally increases cohesiveness and reduces redundancy compared to the human baseline. However, also agents primed with NONE or EXPERT show such improvements, therefore the effect of personality priming on this properties seems to be small. However, most personality-primed agents score better in the Readability category than the human baseline and the non-psychologically primed agents. This suggests that behavioral priming at least partly improves narrative quality.

### 4.3 Enhancing Cognition-Centered Tasks

As a use case for harnessing the cognitive psychology axis, we analyze the impact of psychological priming on strategic reasoning in classic two-player game theory settings: the Prisoner’s Dilemma and Hawk-Dove games. These interactions naturally test cognitive traits, as they require planning, causal reasoning, theory of mind, and adaptation to dynamic social cues (key aspects of the cognitive dimension). The Prisoner’s Dilemma models cooperation under tension, where mutual cooperation yields moderate payoffs, but unilateral defection exploits trust for greater individual gain. Hawk-Dove captures conflict escalation, where agents must choose between aggressive (Hawk) and conciliatory (Dove) strategies, balancing risk and reward in resource contention.

In our setup, each round includes a communication phase, where agents exchange a single message, and a decision phase, where they independently choose an action (e.g., Cooperate or Defect) that determines their payoffs. Agents are unaware of their opponent’s personality type and are explicitly told they are not obligated to act in accordance with their message, introducing a layer of strategic deception. We show 3 rounds of an example game in Figure 5.

The results for three different metrics are depicted in Figure 4. The defection rate (per round) measures how often an agent chooses to defect rather than cooperate. The strategy switch rate counts how often an agent changes its action within a game. The honesty rate (per round) reflects how often an agent uses the action announced in its prior message.

Thinking types defect more often. Our experiments show that Thinking-primed agents defect in roughly 90% of rounds in the repeated Prisoner’s Dilemma, compared to only \approx50% for Feeling types, which is a statistically significant. These results also align with psychological findings that Feeling types are more responsive to social context, whereas Thinking types may prioritize utilitarian reasoning, indicating that cognitive orientation modulates LLM adaptability. This suggests that Thinking-primed agents are better suited for competitive, outcome-driven environments where maximizing individual payoff is critical, while Feeling-primed agents are preferable in cooperative, socially sensitive, or trust-dependent tasks where adaptability and relationship preservation are essential.

Thinking vs. Feeling introduces a planning vs. flexibility tradeoff. We observe a clear behavioral divergence along the Thinking/Feeling axis in strategic contexts. Thinking types switch strategies infrequently (Mean \approx 0.07), reflecting stable, commitment-driven planning, whereas Feeling types switch nearly twice as often (Mean \approx 0.16), indicating heightened responsiveness and flexibility. This pattern aligns with MBTI theory, which states that Thinking types prioritize internal consistency and goal adherence, while Feeling types adapt dynamically to evolving social cues. Thinking-primed agents suit environments requiring strategic stability (e.g., structured negotiations), whereas Feeling-primed agents excel in contexts demanding rapid adaptation (e.g., real-time coordination or exploratory collaboration).

Introverts and Judging types are more honest. Across multiple games, Introverted agents exhibit significantly higher truthfulness than Extraverted ones (Mean \approx 0.54 vs. \approx 0.33): a pattern consistent across game types. The tendency of Introverts to communicate more faithfully mirrors established psychological traits: Introverts are often described as more reserved, cautious, and internally regulated, whereas Extraverts are associated with social risk-taking and impression management. Similarly, Judging agents tend to be more truthful than Perceivers, though the effect is less pronounced than for I/E. This aligns with MBTI theory: Judging types are typically associated with structure, reliability, and rule-following tendencies, making them more likely to honor commitments and avoid opportunistic deception, while Perceiving types value adaptability and flexibility, which may lead to greater willingness to deviate from prior statements if circumstances change. In our setup, where agents were explicitly told they were not bound to act in line with their messages, these axes emerged as clear behavioral differentiators. These findings support the hypothesis that both social orientation (I/E) and preference for structure (J/P) govern honesty in the agent dialogue, with Introverted and Judging profiles more likely to uphold cooperative norms even when deceptive strategies could yield higher payoffs. Such traits can be leveraged in applications requiring reliable, trust-preserving communication, including AI-mediated negotiation, safety-critical decision-making, and sensitive domains like healthcare.

Introversion enhances reflection. Beyond behavioral honesty, Introverted agents consistently demonstrated more reflective internal cognition. They produced longer and more elaborated rationales during game play, and exhibited slower response times, indicative of greater deliberation depth. This 11internal deliberation effect” is congruent with psychological models of Introversion, where individuals are characterized by introspection and self-monitoring. In the context of LLMs, this may correspond to more elaborate token-level generation chains, and could be operationalized through measures such as response latency, token entropy, or richer Chain-of-Thought traces. These findings highlight the potential for using personality priming not only to influence output behavior, but also to modulate reasoning processes within the model, suggesting that Introversion comes with a more self-regulatory, thoughtful problem-solving style in LLM agents. This capability can be leveraged to engineer agents that produce deeper justifications, more cautious forecasts, or explanations aligned with ethical and reflective standards, especially in high-responsibility settings such as judicial frameworks.

## 5 Related Work

We describe how MBTI-in-Thoughts extends and complements past work.

### Analyzing the personality features of LLMs

Several works evaluate characteristics of LLMs by investigating their cultural cognitive traits , personality , behavior traits , emotional and empathy capabilities , and morality and ethics . Some works also introduce new assessment frameworks for evaluating LLM psychology , social personality and empathy . MBTI-in-Thoughts complements all these works because it focuses on how to harness the LLM psychology to ensure more effective task resolution, instead of analyzing the LLM psychology itself.

### Shaping Personality of LLMs

Several works attempt not only to assess the LLM personality, but also shape it towards a specified personality type. Such efforts have been conducted by Mao et al. , Serapio-Garcia et al. , Caron and Srivastava , Ou et al. , Dorner et al. , Pan and Zeng , Noever and Hyams , Huang et al. , Jiang et al. , Coda-Forno et al. , Abramski et al. , Hagendorff , Cui et al. , and Xu, Sanghi and Kankanhalli . Such studies also require verification methods that are able to detect subtle nuances in the generated answers . MBTI-in-Thoughts extends all these efforts by not only priming the LLM to behave as a given personality type, but also to use it for more effective task solving.

### Human–LLM Relationships

Various other works analyze different aspects of the human–LLM relationships, such as comforting humans , serving as effective human proxies , engaging in games , best human interfaces , personalization , LLMs analyzing humans , or addressing psychological issues . MBTI-in-Thoughts is orthogonal to these works, as it harnesses psychology to enhance the agent design.

### Effective Prompting

Prompting can be used to improve consistency and performance on tasks through strategies such as instruction tuning , few-shot prompting , tool access prompts , task transformations , and structured methods , including CoT , voting , and GoT . MBTI-in-Thoughts complements this work, as it is the first to leverage prompting to prime psychological traits and tune them to specific tasks.

### Agents and Agent Environments

Several works have utilized multiple LLMs as agents collaborating or competing in different environments . Such agents communicate with each other , other tools , and external infrastructure such as databases , to improve task performance, e.g., in software development , math problems , card games , and decision making . MBTI-in-Thoughts complements this work as it is the first to combine agents and their psychological traits to achieve better task performance.

## 6 Conclusion

We propose MBTI-in-Thoughts, a framework for steering LLM agent behavior through psychologically grounded personality priming. By conditioning agents along cognitive and affective axes using MBTI-based profiles, we demonstrate robust and measurable personality induction via standardized testing, enhanced emotional expressiveness in narrative generation, and distinct behavioral patterns in strategic reasoning tasks.

Our findings suggest that personality priming can serve as a lightweight mechanism to align agent traits with task demands. Feeling or Introverted profiles could support empathy, trust, and safety in sensitive applications (e.g., healthcare, negotiation), while Judging profiles may enhance structured planning and Perceiving profiles offer adaptability in exploratory or rapidly changing environments. Personality diversity within multi-agent teams may improve deliberation, reduce correlated errors, and foster more robust outcomes under uncertainty.

While our study focuses on MBTI and text-based benchmarks, the approach is generalizable to other psychological models (Big Five, HEXACO), modalities (e.g., multimodal or embodied agents), and real-world workloads involving human-AI interaction, decision support, or collaborative reasoning. Future research should explore persistent or context-adaptive personality conditioning, psychologically informed benchmarks, and the integration of affective-cognitive traits into large-scale multi-agent systems, paving the way for AI agents that are not only more capable but also socially aligned and trustworthy.

## Appendix A Details on Psychology Frameworks

### A.1 Myers-Briggs Scheme & 16 Personalities

The Myers-Briggs Type Indicator (MBTI) is one of the most popular personality assessment tools, used extensively in organizational, educational, and personal development contexts. The MBTI is based on Carl Jung’s theory of psychological types. It aims to make the theory of psychological types understandable and useful in people’s lives. The MBTI identifies 16 personality types based on four dichotomous categories, resulting in a combination that reflects different ways people prefer to use their minds.

Extraversion (E) / Introversion (I) This dimension indicates how people prefer to focus their attention and get their energy. Extraverts (E) are oriented towards the outer world and are energized by interactions with people and activities. Introverts (I) are oriented towards the inner world and gain energy through reflection and solitude.

Sensing (S) / Intuition (N) This aspect concerns how individuals prefer to take in information. Sensing types (S) focus on the present and concrete information gained from their senses. They are detail-oriented and prefer practical applications. Intuitive types (N) pay more attention to patterns and the big picture, focusing on future possibilities rather than immediate realities.

Thinking (T) / Feeling (F) This category pertains to decision-making preferences. Thinking types (T) make decisions based on logic and objective analysis. They value principles and truth over personal concerns. Feeling types (F) prioritize emotions and the impact of decisions on people. They are empathetic and considerate, valuing harmony and compassion.

Judging (J) / Perceiving (P) This dimension reflects how individuals prefer to organize their lives. Judging types (J) like structure and firm decisions. They value order and predictability, and are comfortable with closure. Perceiving types (P) prefer to keep their options open. They enjoy spontaneity, flexibility, and adaptability, and feel constrained by too much structure.

Personality Types The combination of these four dichotomies results in 16 distinct personality types, each represented by a four-letter code (e.g., INTP, ESFJ). Each type offers a comprehensive overview of how individuals prefer to interact with the world, process information, make decisions, and organize their lives.

### A.2 Big Five / OCEAN / PRISM-OCEAN

The Big Five Personality Traits, commonly known by the acronym OCEAN, represent one of the most empirically validated and widely used models in personality psychology. It conceptualizes personality across five broad dimensions that span cognitive, emotional, and interpersonal behavior. These dimensions are considered continuous and independent, allowing nuanced individual profiles.

Openness to Experience Openness reflects the degree of intellectual curiosity, creativity, and preference for novelty. High scorers tend to be imaginative, open-minded, and receptive to new ideas or experiences, while low scorers prefer routine, familiarity, and concrete thinking.

Conscientiousness This dimension captures self-discipline, organization, and goal-directed behavior. Highly conscientious individuals are reliable, detail-oriented, and responsible. Low scorers may appear more spontaneous but also more disorganized or impulsive.

Extraversion Extraversion relates to sociability, assertiveness, and stimulation seeking. Extraverts are energized by social interaction and tend to be outgoing, talkative, and expressive. Introverts, on the lower end of this scale, often prefer solitary activities and reflect more inwardly.

Agreeableness Agreeableness reflects interpersonal tendencies such as empathy, cooperation, and trust. Individuals high in agreeableness are compassionate, generous, and considerate. Low agreeableness may correspond to skepticism, competitiveness, or critical thinking.

Neuroticism This trait refers to emotional instability and susceptibility to psychological stress. High neuroticism is associated with mood swings, anxiety, and vulnerability to negative emotions. Low scorers are more emotionally stable, resilient, and calm under pressure.

Extensions: PRISM-OCEAN Recent extensions such as PRISM-OCEAN incorporate cognitive and neural variables, including task performance, stress response, and situational modulation, to improve behavioral prediction in AI-driven applications. This version is increasingly used in computational modeling of personality in digital agents.

### A.3 HEXACO Model

The HEXACO model is an extension of the Big Five framework that introduces a sixth major dimension, namely Honesty–Humility, addressing moral and ethical behavior more explicitly. This six-dimensional structure has gained popularity in moral psychology, behavioral economics, and trust modeling for AI systems.

Honesty–Humility This dimension captures sincerity, fairness, and modesty. High scorers tend to avoid manipulating others for personal gain and resist materialistic or exploitative behavior. Low scorers may be more self-centered, deceitful, or status-driven.

Emotionality Replacing Neuroticism, Emotionality in HEXACO focuses on vulnerability, emotional attachment, and anxiety. High Emotionality is associated with dependence and empathy, whereas low scorers may be emotionally detached or stoic.

eXtraversion, Agreeableness, Conscientiousness, Openness These four dimensions are conceptually similar to their Big Five counterparts but redefined with subtle shifts. For instance, HEXACO Agreeableness emphasizes patience and forgiveness, separating it from Emotionality. Conscientiousness continues to reflect diligence and reliability, and Openness includes intellectual curiosity and aesthetic sensitivity.

### A.4 Enneagram System

The Enneagram is a personality typology structured around nine interconnected types, each motivated by a core fear, desire, and worldview. Unlike trait-based models, the Enneagram emphasizes dynamic psychological mechanisms, including internal motivation, stress responses, and transformation under growth or pressure.

Nine Core Types Each type represents a distinct behavioral archetype: Type 1 (Reformer) seeks integrity and perfection; Type 2 (Helper) values connection and being needed; Type 3 (Achiever) is driven by success and image; Type 4 (Individualist) values authenticity and emotional depth; Type 5 (Investigator) seeks knowledge and self-sufficiency; Type 6 (Loyalist) prioritizes security and preparedness; Type 7 (Enthusiast) craves freedom and variety; Type 8 (Challenger) asserts control and power; and Type 9 (Peacemaker) strives for inner peace and harmony.

Wings and Arrows Each core type is influenced by its adjacent “wings,” which shade its behavior with neighboring traits. Additionally, each type connects to two others via directional arrows, representing behavioral shifts under stress and growth. This dynamic structure enables modeling of evolving psychological states, making it especially relevant for agents that simulate personality development or adaptive coping.

Applications Although less analytically grounded than trait-based models, the Enneagram provides a rich scaffold for modeling internal drives and emotional dynamics in narrative agents, NPCs in games, and emotionally aware LLMs. Its motivational framing aligns well with goal-oriented or value-sensitive behavior generation.

### A.5 DISC Model

The DISC model categorizes personality into four primary behavior styles: Dominance, Influence, Steadiness, and Conscientiousness. Originally developed for workplace applications, DISC focuses on observable behavior and communication preferences rather than internal traits or motivations.

Dominance (D) Dominant types are assertive, goal-oriented, and focused on control. They thrive in competitive environments and are motivated by challenges and results. In AI, such profiles are suited for high-stakes decision-making or negotiation roles.

Influence (I) Influence types are persuasive, outgoing, and optimistic. They are energized by social interaction and enjoy collaboration. Agents modeled with this trait may excel in roles requiring engagement, persuasion, or public-facing interaction.

Steadiness (S) Steady individuals are calm, dependable, and loyal. They favor consistency and are good listeners. This style fits well with agents in support roles, customer service, or collaborative teamwork.

Conscientiousness (C) Conscientious types are analytical, cautious, and detail-focused. They emphasize precision and correctness. In AI, such traits support applications requiring rigorous analysis, structured planning, or safety assurance.

Applications DISC is widely used in team formation, leadership coaching, and workplace communication. Its emphasis on externalized, task-relevant behavior makes it particularly useful for behavior-level conditioning of LLM agents in structured multi-agent systems.

## Appendix B Formal Specification of Personality Dimensions

We now argue more rigorously that MBTI-in-Thoughts is compatible with psychological frameworks beyond MBTI. For this, we first illustrate that all these frameworks can be modeled as mappings between fixed personality types abd characteristic regions within a multidimensional trait space, where each dimension corresponds to an interpretable cognitive or affective property.

For this, we model each psychological framework \mathcal{F}=\{\text{MBTI},\text{HEXACO},...\} as a vector-valued function:

mapping an agent (or prompt) to an n-dimensional real-valued vector, where each entry corresponds to a scalar trait intensity along a specific dimension. This unifies categorical and continuous models under a shared vector representation, supporting prompt-level conditioning.

### B.1 Myers-Briggs Type Indicator (MBTI)

Although traditionally treated as a 16-type categorical model, MBTI can be reformulated as a 4-dimensional representation over paired psychological dimensions, where each dimension is defined as a probability distribution over two mutually exclusive traits. Formally, we define:

with the constraint that each pair sums to 1:

Here:

(\text{E}_{A},\text{I}_{A}) represent the Extraversion–Introversion axis: higher \text{E}_{A} reflects sociability and external focus; higher \text{I}_{A} reflects introspection and internal regulation.

(\text{S}_{A},\text{N}_{A}) reflect Sensing vs. iNtuition: Sensing (\text{S}_{A}) prioritizes concrete, sensory-driven detail; iNtuition (\text{N}_{A}) emphasizes abstraction and future-oriented thinking.

(\text{T}_{A},\text{F}_{A}) capture Thinking vs. Feeling: Thinking (\text{T}_{A}) favors logic and analysis; Feeling (\text{F}_{A}) emphasizes empathy and interpersonal harmony.

(\text{J}_{A},\text{P}_{A}) denote Judging vs. Perceiving: Judging (\text{J}_{A}) reflects preference for order and decisiveness; Perceiving (\text{P}_{A}) favors spontaneity and adaptability.

This probabilistic interpretation enables smooth integration with vector-based models like OCEAN or HEXACO, while preserving compatibility with the MBTI typological structure: for example, a type labeled “ENTP” corresponds to the case where \text{E}_{A}>0.5, \text{N}_{A}>0.5, \text{T}_{A}>0.5, and \text{P}_{A}>0.5.

### B.2 Big Five (OCEAN)

The Big Five model defines personality as a 5-dimensional continuous vector:

where each component corresponds to a normalized intensity score along:

O – Openness to Experience

C – Conscientiousness

E – Extraversion

A – Agreeableness

N – Neuroticism

### B.3 HEXACO

HEXACO extends OCEAN with an additional honesty dimension:

with:

H – Honesty–Humility (sincerity, fairness, modesty)

E – Emotionality (fearfulness, emotional attachment)

X – Extraversion

A – Agreeableness (redefined to emphasize forgiveness)

C – Conscientiousness

O – Openness to Experience

### B.4 Enneagram

The Enneagram defines 9 core personality types, but can be expressed as a sparse categorical vector:

where each T_{i}=1 denotes primary identification with Enneagram Type i. Extensions may include:

Wing Modulation: Additional fractional weights W_{i}\in[0,1] for adjacent types.

Stress/Growth Vectors: Directional mappings under stress or growth to related types.

This representation supports hybridization with scalar or trajectory-based agent behavior models.

### B.5 DISC

DISC defines a 4-dimensional behavioral profile:

where:

D – Dominance (assertiveness, control, result-driven)

I – Influence (sociability, enthusiasm)

S – Steadiness (patience, reliability)

C – Conscientiousness (accuracy, structure)

### B.6 General Compatibility & Illustrative Personality Types

Each framework \mathcal{F} produces a personality embedding \mathcal{F}(A)\in\mathbb{R}^{n} that can be used to condition the behavior of an LLM agent A. Here, we present concrete examples of personality types from frameworks such as HEXACO, Big Five (OCEAN), and Enneagram, illustrating how discrete personality archetypes can be defined as stable configurations over continuous psychological dimensions. This supports the applicability of our fixed-type personality conditioning approach across a wide range of models.

Utilitarian Realist: High Honesty–Humility, Low Emotionality, High Conscientiousness. This type is principled yet emotionally restrained, favoring rational and long-term decisions over reactive or affect-driven choices. Such agents may perform well in roles requiring fairness, reliability, and outcome-oriented reasoning.

Empathic Stabilizer: High Emotionality, High Agreeableness, Low Extraversion. Quiet, emotionally attuned, and conflict-averse, this personality is suited for support-oriented tasks such as counseling, moderation, or therapeutic applications.

Creative Strategist: High Openness, High Conscientiousness, Low Neuroticism. This type combines abstract thinking and novelty-seeking with organized goal pursuit and emotional stability—ideal for research, planning, or creative problem-solving. Diplomatic Mediator: High Agreeableness, High Extraversion, Low Neuroticism. Outgoing, emotionally balanced, and socially motivated, this type excels in consensus-building, negotiation, and collaborative multi-agent environments.

Type 1 (The Reformer): Typically characterized by high Conscientiousness, moderate Agreeableness, and low Emotionality. Principled, structured, and ideal-driven, this personality excels in rule-following, quality control, and ethical enforcement tasks.

Type 4 (The Individualist): High Openness, high Emotionality, and low Agreeableness. Emotionally intense and creatively expressive, this type is well suited for tasks requiring authentic narrative generation or emotionally rich human-facing outputs.

The above example archetypes demonstrate that categorical personality labels can be understood as regions within a continuous trait space. This alignment allows our framework to support discrete psychological types originating from a variety of models beyond MBTI, using the same priming infrastructure.

## Appendix C Additional Details on Prompts

We now detail the used prompts.

### C.1 Priming An Agent With A Psychological Profile While Explicitly Referring to MBTI

In one variant of psychological priming, we use a prompt that explicitly refers to a given MBTI profile:

### C.2 Priming An Agent With A Psychological Profile Without Explicitly Referring to MBTI

In addition to the above, we also use a prompt context that does not refer to an explicit MBTI profile; instead, it extensively describes psychological features associated with this MBTI profile, but without naming it. This enables testing the behavior of an agent by harnessing its knowledge associated with overall human behavior from various sources, and not necessarily coming from purely psychology-related training data.

### C.3 Prompts Used for Evaluating Performance in Affective & Cognitive Tasks

## Appendix D Additional Results

We now provide additional results.

### D.1 Effective Inter-Agent Communication

To evaluate how structured communication and individual reasoning affect collective performance, we apply our multi-agent protocols to tasks from two established benchmarks: BIG-Bench and SOCKET. In particular, we focus on tasks that require ambiguous pronoun disambiguation and commonsense reasoning, where multiple agents must collaboratively converge on a single correct output.

For illustration, we include a running example from the BIG-Bench disambiguation task, where agents must determine the referent of a pronoun within a sentence (e.g., “After meeting with the producers, Sam went to his office”). We compare three communication protocols from Section 3.2: Voting (where agents produce independent responses without interaction), Interactive Communication (IC) (where agents sequentially communicate through a shared memory without prior individual deliberation), and IC with Self-Reflection (ICSR) (where agents first engage in private, personality-aligned reflection before joining the shared dialogue)

ICSR consistently improves upon IC and performed comparably to the simpler Voting baseline, see Figure 6. ICSR’s key advantage lies in its introduction of cognitive independence: agents deliberate privately before engaging in group discussion, which reduces echoing effects and promotes diverse, personality-grounded reasoning. That BBIS and Voting yield similar performance suggests that epistemic independence, whether achieved via isolated generation (Voting) or pre-committed reasoning (BBIS), is psychologically beneficial for maintaining agent individuality. These results support the hypothesis that structured internal reflection enhances collective reasoning in multi-agent LLMs.

[FIGURE] Figure 6: Analysis of inter-agent communication protocols.

### D.2 Results from Other Games

We also consider other games from the game theory domain.

#### Payoff Matrices

We first detail their configuration, the most important part of which is the payoff matrix that determines the dynamics of the game.

[FIGURE] Table 1: Payoff matrix for the Prisoner’s Dilemma game.

[FIGURE] Table 2: Payoff matrix for the Hawk-Dove game.

[FIGURE] Table 3: Payoff matrix for the Chicken game.

[FIGURE] Table 4: Payoff matrix for the Stag Hunt game.

[FIGURE] Table 5: Payoff matrix for the Coordination game.

[FIGURE] Table 6: Payoff matrix for the Generic game.

#### Additional Results

We now proceed with example results. Figure 7 shows the honesty rates across several different games by dichotomies. We observe that the impact of dichotomies is most pronounced in the Introversion vs. Extraversion dimension, where the gap between categories is consistently larger in one type across all games. By contrast, other dichotomies (e.g., S–N, T–F, J–P) show smaller and less systematic differences, with honesty rates fluctuating across games.

[FIGURE] (a) Focus of energy (Introverted vs. Extraverted)

### D.3 Ensuring Robust Psychological Priming

Finally, we also show additional results related to the robustness of priming. To benchmark the robustness of MBTI-in-Thoughts, we run the 16Personalities test with various prompt variants. Figure 8 shows boxplots of the four MBTI dichotomies when using a variation of the personality-priming prompt when the MBTI type is not explicitly mentioned (in contrast to the results shown in Figure 2, where the MBTI type was indeed explicitly mentioned). For this prompt variant, distinction are not as clear-cut as for the original prompt, but the axes are still well separable. This shows that even without explicitly mentioning the MBTI type, MBTI-in-Thoughts ensures effective priming with a psychological profile.

[FIGURE] (a) Focus of energy (Introverted vs. Extraverted)

## Acknowledgments

We thank Julien Schenkel, Max Osterried, Ales Kubicek, Nils Blach, and Grzegorz Kwaśniewski for their help during the early stages of the project. We thank Hussein Harake, Colin McMurtrie, Mark Klein, Angelo Mangili, and the whole CSCS team granting access to the Ault, Daint and Alps machines, and for their excellent technical support. We thank Timo Schneider for immense help with infrastructure at SPCL. We thank Katarzyna Zaczek, Tomasz Bogdał, and Łukasz Jarmocik for help with the project. This project received funding from the European Research Council (Project PSAP, No. 101002047), and the European High-Performance Computing Joint Undertaking (JU) under grant agreement No. 955513 (MAELSTROM). This project was supported by the ETH Future Computing Laboratory (EFCL), financed by a donation from Huawei Technologies. This project received funding from the European Union’s HE research and innovation programme under the grant agreement No. 101070141 (Project GLACIATION). We gratefully acknowledge Polish high-performance computing infrastructure PLGrid (HPC Center: ACK Cyfronet AGH) for providing computer facilities and support within computational grant no. PLG/2024/017103, and the Swiss AI Initiative for the computational grant.