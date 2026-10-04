#!/usr/bin/env python3
"""Verbatim checker: every sentence of bilingual[].en / quotes[].en must appear in the source md.
Usage: check-verbatim.py <reads-json> <source-md>
Segments separated by '[…]' are checked independently."""
import json, re, sys

def norm(s):
    s = re.sub(r'!\[[^\]]*\]\([^)]*\)', ' ', s)           # images
    s = re.sub(r'\[\d+\]\(#footnote-\d+\)', '', s)        # footnote refs (before links!)
    s = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', s)        # links
    s = s.replace('\\[', '[').replace('\\]', ']')
    s = re.sub(r'[_*]', '', s)
    for a, b in [('\u2019', "'"), ('\u2018', "'"), ('\u201c', '"'), ('\u201d', '"'), ('\u2014', '—')]:
        s = s.replace(a, b)
    return re.sub(r'\s+', ' ', s).strip()

data = json.load(open(sys.argv[1]))
src = norm(open(sys.argv[2]).read())
src = re.sub(r'(\D)\d{1,2}(?=\s)', r'\1', src) if False else src
bad = 0
items = [('bilingual', i, b['en']) for i, b in enumerate(data['bilingual'])] + \
        [('quotes', i, q['en']) for i, q in enumerate(data['quotes'])]
for kind, i, en in items:
    for seg in re.split(r'\s*\[…\]\s*', en):
        for para in seg.split('\n'):
            p = norm(para)
            if not p:
                continue
            # whole paragraph must be contiguous in source (catches silently skipped sentences)
            if p not in src:
                bad += 1
                # locate first failing sentence for diagnostics
                sents = re.split(r'(?<=[.!?)"])\s+(?=[A-Z"(])', p)
                where = next((x for x in sents if x not in src), None)
                if where is None:
                    for k in range(len(sents) - 1):
                        if (sents[k] + ' ' + sents[k + 1]) not in src:
                            where = 'GAP after: ' + sents[k][-80:]; break
                print(f'✗ {kind}[{i}]: {where[:160] if where else p[:120]}')
print(f'\n{"PASS" if bad == 0 else "FAIL"}: {bad} non-verbatim sentence(s)')
sys.exit(1 if bad else 0)
