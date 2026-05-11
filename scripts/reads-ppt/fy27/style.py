"""FY27 IE PPT Style Guide — palette, font, and dimension constants."""

from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

FONT = "Calibri"

# ---------- Palette (strict, 12 colors only) ----------
C = {
    "ink": RGBColor(0x1A, 0x1A, 0x2E),
    "ink_soft": RGBColor(0x4A, 0x4A, 0x5E),
    "muted": RGBColor(0x6B, 0x6B, 0x80),
    "muted_light": RGBColor(0x9E, 0x9E, 0xAE),
    "purple": RGBColor(0xA1, 0x00, 0xFF),
    "purple_deep": RGBColor(0x46, 0x00, 0x73),
    "purple_tint": RGBColor(0xF5, 0xEF, 0xFA),
    "purple_edge": RGBColor(0xE6, 0xD7, 0xF5),
    "teal": RGBColor(0x00, 0xBF, 0xA5),
    "border": RGBColor(0xD9, 0xD9, 0xE3),
    "bg_soft": RGBColor(0xFA, 0xFA, 0xFC),
    "white": RGBColor(0xFF, 0xFF, 0xFF),
}

# ---------- Slide dimensions (16:9 widescreen) ----------
SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)
