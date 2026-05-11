"""Builders A — cover, context, section_divider, stat_grid, thesis_quote."""
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from . import style as S
from .drawing import add_rect, add_textbox, add_paragraphs, add_hrule, fill_background
from .chrome import (
    apply_page_background, add_brand_mark, add_kicker, add_footer,
    add_standard_page_frame, add_title, add_subtitle,
)


def _fit_size(text, *, base, max_chars, min_size, step=4):
    if not text:
        return base
    L = len(text)
    if L <= max_chars:
        return base
    overflow = L - max_chars
    size = base - (overflow // 2) * step
    return max(min_size, size)


# ---------- Cover ----------
def build_cover(slide, sd, page, total):
    apply_page_background(slide)
    add_brand_mark(slide)
    add_footer(slide, page, total)

    # left column - title block
    add_kicker(slide, sd.get("kicker", ""), y=Inches(1.30))

    title = sd.get("title", "")
    # title is multi-line so respect newlines
    add_textbox(
        slide, S.M_LEFT, Inches(1.70), Inches(8.5), Inches(3.0),
        title,
        font=S.FONT_HEAD, font_size=Pt(50), bold=True, color=S.DARK,
        line_spacing=1.06, margin=Inches(0),
    )

    sub = sd.get("subtitle", "")
    if sub:
        add_textbox(
            slide, S.M_LEFT, Inches(4.85), Inches(8.5), Inches(0.9),
            sub,
            font=S.FONT_BODY, font_size=Pt(15), italic=True, color=S.MID_GRAY,
            line_spacing=1.35, margin=Inches(0),
        )

    byline = sd.get("byline", "")
    if byline:
        add_hrule(
            slide, S.M_LEFT, Inches(6.10), Inches(2.5),
            color=S.ORANGE, height=Pt(2),
        )
        add_textbox(
            slide, S.M_LEFT, Inches(6.25), Inches(8.5), Inches(0.45),
            byline,
            font=S.FONT_HEAD, font_size=Pt(10), bold=True, color=S.DARK,
            char_spacing=S.CSP_LABEL, margin=Inches(0),
        )

    # right column - 3 headline stats
    stats = sd.get("headline_stats", [])[:3]
    if not stats:
        return
    rx = Inches(9.4)
    rw = Inches(3.20)
    # vertical orange rule
    add_rect(slide, rx, Inches(1.30), Pt(2), Inches(5.2),
             fill=S.ORANGE, line=S.ORANGE)
    sx = rx + Inches(0.25)
    sw = rw - Inches(0.25)
    sy = Inches(1.50)
    block_h = Inches(1.65)
    for i, st in enumerate(stats):
        y = sy + block_h * i
        v = st.get("value", "")
        lbl = st.get("label", "")
        v_size = _fit_size(v, base=44, max_chars=7, min_size=22, step=4)
        add_textbox(
            slide, sx, y, sw, Inches(0.80),
            v,
            font=S.FONT_HEAD, font_size=Pt(v_size), bold=True, color=S.DARK,
            line_spacing=1.0, margin=Inches(0),
        )
        add_textbox(
            slide, sx, y + Inches(0.85), sw, Inches(0.70),
            lbl,
            font=S.FONT_BODY, font_size=Pt(11), italic=True, color=S.MID_GRAY,
            line_spacing=1.25, margin=Inches(0),
        )


# ---------- Context ----------
def build_context(slide, sd, page, total):
    add_standard_page_frame(slide, sd.get("kicker", ""), page, total,
                            color=S.ACCENTS.get(sd.get("act_color", "orange")))
    title = sd.get("title", "")
    add_title(slide, title, y=Inches(1.45), size=Pt(32))

    lede = sd.get("lede", "")
    if lede:
        add_textbox(
            slide, S.M_LEFT, Inches(3.10), Inches(11.93), Inches(0.95),
            lede,
            font=S.FONT_BODY, font_size=Pt(12.5), italic=True, color=S.DARK,
            line_spacing=1.45, margin=Inches(0),
        )

    # two columns - FROM / TO
    from_b = sd.get("from_block", {})
    to_b = sd.get("to_block", {})

    col_w = Inches(5.85)
    gap = Inches(0.23)
    x_left = S.M_LEFT
    x_right = x_left + col_w + gap
    top = Inches(4.30)
    col_h = Inches(2.50)

    _draw_context_col(slide, x_left, top, col_w, col_h, from_b,
                      label_color=S.MID_GRAY)
    _draw_context_col(slide, x_right, top, col_w, col_h, to_b,
                      label_color=S.ORANGE, accent=True)


def _draw_context_col(slide, x, y, w, h, blk, *, label_color, accent=False):
    label = blk.get("label", "")
    points = blk.get("points", [])
    # top thin rule (orange if accent, gray otherwise)
    rule_color = S.ORANGE if accent else S.MID_GRAY
    add_hrule(slide, x, y, Inches(2.0), color=rule_color, height=Pt(2))
    # label
    add_textbox(
        slide, x, y + Inches(0.10), w, Inches(0.35),
        label.upper(),
        font=S.FONT_HEAD, font_size=Pt(10), bold=True, color=label_color,
        char_spacing=S.CSP_KICKER, margin=Inches(0),
    )
    # bullets
    if not points:
        return
    specs = []
    for p in points:
        specs.append({
            "runs": [
                {"text": S.BULLET + "  ", "size": Pt(11),
                 "color": rule_color, "bold": True, "font": S.FONT_HEAD},
                {"text": p, "size": Pt(11.5),
                 "color": S.DARK, "font": S.FONT_BODY},
            ],
            "line_spacing": 1.40,
            "space_after": Pt(5),
        })
    add_paragraphs(
        slide, x, y + Inches(0.55), w, h - Inches(0.55),
        specs, margin=Inches(0),
    )


# ---------- Section Divider ----------
def build_section_divider(slide, sd, page, total):
    """Full-color hero page introducing each ACT."""
    color_name = sd.get("color", "orange")
    accent = S.ACCENTS.get(color_name, S.ORANGE)
    fill_background(slide, accent)

    # brand mark - light on color
    add_brand_mark(slide, on_dark=True)
    add_footer(slide, page, total, on_dark=True)

    act_num = sd.get("act_num", "01")
    section_label = sd.get("section_label", "")
    section_title = sd.get("section_title", "")
    preview = sd.get("preview", [])

    # left: huge act number
    add_textbox(
        slide, Inches(0.5), Inches(0.90), Inches(2.0), Inches(0.4),
        "ACT",
        font=S.FONT_HEAD, font_size=Pt(13), bold=True, color=S.LIGHT,
        char_spacing=S.CSP_KICKER, margin=Inches(0),
    )
    add_textbox(
        slide, Inches(0.45), Inches(1.20), Inches(5.0), Inches(5.0),
        act_num,
        font=S.FONT_HEAD, font_size=S.SZ_SECT_ACT_NUM, bold=True,
        color=S.LIGHT, line_spacing=0.9, margin=Inches(0),
    )

    # vertical rule
    add_rect(slide, Inches(5.4), Inches(1.30), Pt(1), Inches(4.5),
             fill=S.LIGHT, line=S.LIGHT)

    # right: section label + title + preview
    rx = Inches(5.85)
    rw = Inches(6.95)
    add_textbox(
        slide, rx, Inches(1.30), rw, Inches(0.35),
        section_label.upper(),
        font=S.FONT_HEAD, font_size=Pt(11), bold=True, color=S.LIGHT,
        char_spacing=S.CSP_KICKER, margin=Inches(0),
    )
    add_textbox(
        slide, rx, Inches(1.75), rw, Inches(2.40),
        section_title,
        font=S.FONT_HEAD, font_size=Pt(38), bold=True, color=S.LIGHT,
        line_spacing=1.10, margin=Inches(0),
    )

    # divider
    add_rect(slide, rx, Inches(4.30), Inches(1.5), Pt(2),
             fill=S.LIGHT, line=S.LIGHT)
    add_textbox(
        slide, rx, Inches(4.45), rw, Inches(0.30),
        "IN THIS SECTION",
        font=S.FONT_HEAD, font_size=Pt(10), bold=True, color=S.LIGHT,
        char_spacing=S.CSP_KICKER, margin=Inches(0),
    )

    if preview:
        specs = []
        for p in preview:
            specs.append({
                "runs": [
                    {"text": S.BULLET + "  ", "size": Pt(13),
                     "color": S.LIGHT, "bold": True, "font": S.FONT_HEAD},
                    {"text": p, "size": Pt(14),
                     "color": S.LIGHT, "italic": True, "font": S.FONT_BODY},
                ],
                "line_spacing": 1.45,
                "space_after": Pt(6),
            })
        add_paragraphs(
            slide, rx, Inches(4.85), rw, Inches(2.0),
            specs, margin=Inches(0),
        )


# ---------- Stat Grid ----------
def build_stat_grid(slide, sd, page, total):
    add_standard_page_frame(slide, sd.get("kicker", ""), page, total)
    add_title(slide, sd.get("title", ""), y=Inches(1.50), size=Pt(32))
    add_subtitle(slide, sd.get("subtitle", ""), y=Inches(2.80))

    stats = sd.get("stats", [])[:4]
    n = len(stats)
    if n == 0:
        return

    # 4 stat columns w/ vertical accent rule
    total_w = S.CONTENT_W
    gap = Inches(0.18)
    col_w = (total_w - gap * (n - 1)) / n
    top = Inches(3.95)
    col_h = Inches(2.90)

    for i, st in enumerate(stats):
        x = S.M_LEFT + (col_w + gap) * i
        accent = S.ACCENTS.get(st.get("color", "orange"), S.ORANGE)
        # vertical accent rule on left
        add_rect(slide, x, top, Pt(2), col_h, fill=accent, line=accent)
        v = st.get("value", "")
        # Aggressive fit for 4-col stat grid (col_w ~2.67" content):
        # short ≤5 chars → 48pt; 6 → 42; 7 → 36; 8 → 30; ≥9 → 26pt
        L = len(v)
        if   L <= 5: v_size = 48
        elif L == 6: v_size = 42
        elif L == 7: v_size = 36
        elif L == 8: v_size = 30
        elif L == 9: v_size = 26
        else:        v_size = 22
        # value
        add_textbox(
            slide, x + Inches(0.18), top, col_w - Inches(0.18), Inches(0.95),
            v,
            font=S.FONT_HEAD, font_size=Pt(v_size), bold=True, color=S.DARK,
            line_spacing=1.0, margin=Inches(0),
        )
        # label
        add_textbox(
            slide, x + Inches(0.18), top + Inches(1.00),
            col_w - Inches(0.18), Inches(0.55),
            st.get("label", ""),
            font=S.FONT_HEAD, font_size=Pt(11), bold=True, color=accent,
            char_spacing=S.CSP_LABEL,
            line_spacing=1.25, margin=Inches(0),
        )
        # note
        note = st.get("note", "")
        if note:
            add_textbox(
                slide, x + Inches(0.18), top + Inches(1.60),
                col_w - Inches(0.18), Inches(1.30),
                note,
                font=S.FONT_BODY, font_size=Pt(9.5), italic=True, color=S.DARK,
                line_spacing=1.35, margin=Inches(0),
            )

    footer = sd.get("footer_note")
    if footer:
        add_hrule(slide, S.M_LEFT, Inches(6.95), S.CONTENT_W,
                  color=S.LIGHT_GRAY, height=Pt(0.5))
        # we already render footer in chrome; this is an extra source note ABOVE footer
        # so position carefully
        # Override: place source note JUST above footer rule (which we render)
        pass


# ---------- Thesis Quote ----------
def build_thesis_quote(slide, sd, page, total):
    add_standard_page_frame(slide, sd.get("kicker", ""), page, total,
                            color=S.BLUE)
    add_title(slide, sd.get("title", ""), y=Inches(1.50), size=Pt(30))
    add_subtitle(slide, sd.get("subtitle", ""), y=Inches(2.85))

    pq = sd.get("primary_quote", "")
    ps = sd.get("primary_source", "")
    sq = sd.get("secondary_quote", "")
    ss = sd.get("secondary_source", "")
    impl = sd.get("implication", "")
    impl_label = sd.get("implication_label", "Why this matters")

    # 2-quote layout
    col_w = Inches(5.85)
    gap = Inches(0.23)
    top = Inches(3.85)
    col_h = Inches(2.25)
    x_left = S.M_LEFT
    x_right = x_left + col_w + gap

    _draw_quote_block(slide, x_left, top, col_w, col_h, pq, ps,
                      accent=S.BLUE, primary=True)
    _draw_quote_block(slide, x_right, top, col_w, col_h, sq, ss,
                      accent=S.ORANGE, primary=False)

    # implication strip
    if impl:
        iy = Inches(6.30)
        ih = Inches(0.60)
        add_hrule(slide, S.M_LEFT, iy, S.CONTENT_W, color=S.DARK,
                  height=Pt(1.5))
        add_paragraphs(
            slide, S.M_LEFT, iy + Inches(0.10), S.CONTENT_W, ih,
            [{"runs": [
                {"text": impl_label.upper() + S.SEP, "size": Pt(10),
                 "bold": True, "color": S.ORANGE, "font": S.FONT_HEAD,
                 "char_spacing": S.CSP_KICKER},
                {"text": impl, "size": Pt(12),
                 "italic": True, "color": S.DARK, "font": S.FONT_BODY},
            ], "line_spacing": 1.35}],
            margin=Inches(0),
        )


def _draw_quote_block(slide, x, y, w, h, text, source, *, accent, primary):
    # big quote glyph
    add_textbox(
        slide, x, y - Inches(0.20), Inches(1.0), Inches(0.9),
        "\u201C",
        font=S.FONT_HEAD, font_size=Pt(72), bold=True, color=accent,
        line_spacing=1.0, margin=Inches(0),
    )
    # body
    add_textbox(
        slide, x + Inches(0.40), y, w - Inches(0.40),
        h - Inches(0.45),
        text,
        font=S.FONT_BODY, font_size=Pt(13.5) if primary else Pt(13),
        italic=True, color=S.DARK,
        line_spacing=1.42, margin=Inches(0),
    )
    # attribution
    if source:
        add_textbox(
            slide, x + Inches(0.40), y + h - Inches(0.40),
            w - Inches(0.40), Inches(0.30),
            S.BULLET + "  " + source,
            font=S.FONT_HEAD, font_size=Pt(9.5), bold=True, color=accent,
            char_spacing=S.CSP_LABEL, margin=Inches(0),
        )
