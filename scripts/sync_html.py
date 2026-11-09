#!/usr/bin/env python3
"""
同步 data/mirrors.json 的配置到 index.html 的静态 Fallback 内容。
包含：
1. 顶部标题下拉镜像列表 (#mirror-dropdown)
2. 页脚相关链接 (#footer-links)
3. 默认搜索引擎配置 (SEARCH_ENGINE_CONFIGS)
保证离线环境、首屏直出以及查看源码时均与最新数据完全一致。
"""

import sys
import re
import json
import html
from pathlib import Path

def normalize_mirror_url(url: str) -> str:
    url = str(url or '').strip()
    url = re.sub(r'/\?s=?$', '', url)
    return url.rstrip('/')

def generate_mirror_dropdown_html(data: dict) -> str:
    dropdown = data.get('dropdown', {})
    title = str(dropdown.get('title') or '「影子图书馆」网址列表').strip()
    tip = str(dropdown.get('tip') or '点击访问').strip()

    mirrors = [
        m for m in data.get('mirrors', [])
        if m and m.get('url') and m.get('enabled') is not False
    ]

    items_html = []
    for m in mirrors:
        url = str(m['url']).strip()
        display = str(m.get('display') or '').strip() or normalize_mirror_url(url)
        label = str(m.get('label') or '').strip()

        label_part = f'\n                <span class="mirror-rec-text">{html.escape(label)}</span>' if label else ''
        item = f'''            <li role="none">
              <a
                href="{html.escape(url)}"
                target="_blank"
                rel="noopener noreferrer"
                class="mirror-link"
                role="menuitem"
              >
                <span class="mirror-domain">{html.escape(display)}</span>{label_part}
              </a>
            </li>'''
        items_html.append(item)

    items_str = '\n'.join(items_html)
    return f'''        <!-- Dropdown Mirror Websites Panel -->
        <div class="mirror-dropdown" id="mirror-dropdown" role="menu" aria-label="可用镜像网站列表">
          <div class="mirror-dropdown-header">
            <span class="mirror-header-title">{html.escape(title)}</span>
            <span class="mirror-header-tip">{html.escape(tip)}</span>
          </div>
          <ul class="mirror-list">
{items_str}
          </ul>
        </div>'''

def generate_footer_links_html(data: dict) -> str:
    footer_links = [
        f for f in data.get('footerLinks', [])
        if f and (f.get('url') or f.get('text')) and f.get('enabled') is not False
    ]

    links_html = []
    for i, item in enumerate(footer_links):
        url = str(item.get('url') or '').strip()
        text = str(item.get('text') or item.get('url') or '').strip()
        icon = str(item.get('icon') or '').strip()

        sep = '        <span class="footer-sep" aria-hidden="true">、</span>\n' if i > 0 else ''
        icon_html = f'<img src="{html.escape(icon)}" class="footer-link-icon" alt="" aria-hidden="true" onerror="this.style.display=\'none\'" />\n          ' if icon else ''

        target_rel = ' target="_blank" rel="noopener noreferrer"' if url else ''
        href_val = html.escape(url) if url else '#'

        link = f'''{sep}        <a href="{href_val}"{target_rel} class="footer-link">
          {icon_html}<span class="footer-link-text">{html.escape(text)}</span>
        </a>'''
        links_html.append(link)

    inner = '\n'.join(links_html)
    return f'''      <div class="footer-links" id="footer-links">
{inner}
      </div>'''

def generate_search_engines_js(data: dict) -> str:
    engines = [e for e in data.get('searchEngines', []) if e and e.get('domain')]
    lines = ['      let SEARCH_ENGINE_CONFIGS = [']
    for i, e in enumerate(engines):
        name = str(e.get('name') or '通用').strip()
        domain = str(e.get('domain') or '').strip().rstrip('/')
        weight = int(e.get('weight', 25))
        enabled = 'true' if e.get('enabled') is not False else 'false'
        comma = ',' if i < len(engines) - 1 else ''
        lines.append(f"        {{ name: {json.dumps(name, ensure_ascii=False)}, domain: {json.dumps(domain, ensure_ascii=False)}, weight: {weight}, enabled: {enabled} }}{comma}")
    lines.append('      ];')
    return '\n'.join(lines)

def sync_html_fallback(root_dir: Path = None) -> bool:
    if root_dir is None:
        root_dir = Path(__file__).resolve().parent.parent

    data_file = root_dir / 'data' / 'mirrors.json'
    html_file = root_dir / 'index.html'

    if not data_file.is_file() or not html_file.is_file():
        print(f"[Sync Error] 找不到必要文件: {data_file} 或 {html_file}", file=sys.stderr)
        return False

    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    html_content = html_file.read_text(encoding='utf-8')

    # 1. 替换 mirror-dropdown
    dropdown_html = generate_mirror_dropdown_html(data)
    dropdown_pattern = re.compile(
        r'([ \t]*<!-- Dropdown Mirror Websites Panel -->\s*<div class="mirror-dropdown" id="mirror-dropdown".*?</ul>\s*</div>)',
        re.DOTALL
    )
    if not dropdown_pattern.search(html_content):
        print("[Sync Warning] 未在 index.html 匹配到 #mirror-dropdown 区块", file=sys.stderr)
    else:
        html_content = dropdown_pattern.sub(dropdown_html, html_content, count=1)

    # 2. 替换 footer-links
    footer_html = generate_footer_links_html(data)
    footer_pattern = re.compile(
        r'([ \t]*<div class="footer-links" id="footer-links">.*?</div>)',
        re.DOTALL
    )
    if not footer_pattern.search(html_content):
        print("[Sync Warning] 未在 index.html 匹配到 #footer-links 区块", file=sys.stderr)
    else:
        html_content = footer_pattern.sub(footer_html, html_content, count=1)

    # 3. 替换 SEARCH_ENGINE_CONFIGS
    engines_js = generate_search_engines_js(data)
    engines_pattern = re.compile(
        r'([ \t]*let SEARCH_ENGINE_CONFIGS = \[.*?\];)',
        re.DOTALL
    )
    if not engines_pattern.search(html_content):
        print("[Sync Warning] 未在 index.html 匹配到 SEARCH_ENGINE_CONFIGS 区块", file=sys.stderr)
    else:
        html_content = engines_pattern.sub(engines_js, html_content, count=1)

    html_file.write_text(html_content, encoding='utf-8')
    print(f"[Sync] 成功将 {data_file.relative_to(root_dir)} 的最新内容同步到 {html_file.relative_to(root_dir)}")
    return True

if __name__ == '__main__':
    success = sync_html_fallback()
    sys.exit(0 if success else 1)
