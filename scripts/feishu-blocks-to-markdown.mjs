// Usage: node scripts/feishu-blocks-to-markdown.mjs <input.json> > output.md
// Input: { blocks: [...] } from feishu list_blocks
// Output: GFM markdown
import { readFileSync } from 'fs';

function decodeLink(url) {
  let decoded = url;
  for (let i = 0; i < 3; i++) {
    try {
      const next = decodeURIComponent(decoded);
      if (next === decoded) break;
      decoded = next;
    } catch { break; }
  }
  return decoded;
}

function inlineFromElements(elements) {
  if (!elements) return '';
  return elements.map(el => {
    if (!el.text_run) return '';
    const { content, text_element_style: s = {} } = el.text_run;
    let text = content;
    if (s.inline_code) text = '`' + text + '`';
    if (s.italic && !s.inline_code) text = '*' + text + '*';
    if (s.bold && !s.inline_code) text = '**' + text + '**';
    if (s.strikethrough) text = '~~' + text + '~~';
    if (s.link?.url) text = `[${text}](${decodeLink(s.link.url)})`;
    return text;
  }).join('');
}

// Feishu code language enum -> markdown fence label
const LANG_MAP = {
  1: '', 2: 'abap', 3: 'ada', 4: 'apache', 5: 'apex', 6: 'asm', 7: 'bash',
  8: 'csharp', 9: 'cpp', 10: 'c', 11: 'cobol', 12: 'css', 13: 'cuesheet',
  14: 'd', 15: 'dart', 16: 'dockerfile', 17: 'erlang', 18: 'fortran',
  19: 'foxpro', 20: 'go', 21: 'groovy', 22: 'html', 23: 'htmlbars',
  24: 'http', 25: 'haskell', 26: 'json', 27: 'java', 28: 'javascript',
  29: 'julia', 30: 'kotlin', 31: 'latex', 32: 'lisp', 33: 'logo', 34: 'lua',
  35: 'matlab', 36: 'makefile', 37: 'markdown', 38: 'nginx', 39: 'objc',
  40: 'openedgeabl', 41: 'php', 42: 'perl', 43: 'postscript', 44: 'powershell',
  45: 'prolog', 46: 'protobuf', 47: 'python', 48: 'r', 49: 'rpg', 50: 'ruby',
  51: 'rust', 52: 'sas', 53: 'scss', 54: 'sql', 55: 'scala', 56: 'scheme',
  57: 'scratch', 58: 'shell', 59: 'swift', 60: 'thrift', 61: 'typescript',
  62: 'vbscript', 63: 'visualbasic', 64: 'xml', 65: 'yaml', 66: 'cmake',
  67: 'diff', 68: 'gherkin', 69: 'graphql',
};

function langStr(lang) {
  if (typeof lang === 'number') return LANG_MAP[lang] || '';
  if (typeof lang === 'string') return lang.toLowerCase();
  return '';
}

function processBlock(block, blockMap, depth = 0) {
  if (!block) return '';
  const t = block.block_type;

  // Page root
  if (t === 1) {
    return (block.children || [])
      .map(id => processBlock(blockMap[id], blockMap, 0))
      .filter(s => s !== '')
      .join('\n\n');
  }

  // Headings
  if (t === 3) return '# ' + inlineFromElements(block.heading1?.elements);
  if (t === 4) return '## ' + inlineFromElements(block.heading2?.elements);
  if (t === 5) return '### ' + inlineFromElements(block.heading3?.elements);
  if (t === 6) return '#### ' + inlineFromElements(block.heading4?.elements);
  if (t === 7) return '##### ' + inlineFromElements(block.heading5?.elements);
  if (t === 8) return '###### ' + inlineFromElements(block.heading6?.elements);
  // Some docs use 9/10/11 for h7-h9, fold into h6
  if (t === 9 || t === 10 || t === 11) {
    const key = `heading${t - 2}`;
    return '###### ' + inlineFromElements(block[key]?.elements);
  }

  // Text paragraph
  if (t === 2) {
    let line = inlineFromElements(block.text?.elements);
    if (block.children?.length) {
      const child = block.children
        .map(id => processBlock(blockMap[id], blockMap, depth + 1))
        .filter(s => s !== '')
        .join('\n\n');
      if (child) line += '\n\n' + child;
    }
    return line;
  }

  // Bullet
  if (t === 12) {
    const indent = '  '.repeat(depth);
    let line = `${indent}- ${inlineFromElements(block.bullet?.elements)}`;
    if (block.children?.length) {
      const child = block.children
        .map(id => processBlock(blockMap[id], blockMap, depth + 1))
        .filter(s => s !== '')
        .join('\n');
      if (child) line += '\n' + child;
    }
    return line;
  }

  // Ordered
  if (t === 13) {
    const indent = '  '.repeat(depth);
    let line = `${indent}1. ${inlineFromElements(block.ordered?.elements)}`;
    if (block.children?.length) {
      const child = block.children
        .map(id => processBlock(blockMap[id], blockMap, depth + 1))
        .filter(s => s !== '')
        .join('\n');
      if (child) line += '\n' + child;
    }
    return line;
  }

  // Code
  if (t === 14) {
    const lang = langStr(block.code?.style?.language);
    const content = (block.code?.elements || []).map(el => el.text_run?.content || '').join('');
    return '```' + lang + '\n' + content + '\n```';
  }

  // Quote
  if (t === 15) {
    const text = inlineFromElements(block.quote?.elements);
    let out = text.split('\n').map(line => '> ' + line).join('\n');
    if (block.children?.length) {
      const child = block.children
        .map(id => processBlock(blockMap[id], blockMap, 0))
        .filter(s => s !== '')
        .join('\n');
      if (child) out += '\n' + child.split('\n').map(l => '> ' + l).join('\n');
    }
    return out;
  }

  // Todo
  if (t === 17) {
    const indent = '  '.repeat(depth);
    const checked = block.todo?.style?.done ? 'x' : ' ';
    return `${indent}- [${checked}] ${inlineFromElements(block.todo?.elements)}`;
  }

  // Divider
  if (t === 22) return '---';

  // Table
  if (t === 31) {
    const rows = block.table?.property?.row_size || 0;
    const cols = block.table?.property?.column_size || 0;
    if (!rows || !cols) return '';
    const cells = (block.children || []).map(id => blockMap[id]);
    const grid = [];
    for (let r = 0; r < rows; r++) {
      const row = [];
      for (let c = 0; c < cols; c++) {
        const cell = cells[r * cols + c];
        if (!cell) { row.push(''); continue; }
        const cellChildren = (cell.children || []).map(id => blockMap[id]);
        const cellText = cellChildren
          .map(ch => {
            if (!ch) return '';
            if (ch.block_type === 2) return inlineFromElements(ch.text?.elements);
            return processBlock(ch, blockMap, 0);
          })
          .join(' ')
          .replace(/\r?\n+/g, '<br>')
          .replace(/\|/g, '\\|');
        row.push(cellText.trim());
      }
      grid.push(row);
    }
    const lines = [];
    lines.push('| ' + grid[0].join(' | ') + ' |');
    lines.push('| ' + grid[0].map(() => '---').join(' | ') + ' |');
    for (let i = 1; i < grid.length; i++) {
      lines.push('| ' + grid[i].join(' | ') + ' |');
    }
    return lines.join('\n');
  }

  // TableCell — handled by table
  if (t === 32) return '';

  // Callout (19) — render as quote
  if (t === 19) {
    const child = (block.children || [])
      .map(id => processBlock(blockMap[id], blockMap, 0))
      .filter(s => s !== '')
      .join('\n\n');
    if (!child) return '';
    return child.split('\n').map(l => '> ' + l).join('\n');
  }

  // Unknown
  process.stderr.write(`[WARN] Unknown block_type=${t}, id=${block.block_id}\n`);
  return '';
}

const path = process.argv[2];
if (!path) {
  console.error('Usage: node feishu-blocks-to-markdown.mjs <input.json>');
  process.exit(1);
}
const input = JSON.parse(readFileSync(path, 'utf-8'));
const blocks = input.blocks || input.items || [];
if (!Array.isArray(blocks) || blocks.length === 0) {
  console.error('No blocks found in input');
  process.exit(1);
}
const blockMap = Object.fromEntries(blocks.map(b => [b.block_id, b]));
const root = blocks.find(b => b.block_type === 1) || blocks[0];
const md = processBlock(root, blockMap);
process.stdout.write(md + '\n');
