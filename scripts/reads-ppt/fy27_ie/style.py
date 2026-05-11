"""FY27 IE Style constants — palette, font, sizes.

Per FY27 IE PPT Style Guide v1.0. Do not introduce new colors.
"""
from pptx.dml.color import RGBColor
from pptx.util import Inches, Pt

# ---- Palette (strict) ----
INK        = RGBColor(0x1A, 0x1A, 0x2E)
INK_SOFT   = RGBColor(0x4A, 0x4A, 0x5E)
MUTED      = RGBColor(0x6B, 0x6B, 0x80)
MUTED_LT   = RGBColor(0x9E, 0x9E, 0xAE)
PURPLE     = RGBColor(0xA1, 0x00, 0xFF)
PURPLE_DEEP = RGBColor(0x46, 0x00, 0x73)
PURPLE_TINT = RGBColor(0xF5, 0xEF, 0xFA)
PURPLE_EDGE = RGBColor(0xE6, 0xD7, 0xF5)
TEAL       = RGBColor(0x00, 0xBF, 0xA5)
BORDER     = RGBColor(0xD9, 0xD9, 0xE3)
BG_SOFT    = RGBColor(0xFA, 0xFA, 0xFC)
WHITE      = RGBColor(0xFF, 0xFF, 0xFF)

# ---- Font ----
FONT = "Calibri"

# ---- Slide geometry (16:9 widescreen) ----
SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)

# Margins
M_LEFT   = Inches(0.5)
M_RIGHT  = Inches(0.5)
M_TOP    = Inches(0.25)
M_BOTTOM = Inches(0.4)

# Content zone (after header / before footer)
CONTENT_TOP    = Inches(2.05)
CONTENT_BOTTOM = Inches(7.05)
CONTENT_W      = Inches(12.333)  # 13.333 - 0.5*2

# Footer zone
FOOTER_Y = Inches(7.18)

# ---- Font size shortcuts (pt) ----
SZ_TITLE       = Pt(26)
SZ_EYEBROW     = Pt(11)
SZ_SUBTITLE    = Pt(11.5)
SZ_SECTION_HDR = Pt(11)
SZ_CARD_TITLE  = Pt(10.5)
SZ_CARD_BODY   = Pt(8)
SZ_BULLET      = Pt(8)
SZ_FROMTO_LBL  = Pt(7)
SZ_OFFER_LBL   = Pt(7)
SZ_OFFER_BODY  = Pt(7)
SZ_VALUE_LBL   = Pt(9)
SZ_VALUE_BODY  = Pt(9)
SZ_PILL        = Pt(9)
SZ_FOOTER      = Pt(8)
SZ_STAT_BIG    = Pt(36)
SZ_STAT_LABEL  = Pt(8.5)
SZ_QUOTE       = Pt(14)
SZ_QUOTE_ATTR  = Pt(8.5)
SZ_AGENDA_NUM  = Pt(28)
SZ_AGENDA_LBL  = Pt(10)

# ---- Char spacing helpers (in units of 1/100 pt for python-pptx) ----
CSP_EYEBROW = 4   # +4 spacing for eyebrow
CSP_TAG     = 3   # +3 for ★ NEW FOR FY27 etc
CSP_PILL    = 2   # +2 for pill / section header

# ---- Common copy ----
COPYRIGHT_TEXT = "Copyright © 2026 aidigest.club · AI Daily Reads · Executive Brief"
BULLET_CHAR = "\u25CF"  # ●
SEP = "  ·  "  # 3 spaces · 3 spaces

# ---- ACT eyebrow format ----
def act_eyebrow(act_num: str, act_title: str) -> str:
    """Produce 'ACT 01 · FINDINGS & TRENDS' style eyebrow."""
    return f"ACT {act_num} · {act_title.upper()}"
