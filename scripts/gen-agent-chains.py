#!/usr/bin/env python3
"""Generate src/data/agent-chains.json from the live OpenClaw config.

Single source of truth: /root/.openclaw/openclaw.json (agents.list[].model).
The agents dashboard (src/pages/agents/index.astro) previously hardcoded two
tables that had to be hand-synced on every model change:
  1) CHAINS         — per-agent model chain (index 0 = primary, highlighted)
  2) ARCH_AGENT_EP  — primary/fallback endpoint mapping for the topology graph

Both are now derived here so a change in openclaw.json flows automatically.

Output shape (src/data/agent-chains.json):
{
  "generated_at": "...",
  "source": "/root/.openclaw/openclaw.json",
  "chains":       { "<agentId>": ["short1","short2",...], ... },
  "archAgentEp":  { "<agentId>": {"primary":"ep-x","fallback":["ep-y",...]}, ... },
  "chainModelKeys": { "<short>": "<provider/model full>", ... }
}

Short names + endpoint ids MUST stay consistent with the page's existing
CHAIN_MODEL_KEYS / ARCH_MODEL_EP so the rendered UI is byte-identical (except
for genuine config changes).

Fails soft: if openclaw.json is unreadable, we DO NOT overwrite an existing
JSON (so the last-good file survives). Exit 0 with a warning in that case.
"""
import json
import os
import sys
from datetime import datetime, timezone, timedelta

OPENCLAW_CONFIG = os.environ.get('OPENCLAW_CONFIG', '/root/.openclaw/openclaw.json')
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_PATH = os.path.join(REPO, 'src', 'data', 'agent-chains.json')

# Agents rendered on the dashboard (keeps unrelated future agents out of the UI).
KNOWN_AGENTS = ['main', 'aima', 'mk2', 'mk46', 'claude-researcher']

# full provider/model  ->  short label used on the cards / chain rail.
# Mirrors CHAIN_MODEL_KEYS (short->full) in src/pages/agents/index.astro, inverted.
FULL_TO_SHORT = {
    'aigw-claude-48-main/claude-opus-4-8': 'opus-4.8',
    'aigw-claude-48-main/claude-fable-5': 'fable-5',
    'azure-claude-48/claude-opus-4-8': 'opus-4.8',
    'azure-claude/claude-opus-4-7': 'opus-4.7',
    'azure-openai-responses/gpt-5.5': 'gpt-5.5',
    'azure-openai-responses/gpt-5.6-sol-2026-07-09': 'gpt-5.6-sol',
    'qwen/qwen3.7-max': 'qwen3.7-max',
    'anthropic/claude-sonnet-4-6': 'sonnet-4.6',
    'deepseek/DeepSeek-V4-Pro': 'deepseek-v4-pro',
}

# short label -> full provider/model (subset that the page's CHAIN_MODEL_KEYS knows).
# Only shorts that appear in an actual chain get emitted, but keep the full table
# so the page can resolve any of them for live-token lookups.
CHAIN_MODEL_KEYS = {
    'opus-4.8': 'aigw-claude-48-main/claude-opus-4-8',
    'fable-5': 'aigw-claude-48-main/claude-fable-5',
    'gpt-5.5': 'azure-openai-responses/gpt-5.5',
    'gpt-5.6-sol': 'azure-openai-responses/gpt-5.6-sol-2026-07-09',
    'qwen3.7-max': 'qwen/qwen3.7-max',
    'sonnet-4.6': 'anthropic/claude-sonnet-4-6',
}

# full provider/model -> topology endpoint node id.
# Mirrors ARCH_MODEL_EP in src/pages/agents/index.astro.
MODEL_EP = {
    'aigw-claude-48-main/claude-opus-4-8': 'ep-opus',
    'aigw-claude-48-main/claude-fable-5': 'ep-fable',
    'azure-claude-48/claude-opus-4-8': 'ep-opus',
    'azure-claude/claude-opus-4-7': 'ep-opus',
    'anthropic/claude-sonnet-4-6': 'ep-opus',
    'azure-openai-responses/gpt-5.5': 'ep-gpt',
    'azure-openai-responses/gpt-5.6-sol-2026-07-09': 'ep-gpt',
    'qwen/qwen3.7-max': 'ep-qwen',
}


def _load_config():
    with open(OPENCLAW_CONFIG) as f:
        return json.load(f)


def _short(full):
    if full in FULL_TO_SHORT:
        return FULL_TO_SHORT[full]
    # graceful fallback: strip provider prefix so we never emit a raw full ref.
    return full.split('/', 1)[1] if '/' in full else full


def _ep(full):
    return MODEL_EP.get(full, 'ep-opus')  # ep-opus is the neutral default node


def build():
    cfg = _load_config()
    agents = cfg.get('agents') or {}
    defaults = (agents.get('defaults') or {}).get('model') or {}
    default_primary = defaults.get('primary')
    default_fallbacks = defaults.get('fallbacks') or []

    by_id = {}
    for item in (agents.get('list') or []):
        aid = item.get('id')
        if aid:
            by_id[aid] = item

    chains = {}
    arch = {}
    for aid in KNOWN_AGENTS:
        item = by_id.get(aid, {})
        model_cfg = item.get('model') or {}
        primary = model_cfg.get('primary') or default_primary
        fallbacks = model_cfg.get('fallbacks')
        if fallbacks is None:
            fallbacks = default_fallbacks
        if not primary:
            continue
        full_chain = [primary] + list(fallbacks)
        chains[aid] = [_short(m) for m in full_chain]
        arch[aid] = {
            'primary': _ep(primary),
            'fallback': [_ep(m) for m in fallbacks],
        }

    now = datetime.now(timezone(timedelta(hours=8)))
    return {
        'generated_at': now.strftime('%Y-%m-%d %H:%M:%S %z'),
        'source': OPENCLAW_CONFIG,
        'chains': chains,
        'archAgentEp': arch,
        'chainModelKeys': CHAIN_MODEL_KEYS,
    }


def main():
    try:
        data = build()
    except Exception as e:  # noqa: BLE001 — fail soft, keep last-good file
        sys.stderr.write(f'[gen-agent-chains] WARN: {e}; keeping existing {OUT_PATH}\n')
        # Only hard-fail if there is no existing file at all (build would break).
        if not os.path.exists(OUT_PATH):
            sys.stderr.write('[gen-agent-chains] ERROR: no existing file to fall back to\n')
            return 1
        return 0

    # 2026-07-25 P2 降频：除 generated_at 外内容未变则不重写——
    # 否则时间戳每次刷新都制造 git diff，让 deploy 脚本误判「链路变化」而即时 push
    if os.path.exists(OUT_PATH):
        try:
            with open(OUT_PATH) as f:
                old = json.load(f)
            if {k: v for k, v in old.items() if k != 'generated_at'} == \
               {k: v for k, v in data.items() if k != 'generated_at'}:
                sys.stderr.write(f'[gen-agent-chains] unchanged (ignoring timestamp), keep {OUT_PATH}\n')
                return 0
        except Exception:
            pass  # 旧文件坏了就直接重写

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    tmp = OUT_PATH + '.tmp'
    with open(tmp, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write('\n')
    os.replace(tmp, OUT_PATH)
    sys.stderr.write(f'[gen-agent-chains] wrote {OUT_PATH}\n')
    sys.stderr.write(f'  chains: {json.dumps(data["chains"], ensure_ascii=False)}\n')
    return 0


if __name__ == '__main__':
    sys.exit(main())
