"""Slide builders: insight_pair, action_table, summary, references, closing."""

from pptx.util import Inches, Pt

from .style import C, SLIDE_H
from .drawing import (
    add_blank_slide, set_bg, add_rect, add_textbox, add_paragraphs,
    add_header, add_footer,
)


def build_insight_pair(prs, data, total, page_no):
    slide = add_blank_slide(prs)
    set_bg(slide)
    add_header(slide, eyebrow=data.get("eyebrow"), title=data.get("title"),
               subtitle=data.get("subtitle"))

    cards = data.get("cards", [])
    n = max(len(cards), 1)
    top = 2.20
    h = 4.6
    gap = 0.30
    card_w = (12.3 - gap * (n - 1)) / n

    for i, card in enumerate(cards):
        x = 0.5 + i * (card_w + gap)
        add_rect(slide, Inches(x), Inches(top), Inches(card_w), Inches(h),
                 fill=C["white"], line=C["border"], line_w=Pt(0.5))
        add_rect(slide, Inches(x), Inches(top), Inches(0.10), Inches(h), fill=C["purple"])

        tag = card.get("tag", "")
        if tag:
            pill_w = 1.5
            add_rect(slide, Inches(x + 0.3), Inches(top + 0.25),
                     Inches(pill_w), Inches(0.30), fill=C["teal"])
            add_textbox(slide, Inches(x + 0.3), Inches(top + 0.25),
                        Inches(pill_w), Inches(0.30),
                        tag, font_size=9, bold=True, color=C["white"],
                        align="center", valign="middle", char_spacing=2)
        add_textbox(slide, Inches(x + 0.3), Inches(top + 0.70),
                    Inches(card_w - 0.6), Inches(0.7),
                    card.get("header", ""), font_size=16, bold=True, color=C["ink"])
        add_textbox(slide, Inches(x + 0.3), Inches(top + 1.50),
                    Inches(card_w - 0.6), Inches(1.0),
                    card.get("body", ""), font_size=10.5, color=C["ink_soft"])
        add_rect(slide, Inches(x + 0.3), Inches(top + 2.65),
                 Inches(card_w - 0.6), Inches(0.01), fill=C["border"])
        add_textbox(slide, Inches(x + 0.3), Inches(top + 2.75),
                    Inches(card_w - 0.6), Inches(0.25),
                    card.get("evidence_label", "Evidence").upper(),
                    font_size=8.5, bold=True, color=C["purple"], char_spacing=3)
        add_textbox(slide, Inches(x + 0.3), Inches(top + 3.02),
                    Inches(card_w - 0.6), Inches(0.85),
                    card.get("evidence", ""), font_size=9.5,
                    italic=True, color=C["ink_soft"])

        impl_top = top + h - 1.10
        add_rect(slide, Inches(x + 0.10), Inches(impl_top),
                 Inches(card_w - 0.20), Inches(0.95),
                 fill=C["purple_tint"], line=C["purple_edge"], line_w=Pt(0.5))
        add_textbox(slide, Inches(x + 0.3), Inches(impl_top + 0.08),
                    Inches(card_w - 0.6), Inches(0.25),
                    card.get("implication_label", "Implication").upper(),
                    font_size=8.5, bold=True, color=C["purple_deep"], char_spacing=3)
        add_textbox(slide, Inches(x + 0.3), Inches(impl_top + 0.32),
                    Inches(card_w - 0.6), Inches(0.55),
                    card.get("implication", ""), font_size=10,
                    bold=True, color=C["purple_deep"])

    if data.get("source_note"):
        add_textbox(slide, Inches(0.5), Inches(top + h + 0.05),
                    Inches(12.3), Inches(0.18),
                    data["source_note"], font_size=8, italic=True, color=C["muted"])

    add_footer(slide, page_no, total)


def build_action_table(prs, data, total, page_no):
    slide = add_blank_slide(prs)
    set_bg(slide)
    add_header(slide, eyebrow=data.get("eyebrow"), title=data.get("title"),
               subtitle=data.get("subtitle"))

    actions = data.get("actions", [])
    n = max(len(actions), 1)
    head_top = 2.15
    head_h = 0.40
    add_rect(slide, Inches(0.5), Inches(head_top), Inches(12.3), Inches(head_h),
             fill=C["ink"], line=None)
    headers = ["#", "ACTION", "WHAT TO DO", "VALUE"]
    col_x = [0.5, 1.10, 5.0, 9.2]
    col_w = [0.55, 3.85, 4.15, 3.65]
    for i, txt in enumerate(headers):
        add_textbox(slide, Inches(col_x[i] + 0.1), Inches(head_top),
                    Inches(col_w[i] - 0.1), Inches(head_h),
                    txt, font_size=10, bold=True, color=C["white"],
                    char_spacing=3, valign="middle")

    body_top = head_top + head_h + 0.08
    body_h = 7.0 - body_top - 0.05
    gap = 0.10
    row_h = (body_h - gap * (n - 1)) / n

    for i, act in enumerate(actions):
        y = body_top + i * (row_h + gap)
        bg = C["white"] if i % 2 == 0 else C["bg_soft"]
        add_rect(slide, Inches(0.5), Inches(y), Inches(12.3), Inches(row_h),
                 fill=bg, line=C["border"], line_w=Pt(0.3))
        add_textbox(slide, Inches(col_x[0] + 0.1), Inches(y),
                    Inches(col_w[0]), Inches(row_h),
                    str(i + 1).zfill(2), font_size=18, bold=True,
                    color=C["purple"], valign="middle")
        add_textbox(slide, Inches(col_x[1] + 0.1), Inches(y + 0.08),
                    Inches(col_w[1] - 0.2), Inches(row_h - 0.15),
                    act.get("header", ""), font_size=12, bold=True,
                    color=C["ink"], valign="middle")
        add_textbox(slide, Inches(col_x[2] + 0.1), Inches(y + 0.08),
                    Inches(col_w[2] - 0.2), Inches(row_h - 0.15),
                    act.get("what", ""), font_size=10, color=C["ink_soft"],
                    valign="middle")
        add_textbox(slide, Inches(col_x[3] + 0.1), Inches(y + 0.08),
                    Inches(col_w[3] - 0.2), Inches(row_h - 0.15),
                    act.get("value", ""), font_size=10, italic=True,
                    color=C["purple_deep"], valign="middle")

    add_footer(slide, page_no, total)


def build_summary(prs, data, total, page_no):
    slide = add_blank_slide(prs)
    set_bg(slide)
    add_header(slide, eyebrow=data.get("eyebrow"), title=data.get("title"),
               subtitle=data.get("subtitle"))

    pillars = data.get("pillars", [])
    n = max(len(pillars), 1)
    top = 2.20
    h = 3.6
    gap = 0.20
    card_w = (12.3 - gap * (n - 1)) / n

    for i, p in enumerate(pillars):
        x = 0.5 + i * (card_w + gap)
        add_rect(slide, Inches(x), Inches(top), Inches(card_w), Inches(h),
                 fill=C["purple_tint"], line=C["purple_edge"], line_w=Pt(0.5))
        add_textbox(slide, Inches(x + 0.3), Inches(top + 0.25),
                    Inches(card_w - 0.6), Inches(0.7),
                    str(i + 1).zfill(2), font_size=36, bold=True, color=C["purple"])
        add_textbox(slide, Inches(x + 0.3), Inches(top + 1.10),
                    Inches(card_w - 0.6), Inches(0.6),
                    p.get("header", ""), font_size=15, bold=True, color=C["purple_deep"])
        add_rect(slide, Inches(x + 0.3), Inches(top + 1.78),
                 Inches(0.5), Inches(0.03), fill=C["purple"])
        add_textbox(slide, Inches(x + 0.3), Inches(top + 1.95),
                    Inches(card_w - 0.6), Inches(h - 2.1),
                    p.get("body", ""), font_size=11, color=C["ink_soft"])

    if data.get("closing_line"):
        cl_top = top + h + 0.30
        add_rect(slide, Inches(0.5), Inches(cl_top), Inches(12.3), Inches(0.85),
                 fill=C["ink"], line=None)
        add_textbox(slide, Inches(0.5), Inches(cl_top),
                    Inches(12.3), Inches(0.85),
                    data["closing_line"], font_size=13, italic=True,
                    color=C["white"], align="center", valign="middle")

    add_footer(slide, page_no, total)


def build_references(prs, data, total, page_no):
    slide = add_blank_slide(prs)
    set_bg(slide)
    add_header(slide, eyebrow=data.get("eyebrow"), title=data.get("title"),
               subtitle=data.get("subtitle"))

    blocks = [data.get("primary", {}), data.get("method", {}), data.get("citations", {})]
    top = 2.20
    h = 4.6
    gap = 0.20
    card_w = (12.3 - gap * 2) / 3

    for i, blk in enumerate(blocks):
        x = 0.5 + i * (card_w + gap)
        add_rect(slide, Inches(x), Inches(top), Inches(card_w), Inches(h),
                 fill=C["white"], line=C["border"], line_w=Pt(0.5))
        add_rect(slide, Inches(x), Inches(top), Inches(card_w), Inches(0.05), fill=C["purple"])
        add_textbox(slide, Inches(x + 0.25), Inches(top + 0.20),
                    Inches(card_w - 0.5), Inches(0.45),
                    blk.get("header", "").upper(), font_size=11, bold=True,
                    color=C["purple"], char_spacing=3)
        add_paragraphs(slide, Inches(x + 0.25), Inches(top + 0.75),
                       Inches(card_w - 0.5), Inches(h - 0.85),
                       blk.get("items", []),
                       font_size=9.5, color=C["ink_soft"], bullet=True,
                       line_spacing=1.4)

    add_footer(slide, page_no, total)


def build_closing(prs, data, total, page_no):
    slide = add_blank_slide(prs)
    set_bg(slide)

    add_rect(slide, Inches(8.5), Inches(0), Inches(4.833), SLIDE_H, fill=C["purple"])

    add_textbox(slide, Inches(0.8), Inches(0.6), Inches(2.0), Inches(0.4),
                "accenture", font_size=14, bold=True, color=C["ink"], valign="middle")
    add_rect(slide, Inches(2.45), Inches(0.74), Inches(0.16), Inches(0.16), fill=C["purple"])

    add_textbox(slide, Inches(0.8), Inches(2.6), Inches(7.0), Inches(0.4),
                data.get("eyebrow", "AI DAILY READS").upper(),
                font_size=12, bold=True, color=C["purple"], char_spacing=5)
    add_textbox(slide, Inches(0.8), Inches(3.1), Inches(7.0), Inches(1.5),
                data.get("title", "Thank You"), font_size=48, bold=True, color=C["ink"])
    add_textbox(slide, Inches(0.8), Inches(4.7), Inches(7.0), Inches(0.5),
                data.get("subtitle", ""), font_size=14, italic=True, color=C["ink_soft"])

    if data.get("url_text"):
        add_textbox(slide, Inches(0.8), Inches(5.6), Inches(7.0), Inches(0.3),
                    data.get("url_label", "Read the full source").upper(),
                    font_size=9.5, bold=True, color=C["purple"], char_spacing=3)
        add_textbox(slide, Inches(0.8), Inches(5.95), Inches(7.0), Inches(0.5),
                    data["url_text"], font_size=12, color=C["ink"])

    # right panel content
    add_textbox(slide, Inches(8.85), Inches(2.6),
                Inches(4.3), Inches(0.4),
                "VISIT", font_size=11, bold=True, color=C["white"], char_spacing=4)
    add_textbox(slide, Inches(8.85), Inches(3.1),
                Inches(4.3), Inches(2.0),
                "aidigest.club / reads", font_size=22, bold=True, color=C["white"])
    add_textbox(slide, Inches(8.85), Inches(4.2),
                Inches(4.3), Inches(2.5),
                "Daily curated AI signals \u00b7 Deep-read briefs \u00b7 GitHub trending \u00b7 LMArena monthly rankings",
                font_size=11, italic=True, color=C["white"])
