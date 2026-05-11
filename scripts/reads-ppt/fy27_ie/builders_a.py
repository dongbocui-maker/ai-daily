"""Builders A — cover, context, agenda, section_header.

Schema matches outlines/anthropic-81k-economics.json fields exactly.
"""
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from . import style as S
from .drawing import add_rect, add_textbox, add_paragraphs, add_card
from .chrome import add_header, add_footer


def _fit_size(text, *, base=36, max_chars=7, min_size=18, step=4):
    """Return a pt size that shrinks when text exceeds max_chars."""
    if not text:
        return base
    overflow = max(0, len(text) - max_chars)
    size = base - (overflow // 2) * step
    return max(min_size, size)


# ---------- Cover ----------
def build_cover(slide, sd, page, total):
    meta = sd.get("_deck_meta", {})
    eyebrow = sd.get("eyebrow", "AI DAILY READS · EXECUTIVE BRIEF")
    title = sd.get("title", meta.get("title", ""))
    subtitle = sd.get("subtitle", meta.get("subtitle", ""))
    source_line = sd.get("source_line", "")

    add_header(slide, eyebrow, title, subtitle)
    add_footer(slide, page, total)

    if source_line:
        add_textbox(
            slide, Inches(0.5), Inches(2.05), Inches(12), Inches(0.28),
            source_line,
            font_size=Pt(10), italic=True, color=S.MUTED, margin=Inches(0),
        )

    highlights = sd.get("highlights", [])[:4]
    if not highlights:
        return

    n = len(highlights)
    total_w = Inches(12.333)
    gap = Inches(0.18)
    card_w = (total_w - gap * (n - 1)) / n
    card_h = Inches(2.6)
    top = Inches(3.6)

    for i, h in enumerate(highlights):
        x = Inches(0.5) + (card_w + gap) * i
        add_card(slide, x, top, card_w, card_h,
                 accent_top=True, accent_color=S.PURPLE)
        value = h.get("value", "")
        label = h.get("label", "")
        # auto-shrink long values so they fit on one line
        v_size = _fit_size(value, base=36, max_chars=7, min_size=20)
        add_textbox(
            slide, x, top + Inches(0.35), card_w, Inches(0.95),
            value,
            font_size=Pt(v_size), bold=True, color=S.PURPLE_DEEP,
            align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, margin=Inches(0.05),
        )
        rule_w = Inches(0.6)
        add_rect(slide, x + (card_w - rule_w) / 2, top + Inches(1.55),
                 rule_w, Inches(0.025), fill=S.PURPLE, line=S.PURPLE)
        add_textbox(
            slide, x + Inches(0.15), top + Inches(1.75), card_w - Inches(0.3), Inches(0.75),
            label,
            font_size=Pt(11), italic=True, color=S.INK_SOFT,
            align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.TOP, margin=Inches(0.02),
        )


# ---------- Context (FROM / TO + optional stat_band) ----------
def build_context(slide, sd, page, total):
    add_header(slide, sd.get("eyebrow", ""), sd.get("title", ""),
               sd.get("subtitle"))
    add_footer(slide, page, total)

    km = sd.get("key_message") or sd.get("source_note")
    y_top = Inches(2.10)
    if km:
        add_rect(slide, Inches(0.5), y_top, Inches(12.333), Inches(0.42),
                 fill=S.PURPLE_TINT, line=S.PURPLE_EDGE)
        add_rect(slide, Inches(0.5), y_top, Inches(0.10), Inches(0.42),
                 fill=S.PURPLE, line=S.PURPLE)
        add_textbox(
            slide, Inches(0.75), y_top, Inches(12.0), Inches(0.42),
            km,
            font_size=Pt(10.5), italic=True, color=S.PURPLE_DEEP,
            anchor=MSO_ANCHOR.MIDDLE, margin=Inches(0.05),
        )
        y_top = y_top + Inches(0.58)

    from_b = sd.get("from_block", {})
    to_b = sd.get("to_block", {})

    col_w = Inches(6.0)
    gap = Inches(0.333)
    x_left = Inches(0.5)
    x_right = x_left + col_w + gap

    # Determine card height; reserve space for stat_band if present
    stat_band = sd.get("stat_band", [])
    col_h = Inches(3.7) if stat_band else Inches(4.7)

    _build_fromto_card(slide, x_left, y_top, col_w, col_h,
                       label=from_b.get("label", "FROM"),
                       header=from_b.get("header", ""),
                       points=from_b.get("points", []),
                       label_color=S.MUTED,
                       header_color=S.INK_SOFT)
    _build_fromto_card(slide, x_right, y_top, col_w, col_h,
                       label=to_b.get("label", "TO"),
                       header=to_b.get("header", ""),
                       points=to_b.get("points", []),
                       label_color=S.PURPLE,
                       header_color=S.INK,
                       accent_top=True)

    # stat band at the bottom
    if stat_band:
        sb_y = y_top + col_h + Inches(0.18)
        sb_h = Inches(0.85)
        add_rect(slide, Inches(0.5), sb_y, Inches(12.333), sb_h,
                 fill=S.BG_SOFT, line=S.BORDER)
        n = len(stat_band)
        cell_w = Inches(12.333) / n
        for i, st in enumerate(stat_band):
            cx = Inches(0.5) + cell_w * i
            if i > 0:
                # vertical divider
                add_rect(slide, cx, sb_y + Inches(0.1), Inches(0.005),
                         sb_h - Inches(0.2),
                         fill=S.BORDER, line=S.BORDER)
            add_textbox(
                slide, cx, sb_y + Inches(0.10), cell_w, Inches(0.4),
                st.get("value", ""),
                font_size=Pt(18), bold=True, color=S.PURPLE_DEEP,
                align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, margin=Inches(0),
            )
            add_textbox(
                slide, cx, sb_y + Inches(0.52), cell_w, Inches(0.32),
                st.get("label", ""),
                font_size=Pt(9.5), italic=True, color=S.INK_SOFT,
                align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.TOP, margin=Inches(0),
            )


def _build_fromto_card(slide, x, y, w, h, *,
                       label, header, points,
                       label_color, header_color, accent_top=False):
    add_card(slide, x, y, w, h, accent_top=accent_top, accent_color=S.PURPLE)
    pad = Inches(0.28)
    add_textbox(
        slide, x + pad, y + Inches(0.22), w - pad * 2, Inches(0.28),
        label,
        font_size=Pt(10), bold=True, color=label_color,
        char_spacing=S.CSP_PILL, margin=Inches(0),
    )
    add_textbox(
        slide, x + pad, y + Inches(0.52), w - pad * 2, Inches(0.45),
        header,
        font_size=Pt(14), bold=True, color=header_color, margin=Inches(0),
    )
    bullet_specs = []
    for pt in points:
        bullet_specs.append({
            "runs": [
                {"text": S.BULLET_CHAR + "  ", "size": Pt(9),
                 "color": label_color, "bold": True},
                {"text": pt, "size": Pt(10), "color": S.INK_SOFT},
            ],
            "line_spacing": 1.30,
            "space_after": Pt(5),
        })
    if bullet_specs:
        add_paragraphs(slide, x + pad, y + Inches(1.12),
                       w - pad * 2, h - Inches(1.3),
                       bullet_specs, margin=Inches(0))


# ---------- Agenda ----------
def build_agenda(slide, sd, page, total):
    add_header(slide, sd.get("eyebrow", ""), sd.get("title", ""),
               sd.get("subtitle"))
    add_footer(slide, page, total)

    items = sd.get("items", [])
    n = len(items)
    if n == 0:
        return

    total_w = Inches(12.333)
    gap = Inches(0.15)
    card_w = (total_w - gap * (n - 1)) / n
    card_h = Inches(3.8)
    top = Inches(2.5)

    for i, it in enumerate(items):
        x = Inches(0.5) + (card_w + gap) * i
        add_card(slide, x, top, card_w, card_h, accent_top=True)
        num = it.get("num", f"{i+1:02d}")
        label = it.get("label", "")
        desc = it.get("sub", it.get("desc", ""))
        add_textbox(
            slide, x, top + Inches(0.35), card_w, Inches(0.85),
            num,
            font_size=S.SZ_AGENDA_NUM, bold=True, color=S.PURPLE_DEEP,
            align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, margin=Inches(0),
        )
        add_textbox(
            slide, x + Inches(0.1), top + Inches(1.30), card_w - Inches(0.2), Inches(0.75),
            label,
            font_size=Pt(12), bold=True, color=S.INK,
            align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.TOP, margin=Inches(0.02),
        )
        rule_w = Inches(0.5)
        add_rect(slide, x + (card_w - rule_w) / 2, top + Inches(2.15),
                 rule_w, Inches(0.02), fill=S.PURPLE, line=S.PURPLE)
        if desc:
            add_textbox(
                slide, x + Inches(0.15), top + Inches(2.30),
                card_w - Inches(0.3), Inches(1.35),
                desc,
                font_size=Pt(9.5), italic=True, color=S.INK_SOFT,
                align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.TOP,
                line_spacing=1.30, margin=Inches(0.02),
            )


# ---------- Section Header ----------
def build_section_header(slide, sd, page, total):
    """Dedicated divider page. We DO NOT render the standard header band here
    so the page reads like a clean section opener.

    Layout:
      - Full-bleed navy background
      - Left: tiny purple 'accenture' wordmark + purple square (chrome bits)
      - Top-right: muted purple eyebrow (ACT 01)
      - Center-left big act number (e.g. 01) in giant purple
      - Right: section title (white) + subtitle (italic) + preview bullets
      - Footer same as other pages but white-on-navy variant inline
    """
    eyebrow = sd.get("eyebrow", "")            # e.g. "ACT 01"
    title = sd.get("title", "")                # e.g. "Findings & Trends"
    subtitle = sd.get("subtitle", "")
    preview = sd.get("preview", [])

    # Full-bleed navy background
    add_rect(slide, Inches(0), Inches(0), S.SLIDE_W, S.SLIDE_H,
             fill=S.INK, line=S.INK)
    # left purple rail (full height)
    add_rect(slide, Inches(0), Inches(0), Inches(0.25), S.SLIDE_H,
             fill=S.PURPLE, line=S.PURPLE)

    # accenture wordmark (white on navy)
    add_textbox(
        slide, Inches(0.6), Inches(0.30), Inches(1.5), Inches(0.3),
        "accenture",
        font_size=Pt(11), bold=True, color=S.WHITE,
        anchor=MSO_ANCHOR.MIDDLE, margin=Inches(0),
    )
    add_rect(slide, Inches(2.05), Inches(0.38), Inches(0.13), Inches(0.13),
             fill=S.PURPLE, line=S.PURPLE)

    # eyebrow upper-right
    if eyebrow:
        add_textbox(
            slide, Inches(8.5), Inches(0.30), Inches(4.5), Inches(0.30),
            eyebrow.upper(),
            font_size=Pt(11), bold=True, color=S.PURPLE,
            char_spacing=S.CSP_EYEBROW,
            align=PP_ALIGN.RIGHT, margin=Inches(0),
        )

    # Extract act number from eyebrow ("ACT 01" -> "01")
    act_num = ""
    if eyebrow.upper().startswith("ACT "):
        act_num = eyebrow.split()[-1]

    # Center the content vertically
    content_top = Inches(2.20)

    # giant act number on the left
    if act_num:
        # tiny "ACT" label above
        add_textbox(
            slide, Inches(0.95), content_top, Inches(2.5), Inches(0.35),
            "ACT",
            font_size=Pt(14), bold=True, color=S.PURPLE,
            char_spacing=S.CSP_EYEBROW, margin=Inches(0),
        )
        add_textbox(
            slide, Inches(0.85), content_top + Inches(0.30),
            Inches(3.5), Inches(3.0),
            act_num,
            font_size=Pt(180), bold=True, color=S.PURPLE,
            anchor=MSO_ANCHOR.TOP, margin=Inches(0),
        )

    # vertical separator
    sep_x = Inches(4.6)
    add_rect(slide, sep_x, content_top + Inches(0.20),
             Inches(0.02), Inches(3.4),
             fill=S.PURPLE_EDGE, line=S.PURPLE_EDGE)

    # title
    add_textbox(
        slide, Inches(5.0), content_top + Inches(0.25),
        Inches(8.0), Inches(1.1),
        title,
        font_size=Pt(40), bold=True, color=S.WHITE,
        line_spacing=1.10, margin=Inches(0),
    )
    # subtitle
    if subtitle:
        add_textbox(
            slide, Inches(5.0), content_top + Inches(1.40),
            Inches(8.0), Inches(0.45),
            subtitle,
            font_size=Pt(14), italic=True, color=S.PURPLE_EDGE,
            margin=Inches(0),
        )

    # preview bullets
    if preview:
        add_rect(slide, Inches(5.0), content_top + Inches(2.05),
                 Inches(0.8), Inches(0.025),
                 fill=S.PURPLE, line=S.PURPLE)
        add_textbox(
            slide, Inches(5.0), content_top + Inches(2.20),
            Inches(8.0), Inches(0.30),
            "WHAT'S INSIDE",
            font_size=Pt(10), bold=True, color=S.PURPLE,
            char_spacing=S.CSP_EYEBROW, margin=Inches(0),
        )
        specs = []
        for p in preview:
            specs.append({
                "runs": [
                    {"text": S.BULLET_CHAR + "  ", "size": Pt(11),
                     "color": S.PURPLE, "bold": True},
                    {"text": p, "size": Pt(13), "color": S.WHITE},
                ],
                "line_spacing": 1.40,
                "space_after": Pt(4),
            })
        add_paragraphs(
            slide, Inches(5.0), content_top + Inches(2.55),
            Inches(8.0), Inches(1.8),
            specs, margin=Inches(0),
        )

    # Inline footer (white-on-navy variant)
    add_textbox(
        slide, Inches(0.4), Inches(7.18), Inches(0.25), Inches(0.24),
        "\u203A",
        font_size=Pt(11), bold=True, color=S.PURPLE,
        anchor=MSO_ANCHOR.MIDDLE, margin=Inches(0),
    )
    add_textbox(
        slide, Inches(0.62), Inches(7.18), Inches(10.0), Inches(0.24),
        S.COPYRIGHT_TEXT,
        font_size=S.SZ_FOOTER, color=S.PURPLE_EDGE,
        anchor=MSO_ANCHOR.MIDDLE, margin=Inches(0),
    )
    add_textbox(
        slide, Inches(11.5), Inches(7.18), Inches(1.4), Inches(0.24),
        f"{page:02d} / {total:02d}",
        font_size=S.SZ_FOOTER, color=S.PURPLE_EDGE,
        align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE, margin=Inches(0),
    )
