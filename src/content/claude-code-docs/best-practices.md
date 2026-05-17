---
slug: claude-code-best-practices
title: "Best Practices for Claude Code"
subtitle: "Anthropic 官方发布 · Agentic Coding 通用最佳实践"
sourceUrl: "https://code.claude.com/docs/en/best-practices"
sourceLabel: "code.claude.com/docs/en/best-practices"
updated: "2026-05-17"
---

<aside class="not-prose my-8 px-6 py-6 bg-gradient-to-br from-accent-purple/10 to-accent-purple/5 border-l-4 border-accent-purple rounded-r">
<h3 class="text-base font-bold text-accent-purple tracking-wide uppercase mb-3">🎯 核心观点汇总（给忙人看的精华）</h3>
<ul class="space-y-2 text-[15px] text-accent-gray-800 leading-relaxed list-disc pl-5">
<li><strong>上下文是最稀缺的资源</strong>。整篇指南的所有实践本质上都在解决一件事：Claude 的上下文窗口会迅速被填满，而填满后表现会显著下降——所以一切都围绕「如何高效用、及时清、隔离用」上下文展开。</li>
<li><strong>给 Claude 一个自检的方法是杠杆最高的一件事</strong>。测试用例、截图、预期输出——任何能让 Claude 自己验证「做对了没」的反馈回路，比你后期一遍遍修正都更省事。</li>
<li><strong>探索 → 计划 → 实施 → 提交（四阶段工作流）</strong>。复杂任务先用 plan mode 探索和规划，再切到实施模式；典型小改动则可以直接跳过 plan 阶段。</li>
<li><strong>提示词的精度决定迭代次数</strong>。说清「改哪个文件、什么场景、参考哪个已有 pattern」比模糊地说「修一下 bug」省下 80% 的修正成本。</li>
<li><strong>CLAUDE.md 是项目记忆，要短、要狠</strong>。只放「Claude 自己猜不到」的东西（特殊 bash 命令、非默认风格、踩过的坑）；写得太长反而会让 Claude 忽略关键规则。</li>
<li><strong>用子代理隔离脏活</strong>。研究、审查、批量调查这类「会读大量文件」的活，交给 subagent 在独立上下文里做，主对话保持干净。</li>
<li><strong>横向扩展：非交互模式 + 并行 session + fan-out</strong>。`claude -p` 进 CI / 脚本；多个 session 跑 worktree；大规模迁移用循环 fan-out 分发。</li>
<li><strong>识别五个反模式</strong>：kitchen sink session、反复纠正、过度膨胀的 CLAUDE.md、信任但未验证、无边界的探索——遇到立刻 `/clear` 或换打法。</li>
</ul>
</aside>

Claude Code is an agentic coding environment. Unlike a chatbot that answers questions and waits, Claude Code can read your files, run commands, make changes, and autonomously work through problems while you watch, redirect, or step away entirely.

This changes how you work. Instead of writing code yourself and asking Claude to review it, you describe what you want and Claude figures out how to build it. Claude explores, plans, and implements.

But this autonomy still comes with a learning curve. Claude works within certain constraints you need to understand.

This guide covers patterns that have proven effective across Anthropic's internal teams and for engineers using Claude Code across various codebases, languages, and environments.

---

Most best practices are based on one constraint: Claude's context window fills up fast, and performance degrades as it fills.

Claude's context window holds your entire conversation, including every message, every file Claude reads, and every command output. However, this can fill up fast. A single debugging session or codebase exploration might generate and consume tens of thousands of tokens.

This matters since LLM performance degrades as context fills. When the context window is getting full, Claude may start "forgetting" earlier instructions or making more mistakes. The context window is the most important resource to manage.

---

<aside class="not-prose my-8 px-6 py-5 bg-accent-purple/5 border-l-4 border-accent-purple rounded-r">
<h3 class="text-sm font-bold text-accent-purple tracking-wide uppercase mb-2">📌 章节导读 · 1. 给 Claude 一个自检的办法</h3>
<p class="text-[15px] text-accent-gray-800 leading-relaxed">这是整个指南里 Anthropic 自己定调的「单点杠杆最高」的实践。让 Claude 自己能跑测试、对比截图、验证输出——它的表现会显著好于「人当唯一回路」的模式。三个典型策略：给验证标准（测试用例、期望值）、用浏览器扩展验证 UI 变化、追根因而非压症状。</p>
</aside>

## Give Claude a way to verify its work

> 💡 **Tip**: Include tests, screenshots, or expected outputs so Claude can check itself. This is the single highest-leverage thing you can do.

Claude performs dramatically better when it can verify its own work, like run tests, compare screenshots, and validate outputs.

Without clear success criteria, it might produce something that looks right but actually doesn't work. You become the only feedback loop, and every mistake requires your attention.

| Strategy | Before | After |
|---|---|---|
| **Provide verification criteria** | *"implement a function that validates email addresses"* | *"write a validateEmail function. example test cases: user@example.com is true, invalid is false, user@.com is false. run the tests after implementing"* |
| **Verify UI changes visually** | *"make the dashboard look better"* | *"[paste screenshot] implement this design. take a screenshot of the result and compare it to the original. list differences and fix them"* |
| **Address root causes, not symptoms** | *"the build is failing"* | *"the build fails with this error: [paste error]. fix it and verify the build succeeds. address the root cause, don't suppress the error"* |

UI changes can be verified using the Claude in Chrome extension. It opens new tabs in your browser, tests the UI, and iterates until the code works.

Your verification can also be a test suite, a linter, or a Bash command that checks output. Invest in making your verification rock-solid.

---

<aside class="not-prose my-8 px-6 py-5 bg-accent-purple/5 border-l-4 border-accent-purple rounded-r">
<h3 class="text-sm font-bold text-accent-purple tracking-wide uppercase mb-2">📌 章节导读 · 2. 探索 → 计划 → 实施 → 提交</h3>
<p class="text-[15px] text-accent-gray-800 leading-relaxed">推荐的四阶段工作流：先用 plan mode 让 Claude 只读不改、理解代码 → 再让它出实施计划 → 切回默认模式让它写代码、跑测试 → 最后提交 PR。<strong>但 plan mode 也有成本</strong>——改一行错别字、加一行日志这种「diff 一句话能描述清楚」的小改动，直接让它干、跳过 plan。Plan 适用于「方案不确定 / 跨多个文件 / 你对代码不熟」三种情况。</p>
</aside>

## Explore first, then plan, then code

> 💡 **Tip**: Separate research and planning from implementation to avoid solving the wrong problem.

Letting Claude jump straight to coding can produce code that solves the wrong problem. Use plan mode to separate exploration from execution.

The recommended workflow has four phases:

**1. Explore** — Enter plan mode. Claude reads files and answers questions without making changes.

```text
read /src/auth and understand how we handle sessions and login.
also look at how we manage environment variables for secrets.
```

**2. Plan** — Ask Claude to create a detailed implementation plan.

```text
I want to add Google OAuth. What files need to change?
What's the session flow? Create a plan.
```

Press `Ctrl+G` to open the plan in your text editor for direct editing before Claude proceeds.

**3. Implement** — Switch out of plan mode and let Claude code, verifying against its plan.

```text
implement the OAuth flow from your plan. write tests for the
callback handler, run the test suite and fix any failures.
```

**4. Commit** — Ask Claude to commit with a descriptive message and create a PR.

```text
commit with a descriptive message and open a PR
```

> ⚠️ **Callout**: Plan mode is useful, but also adds overhead.
>
> For tasks where the scope is clear and the fix is small (like fixing a typo, adding a log line, or renaming a variable) ask Claude to do it directly.
>
> Planning is most useful when you're uncertain about the approach, when the change modifies multiple files, or when you're unfamiliar with the code being modified. If you could describe the diff in one sentence, skip the plan.

---

<aside class="not-prose my-8 px-6 py-5 bg-accent-purple/5 border-l-4 border-accent-purple rounded-r">
<h3 class="text-sm font-bold text-accent-purple tracking-wide uppercase mb-2">📌 章节导读 · 3. 提示词要具体</h3>
<p class="text-[15px] text-accent-gray-800 leading-relaxed">Claude 能推断意图但读不懂你的心。<strong>说清楚四件事</strong>：(1) 任务范围——哪个文件、什么场景、要不要 mock；(2) 信息源——让它去查 git 历史、specific file 而不是凭印象；(3) 已有模式——指向 codebase 里类似的实现作参考；(4) 症状描述——而非「修一下 bug」这种含糊话。<strong>例外</strong>：探索性场景下，模糊提示 (`"这个文件你觉得能改进什么？"`) 反而能挖出你没想到的方向。</p>
</aside>

## Provide specific context in your prompts

> 💡 **Tip**: The more precise your instructions, the fewer corrections you'll need.

Claude can infer intent, but it can't read your mind. Reference specific files, mention constraints, and point to example patterns.

| Strategy | Before | After |
|---|---|---|
| **Scope the task.** Specify which file, what scenario, and testing preferences. | *"add tests for foo.py"* | *"write a test for foo.py covering the edge case where the user is logged out. avoid mocks."* |
| **Point to sources.** Direct Claude to the source that can answer a question. | *"why does ExecutionFactory have such a weird api?"* | *"look through ExecutionFactory's git history and summarize how its api came to be"* |
| **Reference existing patterns.** Point Claude to patterns in your codebase. | *"add a calendar widget"* | *"look at how existing widgets are implemented on the home page to understand the patterns. HotDogWidget.php is a good example. follow the pattern to implement a new calendar widget..."* |
| **Describe the symptom.** Provide the symptom, the likely location, and what "fixed" looks like. | *"fix the login bug"* | *"users report that login fails after session timeout. check the auth flow in src/auth/, especially token refresh. write a failing test that reproduces the issue, then fix it"* |

Vague prompts can be useful when you're exploring and can afford to course-correct. A prompt like `"what would you improve in this file?"` can surface things you wouldn't have thought to ask about.

### Provide rich content

> 💡 **Tip**: Use `@` to reference files, paste screenshots/images, or pipe data directly.

You can provide rich data to Claude in several ways:

- **Reference files with `@`** instead of describing where code lives. Claude reads the file before responding.
- **Paste images directly**. Copy/paste or drag and drop images into the prompt.
- **Give URLs** for documentation and API references. Use `/permissions` to allowlist frequently-used domains.
- **Pipe in data** by running `cat error.log | claude` to send file contents directly.
- **Let Claude fetch what it needs**. Tell Claude to pull context itself using Bash commands, MCP tools, or by reading files.

---

<aside class="not-prose my-8 px-6 py-5 bg-accent-purple/5 border-l-4 border-accent-purple rounded-r">
<h3 class="text-sm font-bold text-accent-purple tracking-wide uppercase mb-2">📌 章节导读 · 4. 配置好你的环境</h3>
<p class="text-[15px] text-accent-gray-800 leading-relaxed">几个一次性设置能让 Claude Code 长期变好用：<strong>(1) CLAUDE.md</strong>——项目持久化记忆，要短狠精；<strong>(2) 权限</strong>——auto mode / 白名单 / sandbox 三选一减少打断；<strong>(3) CLI 工具</strong>——`gh aws gcloud` 这类 CLI 比 API 更省 token；<strong>(4) MCP servers</strong>——接 Notion / Figma / 数据库；<strong>(5) Hooks</strong>——「必须每次都执行」的动作（lint、格式化）；<strong>(6) Skills</strong>——按需加载的领域知识；<strong>(7) Subagents</strong>——隔离上下文的专门助手；<strong>(8) Plugins</strong>——社区/官方打包的能力组合。<strong>关键判断</strong>：广泛适用的放 CLAUDE.md，偶尔用的放 skill；CLAUDE.md 行行问自己「删了这行 Claude 会出错吗？不会就删」。</p>
</aside>

## Configure your environment

A few setup steps make Claude Code significantly more effective across all your sessions.

### Write an effective CLAUDE.md

> 💡 **Tip**: Run `/init` to generate a starter CLAUDE.md file based on your current project structure, then refine over time.

CLAUDE.md is a special file that Claude reads at the start of every conversation. Include Bash commands, code style, and workflow rules. This gives Claude persistent context it can't infer from code alone.

The `/init` command analyzes your codebase to detect build systems, test frameworks, and code patterns, giving you a solid foundation to refine.

There's no required format for CLAUDE.md files, but keep it short and human-readable. For example:

```markdown
# Code style
- Use ES modules (import/export) syntax, not CommonJS (require)
- Destructure imports when possible (eg. import { foo } from 'bar')

# Workflow
- Be sure to typecheck when you're done making a series of code changes
- Prefer running single tests, and not the whole test suite, for performance
```

CLAUDE.md is loaded every session, so only include things that apply broadly. For domain knowledge or workflows that are only relevant sometimes, use **skills** instead. Claude loads them on demand without bloating every conversation.

Keep it concise. For each line, ask: *"Would removing this cause Claude to make mistakes?"* If not, cut it. Bloated CLAUDE.md files cause Claude to ignore your actual instructions!

| ✅ Include | ❌ Exclude |
|---|---|
| Bash commands Claude can't guess | Anything Claude can figure out by reading code |
| Code style rules that differ from defaults | Standard language conventions Claude already knows |
| Testing instructions and preferred test runners | Detailed API documentation (link to docs instead) |
| Repository etiquette (branch naming, PR conventions) | Information that changes frequently |
| Architectural decisions specific to your project | Long explanations or tutorials |
| Developer environment quirks (required env vars) | File-by-file descriptions of the codebase |
| Common gotchas or non-obvious behaviors | Self-evident practices like "write clean code" |

If Claude keeps doing something you don't want despite having a rule against it, the file is probably too long and the rule is getting lost. If Claude asks you questions that are answered in CLAUDE.md, the phrasing might be ambiguous. Treat CLAUDE.md like code: review it when things go wrong, prune it regularly, and test changes by observing whether Claude's behavior actually shifts.

You can tune instructions by adding emphasis (e.g., "IMPORTANT" or "YOU MUST") to improve adherence. Check CLAUDE.md into git so your team can contribute. The file compounds in value over time.

CLAUDE.md files can import additional files using `@path/to/import` syntax:

```markdown
See @README.md for project overview and @package.json for available npm commands.

# Additional Instructions
- Git workflow: @docs/git-instructions.md
- Personal overrides: @~/.claude/my-project-instructions.md
```

You can place CLAUDE.md files in several locations:

- **Home folder (`~/.claude/CLAUDE.md`)**: applies to all Claude sessions
- **Project root (`./CLAUDE.md`)**: check into git to share with your team
- **Project root (`./CLAUDE.local.md`)**: personal project-specific notes; add this file to your `.gitignore` so it isn't shared with your team
- **Parent directories**: useful for monorepos where both `root/CLAUDE.md` and `root/foo/CLAUDE.md` are pulled in automatically
- **Child directories**: Claude pulls in child CLAUDE.md files on demand when working with files in those directories

### Configure permissions

> 💡 **Tip**: Use **auto mode** to let a classifier handle approvals, `/permissions` to allowlist specific commands, or `/sandbox` for OS-level isolation. Each reduces interruptions while keeping you in control.

By default, Claude Code requests permission for actions that might modify your system: file writes, Bash commands, MCP tools, etc. This is safe but tedious. After the tenth approval you're not really reviewing anymore, you're just clicking through. There are three ways to reduce these interruptions:

- **Auto mode**: a separate classifier model reviews commands and blocks only what looks risky: scope escalation, unknown infrastructure, or hostile-content-driven actions. Best when you trust the general direction of a task but don't want to click through every step
- **Permission allowlists**: permit specific tools you know are safe, like `npm run lint` or `git commit`
- **Sandboxing**: enable OS-level isolation that restricts filesystem and network access, allowing Claude to work more freely within defined boundaries

### Use CLI tools

> 💡 **Tip**: Tell Claude Code to use CLI tools like `gh`, `aws`, `gcloud`, and `sentry-cli` when interacting with external services.

CLI tools are the most context-efficient way to interact with external services. If you use GitHub, install the `gh` CLI. Claude knows how to use it for creating issues, opening pull requests, and reading comments. Without `gh`, Claude can still use the GitHub API, but unauthenticated requests often hit rate limits.

Claude is also effective at learning CLI tools it doesn't already know. Try prompts like `Use 'foo-cli-tool --help' to learn about foo tool, then use it to solve A, B, C.`

### Connect MCP servers

> 💡 **Tip**: Run `claude mcp add` to connect external tools like Notion, Figma, or your database.

With **MCP servers**, you can ask Claude to implement features from issue trackers, query databases, analyze monitoring data, integrate designs from Figma, and automate workflows.

### Set up hooks

> 💡 **Tip**: Use hooks for actions that must happen every time with zero exceptions.

**Hooks** run scripts automatically at specific points in Claude's workflow. Unlike CLAUDE.md instructions which are advisory, hooks are deterministic and guarantee the action happens.

Claude can write hooks for you. Try prompts like *"Write a hook that runs eslint after every file edit"* or *"Write a hook that blocks writes to the migrations folder."* Edit `.claude/settings.json` directly to configure hooks by hand, and run `/hooks` to browse what's configured.

### Create skills

> 💡 **Tip**: Create `SKILL.md` files in `.claude/skills/` to give Claude domain knowledge and reusable workflows.

**Skills** extend Claude's knowledge with information specific to your project, team, or domain. Claude applies them automatically when relevant, or you can invoke them directly with `/skill-name`.

Create a skill by adding a directory with a `SKILL.md` to `.claude/skills/`:

```markdown
---
name: api-conventions
description: REST API design conventions for our services
---
# API Conventions
- Use kebab-case for URL paths
- Use camelCase for JSON properties
- Always include pagination for list endpoints
- Version APIs in the URL path (/v1/, /v2/)
```

Skills can also define repeatable workflows you invoke directly:

```markdown
---
name: fix-issue
description: Fix a GitHub issue
disable-model-invocation: true
---
Analyze and fix the GitHub issue: $ARGUMENTS.

1. Use `gh issue view` to get the issue details
2. Understand the problem described in the issue
3. Search the codebase for relevant files
4. Implement the necessary changes to fix the issue
5. Write and run tests to verify the fix
6. Ensure code passes linting and type checking
7. Create a descriptive commit message
8. Push and create a PR
```

Run `/fix-issue 1234` to invoke it. Use `disable-model-invocation: true` for workflows with side effects that you want to trigger manually.

### Create custom subagents

> 💡 **Tip**: Define specialized assistants in `.claude/agents/` that Claude can delegate to for isolated tasks.

**Subagents** run in their own context with their own set of allowed tools. They're useful for tasks that read many files or need specialized focus without cluttering your main conversation.

```markdown
---
name: security-reviewer
description: Reviews code for security vulnerabilities
tools: Read, Grep, Glob, Bash
model: opus
---
You are a senior security engineer. Review code for:
- Injection vulnerabilities (SQL, XSS, command injection)
- Authentication and authorization flaws
- Secrets or credentials in code
- Insecure data handling

Provide specific line references and suggested fixes.
```

Tell Claude to use subagents explicitly: *"Use a subagent to review this code for security issues."*

### Install plugins

> 💡 **Tip**: Run `/plugin` to browse the marketplace. Plugins add skills, tools, and integrations without configuration.

**Plugins** bundle skills, hooks, subagents, and MCP servers into a single installable unit from the community and Anthropic. If you work with a typed language, install a code intelligence plugin to give Claude precise symbol navigation and automatic error detection after edits.

---

<aside class="not-prose my-8 px-6 py-5 bg-accent-purple/5 border-l-4 border-accent-purple rounded-r">
<h3 class="text-sm font-bold text-accent-purple tracking-wide uppercase mb-2">📌 章节导读 · 5. 有效沟通</h3>
<p class="text-[15px] text-accent-gray-800 leading-relaxed">两个高价值套路：<strong>(1) 把 Claude 当资深工程师问</strong>——上手陌生代码库时，直接问「日志怎么工作」「这个 async move 是什么意思」这种问题，比读半天源码快得多；<strong>(2) 让 Claude 反过来面试你</strong>——做大功能时给一个最小描述，让它用 AskUserQuestion 工具反问你技术实现、UI/UX、edge case 和取舍，最后输出一份完整 SPEC.md，再开新 session 干活。这两招把「上下文构建」的工作从你单方面输入变成对话式协同。</p>
</aside>

## Communicate effectively

The way you communicate with Claude Code significantly impacts the quality of results.

### Ask codebase questions

> 💡 **Tip**: Ask Claude questions you'd ask a senior engineer.

When onboarding to a new codebase, use Claude Code for learning and exploration. You can ask Claude the same sorts of questions you would ask another engineer:

- How does logging work?
- How do I make a new API endpoint?
- What does `async move { ... }` do on line 134 of `foo.rs`?
- What edge cases does `CustomerOnboardingFlowImpl` handle?
- Why does this code call `foo()` instead of `bar()` on line 333?

Using Claude Code this way is an effective onboarding workflow, improving ramp-up time and reducing load on other engineers. No special prompting required: ask questions directly.

### Let Claude interview you

> 💡 **Tip**: For larger features, have Claude interview you first. Start with a minimal prompt and ask Claude to interview you using the `AskUserQuestion` tool.

Claude asks about things you might not have considered yet, including technical implementation, UI/UX, edge cases, and tradeoffs.

```text
I want to build [brief description]. Interview me in detail using the AskUserQuestion tool.

Ask about technical implementation, UI/UX, edge cases, concerns, and tradeoffs. Don't ask obvious questions, dig into the hard parts I might not have considered.

Keep interviewing until we've covered everything, then write a complete spec to SPEC.md.
```

Once the spec is complete, start a fresh session to execute it. The new session has clean context focused entirely on implementation, and you have a written spec to reference.

---

<aside class="not-prose my-8 px-6 py-5 bg-accent-purple/5 border-l-4 border-accent-purple rounded-r">
<h3 class="text-sm font-bold text-accent-purple tracking-wide uppercase mb-2">📌 章节导读 · 6. 管理你的 session</h3>
<p class="text-[15px] text-accent-gray-800 leading-relaxed">会话是「持久化 + 可逆」的，要主动经营：<strong>(1) 早纠正、勤纠正</strong>——发现 Claude 跑偏立刻 `Esc` 打断、`/rewind` 回滚、`/clear` 重置，反复纠正超过两次就该重写提示词；<strong>(2) 激进管理上下文</strong>——`/clear`、`/compact <指令>` 主动压缩、checkpoint 选段总结，临时的小问题用 `/btw` 不进上下文；<strong>(3) 用子代理调研</strong>——读大量文件的「探查活」交给独立 session；<strong>(4) Checkpoint 让你敢冒险</strong>——失败就回滚；<strong>(5) Resume 让任务跨天</strong>——给 session 起名当作分支用。</p>
</aside>

## Manage your session

Conversations are persistent and reversible. Use this to your advantage!

### Course-correct early and often

> 💡 **Tip**: Correct Claude as soon as you notice it going off track.

The best results come from tight feedback loops. Though Claude occasionally solves problems perfectly on the first attempt, correcting it quickly generally produces better solutions faster.

- **`Esc`**: stop Claude mid-action with the `Esc` key. Context is preserved, so you can redirect.
- **`Esc + Esc` or `/rewind`**: press `Esc` twice or run `/rewind` to open the rewind menu and restore previous conversation and code state, or summarize from a selected message.
- **`"Undo that"`**: have Claude revert its changes.
- **`/clear`**: reset context between unrelated tasks. Long sessions with irrelevant context can reduce performance.

If you've corrected Claude more than twice on the same issue in one session, the context is cluttered with failed approaches. Run `/clear` and start fresh with a more specific prompt that incorporates what you learned. A clean session with a better prompt almost always outperforms a long session with accumulated corrections.

### Manage context aggressively

> 💡 **Tip**: Run `/clear` between unrelated tasks to reset context.

Claude Code automatically compacts conversation history when you approach context limits, which preserves important code and decisions while freeing space.

During long sessions, Claude's context window can fill with irrelevant conversation, file contents, and commands. This can reduce performance and sometimes distract Claude.

- Use `/clear` frequently between tasks to reset the context window entirely
- When auto compaction triggers, Claude summarizes what matters most, including code patterns, file states, and key decisions
- For more control, run `/compact <instructions>`, like `/compact Focus on the API changes`
- To compact only part of the conversation, use `Esc + Esc` or `/rewind`, select a message checkpoint, and choose **Summarize from here** or **Summarize up to here**.
- Customize compaction behavior in CLAUDE.md with instructions like `"When compacting, always preserve the full list of modified files and any test commands"` to ensure critical context survives summarization
- For quick questions that don't need to stay in context, use `/btw`. The answer appears in a dismissible overlay and never enters conversation history, so you can check a detail without growing context.

### Use subagents for investigation

> 💡 **Tip**: Delegate research with `"use subagents to investigate X"`. They explore in a separate context, keeping your main conversation clean for implementation.

Since context is your fundamental constraint, subagents are one of the most powerful tools available. When Claude researches a codebase it reads lots of files, all of which consume your context. Subagents run in separate context windows and report back summaries:

```text
Use subagents to investigate how our authentication system handles token
refresh, and whether we have any existing OAuth utilities I should reuse.
```

The subagent explores the codebase, reads relevant files, and reports back with findings, all without cluttering your main conversation.

You can also use subagents for verification after Claude implements something:

```text
use a subagent to review this code for edge cases
```

### Rewind with checkpoints

> 💡 **Tip**: Every prompt you send creates a checkpoint. You can restore conversation, code, or both to any previous checkpoint.

Claude automatically snapshots files before each change so a checkpoint can restore them. Double-tap `Escape` or run `/rewind` to open the rewind menu. You can restore conversation only, restore code only, restore both, or summarize from a selected message.

Instead of carefully planning every move, you can tell Claude to try something risky. If it doesn't work, rewind and try a different approach. Checkpoints persist across sessions, so you can close your terminal and still rewind later.

> ⚠️ **Warning**: Checkpoints only track changes made *by Claude*, not external processes. This isn't a replacement for git.

### Resume conversations

> 💡 **Tip**: Name sessions with `/rename` and treat them like branches: each workstream gets its own persistent context.

Claude Code saves conversations locally, so when a task spans multiple sittings you don't have to re-explain the context. Run `claude --continue` to pick up the most recent session, or `claude --resume` to choose from a list. Give sessions descriptive names like `oauth-migration` so you can find them later.

---

<aside class="not-prose my-8 px-6 py-5 bg-accent-purple/5 border-l-4 border-accent-purple rounded-r">
<h3 class="text-sm font-bold text-accent-purple tracking-wide uppercase mb-2">📌 章节导读 · 7. 自动化与扩展</h3>
<p class="text-[15px] text-accent-gray-800 leading-relaxed">单 session 用熟之后，靠并行成倍放大产出：<strong>(1) 非交互模式</strong> `claude -p` 接 CI、pre-commit hook、脚本，可输出 JSON / 流式 JSON 给下游程序消费；<strong>(2) 并行 session</strong>——worktree 隔离、桌面 app 可视化管多个 session、web 版跑在云端 VM、agent teams 自动化协调；典型用法是「Writer / Reviewer」分工，让另一个 session 干净地审查刚写完的代码；<strong>(3) Fan-out 跨文件</strong>——大规模迁移用 for 循环对每个文件跑 `claude -p`，先在 2-3 个上试错、再批量；<strong>(4) Auto mode</strong>——后台分类器审命令，让 Claude 不打断地连续干活。</p>
</aside>

## Automate and scale

Once you're effective with one Claude, multiply your output with parallel sessions, non-interactive mode, and fan-out patterns.

Everything so far assumes one human, one Claude, and one conversation. But Claude Code scales horizontally. The techniques in this section show how you can get more done.

### Run non-interactive mode

> 💡 **Tip**: Use `claude -p "prompt"` in CI, pre-commit hooks, or scripts. Add `--output-format stream-json` for streaming JSON output.

With `claude -p "your prompt"`, you can run Claude non-interactively, without a session. **Non-interactive mode** is how you integrate Claude into CI pipelines, pre-commit hooks, or any automated workflow. The output formats let you parse results programmatically: plain text, JSON, or streaming JSON.

```bash
# One-off queries
claude -p "Explain what this project does"

# Structured output for scripts
claude -p "List all API endpoints" --output-format json

# Streaming for real-time processing
claude -p "Analyze this log file" --output-format stream-json
```

### Run multiple Claude sessions

> 💡 **Tip**: Run multiple Claude sessions in parallel to speed up development, run isolated experiments, or start complex workflows.

Pick the parallel approach that fits how much coordination you want to do yourself:

- **Worktrees**: run separate CLI sessions in isolated git checkouts so edits don't collide
- **Desktop app**: manage multiple local sessions visually, each in its own worktree
- **Claude Code on the web**: run sessions on Anthropic-managed cloud infrastructure in isolated VMs
- **Agent teams**: automated coordination of multiple sessions with shared tasks, messaging, and a team lead

Beyond parallelizing work, multiple sessions enable quality-focused workflows. A fresh context improves code review since Claude won't be biased toward code it just wrote.

For example, use a Writer/Reviewer pattern:

| Session A (Writer) | Session B (Reviewer) |
|---|---|
| `Implement a rate limiter for our API endpoints` | |
| | `Review the rate limiter implementation in @src/middleware/rateLimiter.ts. Look for edge cases, race conditions, and consistency with our existing middleware patterns.` |
| `Here's the review feedback: [Session B output]. Address these issues.` | |

You can do something similar with tests: have one Claude write tests, then another write code to pass them.

### Fan out across files

> 💡 **Tip**: Loop through tasks calling `claude -p` for each. Use `--allowedTools` to scope permissions for batch operations.

For large migrations or analyses, you can distribute work across many parallel Claude invocations:

**1. Generate a task list** — Have Claude list all files that need migrating (e.g., `list all 2,000 Python files that need migrating`)

**2. Write a script to loop through the list**:

```bash
for file in $(cat files.txt); do
  claude -p "Migrate $file from React to Vue. Return OK or FAIL." \
    --allowedTools "Edit,Bash(git commit *)"
done
```

**3. Test on a few files, then run at scale** — Refine your prompt based on what goes wrong with the first 2-3 files, then run on the full set. The `--allowedTools` flag restricts what Claude can do, which matters when you're running unattended.

You can also integrate Claude into existing data/processing pipelines:

```bash
claude -p "<your prompt>" --output-format json | your_command
```

Use `--verbose` for debugging during development, and turn it off in production.

### Run autonomously with auto mode

For uninterrupted execution with background safety checks, use **auto mode**. A classifier model reviews commands before they run, blocking scope escalation, unknown infrastructure, and hostile-content-driven actions while letting routine work proceed without prompts.

```bash
claude --permission-mode auto -p "fix all lint errors"
```

For non-interactive runs with the `-p` flag, auto mode aborts if the classifier repeatedly blocks actions, since there is no user to fall back to.

---

<aside class="not-prose my-8 px-6 py-5 bg-accent-purple/5 border-l-4 border-accent-purple rounded-r">
<h3 class="text-sm font-bold text-accent-purple tracking-wide uppercase mb-2">📌 章节导读 · 8. 避开常见反模式</h3>
<p class="text-[15px] text-accent-gray-800 leading-relaxed">五个高频踩坑，每个都给了一句话解药：<strong>(1) 一锅烩 session</strong>——任务切换没 `/clear`，上下文全是杂质 → 切任务先 `/clear`；<strong>(2) 反复纠正</strong>——两次纠正还是错，说明上下文已经被失败方案污染 → `/clear` 重写提示词；<strong>(3) CLAUDE.md 太膨胀</strong>——长到关键规则被淹没 → 狠删，能用 hook 强制的就别写在 CLAUDE.md；<strong>(4) 信任但没验证</strong>——看着像对的实际不处理 edge case → 没验证手段就别上线；<strong>(5) 无边界探索</strong>——「调查一下 X」会读几百个文件 → 圈定范围 / 用 subagent。</p>
</aside>

## Avoid common failure patterns

These are common mistakes. Recognizing them early saves time:

- **The kitchen sink session.** You start with one task, then ask Claude something unrelated, then go back to the first task. Context is full of irrelevant information.
  > **Fix**: `/clear` between unrelated tasks.
- **Correcting over and over.** Claude does something wrong, you correct it, it's still wrong, you correct again. Context is polluted with failed approaches.
  > **Fix**: After two failed corrections, `/clear` and write a better initial prompt incorporating what you learned.
- **The over-specified CLAUDE.md.** If your CLAUDE.md is too long, Claude ignores half of it because important rules get lost in the noise.
  > **Fix**: Ruthlessly prune. If Claude already does something correctly without the instruction, delete it or convert it to a hook.
- **The trust-then-verify gap.** Claude produces a plausible-looking implementation that doesn't handle edge cases.
  > **Fix**: Always provide verification (tests, scripts, screenshots). If you can't verify it, don't ship it.
- **The infinite exploration.** You ask Claude to "investigate" something without scoping it. Claude reads hundreds of files, filling the context.
  > **Fix**: Scope investigations narrowly or use subagents so the exploration doesn't consume your main context.

---

<aside class="not-prose my-8 px-6 py-5 bg-accent-purple/5 border-l-4 border-accent-purple rounded-r">
<h3 class="text-sm font-bold text-accent-purple tracking-wide uppercase mb-2">📌 章节导读 · 9. 培养你的直觉</h3>
<p class="text-[15px] text-accent-gray-800 leading-relaxed">前面的所有规则都是「通常情况下好用」的起点，不是教条。<strong>有时候反规则才对</strong>：深陷复杂问题时让上下文积累有价值；探索性任务跳过 plan 反而高效；模糊提示在「想看看 Claude 怎么理解问题」时正好。<strong>核心练习</strong>：观察哪些做法让 Claude 表现好（提示结构？上下文？模式？），又是什么让它卡壳（上下文太脏？提示太模糊？任务太大？）——长期下来你会形成任何指南都教不会的直觉。</p>
</aside>

## Develop your intuition

The patterns in this guide aren't set in stone. They're starting points that work well in general, but might not be optimal for every situation.

Sometimes you *should* let context accumulate because you're deep in one complex problem and the history is valuable. Sometimes you should skip planning and let Claude figure it out because the task is exploratory. Sometimes a vague prompt is exactly right because you want to see how Claude interprets the problem before constraining it.

Pay attention to what works. When Claude produces great output, notice what you did: the prompt structure, the context you provided, the mode you were in. When Claude struggles, ask why. Was the context too noisy? The prompt too vague? The task too big for one pass?

Over time, you'll develop intuition that no guide can capture. You'll know when to be specific and when to be open-ended, when to plan and when to explore, when to clear context and when to let it accumulate.

---

## Related resources

- [How Claude Code works](https://code.claude.com/docs/en/how-claude-code-works): the agentic loop, tools, and context management
- [Extend Claude Code](https://code.claude.com/docs/en/features-overview): skills, hooks, MCP, subagents, and plugins
- [Common workflows](https://code.claude.com/docs/en/common-workflows): step-by-step recipes for debugging, testing, PRs, and more
- [CLAUDE.md](https://code.claude.com/docs/en/memory): store project conventions and persistent context
