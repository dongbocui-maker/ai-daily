#!/usr/bin/env python3
"""Generate Accenture FY27 IE-style PPT deck from a structured outline JSON.

Usage:
    python3 generate_deck_fy27.py outlines/<slug>.json output/<slug>-fy27.pptx
"""

import json
import sys
from pathlib import Path

from pptx import Presentation

# Local imports (relative to this file's directory)
sys.path.insert(0, str(Path(__file__).parent))

from fy27.style import SLIDE_W, SLIDE_H
from fy27.builders_a import (
    build_cover, build_context, build_agenda, build_section_header, build_stat_grid,
)
from fy27.builders_b import (
    build_quote_pair, build_three_card, build_two_column,
)
from fy27.builders_c import (
    build_insight_pair, build_action_table, build_summary, build_references, build_closing,
)


BUILDERS = {
    "cover": build_cover,
    "context": build_context,
    "agenda": build_agenda,
    "section_header": build_section_header,
    "stat_grid": build_stat_grid,
    "quote_pair": build_quote_pair,
    "three_card": build_three_card,
    "two_column": build_two_column,
    "insight_pair": build_insight_pair,
    "action_table": build_action_table,
    "summary": build_summary,
    "references": build_references,
    "closing": build_closing,
}


def generate(outline_path: Path, output_path: Path):
    with outline_path.open() as f:
        outline = json.load(f)

    slides = outline["slides"]
    total = len(slides)

    prs = Presentation()
    prs.slide_width = SLIDE_W
    prs.slide_height = SLIDE_H

    for idx, slide_data in enumerate(slides):
        page_no = idx + 1
        stype = slide_data.get("type")
        builder = BUILDERS.get(stype)
        if not builder:
            print(f"WARN: no builder for slide type '{stype}' (page {page_no})")
            continue
        builder(prs, slide_data, total, page_no)

    prs.save(output_path)
    print(f"OK: wrote {output_path} ({total} slides)")


def main():
    if len(sys.argv) != 3:
        print("Usage: generate_deck_fy27.py <outline.json> <output.pptx>")
        sys.exit(1)
    generate(Path(sys.argv[1]), Path(sys.argv[2]))


if __name__ == "__main__":
    main()
