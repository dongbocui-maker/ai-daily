#!/usr/bin/env node
// 把 markdown 里的 inline 外链 [text](url) 转换成数字角标 + 文末参考文献
//
// 规则：
// 1. 仅处理外部链接（https://，不含 my.feishu.cn 的内部跳转链）
//    — 但 my.feishu.cn/docx/ 也作为外部参考保留（飞书文档算"原文"）
//    — 站内绝对路径（如 /learn/...）不处理
//    — 资源总索引 v2 等飞书内部链 → 也算参考文献（用户期望"原文名称"）
// 2. 同一 URL 重复出现 → 共享同一个编号
// 3. 文末添加 "## 参考文献"，按编号顺序列出：每条带反向锚点
// 4. 正文角标格式：[<sup>[N]</sup>](#ref-N)，文末条目格式：`<a id="ref-N"></a>N. 名称`
// 5. 保留原链接 text 作为"原文名称"，去重时取第一次出现的 text
//
// 用法：node scripts/markdown-to-footnotes.mjs input.md > output.md

import { readFileSync } from 'fs';

function transform(md) {
  const refs = [];       // [{ url, text }]
  const urlIndex = {};   // url -> 1-based index

  // 提取 frontmatter（保持不动）
  const fmMatch = md.match(/^---\n([\s\S]*?)\n---\n/);
  const frontmatter = fmMatch ? fmMatch[0] : '';
  const body = fmMatch ? md.slice(fmMatch[0].length) : md;

  // 匹配 inline link：[text](url)
  // 注意 markdown 链接 text 可能含转义 ], url 可能含括号——保守匹配，避开嵌套
  const linkRe = /\[([^\[\]]+?)\]\((https?:\/\/[^\s\)]+)\)/g;

  const transformed = body.replace(linkRe, (match, text, url) => {
    // 跳过站内/特殊链接？目前所有 https:// 都进参考
    let idx = urlIndex[url];
    if (idx === undefined) {
      refs.push({ url, text });
      idx = refs.length;
      urlIndex[url] = idx;
    }
    // 保留原 text，后面加上角标
    return `${text}<sup>[[${idx}]](#ref-${idx})</sup>`;
  });

  if (refs.length === 0) return md;

  // 文末添加参考文献区
  const footer = [
    '',
    '---',
    '',
    '## 参考文献',
    '',
    ...refs.flatMap((r, i) => {
      const n = i + 1;
      // 反向锚点 + 编号 + 名称 + URL，每条后面加空行以产生独立段落
      return [`<a id="ref-${n}"></a>${n}. [${r.text}](${r.url})`, ''];
    }),
  ].join('\n');

  return frontmatter + transformed + footer;
}

const path = process.argv[2];
if (!path) {
  console.error('Usage: node markdown-to-footnotes.mjs <input.md>');
  process.exit(1);
}
const md = readFileSync(path, 'utf-8');
process.stdout.write(transform(md));
