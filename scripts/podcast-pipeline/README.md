# podcast-pipeline — 精读播客状态机管线

替代旧的单线程 `generate-podcast.sh`。三层职责分离 + 状态机 + 断点续跑。

## 设计目标

之前的痛点：
- NotebookLM CSRF 30s 超时 → 整个流程崩
- COS SSL EOF → 浪费 25 分钟重新生成音频
- 我（钢铁虾）session 切换 → 长任务上下文丢
- 没有断点续跑：失败 = 从头再来

新架构：
- **Layer 1 (`enqueue.py`)**：秒级提交任务，写 state 即返回
- **Layer 2 (`worker.py`)**：cron 每 5 分钟一次，扫 active state 推进
- **Layer 3 (`status.py`)**：秒级查询任务状态

## 状态机

```
submitted → source_added → queued → audio_ready → downloaded → uploaded → published → done
                                                  ↘ stuck (重试过多) ↗
                                                  ↘ failed (不可恢复) ↗
```

每步独立的 handler，**幂等**：成功 → 推进；失败 → attempts +1，state 不变，下次 cron 再跑。

每个任务一个文件：`state/podcasts/<slug>.json`

## 用法

### 提交任务

```bash
python3 enqueue.py <slug>
# 例：
python3 enqueue.py brynjolfsson-generative-ai-at-work
```

会做：
1. 验证精读 JSON 存在 + quotes 格式（防 5/7 那种纯字符串列表的坑）
2. 创建/复用本月 notebook（`AI 日报精读 YYYY-MM`）
3. 加 source（如果同名 source 已存在则复用）
4. 调 `generate audio --json` 拿 task_id
5. 写 state.json (step=queued)，立即返回

如果中间失败，state 文件已存在但 step 卡在某步——下一轮 worker 接管。

### 查状态

```bash
# 总览
python3 status.py

# 详情
python3 status.py <slug>

# JSON 输出
python3 status.py --json
python3 status.py <slug> --json
```

### Worker（cron 自动跑）

cron 每 5 分钟一次：
```
*/5 * * * * cd /root/.openclaw/workspace && /usr/bin/python3 /root/.openclaw/workspace/projects/ai-daily/scripts/podcast-pipeline/worker.py
```

手动测一下：
```bash
# dry-run（只看会做什么）
python3 worker.py --dry-run

# 跑一轮（处理所有 active）
python3 worker.py

# 只跑某个
python3 worker.py --slug <slug>
```

## 故障恢复

### stuck 任务

某 step 重试次数超过 `MAX_ATTEMPTS_PER_STEP` 就会标 `stuck`，worker 跳过。

恢复：
```bash
python3 -c "
import sys; sys.path.insert(0, '/root/.openclaw/workspace/projects/ai-daily/scripts/podcast-pipeline')
import state as S
S.reset_stuck('<slug>')
"
```

### m4a 文件丢失

`/tmp/podcast-*` 偶尔会被系统清理。worker 检测到会自动回退 step：
- `downloaded` 时 m4a 没了 → 自动回退到 `audio_ready`，下次重下

### NotebookLM 报告 task failed

任务标 `failed`（终态）。需要人工：
1. 看 state.json 里的 `last_error`
2. 用 `enqueue.py --force` 重新提交

## 文件位置

```
/root/.openclaw/workspace/projects/ai-daily/scripts/podcast-pipeline/
├── README.md            # 本文档
├── enqueue.py           # Layer 1：提交
├── worker.py            # Layer 2：状态机推进
├── status.py            # Layer 3：查询
├── state.py             # 状态文件读写抽象
└── util.py              # subprocess + NotebookLM CLI 封装

/root/.openclaw/workspace/projects/ai-daily/state/podcasts/
├── <slug>.json          # 活跃任务
├── .archive/            # 归档（done 后挪进来）
└── .logs/               # 日志（enqueue.log / worker.log / cron.log）
```

## MAX_ATTEMPTS_PER_STEP（在 state.py 里）

| step | 上限 | 解释 |
|---|---|---|
| submitted | 3 | 入队失败一般是 NotebookLM 端问题，重试有限 |
| source_added | 5 | source add + index 期望快 |
| queued | 200 | NotebookLM 13-25 min 生成，cron 5min/次，给足 200 次 ≈ 17 小时容错 |
| audio_ready | 5 | 下载失败重试 |
| downloaded | 5 | m4a 丢失会自动回退 |
| uploaded | 8 | COS SSL EOF 偶发抖动，多重试几次 |
| published | 8 | git push 偶发抖动 |

## 设计决策

**为什么不用 OpenClaw cron？** isolated session 5/8 早上踩过失忆坑，model fallback 4/30 还有 bug。系统 cron 简单可靠。

**为什么 Python 而不是 bash？** 状态机用 Python 干净——dict 操作、JSON 读写、原子写。bash 写 state.json 容易出竞态。

**为什么 `MAX_ATTEMPTS` 不是无限？** 防止真正坏掉的任务循环占用资源。stuck 提示介入。

## 历史

2026-05-08 立。替代 `generate-podcast.sh` + `batch-podcast.sh` 的单线程模式。
