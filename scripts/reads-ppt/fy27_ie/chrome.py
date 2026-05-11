"""Page chrome — header (wordmark + eyebrow + title + subtitle) and footer."""
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from . import style as S
from .drawing import add_rect, add_textbox


def add_header(slide, eyebrow, title, subtitle=None):
    """Render top-of-page identity stack.

    Header zone occupies y ~ 0.25"–1.90". Returns nothing.
    """
    # accenture wordmark
    add_textbox(
        slide, Inches(0.5), Inches(0.25), Inches(1.5), Inches(0.3),
        "accenture",
        font_size=Pt(11), bold=True, color=S.INK,
        anchor=MSO_ANCHOR.MIDDLE, margin=Inches(0),
    )
    # purple square accent
    add_rect(slide, Inches(1.95), Inches(0.34), Inches(0.13), Inches(0.13),
             fill=S.PURPLE, line=S.PURPLE)
    # eyebrow
    if eyebrow:
        add_textbox(
            slide, Inches(0.5), Inches(0.72), Inches(12), Inches(0.28),
            eyebrow,
            font_size=S.SZ_EYEBROW, bold=True, color=S.PURPLE,
            char_spacing=S.CSP_EYEBROW, margin=Inches(0),
        )
    # title
    add_textbox(
        slide, Inches(0.5), Inches(1.00), Inches(12.3), Inches(0.55),
        title,
        font_size=S.SZ_TITLE, bold=True, color=S.INK, margin=Inches(0),
    )
    # subtitle (allow up to 2 wrap lines)
    if subtitle:
        add_textbox(
            slide, Inches(0.5), Inches(1.58), Inches(12.3), Inches(0.55),
            subtitle,
            font_size=S.SZ_SUBTITLE, italic=True, color=S.INK_SOFT,
            line_spacing=1.20, margin=Inches(0),
        )


def add_footer(slide, page_num, total):
    """Render footer chevron + copyright + page count."""
    # › chevron in purple
    add_textbox(
        slide, Inches(0.4), Inches(7.18), Inches(0.25), Inches(0.24),
        "›",
        font_size=Pt(11), bold=True, color=S.PURPLE,
        anchor=MSO_ANCHOR.MIDDLE, margin=Inches(0),
    )
    # copyright text
    add_textbox(
        slide, Inches(0.62), Inches(7.18), Inches(10.0), Inches(0.24),
        S.COPYRIGHT_TEXT,
        font_size=S.SZ_FOOTER, color=S.MUTED,
        anchor=MSO_ANCHOR.MIDDLE, margin=Inches(0),
    )
    # page count
    add_textbox(
        slide, Inches(11.5), Inches(7.18), Inches(1.4), Inches(0.24),
        f"{page_num:02d} / {total:02d}",
        font_size=S.SZ_FOOTER, color=S.MUTED,
        align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE, margin=Inches(0),
    )
