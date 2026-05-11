"""Anthropic brand constants — palette, typography, sizing.

Per Anthropic Brand Guidelines:
  Dark        #141413  primary text / dark backgrounds
  Light       #faf9f5  warm-cream backgrounds, text on dark
  Mid Gray    #b0aea5  secondary text
  Light Gray  #e8e6dc  subtle backgrounds, dividers
  Orange      #d97757  primary accent
  Blue        #6a9bcc  secondary accent
  Green       #788c5d  tertiary accent

Headings   -> Poppins (fallback Arial)
Body       -> Lora (fallback Georgia)
"""
from pptx.dml.color import RGBColor
from pptx.util import Inches, Pt

# ---- Palette ----
DARK      = RGBColor(0x14, 0x14, 0x13)
LIGHT     = RGBColor(0xfa, 0xf9, 0xf5)
MID_GRAY  = RGBColor(0xb0, 0xae, 0xa5)
LIGHT_GRAY = RGBColor(0xe8, 0xe6, 0xdc)
ORANGE    = RGBColor(0xd9, 0x77, 0x57)
BLUE      = RGBColor(0x6a, 0x9b, 0xcc)
GREEN     = RGBColor(0x78, 0x8c, 0x5d)
WHITE     = RGBColor(0xFF, 0xFF, 0xFF)

ACCENTS = {"orange": ORANGE, "blue": BLUE, "green": GREEN}

# ---- Typography ----
FONT_HEAD = "Poppins"
FONT_BODY = "Lora"

# ---- Slide geometry (16:9) ----
SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)

# Generous editorial margins
M_LEFT   = Inches(0.7)
M_RIGHT  = Inches(0.7)
M_TOP    = Inches(0.45)
M_BOTTOM = Inches(0.45)

CONTENT_W = SLIDE_W - M_LEFT - M_RIGHT  # 11.933
HEADER_BOTTOM = Inches(1.95)
FOOTER_TOP = Inches(7.05)

# ---- Font size scale ----
SZ_KICKER       = Pt(10)
SZ_TITLE_BIG    = Pt(40)
SZ_TITLE_MED    = Pt(30)
SZ_TITLE_SMALL  = Pt(22)
SZ_SUBTITLE     = Pt(13)
SZ_BODY         = Pt(11)
SZ_BODY_SMALL   = Pt(10)
SZ_BULLET       = Pt(11)
SZ_LABEL        = Pt(9)
SZ_FOOTER       = Pt(8.5)
SZ_STAT_BIG     = Pt(60)
SZ_STAT_MED     = Pt(46)
SZ_STAT_LABEL   = Pt(11)
SZ_STAT_NOTE    = Pt(9.5)
SZ_QUOTE        = Pt(16)
SZ_QUOTE_ATTR   = Pt(9.5)
SZ_SECT_ACT_NUM = Pt(180)
SZ_SECT_TITLE   = Pt(46)

# ---- Char spacing ----
CSP_KICKER  = 4  # +4 spacing pt (uppercase)
CSP_LABEL   = 2

# ---- Footer ----
COPYRIGHT_TEXT = "Curated by aidigest.club  /  Anthropic Research"

# ---- Common strings ----
BULLET = "\u2014"   # em dash for editorial style
SEP = "  \u00b7  "
