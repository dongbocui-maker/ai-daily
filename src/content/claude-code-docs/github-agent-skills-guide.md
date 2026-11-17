---
slug: github-agent-skills-guide
title: "Build once, run on any agent: A practical guide to agent skills"
subtitle: "GitHub 官方 · 把可重复的工程工作沉淀成团队可评审、可复用的 skill 文件——工具、项目上下文与权限仍归运行它的宿主"
sourceUrl: "https://github.blog/ai-and-ml/github-copilot/build-once-run-on-any-agent-a-practical-guide-to-agent-skills/"
sourceLabel: "github.blog · Andrea Griffiths · 2026-11-12"
updated: "2026-11-17"
---

<div class="not-prose my-6 flex flex-wrap gap-3">
<a href="https://github.blog/ai-and-ml/github-copilot/build-once-run-on-any-agent-a-practical-guide-to-agent-skills/" target="_blank" rel="noopener noreferrer" class="inline-flex items-center gap-2 px-4 py-2.5 bg-accent-ink text-white text-sm font-semibold rounded hover:bg-accent-purple transition">📖 官方原文（github.blog）</a>
<a href="https://github.com/githubevents/build-once-run-on-any-agent" target="_blank" rel="noopener noreferrer" class="inline-flex items-center gap-2 px-4 py-2.5 border border-accent-gray-300 text-sm font-semibold rounded hover:border-accent-purple hover:text-accent-purple transition">🛠 配套 Demo 仓库（Proof Agent / Data Forge）</a>
<a href="https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills" target="_blank" rel="noopener noreferrer" class="inline-flex items-center gap-2 px-4 py-2.5 border border-accent-gray-300 text-sm font-semibold rounded hover:border-accent-purple hover:text-accent-purple transition">📘 GitHub Docs · 给 Copilot 添加 skill</a>
</div>

<aside class="not-prose my-8 px-6 py-6 bg-gradient-to-br from-accent-purple/10 to-accent-purple/5 border-l-4 border-accent-purple rounded-r">
<h3 class="text-[length:var(--fs-body)] font-bold text-accent-purple tracking-wide uppercase mb-3">🎯 核心观点汇总（给忙人看的精华）</h3>
<ul class="space-y-2 text-[length:var(--fs-sub)] text-accent-gray-800 leading-relaxed list-disc pl-5">
<li><strong>Skill 承载指令，不承载权限</strong>。agent skill 是以 <code>SKILL.md</code> 为中心的版本化目录，描述何时、如何做一件可重复的事；指令可以跨 agent 共享，工具、凭证、权限仍由运行环境提供。</li>
<li><strong>一个 skill 一件事，且自我验证不算验证</strong>。Proof Agent 示例用独立验证者核对 AI 生成的改动。在其 GitHub Actions 工作流中（见「检查与审批点」一节），验证者拿到原始需求和代码改动，拿不到 coding agent 的自我评估，结论为 <code>PASS</code> / <code>FAIL</code> / <code>PARTIAL</code> 并须引用变更文件中的证据。</li>
<li><strong>大工作流拆成职责清晰的多个 skill，共享同一份上下文</strong>。Data Forge 示例中 <code>forge-init</code> 发现项目细节并写入 resolved manifest，<code>forge-builder</code> 从 issue 编排到 pull request，<code>forge-dbx</code> 统一访问数据平台，<code>forge-lint</code> 套用团队标准；某一步变了只改一个 skill。</li>
<li><strong>项目配置外置到 manifest</strong>。检查可移植性时，原文建议问：另一个团队带上自己的 manifest，能否不重写 skill 直接用。仓库里发现的模式不自动等于要保留的规则；发现的细节要可审阅，涉及业务判断处由人确认或修改。</li>
<li><strong>检查点和审批点写进工作流，强制力留给仓库规则</strong>。support-desk 工作流七个阶段各有人工检查点，schema 变更前要审批；必须阻断合并或部署的检查，在仓库的 CI 检查与规则里配置。</li>
<li><strong>多客户端支持：Data Forge 示例用单一源打包生成</strong>。该示例以 <code>skills/*/SKILL.md</code> 为源，脚本生成 Claude Code、Cursor、GitHub Copilot 各自的文件，并带 CI 用的 <code>--check</code> 模式；原文建议安装后逐个客户端确认 skill 能被识别、引用能加载、所需工具可用、能返回 skill 要求的证据。</li>
<li><strong>Skill 有适用边界</strong>。适合有边界、可重复、受益于可复用判断的工作（checklist、发布、迁移、指标管道）；需要稳定接口、共享状态、审计链、长时运行控制或模型外强制权限的，做成应用更合适。</li>
</ul>
</aside>

<aside class="not-prose my-8 px-6 py-5 bg-accent-purple/5 border-l-4 border-accent-purple rounded-r">
<h3 class="text-[length:var(--fs-sub)] font-bold text-accent-purple tracking-wide uppercase mb-2">📌 章节导读 · 开篇 · Skill 是什么、不是什么</h3>
<p class="text-[length:var(--fs-sub)] text-accent-gray-800 leading-relaxed">文章从一个日常痛点切入：同一件事反复向 agent 解释，或者反复去问那位掌握组织知识的同事。作者给 agent skill 的定义是「以 <code>SKILL.md</code> 为中心的版本化目录，描述何时、如何完成一项可重复的任务」。紧接着给出一条边界：指令可以跨 agent 共享，但工具、凭证和权限仍由运行环境提供——skill 可以写清楚怎么查数据库，却不授予数据库的访问权。作者说明，她在 GitHub Universe 2026 期间与 Procore 数据工程高级经理 Shishir Tewari 现场讲过这个主题，session 标题与本文相同。</p>
</aside>

How many times this week did you re-explain the same task to an agent? How many times did you ask your colleague with deep institutional knowledge how to solve a specific problem? That context shouldn’t be lost in a chat or locked in one person’s head. Agent skills let you capture repeatable instructions so you and your agents can reuse them. The skill you write for yourself tonight can later become part of a team’s pipeline.

An agent skill is a versioned directory centered on a `SKILL.md` file that describes when and how to do a repeatable task. You can share those instructions across agents, but the environment still needs to provide the tools, credentials, and permissions to carry them out. A skill can describe how to query a database, for example, but it doesn’t grant access to that database.

*I covered this topic live with Shishir Tewari, Senior Manager, Data Engineering at Procore, during GitHub Universe 2026. Our session was titled [“Build once, run on any agent: a practical guide to agent skills”](https://reg.githubuniverse.com/flow/github/universe26/attendee-portal/page/sessioncatalog?search=BLD1787B).*

<aside class="not-prose my-8 px-6 py-5 bg-accent-purple/5 border-l-4 border-accent-purple rounded-r">
<h3 class="text-[length:var(--fs-sub)] font-bold text-accent-purple tracking-wide uppercase mb-2">📌 章节导读 · 一个 skill 只做一件事</h3>
<p class="text-[length:var(--fs-sub)] text-accent-gray-800 leading-relaxed">第一条原则：skill 要有清晰的职责、输入和输出。示例是 Proof Agent——用一个独立的验证者去核对 AI 生成的改动是否符合原始需求。理由是如果由同一个 agent 评估自己的工作，它的解释可能影响评审结论。原文把这条规则浓缩成一句话：self-verification is not verification（自我验证不算验证）。frontmatter 里的 <code>name</code> 和 <code>description</code> 负责说明任务与用途，<code>SKILL.md</code> 中的 When to Verify 一节说明何时调用。</p>
</aside>

## Define one job and when it applies

A skill works best when it has a clear job, input, and output. For example, let’s say you’re building an agent that checks AI-generated changes against the original request. If the same agent assesses its own work, its explanation might influence the review. With [Proof Agent](https://github.com/githubevents/build-once-run-on-any-agent/tree/main/demos/proof-agent), we use a separate verifier to examine the changes and provide evidence for its findings. The skill’s frontmatter names the task and describes its purpose:

```
---
name: proof-agent
description: Adversarial verification of AI-generated work. Spawns an independent verifier to check for false claims, broken code, and security issues.
---
```

At the center is a simple rule: self-verification is not verification.

The `When to Verify` section in Proof Agent’s [`SKILL.md`](https://github.com/githubevents/build-once-run-on-any-agent/blob/main/demos/proof-agent/SKILL.md) says when to invoke the skill. The remaining instructions explain what the verifier reviews and what evidence to include in its findings.

<aside class="not-prose my-8 px-6 py-5 bg-accent-purple/5 border-l-4 border-accent-purple rounded-r">
<h3 class="text-[length:var(--fs-sub)] font-bold text-accent-purple tracking-wide uppercase mb-2">📌 章节导读 · 多个 skill 协同完成更大的工作流</h3>
<p class="text-[length:var(--fs-sub)] text-accent-gray-800 leading-relaxed">第二个示例 Data Forge 处理的是另一类问题：让一条数据管道「正确」的判断分散在四个人的脑子里时，这四个人就是路线图——管道的每次改动都取决于他们是否有空，以及他们对数据的了解。做法是把判断拆进几个各司其职的 skill：<code>forge-init</code> 先发现源表、命名规范等细节并写入一份 resolved manifest，其余 skill 都从这份 manifest 读取项目上下文；<code>forge-builder</code> 负责从 issue 一路编排到 pull request，过程中调用 <code>forge-dbx</code> 查询数据平台、调用 <code>forge-lint</code> 套用团队标准，并由人在途中审阅决策。本节末尾给出了 skill 的适用边界：有边界、可重复、受益于可复用判断的工作适合做成 skill；需要稳定接口、共享状态、审计链、长时运行控制或在模型之外强制执行权限的工作流，更适合做成应用。</p>
</aside>

## Coordinate multiple skills for a larger workflow

When the judgment that makes a data pipeline correct lives in four different people’s heads, those four people are the roadmap. Each change to the pipeline depends on their availability and knowledge of the data. [Data Forge](https://github.com/githubevents/build-once-run-on-any-agent/tree/main/demos/dataforge) is an example of how to capture parts of that judgment in skills that work together.

In the [support-desk pipeline example](https://github.com/githubevents/build-once-run-on-any-agent/blob/main/demos/dataforge/examples/support-desk/DEMO.md), we start with a request for metrics that count incidents created and resolved. Before building the pipeline, the `forge-init` skill discovers details such as source tables and naming conventions, then writes them to a resolved manifest. The other skills read that manifest for the project context they need.

The `forge-builder` skill then coordinates the work from the issue through to a pull request. It uses `forge-dbx` to query the data platform and `forge-lint` to apply the team’s standards as it designs and builds the pipeline. A person reviews the proposed decisions along the way, and the resulting pull request contains the pipeline code, schema changes, and tests.

Each skill has a defined responsibility, and they share project context instead of rediscovering it independently. When a step changes, you can change one skill and leave the rest alone.

Skills fit bounded, repeatable work that benefits from reusable judgment, such as a checklist, release, migration, or metric pipeline. If a workflow needs a stable interface, shared state, an audit trail, long-running control, or permissions enforced outside the model, an application is a better fit.

<aside class="not-prose my-8 px-6 py-5 bg-accent-purple/5 border-l-4 border-accent-purple rounded-r">
<h3 class="text-[length:var(--fs-sub)] font-bold text-accent-purple tracking-wide uppercase mb-2">📌 章节导读 · 项目配置不写进 skill</h3>
<p class="text-[length:var(--fs-sub)] text-accent-gray-800 leading-relaxed">项目名、数据库、规范不硬编码进 skill，而是放进 manifest。原文还要求把两类东西分开：「从仓库里发现的项目细节」和「团队标准」。前者由 <code>forge-init</code> 检查现有 schema 与代码模式得到，后者由 <code>forge-lint</code> 提供。仓库里存在的模式不自动等于应当保留的规则，所以发现的细节要可审阅，涉及业务判断处由人确认或修改。原文建议用一个问题来检查可移植性：另一个团队带上自己的 manifest，能否不重写这些 skill 就直接用？</p>
</aside>

## Keep project configuration out of the skill

We don’t want to hardcode every project’s names, database, or conventions into the skills. In the Data Forge support-desk example, a [manifest](https://github.com/githubevents/build-once-run-on-any-agent/blob/main/demos/dataforge/examples/support-desk/dataforge.manifest.yaml) describes the project, metric store, and platform so the skills can use the right project details without baking them into their instructions:

```
project:
  name: "support-desk"
  store_name: "support_metric_store"

platform:
  engine: "duckdb"
  pipeline_framework: "spark_python"
  duckdb_dir: "warehouse"
```

With the discovered details in the resolved manifest, the other skills don’t have to make their own assumptions about the project.

Keep discovered project details separate from team standards. The `forge-init` initialization skill can inspect existing schemas and code patterns; the `forge-lint` skill supplies the rules to follow before code is generated. A pattern found in a repository isn’t automatically a rule to preserve, so make discovered details reviewable and let people confirm or change them where business judgment is needed. To check portability, ask: could another team use these skills with its own manifest without rewriting them?

<aside class="not-prose my-8 px-6 py-5 bg-accent-purple/5 border-l-4 border-accent-purple rounded-r">
<h3 class="text-[length:var(--fs-sub)] font-bold text-accent-purple tracking-wide uppercase mb-2">📌 章节导读 · skill 之间共用一条执行路径</h3>
<p class="text-[length:var(--fs-sub)] text-accent-gray-800 leading-relaxed"><code>forge-dbx</code> 给其他 Data Forge skill 提供一种统一的数据平台访问方式：它读取 manifest，再选择 Databricks 或 DuckDB 适配器，其他 skill 不必各自维护连接和查询逻辑。原文同时说明：manifest 可以为本地 demo 选择 DuckDB，但装不了 DuckDB CLI，也给不了数据库权限。原文的总结是：manifest 选引擎，宿主给访问权。</p>
</aside>

## Share execution paths between skills

The `forge-dbx` skill gives the other Data Forge skills one way to access the data platform. It reads the manifest and selects a Databricks or DuckDB adapter, so each skill doesn’t need its own connection and query logic.

The manifest can choose DuckDB for the local support-desk demo, but it can’t install the DuckDB CLI or grant database access. Those remain setup responsibilities for the environment and its user. The manifest picks the engine; the host provides the access.

<aside class="not-prose my-8 px-6 py-5 bg-accent-purple/5 border-l-4 border-accent-purple rounded-r">
<h3 class="text-[length:var(--fs-sub)] font-bold text-accent-purple tracking-wide uppercase mb-2">📌 章节导读 · 把检查点和审批点放进工作流</h3>
<p class="text-[length:var(--fs-sub)] text-accent-gray-800 leading-relaxed">Data Forge 的 support-desk 工作流共七个阶段，每个阶段都有人工检查点：进入下一阶段前检查上一阶段是否完成，schema 变更执行前请求审批。Proof Agent 把同一原则用到代码评审上：GitHub Actions 工作流只给验证者原始需求和代码改动，不给 coding agent 的自我评估；验证者返回 <code>PASS</code>、<code>FAIL</code> 或 <code>PARTIAL</code>，并且必须引用变更文件中的证据。需要留意两个限定：这个 Action 只做 diff 的静态审查，不执行代码、不跑测试；demo 中设了 <code>block-on-fail: false</code>，结论仅作参考，而默认行为是 <code>FAIL</code> 让检查失败，若该检查被设为必需则阻断合并。作者的落点是让测试结果和合并要求留在仓库的 CI 检查与规则里。</p>
</aside>

## Put checks and approval points in the workflow

The Data Forge support-desk workflow has seven phases, with a human checkpoint at each one. The [workflow overview](https://github.com/githubevents/build-once-run-on-any-agent/blob/main/demos/dataforge/README.md#the-skills) shows how the skills fit together. Before a phase proceeds, the workflow checks that the previous phase is complete; before schema changes run, it asks for approval.

The Proof Agent example applies the same principle to code review. A GitHub Actions workflow gives the verifier the original request and code changes, but not the coding agent’s own assessment. The verifier returns `PASS`, `FAIL`, or `PARTIAL` and must cite evidence in the changed files. The GitHub Action does a static review of the diff; it doesn’t execute code or run tests. In the demo workflow, we set `block-on-fail: false` so findings were advisory. By default, a `FAIL` fails the check, which blocks the merge if the check is required. The aim is to keep test results and merge requirements in your repository’s CI checks and rules.

<aside class="not-prose my-8 px-6 py-5 bg-accent-purple/5 border-l-4 border-accent-purple rounded-r">
<h3 class="text-[length:var(--fs-sub)] font-bold text-accent-purple tracking-wide uppercase mb-2">📌 章节导读 · 按客户端打包，再逐个验证</h3>
<p class="text-[length:var(--fs-sub)] text-accent-gray-800 leading-relaxed">原文指出，支持多个客户端可能意味着要让同一份指令的多个副本保持同步。Data Forge 示例的做法是以 <code>skills/*/SKILL.md</code> 为源，用打包脚本生成各客户端专用文件——Claude Code 的 <code>.claude-plugin/plugin.json</code>、Cursor 的 <code>.cursor-plugin/plugin.json</code>、GitHub Copilot 的 <code>.github/agents/*.agent.md</code>，脚本还带一个给 CI 用的 check 模式。各客户端在可用模型、工具、凭证和权限上都可能不同。原文建议安装后确认四件事：客户端能否针对目标任务识别该 skill、能否加载它的引用文件、能否使用所需工具、能否返回 skill 要求的证据。</p>
</aside>

## Package for each agent client, then verify its setup

Supporting multiple clients can mean keeping several copies of the same instructions in sync. In the Data Forge example, we keep `skills/*/SKILL.md` as the source and use a packaging script to generate client-specific files: `.claude-plugin/plugin.json` for Claude Code, `.cursor-plugin/plugin.json` for Cursor, and `.github/agents/*.agent.md` for GitHub Copilot. The script also includes a check mode for CI:

```
node scripts/package.mjs --check
```

Clients can differ in their available models, tools, credentials, and permissions. After installing a skill, check that the client recognizes it for the intended task, loads its references, can use the required tools, and returns the evidence the skill calls for.

<aside class="not-prose my-8 px-6 py-5 bg-accent-purple/5 border-l-4 border-accent-purple rounded-r">
<h3 class="text-[length:var(--fs-sub)] font-bold text-accent-purple tracking-wide uppercase mb-2">📌 章节导读 · 三条实践</h3>
<p class="text-[length:var(--fs-sub)] text-accent-gray-800 leading-relaxed">全文收束为三条：业务上下文放进一个文件（manifest），让团队有一个看得见的地方更新配置；相关 skill 用同一种方式使用平台，访问路径更容易理解，各客户端下的行为也更容易检查；用指令引导工作、用检查验证工作——skill 可以告诉 agent 遵循什么标准、何时请求审批，但如果某项检查必须阻断合并或部署，要在仓库规则里配置。最后的起步建议是从你已经解释烦了的那件任务开始，写下它需要什么、在哪里停、评审者能看到什么，再换一个 agent 试跑并迭代。</p>
</aside>

## Three practices for building agent skills

1. **Put business context in one file.** Keep project-specific names, schemas, and conventions in a manifest, and have each skill read it instead of duplicating those facts. This gives the team one visible place to update configuration.

2. **Give related skills one consistent way to use the platform.** Have related skills use the same path to run queries, jobs, and schema changes instead of each defining its own commands and connection logic. This makes the workflow’s access easier to understand and its behavior easier to check in each client.

3. **Use instructions to guide the work, and checks to verify it.** A skill can tell an agent which standards to follow and when to ask for approval. Add human review at decisions that need context or judgment, and use tests and CI checks to catch issues before a change moves forward. If a check must block a merge or deployment, configure that requirement in your repository’s rules.

Start with the task you’re tired of explaining. Write down what it needs, where it stops, and what a reviewer sees. Then try it with another agent and improve it as you learn what works.

[Add an agent skill to GitHub Copilot >](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills)

<aside class="not-prose my-8 px-6 py-5 bg-amber-50 border-l-4 border-amber-500 rounded-r">
<h3 class="text-[length:var(--fs-sub)] font-bold text-amber-700 tracking-wide uppercase mb-2">📝 编者按（本站观点，非原文内容）</h3>
<p class="text-[length:var(--fs-sub)] text-accent-gray-800 leading-relaxed">这篇文章的价值不在介绍 skill 的写法，而在给出一个三层分工：skill 管可复用的判断与流程，manifest 管项目上下文，宿主环境与 CI 规则管权限和强制校验。对企业而言，这个分层直接回答了「skill 能否跨 agent 平台复用」的问题——指令层可以复用，工具与权限层必须按平台各自落地并各自验证。另需注意，本页导读只依据博客正文；Proof Agent 与 Data Forge 的实现细节以配套仓库为准，本站未对仓库代码做独立验证。</p>
</aside>
