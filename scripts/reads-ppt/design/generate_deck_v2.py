#!/usr/bin/env python3
"""
Generate a responsive, scrollable HTML deck — no fixed sizes, no conversion needed.
View directly in any browser. Uses CSS scroll-snap + flex/grid layouts.
"""

import json
from pathlib import Path

OUTLINE_PATH = Path(__file__).parent.parent / "outlines" / "brynjolfsson-generative-ai-at-work.json"
OUTPUT_HTML = Path(__file__).parent.parent / "output" / "brynjolfsson-deck.html"

CSS = """<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Noto+Sans+SC:wght@400;500;700&display=swap');

  /* System font fallback — renders correctly even if Google Fonts blocked */
  @font-face {
    font-family: 'Inter Fallback';
    src: local('Inter'), local('Helvetica Neue'), local('Arial');
    size-adjust: 107%;
  }

  *, *::before, *::after { margin:0; padding:0; box-sizing:border-box; }
  :root {
    --purple-deep: #460073;
    --purple-mid: #7B42F6;
    --purple-bright: #A100FF;
    --purple-light: #BE82FF;
    --purple-bg: #faf7ff;
    --pink: #FF50A0;
    --pink-deep: #C82A80;
    --gray-100: #f5f5f5;
    --gray-200: #e8e8e8;
    --gray-400: #aaa;
    --gray-500: #888;
    --gray-600: #666;
    --gray-700: #555;
    --gray-800: #444;
    --text-white: #fff;
    --text-body: #444;
    --radius-lg: 28px;
    --radius-md: 20px;
    --radius-sm: 16px;
  }
  html { scroll-behavior: smooth; font-size: 16px; }
  body {
    font-family: 'Inter', 'Inter Fallback', 'Noto Sans SC', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    background: #0a0a0a;
    color: var(--text-body);
    line-height: 1.6;
    scroll-snap-type: y mandatory;
    overflow-y: scroll;
    height: 100vh;
    -webkit-font-smoothing: antialiased;
  }

  /* ---- Slide Base ---- */
  .slide {
    min-height: 100vh;
    width: 100%;
    position: relative;
    overflow: hidden;
    scroll-snap-align: start;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .slide-inner {
    width: 100%;
    max-width: 1400px;
    margin: 0 auto;
    padding: 72px 80px;
    position: relative;
    z-index: 1;
  }

  /* ---- Navigation dots ---- */
  .nav-dots {
    position: fixed; right: 20px; top: 50%; transform: translateY(-50%);
    display: flex; flex-direction: column; gap: 10px; z-index: 100;
  }
  .nav-dot {
    width: 10px; height: 10px; border-radius: 50%;
    background: rgba(255,255,255,0.25);
    cursor: pointer; transition: all 0.3s;
  }
  .nav-dot:hover, .nav-dot.active { background: var(--purple-bright); transform: scale(1.4); }

  /* ====== COVER SLIDE ====== */
  .cover {
    background: linear-gradient(160deg, #460073 0%, #2d004a 45%, #1a002e 100%);
    color: var(--text-white);
  }
  .cover .cover-accent {
    position: absolute; right: -5%; top: -10%; width: 60%; height: 120%;
    background: linear-gradient(160deg, rgba(161,0,255,0.25) 0%, transparent 70%);
    clip-path: polygon(18% 0, 100% 0, 100% 100%, 0% 100%);
  }
  .cover .slide-inner { display: flex; flex-direction: column; justify-content: center; min-height: calc(100vh - 144px); }
  .cover .brand-line { width: 60px; height: 5px; background: var(--purple-bright); border-radius: 3px; margin-bottom: 16px; opacity: 0.9; }
  .cover .kicker { font-size: 0.85rem; font-weight: 600; letter-spacing: 2.5px; text-transform: uppercase; color: rgba(255,255,255,0.78); margin-bottom: 40px; }
  .cover h1 { font-size: clamp(2.5rem, 5vw, 4.5rem); font-weight: 900; line-height: 1.08; margin-bottom: 20px; max-width: 700px; letter-spacing: -0.02em; }
  .cover .subtitle { font-size: clamp(1rem, 1.5vw, 1.25rem); font-weight: 400; line-height: 1.6; color: rgba(255,255,255,0.88); max-width: 600px; margin-bottom: 48px; }
  .cover .stat-pills { display: flex; flex-wrap: wrap; gap: 14px; }
  .cover .stat-pill {
    background: rgba(255,255,255,0.07); backdrop-filter: blur(16px);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 16px; padding: 18px 24px;
    text-align: center; min-width: 130px;
  }
  .cover .stat-pill .val { color: var(--purple-light); font-size: 1.5rem; font-weight: 800; display: block; margin-bottom: 2px; }
  .cover .stat-pill .lbl { color: rgba(255,255,255,0.75); font-size: 0.75rem; font-weight: 500; text-transform: uppercase; letter-spacing: 1px; }
  .cover .footer-meta { margin-top: 32px; color: rgba(255,255,255,0.58); font-size: 0.8rem; }

  /* ====== DARK SECTION HEADERS ====== */
  .section-header {
    background: linear-gradient(160deg, #460073 0%, #2d004a 45%, #1a002e 100%);
    color: var(--text-white);
  }
  .section-header .sh-circle {
    position: absolute; right: -8%; top: -12%;
    width: 500px; height: 500px; border-radius: 50%;
    border: 2px solid rgba(161,0,255,0.12);
  }
  .section-header .sh-circle.c2 {
    right: -4%; top: -6%; width: 380px; height: 380px;
    border-color: rgba(255,80,160,0.1);
  }
  .section-header .slide-inner { display: flex; flex-direction: column; justify-content: center; min-height: calc(100vh - 144px); }
  .section-header .sh-kicker { font-size: 0.85rem; font-weight: 600; letter-spacing: 2.5px; text-transform: uppercase; color: rgba(255,255,255,0.72); margin-bottom: 16px; }
  .section-header .sh-line { width: 50px; height: 4px; background: var(--purple-bright); border-radius: 2px; margin-bottom: 32px; }
  .section-header h2 { font-size: clamp(2rem, 4.5vw, 3.5rem); font-weight: 900; line-height: 1.15; margin-bottom: 28px; max-width: 800px; }
  .section-header .sh-previews { display: flex; flex-wrap: wrap; gap: 24px; }
  .section-header .sh-preview { display: flex; align-items: center; gap: 10px; color: rgba(255,255,255,0.78); font-size: 1rem; }
  .section-header .sh-preview-dot { width: 8px; height: 8px; border-radius: 50%; background: var(--pink); flex-shrink: 0; }

  /* ====== WHITE CONTENT SLIDES ====== */
  .content-slide { background: #fff; }
  .content-slide .slide-inner { display: flex; flex-direction: column; justify-content: center; }
  .content-slide .cs-kicker { font-size: 0.7rem; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; color: var(--purple-bright); margin-bottom: 8px; }
  .content-slide h2 { font-size: clamp(1.6rem, 3vw, 2.5rem); font-weight: 800; color: var(--purple-deep); margin-bottom: 12px; line-height: 1.2; }
  .content-slide .cs-km { font-size: 1.05rem; color: var(--gray-600); font-style: italic; margin-bottom: 36px; }

  /* ====== LIGHT BG SLIDES ====== */
  .light-slide { background: var(--purple-bg); }
  .light-slide .slide-inner { display: flex; flex-direction: column; justify-content: center; }
  .light-slide .ls-kicker { font-size: 0.7rem; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; color: var(--purple-bright); margin-bottom: 8px; }
  .light-slide h2 { font-size: clamp(1.6rem, 3vw, 2.5rem); font-weight: 800; color: var(--purple-deep); margin-bottom: 12px; line-height: 1.2; }
  .light-slide .ls-km { font-size: 1.05rem; color: var(--gray-600); font-style: italic; margin-bottom: 36px; }

  /* ====== CONTEXT SLIDE (before/after) ====== */
  .context-cols { display: flex; gap: 30px; }
  .context-card {
    flex: 1; border-radius: var(--radius-lg); padding: 36px;
    position: relative; overflow: hidden;
  }
  .context-card.before { background: var(--gray-100); border: 1px solid var(--gray-200); }
  .context-card.after { background: linear-gradient(135deg, #f3e8ff, #faf7ff); border: 1px solid rgba(161,0,255,0.12); }
  .cc-tag { display: inline-block; padding: 5px 14px; border-radius: 20px; font-size: 0.7rem; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 16px; }
  .context-card.before .cc-tag { background: var(--gray-200); color: var(--gray-600); }
  .context-card.after .cc-tag { background: var(--purple-bright); color: #fff; }
  .context-card h3 { font-size: 1.2rem; font-weight: 700; margin-bottom: 16px; }
  .context-card.before h3 { color: var(--gray-800); }
  .context-card.after h3 { color: var(--purple-deep); }
  .context-card ul { list-style: none; }
  .context-card li { font-size: 0.9rem; color: var(--gray-700); padding: 6px 0 6px 18px; position: relative; line-height: 1.5; }
  .context-card li::before { content: ''; position: absolute; left: 0; top: 14px; width: 7px; height: 7px; border-radius: 50%; }
  .context-card.before li::before { background: #ccc; }
  .context-card.after li::before { background: var(--purple-mid); }
  .stat-band { display: flex; margin-top: 28px; border-radius: 16px; overflow: hidden; }
  .stat-band .sb-item { flex: 1; background: var(--purple-deep); padding: 24px 28px; text-align: center; border-right: 1px solid rgba(255,255,255,0.06); }
  .stat-band .sb-item:last-child { border-right: none; }
  .stat-band .sb-val { color: #fff; font-size: 1.75rem; font-weight: 800; display: block; margin-bottom: 2px; }
  .stat-band .sb-txt { color: rgba(255,255,255,0.78); font-size: 0.8rem; font-weight: 500; }

  /* ====== AGENDA ====== */
  .agenda-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
  .ag-item {
    display: flex; align-items: center; gap: 20px;
    padding: 24px 28px; border-radius: var(--radius-md);
    background: #fff; border: 1px solid rgba(161,0,255,0.06);
  }
  .ag-num {
    width: 52px; height: 52px; border-radius: 50%; flex-shrink: 0;
    background: linear-gradient(135deg, var(--purple-bright), var(--purple-mid));
    display: flex; align-items: center; justify-content: center;
    color: #fff; font-size: 1.1rem; font-weight: 800;
    box-shadow: 0 6px 20px rgba(161,0,255,0.2);
  }
  .ag-content h3 { font-size: 1.1rem; font-weight: 700; color: var(--purple-deep); margin-bottom: 2px; }
  .ag-content span { font-size: 0.82rem; color: var(--gray-600); line-height: 1.4; }

  /* ====== STAT GRID (4 gradient cards) ====== */
  .stat-cards { display: flex; gap: 16px; }
  .stat-card {
    flex: 1; border-radius: var(--radius-lg); padding: 32px 28px;
    display: flex; flex-direction: column; justify-content: space-between;
    min-height: 200px; position: relative; overflow: hidden;
  }
  .stat-card::after {
    content: ''; position: absolute; right: -30px; bottom: -30px;
    width: 120px; height: 120px; border-radius: 50%;
    background: rgba(255,255,255,0.06);
  }
  .stat-card:nth-child(1) { background: linear-gradient(135deg, var(--purple-bright), var(--purple-mid)); }
  .stat-card:nth-child(2) { background: linear-gradient(135deg, var(--purple-deep), #2d004a); }
  .stat-card:nth-child(3) { background: linear-gradient(135deg, var(--purple-mid), var(--purple-bright)); }
  .stat-card:nth-child(4) { background: linear-gradient(135deg, var(--pink-deep), var(--pink)); }
  .stat-card .sc-val { font-size: clamp(2rem, 3.5vw, 3rem); font-weight: 900; color: #fff; line-height: 1; position: relative; z-index: 1; }
  .stat-card .sc-label { font-size: 0.88rem; color: rgba(255,255,255,0.9); line-height: 1.4; position: relative; z-index: 1; margin-top: 6px; }
  .stat-card .sc-ctx { font-size: 0.75rem; color: rgba(255,255,255,0.72); font-style: italic; position: relative; z-index: 1; margin-top: auto; }
  .narrative-bar {
    margin-top: 20px; background: linear-gradient(135deg, #f3e8ff, #faf7ff);
    border-radius: var(--radius-md); padding: 20px 28px;
    border-left: 4px solid var(--purple-bright);
  }
  .narrative-bar p { font-size: 0.88rem; color: var(--gray-700); font-style: italic; line-height: 1.6; }

  /* ====== DISTRIBUTION CHART ====== */
  .dist-chart-wrap { margin-top: 12px; }
  .dist-chart {
    display: flex; align-items: flex-end; gap: 32px;
    padding: 0 60px 0 60px; height: 280px;
    border-bottom: 2px solid #e0e0e0;
  }
  .dist-bar-group { flex: 1; display: flex; flex-direction: column; align-items: center; }
  .dist-val { font-size: 1.3rem; font-weight: 800; color: var(--purple-deep); margin-bottom: 8px; }
  .dist-bar { width: 100%; max-width: 100px; border-radius: 16px 16px 6px 6px; position: relative; }
  .dist-bar.b1 { height: 260px; background: linear-gradient(to top, var(--pink-deep), var(--pink)); }
  .dist-bar.b2 { height: 175px; background: linear-gradient(to top, var(--purple-bright), var(--purple-light)); }
  .dist-bar.b3 { height: 115px; background: linear-gradient(to top, var(--purple-mid), var(--purple-bright)); }
  .dist-bar.b4 { height: 52px; background: linear-gradient(to top, var(--purple-deep), var(--purple-mid)); }
  .dist-bar.b5 { height: 18px; background: linear-gradient(to top, #2d004a, var(--purple-deep)); }
  .dist-label { font-size: 0.75rem; font-weight: 600; color: var(--gray-500); margin-top: 10px; text-align: center; }
  .dist-annots { display: flex; justify-content: space-between; padding: 0 60px; margin-top: 10px; }
  .dist-ann { font-size: 0.75rem; font-weight: 600; padding: 6px 14px; border-radius: 20px; }
  .dist-ann.left { color: var(--pink-deep); background: rgba(255,80,160,0.07); }
  .dist-ann.right { color: var(--gray-500); background: var(--gray-100); }
  .src-note { margin-top: 14px; font-size: 0.75rem; color: var(--gray-600); font-style: italic; }

  /* ====== QUOTE SLIDE ====== */
  .quote-primary {
    background: #fff; border-radius: var(--radius-lg); padding: 40px 48px;
    box-shadow: 0 4px 24px rgba(0,0,0,0.03); position: relative;
  }
  .quote-mark { position: absolute; left: 48px; top: 10px; font-size: 5rem; line-height: 1; color: var(--purple-bright); opacity: 0.12; font-family: Georgia, serif; }
  .quote-primary blockquote { font-size: 1.2rem; font-weight: 500; line-height: 1.55; color: var(--purple-deep); position: relative; z-index: 1; }
  .quote-primary .qp-attrib { font-size: 0.75rem; color: var(--gray-500); font-weight: 600; margin-top: 12px; position: relative; z-index: 1; }
  .quote-secondary {
    margin-top: 16px; background: #fff; border-radius: var(--radius-md);
    padding: 24px 32px; border-left: 4px solid var(--pink);
    box-shadow: 0 2px 12px rgba(0,0,0,0.02);
  }
  .quote-secondary p { font-size: 0.9rem; color: var(--gray-700); font-style: italic; line-height: 1.55; }
  .quote-secondary .qs-attrib { font-size: 0.7rem; color: var(--gray-400); margin-top: 6px; }
  .implication-bar {
    margin-top: 16px; background: var(--purple-deep); border-radius: var(--radius-md);
    padding: 20px 28px; display: flex; gap: 16px; align-items: flex-start;
  }
  .implication-bar .imp-label { color: rgba(255,255,255,0.72); font-size: 0.7rem; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; white-space: nowrap; margin-top: 3px; }
  .implication-bar .imp-text { font-size: 0.92rem; color: rgba(255,255,255,0.92); line-height: 1.55; }

  /* ====== 3 COLUMN ====== */
  .three-cols { display: flex; gap: 24px; }
  .tc-card {
    flex: 1; border-radius: var(--radius-lg); background: #fff;
    border: 1px solid rgba(161,0,255,0.06);
    box-shadow: 0 3px 18px rgba(0,0,0,0.03); overflow: hidden;
    display: flex; flex-direction: column;
  }
  .tc-header {
    padding: 28px 28px 20px; position: relative;
  }
  .tc-card:nth-child(1) .tc-header { background: linear-gradient(135deg, var(--purple-bright), var(--purple-mid)); }
  .tc-card:nth-child(2) .tc-header { background: linear-gradient(135deg, var(--purple-mid), var(--purple-bright)); }
  .tc-card:nth-child(3) .tc-header { background: linear-gradient(135deg, var(--purple-light), var(--purple-bright)); }
  .tc-icon { font-size: 2rem; font-weight: 900; color: #fff; margin-bottom: 8px; }
  .tc-header h3 { font-size: 1.05rem; font-weight: 700; color: #fff; line-height: 1.3; }
  .tc-body { padding: 20px 28px; flex: 1; font-size: 0.82rem; color: var(--gray-600); line-height: 1.6; }
  .tc-evidence { margin: 0 20px 20px; padding: 16px 20px; background: var(--purple-bg); border-radius: 12px; border-left: 3px solid var(--purple-bright); }
  .tc-ev-label { font-size: 0.6rem; font-weight: 700; color: var(--purple-bright); letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 4px; }
  .tc-evidence p { font-size: 0.7rem; color: var(--gray-700); font-style: italic; line-height: 1.5; }
  .tc-src { padding: 0 28px 20px; font-size: 0.72rem; color: var(--gray-600); }

  /* ====== 2 COLUMN SPLIT ====== */
  .two-split { display: flex; gap: 30px; margin-bottom: 16px; }
  .tw-side { flex: 1; border-radius: var(--radius-lg); padding: 32px; position: relative; overflow: hidden; }
  .tw-side.left { background: var(--gray-100); border: 1px solid var(--gray-200); }
  .tw-side.right { background: linear-gradient(135deg, #f3e8ff, #faf7ff); border: 1px solid rgba(161,0,255,0.1); }
  .tw-tag { display: inline-block; padding: 5px 14px; border-radius: 20px; font-size: 0.7rem; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 14px; }
  .tw-side.left .tw-tag { background: var(--gray-200); color: var(--gray-600); }
  .tw-side.right .tw-tag { background: var(--purple-bright); color: #fff; }
  .tw-side h3 { font-size: 1.1rem; font-weight: 700; margin-bottom: 14px; }
  .tw-side.left h3 { color: var(--gray-800); }
  .tw-side.right h3 { color: var(--purple-deep); }
  .tw-side ul { list-style: none; }
  .tw-side li { font-size: 0.85rem; color: var(--gray-600); padding: 5px 0 5px 18px; position: relative; line-height: 1.5; }
  .tw-side li::before { content: ''; position: absolute; left: 0; top: 12px; width: 6px; height: 6px; border-radius: 50%; }
  .tw-side.left li::before { background: #ccc; }
  .tw-side.right li::before { background: var(--purple-mid); }
  .callout-bar {
    background: var(--purple-deep); border-radius: var(--radius-md); padding: 18px 28px;
    display: flex; gap: 14px; align-items: flex-start;
  }
  .callout-bar .co-label { color: rgba(255,255,255,0.72); font-size: 0.7rem; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; white-space: nowrap; margin-top: 2px; }
  .callout-bar .co-text { font-size: 0.92rem; color: rgba(255,255,255,0.92); line-height: 1.55; }

  /* ====== INSIGHT CARDS (2) ====== */
  .insight-cards { display: flex; gap: 30px; }
  .ic-card {
    flex: 1; border-radius: var(--radius-lg); background: #fff; overflow: hidden;
    box-shadow: 0 3px 20px rgba(0,0,0,0.03);
    display: flex; flex-direction: column;
  }
  .ic-card:nth-child(1) { border-top: 7px solid var(--pink-deep); }
  .ic-card:nth-child(2) { border-top: 7px solid var(--purple-deep); }
  .ic-card-header { padding: 28px 28px 14px; }
  .ic-tag { display: inline-block; padding: 3px 12px; border-radius: 20px; font-size: 0.65rem; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 10px; }
  .ic-card:nth-child(1) .ic-tag { background: rgba(200,42,128,0.08); color: var(--pink-deep); }
  .ic-card:nth-child(2) .ic-tag { background: rgba(70,0,115,0.08); color: var(--purple-deep); }
  .ic-card-header h3 { font-size: 1.15rem; font-weight: 700; color: #333; line-height: 1.3; }
  .ic-body { padding: 0 28px; flex: 1; font-size: 0.85rem; color: var(--gray-600); line-height: 1.65; }
  .ic-evidence { margin: 16px 20px 14px; padding: 16px 20px; background: var(--purple-bg); border-radius: 12px; border-left: 3px solid var(--purple-mid); }
  .ic-ev-label { font-size: 0.6rem; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 4px; }
  .ic-card:nth-child(1) .ic-ev-label { color: var(--pink-deep); }
  .ic-card:nth-child(2) .ic-ev-label { color: var(--purple-deep); }
  .ic-evidence p { font-size: 0.7rem; font-style: italic; line-height: 1.5; }
  .ic-card:nth-child(1) .ic-evidence p { color: var(--pink-deep); }
  .ic-card:nth-child(2) .ic-evidence p { color: var(--purple-deep); }
  .ic-implication { padding: 8px 28px 24px; font-size: 0.8rem; font-weight: 700; line-height: 1.5; }
  .ic-card:nth-child(1) .ic-implication { color: var(--pink-deep); }
  .ic-card:nth-child(2) .ic-implication { color: var(--purple-deep); }

  /* ====== ACTION ROWS ====== */
  .action-rows { display: flex; flex-direction: column; gap: 10px; }
  .ar-row {
    display: flex; gap: 16px; align-items: flex-start;
    padding: 18px 24px; border-radius: 16px;
    background: var(--purple-bg); border: 1px solid rgba(161,0,255,0.05);
  }
  .ar-num {
    width: 44px; height: 44px; border-radius: 50%; flex-shrink: 0;
    background: linear-gradient(135deg, var(--purple-bright), var(--purple-mid));
    display: flex; align-items: center; justify-content: center;
    color: #fff; font-size: 1rem; font-weight: 800;
    box-shadow: 0 3px 14px rgba(161,0,255,0.18);
  }
  .ar-action { width: 240px; flex-shrink: 0; font-size: 0.95rem; font-weight: 700; color: var(--purple-deep); line-height: 1.3; }
  .ar-what { flex: 1; font-size: 0.8rem; color: var(--gray-600); line-height: 1.5; }
  .ar-outcome { width: 280px; flex-shrink: 0; font-size: 0.72rem; color: var(--gray-500); font-style: italic; line-height: 1.5; }

  /* ====== SUMMARY (dark) ====== */
  .summary-slide {
    background: linear-gradient(160deg, #460073 0%, #2d004a 45%, #1a002e 100%);
    color: var(--text-white);
  }
  .summary-slide .sum-line {
    position: absolute; top: 0; left: 0; right: 0; height: 5px;
    background: linear-gradient(to right, var(--purple-bright), var(--pink));
  }
  .summary-slide .slide-inner { display: flex; flex-direction: column; justify-content: center; }
  .summary-slide .sum-kicker { font-size: 0.85rem; font-weight: 700; letter-spacing: 2.5px; text-transform: uppercase; color: rgba(255,255,255,0.72); margin-bottom: 8px; }
  .summary-slide h2 { font-size: clamp(1.6rem, 3vw, 2.5rem); font-weight: 800; color: #fff; margin-bottom: 8px; }
  .summary-slide .sum-km { font-size: 1.1rem; color: rgba(255,255,255,0.78); font-style: italic; margin-bottom: 32px; }
  .pillars { display: flex; gap: 24px; }
  .pillar {
    flex: 1; background: rgba(255,255,255,0.05); backdrop-filter: blur(8px);
    border: 1px solid rgba(255,255,255,0.06); border-radius: var(--radius-lg);
    padding: 28px; position: relative; overflow: hidden;
  }
  .pillar::after { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 5px; }
  .pillar:nth-child(1)::after { background: var(--purple-bright); }
  .pillar:nth-child(2)::after { background: var(--purple-light); }
  .pillar:nth-child(3)::after { background: var(--pink); }
  .pillar-num {
    font-size: 2.5rem; font-weight: 900; margin-bottom: 8px;
    background: linear-gradient(135deg, var(--purple-bright), var(--purple-light));
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  }
  .pillar:nth-child(3) .pillar-num { background: linear-gradient(135deg, var(--pink), var(--purple-bright)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
  .pillar h3 { font-size: 1.1rem; font-weight: 700; color: #fff; margin-bottom: 10px; margin-top: 12px; }
  .pillar p { font-size: 0.9rem; color: rgba(255,255,255,0.78); line-height: 1.65; }
  .closing-bar {
    margin-top: 20px; background: rgba(255,255,255,0.03); border-radius: 12px;
    padding: 18px 24px; border-left: 4px solid var(--pink);
  }
  .closing-bar p { font-size: 0.95rem; color: rgba(255,255,255,0.82); font-style: italic; line-height: 1.55; }

  /* ====== REFERENCES ====== */
  .ref-cols { display: flex; gap: 24px; }
  .ref-col {
    flex: 1; background: #fff; border-radius: var(--radius-md); padding: 28px;
    box-shadow: 0 2px 14px rgba(0,0,0,0.02);
  }
  .ref-col:nth-child(1) { border-top: 5px solid var(--purple-bright); }
  .ref-col:nth-child(2) { border-top: 5px solid var(--purple-mid); }
  .ref-col:nth-child(3) { border-top: 5px solid var(--purple-light); }
  .ref-col h3 { font-size: 0.85rem; font-weight: 700; color: var(--purple-deep); margin-bottom: 12px; text-transform: uppercase; letter-spacing: 1px; }
  .ref-col ul { list-style: none; }
  .ref-col li { font-size: 0.7rem; color: var(--gray-600); padding: 4px 0 4px 14px; position: relative; line-height: 1.5; }
  .ref-col li::before { content: ''; position: absolute; left: 0; top: 9px; width: 4px; height: 4px; border-radius: 50%; background: #ccc; }

  /* ====== CLOSING ====== */
  .closing-slide {
    background: linear-gradient(160deg, #460073 0%, #2d004a 45%, #1a002e 100%);
    text-align: center; color: var(--text-white);
  }
  .closing-slide .slide-inner { display: flex; flex-direction: column; align-items: center; justify-content: center; }
  .closing-circle {
    width: 300px; height: 300px; border-radius: 50%;
    border: 2px solid rgba(161,0,255,0.12);
    position: absolute; left: 50%; top: 50%; transform: translate(-50%, -50%);
    pointer-events: none;
  }
  .closing-circle.c2 { width: 220px; height: 220px; border-color: rgba(255,80,160,0.08); }
  .closing-accent { width: 120px; height: 4px; background: var(--purple-bright); border-radius: 2px; margin-bottom: 40px; }
  .closing-slide h1 { font-size: clamp(2.5rem, 5vw, 4rem); font-weight: 900; margin-bottom: 8px; }
  .closing-slide .cl-sub { font-size: 1.1rem; color: rgba(255,255,255,0.78); margin-bottom: 16px; }
  .closing-slide .cl-url { font-size: 0.95rem; color: var(--purple-light); font-weight: 600; margin-bottom: 40px; }
  .closing-slide .cl-footer { font-size: 0.8rem; color: rgba(255,255,255,0.5); }

  /* ====== PAGE COUNTER ====== */
  .page-counter {
    position: absolute; right: 40px; bottom: 28px;
    font-size: 0.8rem; font-weight: 600; color: rgba(161,0,255,0.4);
  }
  .dark-slide .page-counter { color: rgba(255,255,255,0.38); }

  /* ====== RESPONSIVE ====== */
  @media (max-width: 960px) {
    .slide-inner { padding: 48px 28px; }
    .context-cols, .stat-cards, .three-cols, .two-split, .insight-cards, .pillars, .ref-cols { flex-direction: column; }
    .stat-band { flex-wrap: wrap; }
    .stat-band .sb-item { flex: 1 1 50%; }
    .agenda-grid { grid-template-columns: 1fr; }
    .dist-chart { padding: 0 20px; gap: 16px; height: 200px; }
    .dist-annots { padding: 0 20px; }
    .nav-dots { right: 8px; gap: 6px; }
    .nav-dot { width: 7px; height: 7px; }
    .ar-row { flex-wrap: wrap; }
    .ar-action, .ar-outcome { width: 100%; }
  }
  @media (max-width: 640px) {
    .slide-inner { padding: 36px 18px; }
    .cover .stat-pills { gap: 8px; }
    .cover .stat-pill { min-width: auto; padding: 12px 16px; }
    .cover .stat-pill .val { font-size: 1.2rem; }
  }
</style>"""

JS = """<script>
(function(){
  const dots = document.querySelectorAll('.nav-dot');
  const slides = document.querySelectorAll('.slide');
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if(e.isIntersecting) {
        const idx = parseInt(e.target.dataset.slide) - 1;
        dots.forEach((d,i) => d.classList.toggle('active', i === idx));
      }
    });
  }, { threshold: 0.5 });
  slides.forEach(s => observer.observe(s));

  // Keyboard nav
  let currentSlide = 0;
  document.addEventListener('keydown', e => {
    if(e.key === 'ArrowDown' || e.key === 'j' || e.key === 'PageDown') {
      e.preventDefault();
      currentSlide = Math.min(slides.length - 1, currentSlide + 1);
      slides[currentSlide].scrollIntoView({ behavior: 'smooth' });
    } else if(e.key === 'ArrowUp' || e.key === 'k' || e.key === 'PageUp') {
      e.preventDefault();
      currentSlide = Math.max(0, currentSlide - 1);
      slides[currentSlide].scrollIntoView({ behavior: 'smooth' });
    }
  });

  // Update currentSlide on scroll
  const scrollObserver = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if(e.isIntersecting) currentSlide = parseInt(e.target.dataset.slide) - 1;
    });
  }, { threshold: 0.5 });
  slides.forEach(s => scrollObserver.observe(s));
})();
</script>"""


def build_html(outline: dict) -> str:
    slides = outline["slides"]
    meta = outline["deck_meta"]
    total = len(slides)

    # Generate nav dots
    dots_parts = []
    for i in range(total):
        active_cls = ' class="nav-dot active"' if i == 0 else ' class="nav-dot"'
        onclick = 'document.querySelectorAll(\'.slide\')[{}].scrollIntoView({{behavior:\'smooth\'}})'.format(i)
        dots_parts.append('<div{} onclick="{}"></div>'.format(active_cls, onclick))
    dots = "\n".join(dots_parts)

    parts = [
        "<!DOCTYPE html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>",
        "<title>Generative AI at Work — aidigest.club</title>",
        CSS,
        "</head><body>",
        f'<div class="nav-dots">{dots}</div>'
    ]

    for idx, s in enumerate(slides):
        pn = idx + 1
        stype = s.get("type", "")
        dark_types = {"cover", "section_header", "closing"}
        slide_class = "slide"
        if stype in dark_types:
            slide_class += " dark-slide"

        parts.append(f'<div class="{slide_class} {stype}" data-slide="{pn}">')

        # ---------- COVER ----------
        if stype == "cover":
            parts.append(f'''
            <div class="cover-accent"></div>
            <div class="slide-inner">
              <div class="brand-line"></div>
              <div class="kicker">Executive Briefing</div>
              <h1>{s["title"]}</h1>
              <p class="subtitle">{s["subtitle"]}</p>
              <div class="stat-pills">
                {"".join(f'<div class="stat-pill"><span class="val">{h["value"]}</span><span class="lbl">{h["label"]}</span></div>' for h in s.get("highlights", []))}
              </div>
              <p class="footer-meta">{s["footer_meta"]}</p>
            </div>
            <div class="page-counter">{pn} / {total}</div>''')

        # ---------- CONTEXT ----------
        elif stype == "context":
            ba = s["before_after"]
            sb_items = s["stat_band"]
            parts.append(f'''
            <div class="slide-inner">
              <div class="cs-kicker">{s["kicker"]}</div>
              <h2>{s["title"]}</h2>
              <p class="cs-km">{s["key_message"]}</p>
              <div class="context-cols">
                <div class="context-card before">
                  <span class="cc-tag">{ba["before"]["header"]}</span>
                  <h3>Before This Paper</h3>
                  <ul>{"".join(f"<li>{p}</li>" for p in ba["before"]["points"])}</ul>
                </div>
                <div class="context-card after">
                  <span class="cc-tag">{ba["after"]["header"]}</span>
                  <h3>What This Paper Adds</h3>
                  <ul>{"".join(f"<li>{p}</li>" for p in ba["after"]["points"])}</ul>
                </div>
              </div>
              <div class="stat-band">
                {"".join(f'<div class="sb-item"><span class="sb-val">{i["value"]}</span><span class="sb-txt">{i["label"]}</span></div>' for i in sb_items)}
              </div>
            </div>
            <div class="page-counter">{pn} / {total}</div>''')

        # ---------- AGENDA ----------
        elif stype == "agenda":
            items = s["items"]
            parts.append(f'''
            <div class="slide-inner">
              <div class="ls-kicker">Agenda</div>
              <h2>{s["title"]}</h2>
              <div class="agenda-grid">
                {"".join(f'<div class="ag-item"><div class="ag-num">{i+1:02d}</div><div class="ag-content"><h3>{it["label"] if isinstance(it,dict) else it}</h3><span>{it.get("sub","") if isinstance(it,dict) else ""}</span></div></div>' for i,it in enumerate(items))}
              </div>
            </div>
            <div class="page-counter">{pn} / {total}</div>''')

        # ---------- SECTION HEADER ----------
        elif stype == "section_header":
            previews = s.get("preview", [])
            parts.append(f'''
            <div class="sh-circle"></div>
            <div class="sh-circle c2"></div>
            <div class="slide-inner">
              <div class="sh-kicker">{s["kicker"]}</div>
              <div class="sh-line"></div>
              <h2>{s["title"]}</h2>
              <div class="sh-previews">
                {"".join(f'<div class="sh-preview"><div class="sh-preview-dot"></div>{p}</div>' for p in previews)}
              </div>
            </div>
            <div class="page-counter">{pn} / {total}</div>''')

        # ---------- STAT GRID ----------
        elif stype == "stat_grid":
            stats = s["stats"]
            narrative = s.get("narrative", "")
            parts.append(f'''
            <div class="slide-inner">
              <div class="cs-kicker">Findings</div>
              <h2>{s["title"]}</h2>
              <p class="cs-km">{s["key_message"]}</p>
              <div class="stat-cards">
                {"".join(f'<div class="stat-card"><span class="sc-val">{st["value"]}</span><span class="sc-label">{st["label"]}</span><span class="sc-ctx">{st["context"]}</span></div>' for st in stats)}
              </div>
              <div class="narrative-bar"><p>{narrative}</p></div>
            </div>
            <div class="page-counter">{pn} / {total}</div>''')

        # ---------- DISTRIBUTION ----------
        elif stype == "distribution":
            bars = s["bars"]
            bar_classes = ["b1", "b2", "b3", "b4", "b5"]
            parts.append(f'''
            <div class="slide-inner">
              <div class="cs-kicker">{s["kicker"]}</div>
              <h2>{s["title"]}</h2>
              <p class="cs-km">{s["key_message"]}</p>
              <div class="dist-chart-wrap">
                <div class="dist-chart">
                  {"".join(f'<div class="dist-bar-group"><div class="dist-val">{b["display"]}</div><div class="dist-bar {bar_classes[i] if i < len(bar_classes) else ""}"></div><div class="dist-label">{b["label"]}</div></div>' for i,b in enumerate(bars))}
                </div>
                <div class="dist-annots">
                  <span class="dist-ann left">← {s["annotation_left"]}</span>
                  <span class="dist-ann right">{s["annotation_right"]} →</span>
                </div>
              </div>
              <p class="src-note">Source: {s["source_note"]}</p>
            </div>
            <div class="page-counter">{pn} / {total}</div>''')

        # ---------- QUOTE PAIR ----------
        elif stype == "quote_pair":
            parts.append(f'''
            <div class="slide-inner">
              <div class="ls-kicker">{s["kicker"]}</div>
              <h2>{s["title"]}</h2>
              <div class="quote-primary">
                <div class="quote-mark">"</div>
                <blockquote>{s["primary_quote"]}</blockquote>
                <p class="qp-attrib">— {s["primary_attrib"]}</p>
              </div>
              <div class="quote-secondary">
                <p>{s["secondary_quote"]}</p>
                <p class="qs-attrib">— {s["secondary_attrib"]}</p>
              </div>
              <div class="implication-bar">
                <span class="imp-label">{s["implication_label"]}</span>
                <span class="imp-text">{s["implication"]}</span>
              </div>
            </div>
            <div class="page-counter">{pn} / {total}</div>''')

        # ---------- THREE COLUMN ----------
        elif stype == "three_column_rich":
            cols = s["columns"]
            parts.append(f'''
            <div class="slide-inner">
              <div class="cs-kicker">{s["kicker"]}</div>
              <h2>{s["title"]}</h2>
              <p class="cs-km">{s["key_message"]}</p>
              <div class="three-cols">
                {"".join(f'<div class="tc-card"><div class="tc-header"><div class="tc-icon">{c["icon_text"]}</div><h3>{c["header"]}</h3></div><div class="tc-body">{c["body"]}</div><div class="tc-evidence"><div class="tc-ev-label">{c["evidence_label"]}</div><p>{c["evidence"]}</p></div><div class="tc-src">{c["source"]}</div></div>' for c in cols)}
              </div>
            </div>
            <div class="page-counter">{pn} / {total}</div>''')

        # ---------- TWO COLUMN ----------
        elif stype == "two_column_rich":
            l = s["left"]; r = s["right"]; co = s["callout"]
            parts.append(f'''
            <div class="slide-inner">
              <div class="cs-kicker">{s["kicker"]}</div>
              <h2>{s["title"]}</h2>
              <p class="cs-km">{s["key_message"]}</p>
              <div class="two-split">
                <div class="tw-side left">
                  <span class="tw-tag">{l["header"]}</span>
                  <h3>Without AI</h3>
                  <ul>{"".join(f"<li>{p}</li>" for p in l["points"])}</ul>
                </div>
                <div class="tw-side right">
                  <span class="tw-tag">{r["header"]}</span>
                  <h3>With AI</h3>
                  <ul>{"".join(f"<li>{p}</li>" for p in r["points"])}</ul>
                </div>
              </div>
              <div class="callout-bar">
                <span class="co-label">{co["label"]}</span>
                <span class="co-text">{co["text"]}</span>
              </div>
              <p class="src-note">Source: {s["source_note"]}</p>
            </div>
            <div class="page-counter">{pn} / {total}</div>''')

        # ---------- INSIGHT CARDS ----------
        elif stype == "insight_card_rich":
            cards = s["cards"]
            parts.append(f'''
            <div class="slide-inner">
              <div class="ls-kicker">{s["kicker"]}</div>
              <h2>{s["title"]}</h2>
              <p class="ls-km">{s["key_message"]}</p>
              <div class="insight-cards">
                {"".join(f'<div class="ic-card"><div class="ic-card-header"><span class="ic-tag">{c["tag"]}</span><h3>{c["header"]}</h3></div><div class="ic-body">{c["body"]}</div><div class="ic-evidence"><div class="ic-ev-label">{c["evidence_label"]}</div><p>{c["evidence"]}</p></div><div class="ic-implication">{c["implication"]}</div></div>' for c in cards)}
              </div>
              <p class="src-note">Source: {s["source_note"]}</p>
            </div>
            <div class="page-counter">{pn} / {total}</div>''')

        # ---------- ACTION TABLE ----------
        elif stype == "action_table":
            actions = s["actions"]
            parts.append(f'''
            <div class="slide-inner">
              <div class="cs-kicker">{s["kicker"]}</div>
              <h2>{s["title"]}</h2>
              <p class="cs-km">{s["key_message"]}</p>
              <div class="action-rows">
                {"".join(f'<div class="ar-row"><div class="ar-num">{i+1}</div><div class="ar-action">{a["header"]}</div><div class="ar-what">{a["what"]}</div><div class="ar-outcome">{a["outcome"]}</div></div>' for i,a in enumerate(actions))}
              </div>
            </div>
            <div class="page-counter">{pn} / {total}</div>''')

        # ---------- SUMMARY ----------
        elif stype == "summary":
            pillars = s["pillars"]
            parts.append(f'''
            <div class="sum-line"></div>
            <div class="slide-inner">
              <div class="sum-kicker">{s["kicker"]}</div>
              <h2>{s["title"]}</h2>
              <p class="sum-km">{s["key_message"]}</p>
              <div class="pillars">
                {"".join(f'<div class="pillar"><div class="pillar-num">0{i+1}</div><h3>{p["header"]}</h3><p>{p["body"]}</p></div>' for i,p in enumerate(pillars))}
              </div>
              <div class="closing-bar"><p>{s["closing_line"]}</p></div>
            </div>
            <div class="page-counter">{pn} / {total}</div>''')

        # ---------- REFERENCES ----------
        elif stype == "references":
            refs = [s["primary"], s["method"], s["citations"]]
            parts.append(f'''
            <div class="slide-inner">
              <div class="ls-kicker">{s["kicker"]}</div>
              <h2>{s["title"]}</h2>
              <div class="ref-cols">
                {"".join(f'<div class="ref-col"><h3>{r["header"]}</h3><ul>{"".join(f"<li>{i}</li>" for i in r["items"])}</ul></div>' for r in refs)}
              </div>
            </div>
            <div class="page-counter">{pn} / {total}</div>''')

        # ---------- CLOSING ----------
        elif stype == "closing":
            parts.append(f'''
            <div class="closing-circle"></div>
            <div class="closing-circle c2"></div>
            <div class="slide-inner">
              <div class="closing-accent"></div>
              <h1>{s["title"]}</h1>
              <p class="cl-sub">{s["subtitle"]}</p>
              <p class="cl-url">{s.get("url_text", "")}</p>
              <p class="cl-footer">{s["footer_meta"]}</p>
            </div>
            <div class="page-counter">{pn} / {total}</div>''')

        parts.append('</div>')  # close .slide

    parts.append(JS)
    parts.append("</body></html>")
    return "\n".join(parts)


def main():
    with OUTLINE_PATH.open() as f:
        outline = json.load(f)
    html = build_html(outline)
    OUTPUT_HTML.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_HTML.write_text(html)
    print(f"✅ Generated {OUTPUT_HTML}")
    print(f"   {len(outline['slides'])} slides, {len(html):,} bytes")
    print(f"   Responsive scroll-snap layout — open directly in browser")


if __name__ == "__main__":
    main()
