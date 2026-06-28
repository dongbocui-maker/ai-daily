---
title: "Thinking to recall: How reasoning unlocks parametric knowledge in LLMs"
title_zh: "为什么「先想再答」能让模型答对它本来答不出的简单事实？谷歌拆开了推理的两台引擎"
author: "Zorik Gekhman, Roee Aharoni, Jonathan Herzig 等"
author_title: "Google Research（与 Technion 合作）"
publish_date: 2026-06-28
saved_date: 2026-06-28
original_url: "https://research.google/blog/thinking-to-recall-how-reasoning-unlocks-parametric-knowledge-in-llms/"
slug: "google-research-thinking-to-recall"
source: "manual"
fetch_status: "ok"
fetched_at: "2026-06-28T01:50:24.257Z"
fetch_type: "html"
content_length: 9825
tags:
  - "推理"
  - "Chain-of-Thought"
  - "参数化知识"
  - "幻觉"
  - "RAG"
  - "可解释性"
  - "Google-Research"
---
# Thinking to recall: How reasoning unlocks parametric knowledge in LLMs
> 🔗 原文：[https://research.google/blog/thinking-to-recall-how-reasoning-unlocks-parametric-knowledge-in-llms/](https://research.google/blog/thinking-to-recall-how-reasoning-unlocks-parametric-knowledge-in-llms/)
---
It is well-established that allowing large language models (LLMs) to generate step-by-step reasoning traces, commonly known as [chain-of-thought](https://research.google/blog/language-models-perform-reasoning-via-chain-of-thought/) (CoT), enhances performance on complex tasks. When a model solves difficult math equations, writes software, or answers multi-hop factual questions, breaking the problem down into manageable logical steps is highly effective.

However, the utility of this approach remains unclear for simple, single-hop factual questions. For instance, consider a query like: _"What year was Mary Engle Pennington inducted into the National Inventors Hall of Fame?"_ An LLM either has the fact stored in its parametric memory (knowledge encoded directly into its weights) or it doesn't; no complex arithmetic or logical deduction is required. So why would a reasoning trace help?

In "[Thinking to Recall: How Reasoning Unlocks Parametric Knowledge in LLMs](https://arxiv.org/abs/2603.09906)”, we investigate this phenomenon. We demonstrate that allowing a model to generate a reasoning trace unlocks correct answers that are otherwise effectively unreachable. To understand why reasoning aids parametric knowledge recall when there are no complex reasoning steps to execute, we conduct a series of hypothesis-driven controlled experiments. Our findings reveal two complementary mechanisms driving this: a computational buffer effect and factual priming.

## Probing the knowledge boundary

We first measure the parametric recall [capability boundary](https://arxiv.org/pdf/2504.13837) using the [pass@k](https://arxiv.org/pdf/2107.03374) metric. Instead of only checking one model-generated answer, pass@k checks if the correct fact exists within multiple generated attempts. By evaluating the presence of successful reasoning paths in the model’s output distribution while being less sensitive to their exact ranking, pass@k helps us estimate the potential of reasoning for factual recall, rather than only looking at the current model’s top-1 behavior. To assess the impact of reasoning while controlling for parametric knowledge, we focus on reasoning LLMs (R-LLMs) where reasoning can be enabled or disabled (toggled on or off), and compare pass@k between these two modes. We focus on the [Gemini-2.5 (Flash and Pro)](https://storage.googleapis.com/deepmind-media/gemini/gemini_v2_5_report.pdf) and [Qwen3-32B](https://arxiv.org/pdf/2505.09388) models, using two challenging closed-book QA datasets: [SimpleQA Verified](https://arxiv.org/pdf/2509.07968) and [EntityQuestions](https://aclanthology.org/2021.emnlp-main.496.pdf).

The results are surprisingly consistent. When reasoning is enabled, the models successfully recall answers that are virtually unrecoverable when reasoning is off. Importantly, this improvement isn't just because the model is decomposing complex questions. This results from our deliberate focus on datasets containing predominantly simple, single-hop questions.

These results raise the question: if the effect does not come from step-by-step reasoning, what reasoning patterns enable the model to retrieve the correct answer?

## Mechanism 1: The computational buffer

Our first hypothesis focuses on the mechanics of generation. We take the [long-standing hypothesis](https://arxiv.org/pdf/2310.02226) that generating extra tokens acts as extended computation time by providing additional forward passes, and test it in the new setting of parametric knowledge recall in R-LLMs. Specifically, we hypothesize that models implicitly use these reasoning tokens as a computational buffer to perform latent processing, independent of the actual semantic content being generated.

To test this, we design an experiment that removes all meaningful content from the reasoning trace . We intercept the model's reasoning process and replace its generated trace with a meaningless string _"Let me think"_, repeated over and over until it matches the length of the original reasoning trace. We then let the model predict the final answer conditioned on this dummy text.

Remarkably, conditioning the model on this meaningless trace substantially improves its ability to recall the correct answer compared to the baseline where reasoning is completely turned off. This provides strong evidence that simply giving the model more computational runway helps it refine its internal state and fetch hard-to-reach facts.

However, this compute-buffer effect has its limits. Pushing the dummy text to longer lengths eventually offers diminishing returns, and it never fully matches the performance of the model's natural reasoning traces. This means that while extra computation helps, the actual content of the thoughts still matters.

## Mechanism 2: Factual priming

When we analyze the natural reasoning traces generated for simple factual questions, we notice a common pattern. The models aren't writing out logical proofs; they are surfacing related facts.

In human cognition, there is a concept known as [spreading activation](https://psycnet.apa.org/record/1976-03421-001), where processing a specific concept primes related concepts in semantic memory, making them easier to retrieve. We hypothesize that language models exhibit a similar generative self-retrieval mechanism, which we call _factual priming_. By generating facts topically related to the question, the model builds a contextual bridge that facilitates the retrieval of the correct answer.

To test hypotheses, we extract just the concrete facts from the model’s reasoning traces, applying strict filtering to strip away any filler text, search plans, or explicit mentions of the final target answer. We then isolate the effect of the recalled facts, and show that conditioning on a short list of recalled facts recovers most of reasoning’s gains and helps even when reasoning is OFF.

For example, if asked for the name of the 10th King of Nepal, a reasoning model might first list the previous nine kings. Recalling those first nine acts as a semantic warm-up, priming the network to successfully recall the 10th. The facts themselves are the stepping stones.

## The hallucination trap

While generative self-retrieval is a powerful mechanism, it introduces a fundamental risk. Because the model generates these intermediate facts itself, they might be hallucinated. We thus check how these reasoning-stage errors impact the final answer. To find out, we build a large-scale auditing pipeline using a search-enabled verifier to independently check the correctness of every single intermediate fact generated across hundreds of thousands of reasoning traces.

The audit reveals a distinct pattern. If a reasoning trace contains even a single hallucinated intermediate fact, the model is significantly less likely to arrive at the correct final answer. This suggests that, while effective, the factual priming mechanism might be fragile.

## Building more reliable models

Understanding these mechanisms provides practical avenues for improving model reliability. Because factual priming is effective and hallucinated intermediate facts degrade performance, we can leverage both insights to improve model accuracy.

To evaluate the potential of these insights, we use a test-time selection strategy that generates multiple reasoning trajectories for a single question, retaining only those that contain verifiable, hallucination-free facts. Prioritizing these trajectories considerably improves accuracy. In practice, this prioritization could be implemented during training via [process rewards](https://openreview.net/pdf?id=v8L0pN6EOi) that encourage factually supported intermediate steps.

## Conclusion

Our findings highlight that reasoning in language models serves a much broader purpose than just task decomposition or mathematical logic. It acts as a fundamental mechanism for exposing a model's internal memory and expanding its parametric knowledge boundary. These insights open up exciting directions for future research. Knowing that factually accurate reasoning traces yield better answers suggests that training recipes can be further optimized. By utilizing process rewards that specifically encourage factually supported intermediate steps, we might be able to train models that are inherently more reliable and less prone to hallucination. We look forward to seeing how the research community continues to explore the intersections of reasoning, memory, and retrieval.

## Acknowledgements

_This research was conducted by Zorik Gekhman, Roee Aharoni, Eran Ofek, Mor Geva, Roi Reichart and Jonathan Herzig. We thank Eyal Ben-David and Avinatan Hassidim for reviewing the work and their valuable suggestions._