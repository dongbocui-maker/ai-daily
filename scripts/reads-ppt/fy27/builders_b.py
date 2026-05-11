"""Slide builders: quote_pair, three_card, two_column."""

from pptx.util import Inches, Pt

from .style import C
from .drawing import (
    add_blank_slide, set_bg, add_rect, add_textbox, add_paragraphs,
    add_header, add_footer,
)


def build_quote_pair(prs, data, total, page_no):
    slide = add_blank_slide(prs)
    set_bg(slide)
    add_header(slide, eyebrow=data.get("eyebrow"), title=data.get("title"),
               subtitle=data.get("subtitle"))

    top = 2.15
    add_rect(slide, Inches(0.5), Inches(top), Inches(7.5), Inches(3.5),
             fill=C["white"], line=C["border"], line_w=Pt(0.5))
    add_rect(slide, Inches(0.5), Inches(top), Inches(7.5), Inches(0.05), fill=C["purple"])

    add_textbox(slide, Inches(0.65), Inches(top + 0.15), Inches(1.5), Inches(1.2),
                "\u201C", font_size=72, bold=True, color=C["purple"])
    add_textbox(slide, Inches(0.85), Inches(top + 0.80), Inches(7), Inches(2.0),
                data.get("primary_quote", ""), font_size=15, italic=True, color=C["ink"])
    add_textbox(slide, Inches(0.85), Inches(top + 3.05), Inches(7), Inches(0.3),
                f"\u2014 {data.get('primary_attrib', '')}", font_size=10,
                bold=True, color=C["purple_deep"])

    sec_x = 8.3
    sec_w = 4.5
    add_rect(slide, Inches(sec_x), Inches(top), Inches(sec_w), Inches(3.5),
             fill=C["purple_tint"], line=C["purple_edge"], line_w=Pt(0.5))
    add_rect(slide, Inches(sec_x), Inches(top), Inches(0.08), Inches(3.5), fill=C["purple"])
    add_textbox(slide, Inches(sec_x + 0.25), Inches(top + 0.25),
                Inches(sec_w - 0.4), Inches(0.3),
                "VOICE FROM THE FIELD", font_size=9, bold=True,
                color=C["purple"], char_spacing=3)
    add_textbox(slide, Inches(sec_x + 0.25), Inches(top + 0.65),
                Inches(sec_w - 0.4), Inches(2.2),
                f"\u201C{data.get('secondary_quote', '')}\u201D",
                font_size=11.5, italic=True, color=C["ink_soft"])
    add_textbox(slide, Inches(sec_x + 0.25), Inches(top + 3.05),
                Inches(sec_w - 0.4), Inches(0.3),
                f"\u2014 {data.get('secondary_attrib', '')}",
                font_size=9, bold=True, color=C["purple_deep"])

    impl_top = 5.85
    add_rect(slide, Inches(0.5), Inches(impl_top), Inches(12.3), Inches(1.15),
             fill=C["ink"], line=None)
    add_textbox(slide, Inches(0.75), Inches(impl_top + 0.18),
                Inches(11.8), Inches(0.3),
                data.get("implication_label", "Why this matters").upper(),
                font_size=10, bold=True, color=C["teal"], char_spacing=3)
    add_textbox(slide, Inches(0.75), Inches(impl_top + 0.50),
                Inches(11.8), Inches(0.6),
                data.get("implication", ""), font_size=12, color=C["white"])

    add_footer(slide, page_no, total)


def build_three_card(prs, data, total, page_no):
    slide = add_blank_slide(prs)
    set_bg(slide)
    add_header(slide, eyebrow=data.get("eyebrow"), title=data.get("title"),
               subtitle=data.get("subtitle"))

    cards = data.get("cards", [])
    n = max(len(cards), 1)
    top = 2.20
    h = 4.8
    gap = 0.20
    card_w = (12.3 - gap * (n - 1)) / n

    for i, card in enumerate(cards):
        x = 0.5 + i * (card_w + gap)
        add_rect(slide, Inches(x), Inches(top), Inches(card_w), Inches(h),
                 fill=C["white"], line=C["border"], line_w=Pt(0.5))
        add_rect(slide, Inches(x), Inches(top), Inches(card_w), Inches(0.05), fill=C["purple"])

        tag = card.get("tag", "")
        if tag:
            pill_w = 1.5
            add_rect(slide, Inches(x + 0.25), Inches(top + 0.22),
                     Inches(pill_w), Inches(0.28), fill=C["purple"])
            add_textbox(slide, Inches(x + 0.25), Inches(top + 0.22),
                        Inches(pill_w), Inches(0.28),
                        tag, font_size=8.5, bold=True, color=C["white"],
                        align="center", valign="middle", char_spacing=2)
        add_textbox(slide, Inches(x + 0.25), Inches(top + 0.62),
                    Inches(card_w - 0.5), Inches(0.85),
                    card.get("header", ""), font_size=14, bold=True, color=C["ink"])
        add_textbox(slide, Inches(x + 0.25), Inches(top + 1.55),
                    Inches(card_w - 0.5), Inches(1.6),
                    card.get("body", ""), font_size=10.5, color=C["ink_soft"])
        add_rect(slide, Inches(x + 0.25), Inches(top + 3.20),
                 Inches(card_w - 0.5), Inches(0.01), fill=C["border"])
        add_textbox(slide, Inches(x + 0.25), Inches(top + 3.30),
                    Inches(card_w - 0.5), Inches(0.25),
                    card.get("evidence_label", "Evidence").upper(),
                    font_size=8.5, bold=True, color=C["purple"], char_spacing=3)
        add_textbox(slide, Inches(x + 0.25), Inches(top + 3.58),
                    Inches(card_w - 0.5), Inches(0.85),
                    card.get("evidence", ""), font_size=9.5,
                    italic=True, color=C["ink_soft"])
        if card.get("source"):
            add_textbox(slide, Inches(x + 0.25), Inches(top + h - 0.32),
                        Inches(card_w - 0.5), Inches(0.25),
                        f"Source: {card['source']}", font_size=8,
                        italic=True, color=C["muted"])

    add_footer(slide, page_no, total)


def build_two_column(prs, data, total, page_no):
    slide = add_blank_slide(prs)
    set_bg(slide)
    add_header(slide, eyebrow=data.get("eyebrow"), title=data.get("title"),
               subtitle=data.get("subtitle"))

    top = 2.20
    h = 3.8
    gap = 0.30
    col_w = (12.3 - gap) / 2

    for i, side in enumerate(["left", "right"]):
        blk = data.get(side, {})
        x = 0.5 + i * (col_w + gap)
        add_rect(slide, Inches(x), Inches(top), Inches(col_w), Inches(h),
                 fill=C["white"], line=C["border"], line_w=Pt(0.5))
        add_rect(slide, Inches(x), Inches(top), Inches(col_w), Inches(0.05), fill=C["purple"])

        label = blk.get("label", "")
        if label:
            pill_w = 1.8
            add_rect(slide, Inches(x + 0.3), Inches(top + 0.22),
                     Inches(pill_w), Inches(0.30), fill=C["purple"])
            add_textbox(slide, Inches(x + 0.3), Inches(top + 0.22),
                        Inches(pill_w), Inches(0.30),
                        label, font_size=9, bold=True, color=C["white"],
                        align="center", valign="middle", char_spacing=2)
        add_textbox(slide, Inches(x + 0.3), Inches(top + 0.65),
                    Inches(col_w - 0.6), Inches(0.55),
                    blk.get("header", ""), font_size=15, bold=True, color=C["ink"])
        add_paragraphs(slide, Inches(x + 0.3), Inches(top + 1.30),
                       Inches(col_w - 0.6), Inches(h - 1.45),
                       blk.get("points", []),
                       font_size=10.5, color=C["ink_soft"], bullet=True,
                       line_spacing=1.35)

    callout_top = top + h + 0.15
    add_rect(slide, Inches(0.5), Inches(callout_top), Inches(12.3), Inches(0.85),
             fill=C["ink"], line=None)
    add_textbox(slide, Inches(0.75), Inches(callout_top + 0.10),
                Inches(11.8), Inches(0.27),
                data.get("callout_label", "Strategic implication").upper(),
                font_size=9.5, bold=True, color=C["teal"], char_spacing=3)
    add_textbox(slide, Inches(0.75), Inches(callout_top + 0.38),
                Inches(11.8), Inches(0.45),
                data.get("callout", ""), font_size=11.5, color=C["white"])

    if data.get("source_note"):
        add_textbox(slide, Inches(0.5), Inches(7.0), Inches(12.3), Inches(0.18),
                    data["source_note"], font_size=8, italic=True, color=C["muted"])

    add_footer(slide, page_no, total)
