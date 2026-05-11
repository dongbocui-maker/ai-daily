"""Anthropic brand chrome — slide background, kicker, header, footer."""
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from . import style as S
from .drawing import add_rect, add_textbox, add_hrule, fill_background


def apply_page_background(slide, color=None):
    """Apply the warm-cream Anthropic Light as default canvas."""
    if color is None:
        color = S.LIGHT
    fill_background(slide, color)


def add_brand_mark(slide, *, on_dark=False):
    """Top-left brand mark: Anthropic-style wordmark.

    Uses Poppins bold. On light background renders DARK, on dark renders LIGHT.
    """
    color = S.LIGHT if on_dark else S.DARK
    add_textbox(
        slide, S.M_LEFT, Inches(0.45), Inches(2.5), Inches(0.35),
        "aidigest \u00b7 reads",
        font=S.FONT_HEAD, font_size=Pt(11), bold=True, color=color,
        char_spacing=S.CSP_LABEL, margin=Inches(0),
        anchor=MSO_ANCHOR.MIDDLE,
    )
    # tiny dot accent
    add_rect(
        slide, S.M_LEFT + Inches(2.55), Inches(0.59),
        Inches(0.10), Inches(0.10),
        fill=S.ORANGE, line=S.ORANGE,
    )


def add_kicker(slide, kicker, y=Inches(1.05), *, color=None, on_dark=False):
    """Editorial kicker line — small caps, accent-colored, letter-spaced."""
    if not kicker:
        return
    if color is None:
        color = S.ORANGE if not on_dark else S.LIGHT
    add_textbox(
        slide, S.M_LEFT, y, S.CONTENT_W, Inches(0.30),
        kicker.upper(),
        font=S.FONT_HEAD, font_size=S.SZ_KICKER, bold=True, color=color,
        char_spacing=S.CSP_KICKER, margin=Inches(0),
    )


def add_footer(slide, page, total, *, on_dark=False):
    """Footer with kicker-style chevron, copyright, page count."""
    color = S.MID_GRAY
    if on_dark:
        color = S.LIGHT_GRAY
    # thin top divider
    rule_color = S.LIGHT_GRAY if not on_dark else S.MID_GRAY
    add_hrule(
        slide, S.M_LEFT, Inches(7.05),
        S.CONTENT_W, color=rule_color, height=Pt(0.5),
    )
    # left text
    add_textbox(
        slide, S.M_LEFT, Inches(7.15), Inches(8.5), Inches(0.30),
        S.COPYRIGHT_TEXT,
        font=S.FONT_BODY, font_size=S.SZ_FOOTER, italic=True, color=color,
        anchor=MSO_ANCHOR.MIDDLE, margin=Inches(0),
    )
    # page count
    add_textbox(
        slide, Inches(10.5), Inches(7.15), Inches(2.13), Inches(0.30),
        f"{page:02d}  /  {total:02d}",
        font=S.FONT_HEAD, font_size=S.SZ_FOOTER, bold=True, color=color,
        align=PP_ALIGN.RIGHT, char_spacing=S.CSP_LABEL,
        anchor=MSO_ANCHOR.MIDDLE, margin=Inches(0),
    )


def add_standard_page_frame(slide, kicker, page, total, *, color=None):
    """Set up the default page: light bg, brand mark top-left, kicker,
    footer. Returns nothing."""
    apply_page_background(slide)
    add_brand_mark(slide)
    add_kicker(slide, kicker, color=color)
    add_footer(slide, page, total)


def add_title(slide, title, y=Inches(1.50), *,
              size=None, color=None, max_w=None):
    """Large editorial title in Poppins."""
    if size is None:
        size = S.SZ_TITLE_BIG
    if color is None:
        color = S.DARK
    if max_w is None:
        max_w = S.CONTENT_W
    add_textbox(
        slide, S.M_LEFT, y, max_w, Inches(1.80),
        title,
        font=S.FONT_HEAD, font_size=size, bold=True, color=color,
        line_spacing=1.08, margin=Inches(0),
    )


def add_subtitle(slide, subtitle, y=Inches(3.05), *, color=None, max_w=None):
    """Italic Lora subtitle."""
    if color is None:
        color = S.MID_GRAY
    if max_w is None:
        max_w = S.CONTENT_W
    if not subtitle:
        return
    add_textbox(
        slide, S.M_LEFT, y, max_w, Inches(0.60),
        subtitle,
        font=S.FONT_BODY, font_size=S.SZ_SUBTITLE, italic=True, color=color,
        line_spacing=1.30, margin=Inches(0),
    )
