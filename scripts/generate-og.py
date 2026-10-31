import base64
import os
import subprocess
import random

def to_b64(path):
    with open(path, "rb") as f:
        ext = os.path.splitext(path)[1].lower()
        mime = "image/svg+xml" if ext == ".svg" else ("image/png" if ext == ".png" else "image/jpeg")
        return f"data:{mime};base64,{base64.b64encode(f.read()).decode('utf-8')}"

icon_all = to_b64("assets/images/engine-all.svg")
icon_zlib = to_b64("assets/images/engine-zlib.svg")
icon_annas = to_b64("assets/images/engine-annas.png")
icon_libgen = to_b64("assets/images/engine-libgen.svg")
icon_welib = to_b64("assets/images/engine-welib.png")
icon_bookracy = to_b64("assets/images/engine-bookracy.png")
book_plato = to_b64("assets/images/book_7.jpg")
favicon = to_b64("favicon.svg")

def generate_stars_svg():
    rng = random.Random(1337)
    circles = []
    # Tiny background stars
    for _ in range(160):
        cx = rng.randint(10, 1190)
        cy = rng.randint(10, 620)
        r = round(rng.uniform(0.5, 1.4), 2)
        op = round(rng.uniform(0.15, 0.65), 2)
        circles.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#ffffff" opacity="{op}" />')
    # Medium stars
    for _ in range(35):
        cx = rng.randint(20, 1180)
        cy = rng.randint(20, 610)
        r = round(rng.uniform(1.5, 2.2), 2)
        op = round(rng.uniform(0.45, 0.9), 2)
        circles.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#ffffff" opacity="{op}" />')
    # Cosmic soft glow dust
    for _ in range(8):
        cx = rng.randint(40, 1160)
        cy = rng.randint(40, 590)
        r = round(rng.uniform(2.5, 3.8), 2)
        op = round(rng.uniform(0.15, 0.35), 2)
        circles.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#c7d2fe" opacity="{op}" filter="blur(1.5px)" />')
    return f'<svg class="stars-layer" width="1200" height="630" viewBox="0 0 1200 630" xmlns="http://www.w3.org/2000/svg">{"".join(circles)}</svg>'

stars_svg = generate_stars_svg()

COMMON_CSS = f"""
  * {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }}
  body {{
    width: 1200px;
    height: 630px;
    overflow: hidden;
    background-color: #07080a;
    color: #f4f4f5;
    font-family: 'LXGW WenKai', '霞鹜文楷', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    position: relative;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
  }}

  .stars-layer {{
    position: absolute;
    inset: 0;
    pointer-events: none;
    z-index: 1;
  }}

  /* 3D Book Assembly */
  .book-stage {{
    position: relative;
    width: 216px;
    height: 320px;
    perspective: 1200px;
    transform-style: preserve-3d;
    display: flex;
    align-items: center;
    justify-content: center;
  }}

  .book-float-wrapper {{
    position: relative;
    width: 206px;
    height: 310px;
    transform-style: preserve-3d;
    transform: rotateY(-22deg) rotateX(6deg) rotateZ(-1deg);
    filter: drop-shadow(0 20px 36px rgba(0, 0, 0, 0.85));
  }}

  .book-3d {{
    position: relative;
    width: 100%;
    height: 100%;
    transform-style: preserve-3d;
  }}

  .book-face-front {{
    position: absolute;
    inset: 0;
    background-color: #141416;
    border-radius: 2px 5px 5px 2px;
    transform: translateZ(16px);
    box-shadow: 
      0 0 1px 0.5px rgba(0, 0, 0, 0.6),
      inset 16px 0 10px -10px rgba(0, 0, 0, 0.8),
      inset 0 0 1px rgba(255, 255, 255, 0.15);
    overflow: hidden;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 20px 18px 20px 24px;
    border: 1px solid rgba(255, 255, 255, 0.09);
  }}

  .book-face-front::before {{
    content: '';
    position: absolute;
    top: 0;
    left: 11px;
    width: 3px;
    height: 100%;
    background: linear-gradient(to right, rgba(0, 0, 0, 0.65), rgba(255, 255, 255, 0.08));
    box-shadow: 1px 0 2px rgba(0, 0, 0, 0.8);
    pointer-events: none;
  }}

  .book-crosshatch-bg {{
    position: absolute;
    inset: 0;
    background-image: 
      repeating-linear-gradient(45deg, rgba(255, 255, 255, 0.035) 0, rgba(255, 255, 255, 0.035) 1px, transparent 0, transparent 9px),
      repeating-linear-gradient(-45deg, rgba(255, 255, 255, 0.035) 0, rgba(255, 255, 255, 0.035) 1px, transparent 0, transparent 9px);
    pointer-events: none;
  }}

  .cover-header {{
    position: relative;
    z-index: 2;
  }}

  .cover-series-tag {{
    font-size: 0.72rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #71717a;
    font-weight: 500;
  }}

  .cover-image-area {{
    position: relative;
    z-index: 2;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 6px 0;
    width: 100%;
    height: 142px;
    overflow: hidden;
    border-radius: 6px;
    background: #09090b;
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.7), inset 0 0 1px rgba(255, 255, 255, 0.15);
  }}

  .cover-image {{
    width: 100%;
    height: 100%;
    object-fit: cover;
  }}

  .cover-footer {{
    position: relative;
    z-index: 2;
    display: flex;
    flex-direction: column;
    gap: 3px;
  }}

  .cover-author {{
    font-size: 0.82rem;
    color: #a1a1aa;
    font-weight: 400;
  }}

  .cover-main-title {{
    font-size: 1.32rem;
    font-weight: 700;
    color: #f4f4f5;
    letter-spacing: 0.04em;
    line-height: 1.2;
  }}

  .book-face-spine {{
    position: absolute;
    top: 0;
    left: calc(50% - 15px);
    width: 30px;
    height: 310px;
    background: linear-gradient(to right, #070709 0%, #151518 12%, #35353c 30%, #484852 42%, #2a2a30 65%, #141417 86%, #060608 100%);
    transform: rotateY(-90deg) translateZ(103px);
    border-radius: 4px 2px 2px 4px;
    border: 1px solid rgba(255, 255, 255, 0.06);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
    padding: 18px 4px 16px;
    box-shadow: 
      0 0 1px 0.5px rgba(0, 0, 0, 0.6),
      inset 2.5px 0 3px rgba(255, 255, 255, 0.15),
      inset -3px 0 6px rgba(0, 0, 0, 0.85);
  }}

  .spine-title {{
    writing-mode: vertical-rl;
    transform: rotate(180deg);
    font-size: 0.78rem;
    letter-spacing: 0.1em;
    color: #d4d4d8;
  }}

  .spine-logo {{
    width: 16px;
    height: 16px;
    border-radius: 50%;
    border: 1px solid #71717a;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.6rem;
    font-weight: 700;
    color: #a1a1aa;
  }}

  .book-face-pages-right {{
    position: absolute;
    top: 3px;
    left: calc(50% - 15px);
    width: 28px;
    height: 304px;
    border-radius: 1px;
    background: 
      linear-gradient(to right, rgba(0, 0, 0, 0.45) 0%, transparent 16%, transparent 84%, rgba(0, 0, 0, 0.3) 100%),
      repeating-linear-gradient(to right, #f4f4f5 0px, #f4f4f5 1px, #d4d4d8 1px, #a1a1aa 2px, #f4f4f5 2.5px);
    transform: rotateY(90deg) translateZ(101px);
    box-shadow: 0 0 1px 0.5px rgba(0, 0, 0, 0.35);
  }}

  .book-face-pages-top {{
    position: absolute;
    top: 0;
    left: 2px;
    width: 202px;
    height: 28px;
    background: repeating-linear-gradient(to bottom, #f4f4f5 0px, #d4d4d8 1.5px, #a1a1aa 2px);
    transform: rotateX(90deg) translateZ(14px);
    border-radius: 1px;
    opacity: 0.85;
  }}

  .book-floor-shadow {{
    position: absolute;
    bottom: -16px;
    left: 8px;
    width: 216px;
    height: 28px;
    background: radial-gradient(ellipse at center, rgba(0, 0, 0, 0.85) 0%, rgba(0, 0, 0, 0.4) 45%, transparent 75%);
    transform: rotateX(80deg) scale(1.1);
    filter: blur(8px);
    pointer-events: none;
  }}

  /* Dropdown Menu Card (Semi-transparent, closely positioned) */
  .engine-dropdown-card {{
    width: 184px;
    background: rgba(18, 18, 22, 0.65);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 12px;
    padding: 6px;
    box-shadow: 0 18px 40px rgba(0, 0, 0, 0.65), 0 2px 8px rgba(0, 0, 0, 0.4);
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    z-index: 50;
    flex-shrink: 0;
  }}

  .engine-header {{
    display: flex;
    align-items: center;
    padding: 4px 8px 6px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    margin-bottom: 4px;
    font-size: 0.72rem;
    font-weight: 700;
    color: #71717a;
    letter-spacing: 0.04em;
  }}

  .engine-list {{
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 2px;
  }}

  .engine-item {{
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 6px 10px;
    border-radius: 8px;
    color: #f4f4f5;
    font-size: 0.84rem;
  }}

  .engine-item.is-selected {{
    background-color: rgba(255, 255, 255, 0.1);
    font-weight: 600;
  }}

  .engine-item-icon {{
    width: 19px;
    height: 19px;
    object-fit: contain;
    border-radius: 4px;
    flex-shrink: 0;
  }}

  .engine-item-name {{
    flex: 1;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }}

  .engine-item-check {{
    width: 14px;
    height: 14px;
    stroke: currentColor;
    stroke-width: 2.5;
    fill: none;
    color: #f4f4f5;
    flex-shrink: 0;
  }}

  .engine-divider {{
    height: 1px;
    background: rgba(255, 255, 255, 0.08);
    margin: 4px 2px;
  }}

  /* Search Bar */
  .search-bar {{
    display: flex;
    align-items: center;
    background: rgba(20, 20, 24, 0.82);
    border: 1px solid rgba(255, 255, 255, 0.14);
    border-radius: 9999px;
    padding: 5px 6px 5px 16px;
    box-shadow: 0 12px 36px rgba(0, 0, 0, 0.55), inset 0 1px 0 rgba(255, 255, 255, 0.06);
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    width: 100%;
  }}

  .search-left-icon {{
    width: 20px;
    height: 20px;
    margin-right: 12px;
    object-fit: contain;
  }}

  .search-text {{
    flex: 1;
    font-size: 1.05rem;
    color: #f4f4f5;
    font-family: inherit;
    letter-spacing: 0.02em;
  }}

  .search-arrow-btn {{
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background: #27272a;
    border: 1px solid #3f3f46;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #f4f4f5;
  }}

  .search-arrow-btn svg {{
    width: 16px;
    height: 16px;
    stroke: currentColor;
    stroke-width: 2.2;
    fill: none;
  }}
"""

# =========================================================================
# Layout 1: Split Hero (Left: Brand & URLs | Right: Vertically Centered Book & Dropdown)
# =========================================================================
html_split = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>不想看书 - OpenGraph</title>
<style>
{COMMON_CSS}

  .canvas-wrapper {{
    position: relative;
    width: 1200px;
    height: 630px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 76px 0 88px;
    border: 1px solid rgba(255, 255, 255, 0.07);
    background: 
      radial-gradient(circle at 74% 50%, rgba(99, 102, 241, 0.12) 0%, rgba(139, 92, 246, 0.04) 38%, transparent 68%),
      radial-gradient(circle at 25% 40%, rgba(255, 255, 255, 0.02) 0%, transparent 50%),
      #07080a;
  }}

  /* Left Column: NO badge above "不想看书" as requested */
  .left-col {{
    position: relative;
    z-index: 10;
    width: 480px;
    display: flex;
    flex-direction: column;
    gap: 22px;
  }}

  .title-group {{
    display: flex;
    flex-direction: column;
    gap: 14px;
  }}

  .main-title {{
    font-size: 4.6rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    color: #ffffff;
    line-height: 1.02;
    text-shadow: 0 4px 28px rgba(255, 255, 255, 0.22);
  }}

  .main-subtitle {{
    font-size: 1.3rem;
    color: #a1a1aa;
    line-height: 1.5;
    font-weight: 400;
  }}

  .features-grid {{
    display: flex;
    flex-wrap: wrap;
    gap: 7px;
  }}

  .feat-pill {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(24, 24, 27, 0.7);
    border: 1px solid rgba(255, 255, 255, 0.09);
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 0.78rem;
    color: #d4d4d8;
  }}

  .feat-pill img {{
    width: 13px;
    height: 13px;
    object-fit: contain;
  }}

  /* URLs Display Area */
  .url-section {{
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin-top: 4px;
  }}

  .url-card {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: rgba(24, 24, 27, 0.8);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 10px;
    padding: 10px 14px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.05);
  }}

  .url-card.is-primary {{
    border-color: rgba(255, 255, 255, 0.24);
    background: rgba(28, 28, 34, 0.9);
    box-shadow: 0 8px 26px rgba(0, 0, 0, 0.45), 0 0 15px rgba(255, 255, 255, 0.04);
  }}

  .url-card-left {{
    display: flex;
    align-items: center;
    gap: 12px;
  }}

  .url-icon-badge {{
    width: 28px;
    height: 28px;
    border-radius: 7px;
    background: rgba(255, 255, 255, 0.08);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.9rem;
    flex-shrink: 0;
  }}

  .url-card.is-primary .url-icon-badge {{
    background: rgba(99, 102, 241, 0.2);
    border: 1px solid rgba(99, 102, 241, 0.35);
  }}

  .url-text {{
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", monospace;
    font-size: 1.02rem;
    font-weight: 600;
    color: #ffffff;
    letter-spacing: 0.02em;
  }}

  .url-type-badge {{
    font-size: 0.72rem;
    padding: 3px 9px;
    border-radius: 4px;
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid rgba(255, 255, 255, 0.08);
    color: #a1a1aa;
    font-weight: 500;
    white-space: nowrap;
  }}

  .url-card.is-primary .url-type-badge {{
    background: rgba(255, 255, 255, 0.14);
    color: #ffffff;
    border-color: rgba(255, 255, 255, 0.26);
  }}

  /* Right Column: Visual UI Showcase */
  .right-col {{
    position: relative;
    z-index: 10;
    width: 480px;
    display: flex;
    flex-direction: column;
    align-items: center;
  }}

  .ui-cluster {{
    position: relative;
    width: 450px;
    display: flex;
    flex-direction: column;
    align-items: center;
  }}

  /* Top Row: Engine dropdown and Book Cover are vertically centered relative to each other! */
  .ui-top-row {{
    position: relative;
    width: 100%;
    display: flex;
    align-items: center; /* VERTICALLY CENTERED: The book is vertically centered with the engine dropdown */
    justify-content: center;
    gap: 4px; /* Very close to the cover */
    margin-bottom: 14px;
  }}

  .dropdown-wrap {{
    position: relative;
    z-index: 30;
    margin-right: -10px; /* Sits very close to / slightly overlapping the book cover's left edge */
  }}

  .book-wrap {{
    position: relative;
    z-index: 20;
  }}

  .search-pos {{
    position: relative;
    z-index: 40;
    width: 100%;
  }}
</style>
</head>
<body>
  {stars_svg}
  <div class="canvas-wrapper">
    <!-- Left Column: Branding, Value Prop & URLs (NO description above 不想看书) -->
    <div class="left-col">
      <div class="title-group">
        <h1 class="main-title">不想看书</h1>
        <p class="main-subtitle">聚合主流「影子图书馆」<br>你的一站式找书平台。</p>
      </div>

      <div class="features-grid">
        <span class="feat-pill"><img src="{icon_zlib}" alt="" /> Z-Library</span>
        <span class="feat-pill"><img src="{icon_annas}" alt="" /> Anna's Archive</span>
        <span class="feat-pill"><img src="{icon_libgen}" alt="" /> Libgen</span>
        <span class="feat-pill"><img src="{icon_welib}" alt="" /> WeLib</span>
        <span class="feat-pill"><img src="{icon_bookracy}" alt="" /> Bookracy</span>
        <span class="feat-pill"><img src="{icon_all}" alt="" /> 一键聚合搜索</span>
      </div>

      <!-- URLs Section -->
      <div class="url-section">
        <div class="url-card is-primary">
          <div class="url-card-left">
            <div class="url-icon-badge">🌐</div>
            <span class="url-text">https://bxks.pages.dev</span>
          </div>
          <span class="url-type-badge">主访问站</span>
        </div>

        <div class="url-card">
          <div class="url-card-left">
            <div class="url-icon-badge">⚡</div>
            <span class="url-text">https://bxks.sld.tw</span>
          </div>
          <span class="url-type-badge">官方备用镜像</span>
        </div>
      </div>
    </div>

    <!-- Right Column: Visual UI Showcase (Book Vertically Centered with Semi-transparent Engine Dropdown) -->
    <div class="right-col">
      <div class="ui-cluster">
        <div class="ui-top-row">
          <!-- Semi-transparent Engine Dropdown, close to cover -->
          <div class="dropdown-wrap">
            <div class="engine-dropdown-card">
              <div class="engine-header">选择搜索引擎</div>
              <ul class="engine-list">
                <li class="engine-item">
                  <img class="engine-item-icon" src="{icon_zlib}" alt="" />
                  <span class="engine-item-name">Z-Library</span>
                </li>
                <li class="engine-item">
                  <img class="engine-item-icon" src="{icon_annas}" alt="" />
                  <span class="engine-item-name">Anna’s Archive</span>
                </li>
                <li class="engine-item">
                  <img class="engine-item-icon" src="{icon_libgen}" alt="" />
                  <span class="engine-item-name">Libgen</span>
                </li>
                <li class="engine-item">
                  <img class="engine-item-icon" src="{icon_welib}" alt="" />
                  <span class="engine-item-name">WeLib</span>
                </li>
                <li class="engine-item">
                  <img class="engine-item-icon" src="{icon_bookracy}" alt="" />
                  <span class="engine-item-name">Bookracy</span>
                </li>
                <div class="engine-divider"></div>
                <li class="engine-item is-selected">
                  <img class="engine-item-icon" src="{icon_all}" alt="" />
                  <span class="engine-item-name">聚合搜索</span>
                  <svg class="engine-item-check" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"></polyline></svg>
                </li>
              </ul>
            </div>
          </div>

          <!-- 3D Book (Vertically Centered with Dropdown) -->
          <div class="book-wrap">
            <div class="book-stage">
              <div class="book-float-wrapper">
                <div class="book-3d">
                  <div class="book-face-front">
                    <div class="book-crosshatch-bg"></div>
                    <div class="cover-header">
                      <div class="cover-series-tag">Z-LIBRARY EDITION</div>
                    </div>
                    <div class="cover-image-area">
                      <img class="cover-image" src="{book_plato}" alt="" />
                    </div>
                    <div class="cover-footer">
                      <div class="cover-author">柏拉图</div>
                      <div class="cover-main-title">理想国</div>
                    </div>
                  </div>
                  <div class="book-face-spine">
                    <div class="spine-title">理想国</div>
                    <div class="spine-logo">Z</div>
                  </div>
                  <div class="book-face-pages-right"></div>
                  <div class="book-face-pages-top"></div>
                </div>
              </div>
              <div class="book-floor-shadow"></div>
            </div>
          </div>
        </div>

        <!-- Search Bar at Bottom -->
        <div class="search-pos">
          <div class="search-bar">
            <img class="search-left-icon" src="{icon_all}" alt="" />
            <span class="search-text">理想国</span>
            <div class="search-arrow-btn">
              <svg viewBox="0 0 24 24">
                <line x1="5" y1="12" x2="19" y2="12"></line>
                <polyline points="12 5 19 12 12 19"></polyline>
              </svg>
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>
</body>
</html>
"""

# =========================================================================
# Layout 2: Centered Panorama (NO badge above 不想看书, Book Vertically Centered with Dropdown)
# =========================================================================
html_center = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>不想看书 - OpenGraph</title>
<style>
{COMMON_CSS}

  .canvas-wrapper {{
    position: relative;
    width: 1200px;
    height: 630px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: space-between;
    padding: 38px 60px 32px 60px;
    border: 1px solid rgba(255, 255, 255, 0.07);
    background: 
      radial-gradient(circle at 50% 50%, rgba(99, 102, 241, 0.1) 0%, rgba(30, 32, 45, 0.25) 50%, transparent 75%),
      #07080a;
  }}

  /* Top Header: NO badge above "不想看书" as requested */
  .top-header {{
    position: relative;
    z-index: 10;
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 10px;
  }}

  .main-title {{
    font-size: 3.6rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    color: #ffffff;
    line-height: 1.05;
    text-shadow: 0 4px 24px rgba(255, 255, 255, 0.22);
  }}

  .main-subtitle {{
    font-size: 1.2rem;
    color: #a1a1aa;
    font-weight: 400;
    letter-spacing: 0.02em;
  }}

  .center-ui-stage {{
    position: relative;
    z-index: 10;
    width: 480px;
    display: flex;
    flex-direction: column;
    align-items: center;
  }}

  .ui-cluster {{
    position: relative;
    width: 460px;
    display: flex;
    flex-direction: column;
    align-items: center;
  }}

  /* Top Row: Engine dropdown and Book Cover are vertically centered relative to each other! */
  .ui-top-row {{
    position: relative;
    width: 100%;
    display: flex;
    align-items: center; /* VERTICALLY CENTERED */
    justify-content: center;
    gap: 4px; /* Very close to the cover */
    margin-bottom: 12px;
  }}

  .dropdown-wrap {{
    position: relative;
    z-index: 30;
    margin-right: -10px; /* Sits very close to the book */
  }}

  .book-wrap {{
    position: relative;
    z-index: 20;
  }}

  .search-pos {{
    position: relative;
    z-index: 40;
    width: 100%;
  }}

  /* Bottom URLs Dock */
  .bottom-dock {{
    position: relative;
    z-index: 10;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 18px;
    width: 100%;
  }}

  .url-pill {{
    display: flex;
    align-items: center;
    gap: 11px;
    background: rgba(22, 22, 26, 0.82);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 9999px;
    padding: 8px 18px;
    box-shadow: 0 6px 22px rgba(0, 0, 0, 0.4);
  }}

  .url-pill.is-primary {{
    border-color: rgba(255, 255, 255, 0.24);
    background: rgba(26, 26, 32, 0.92);
  }}

  .pill-icon {{
    font-size: 0.95rem;
  }}

  .pill-url {{
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    font-size: 0.94rem;
    font-weight: 600;
    color: #ffffff;
    letter-spacing: 0.02em;
  }}

  .pill-tag {{
    font-size: 0.72rem;
    color: #a1a1aa;
    background: rgba(255, 255, 255, 0.07);
    padding: 2px 8px;
    border-radius: 9999px;
    border: 1px solid rgba(255, 255, 255, 0.06);
  }}

  .url-pill.is-primary .pill-tag {{
    color: #f4f4f5;
    background: rgba(255, 255, 255, 0.14);
    border-color: rgba(255, 255, 255, 0.22);
  }}
</style>
</head>
<body>
  {stars_svg}
  <div class="canvas-wrapper">
    <!-- Top Header: NO badge above "不想看书" -->
    <header class="top-header">
      <h1 class="main-title">不想看书</h1>
      <p class="main-subtitle">聚合主流「影子图书馆」，你的一站式找书平台。</p>
    </header>

    <!-- Center UI Showcase -->
    <div class="center-ui-stage">
      <div class="ui-cluster">
        <div class="ui-top-row">
          <!-- Semi-transparent Dropdown, very close to book -->
          <div class="dropdown-wrap">
            <div class="engine-dropdown-card">
              <div class="engine-header">选择搜索引擎</div>
              <ul class="engine-list">
                <li class="engine-item">
                  <img class="engine-item-icon" src="{icon_zlib}" alt="" />
                  <span class="engine-item-name">Z-Library</span>
                </li>
                <li class="engine-item">
                  <img class="engine-item-icon" src="{icon_annas}" alt="" />
                  <span class="engine-item-name">Anna’s Archive</span>
                </li>
                <li class="engine-item">
                  <img class="engine-item-icon" src="{icon_libgen}" alt="" />
                  <span class="engine-item-name">Libgen</span>
                </li>
                <li class="engine-item">
                  <img class="engine-item-icon" src="{icon_welib}" alt="" />
                  <span class="engine-item-name">WeLib</span>
                </li>
                <li class="engine-item">
                  <img class="engine-item-icon" src="{icon_bookracy}" alt="" />
                  <span class="engine-item-name">Bookracy</span>
                </li>
                <div class="engine-divider"></div>
                <li class="engine-item is-selected">
                  <img class="engine-item-icon" src="{icon_all}" alt="" />
                  <span class="engine-item-name">聚合搜索</span>
                  <svg class="engine-item-check" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"></polyline></svg>
                </li>
              </ul>
            </div>
          </div>

          <!-- 3D Book (Vertically Centered with Dropdown) -->
          <div class="book-wrap">
            <div class="book-stage">
              <div class="book-float-wrapper">
                <div class="book-3d">
                  <div class="book-face-front">
                    <div class="book-crosshatch-bg"></div>
                    <div class="cover-header">
                      <div class="cover-series-tag">Z-LIBRARY EDITION</div>
                    </div>
                    <div class="cover-image-area">
                      <img class="cover-image" src="{book_plato}" alt="" />
                    </div>
                    <div class="cover-footer">
                      <div class="cover-author">柏拉图</div>
                      <div class="cover-main-title">理想国</div>
                    </div>
                  </div>
                  <div class="book-face-spine">
                    <div class="spine-title">理想国</div>
                    <div class="spine-logo">Z</div>
                  </div>
                  <div class="book-face-pages-right"></div>
                  <div class="book-face-pages-top"></div>
                </div>
              </div>
              <div class="book-floor-shadow"></div>
            </div>
          </div>
        </div>

        <!-- Search Bar -->
        <div class="search-pos">
          <div class="search-bar">
            <img class="search-left-icon" src="{icon_all}" alt="" />
            <span class="search-text">理想国</span>
            <div class="search-arrow-btn">
              <svg viewBox="0 0 24 24">
                <line x1="5" y1="12" x2="19" y2="12"></line>
                <polyline points="12 5 19 12 12 19"></polyline>
              </svg>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Bottom URLs Dock -->
    <footer class="bottom-dock">
      <div class="url-pill is-primary">
        <span class="pill-icon">🌐</span>
        <span class="pill-url">https://bxks.pages.dev</span>
        <span class="pill-tag">主访问站</span>
      </div>

      <div class="url-pill">
        <span class="pill-icon">⚡</span>
        <span class="pill-url">https://bxks.sld.tw</span>
        <span class="pill-tag">官方备用镜像</span>
      </div>
    </footer>
  </div>
</body>
</html>
"""

with open("/tmp/og-split.html", "w", encoding="utf-8") as f:
    f.write(html_split)

with open("/tmp/og-center.html", "w", encoding="utf-8") as f:
    f.write(html_center)

print("Generated refined HTML files.")
