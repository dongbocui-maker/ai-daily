---
title: "Two Routes to LLM Coordination from Sakana AI: TRINITY (Evolution Strategy) vs the Conductor (RL)"
title_zh: "Sakana AI 的两条 LLM 协调路线：进化策略的 TRINITY vs 强化学习的 Conductor"
author: "Sakana AI（Jinglue Xu / Stefan Nielsen / Edoardo Cetin / Qi Sun / Peter Schwendeman / Yujin Tang 等）"
author_title: "Sakana AI（日本）/ 密歇根大学 / 东京科学研究所"
publish_date: 2026-04-27
saved_date: 2026-06-24
original_url: "https://arxiv.org/abs/2512.04695"
slug: "sakana-llm-coordination-two-routes"
source: "manual"
fetch_status: "ok"
fetched_at: "2026-06-24T15:34:48.500Z"
fetch_type: "html"
content_length: 2428
tags:
  - "多智能体协调"
  - "LLM-编排"
  - "进化策略"
  - "强化学习"
  - "Test-time-Scaling"
  - "Sakana-AI"
---
# TRINITY: An Evolved LLM Coordinator
*[Submitted on 4 Dec 2025 (v1), last revised 27 Apr 2026 (this version, v3)]*
> 🔗 原文：[https://arxiv.org/abs/2512.04695](https://arxiv.org/abs/2512.04695)
---
[View PDF](https://arxiv.org/pdf/2512.04695) [HTML (experimental)](https://arxiv.org/html/2512.04695v3)

> Abstract:Combining diverse foundation models is promising, but weight-merging is limited by mismatched architectures and closed APIs. Trinity addresses this with a lightweight coordinator that orchestrates collaboration among large language models (LLMs). The coordinator, comprising a compact language model (approximately $0.6$B parameters) and a lightweight head (approximately $10$K parameters), is optimized with an evolutionary strategy for efficient and adaptive delegation. Trinity processes queries over multiple turns, where at each turn the coordinator assigns one of three roles (Thinker, Worker, or Verifier) to a selected LLM, effectively offloading complex skill acquisition from the coordinator itself. Experiments show that Trinity consistently outperforms individual models and existing methods across coding, math, reasoning, and domain knowledge tasks, and generalizes robustly to out-of-distribution tasks. On standard benchmarks, Trinity achieves state-of-the-art results, including a score of 86.2% on LiveCodeBench. Theoretical and empirical analyses identify two main factors behind this performance: (1) the coordinator's hidden-state representations provide rich contextualization of inputs, and (2) under high dimensionality and strict budget constraints, the separable Covariance Matrix Adaptation Evolution Strategy offers advantages over reinforcement learning, imitation learning, and random search by exploiting potential block-epsilon-separability.

Comments:

To appear at the 14th International Conference on Learning Representation (ICLR 2026)

Subjects:

Machine Learning (cs.LG)

Cite as:

[arXiv:2512.04695](https://arxiv.org/abs/2512.04695) \[cs.LG\]

 

(or [arXiv:2512.04695v3](https://arxiv.org/abs/2512.04695v3) \[cs.LG\] for this version)

 

[https://doi.org/10.48550/arXiv.2512.04695](https://doi.org/10.48550/arXiv.2512.04695)

arXiv-issued DOI via DataCite

## Submission history

From: Jinglue Xu \[[view email](https://arxiv.org/show-email/dd8be891/2512.04695)\]  
**[\[v1\]](https://arxiv.org/abs/2512.04695v1)** Thu, 4 Dec 2025 11:45:21 UTC (10,646 KB)  
**[\[v2\]](https://arxiv.org/abs/2512.04695v2)** Mon, 2 Mar 2026 03:04:07 UTC (10,638 KB)  
**\[v3\]** Mon, 27 Apr 2026 04:31:24 UTC (10,646 KB)