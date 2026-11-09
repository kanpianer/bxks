#!/usr/bin/env python3
"""
不想看书 (bxks) 本地预览与 CMS 开发服务。
- 静态文件服务 (带有针对 .html / .json 的无缓存控制)
- 支持 POST /api/cms/save 与 POST /api/save 接口落盘 data/mirrors.json
- 每次本地保存自动在 .cms-backups/ 下创建快照备份
"""

import sys
import os
import json
import socket
import argparse
from pathlib import Path
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT_DIR / 'data' / 'mirrors.json'
BACKUPS_DIR = ROOT_DIR / '.cms-backups'

SCRIPTS_DIR = Path(__file__).resolve().parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))
try:
    from sync_html import sync_html_fallback
except ImportError:
    sync_html_fallback = None

class BXKSRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT_DIR), **kwargs)

    def end_headers(self):
        # Prevent caching for dev preview
        clean_path = self.path.split('?')[0]
        if (clean_path.endswith('.json') or clean_path.endswith('.html') or
            clean_path in ('', '/', '/dtms', '/dtms/')):
            self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Expires', '0')
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        url = self.path.split('?')[0].rstrip('/')
        if url in ('/api/cms/save', '/api/save'):
            self.handle_cms_save()
        else:
            self.send_error(404, "Endpoint not found")

    def do_GET(self):
        url = self.path.split('?')[0].rstrip('/')
        if url in ('/api/cms/status', '/api/status'):
            self.send_json(200, {
                'status': 'ok',
                'project': 'bxks',
                'time': datetime.now().isoformat(),
                'dataFileExists': DATA_FILE.is_file()
            })
            return
        super().do_GET()

    def send_json(self, status_code, data):
        payload = json.dumps(data, ensure_ascii=False, indent=2).encode('utf-8')
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def handle_cms_save(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length <= 0:
                self.send_json(400, {'success': False, 'error': 'Empty request body'})
                return

            body = self.rfile.read(content_length).decode('utf-8')
            parsed = json.loads(body)

            # Support { data: {...}, note: "..." } or direct {...}
            if isinstance(parsed, dict) and 'data' in parsed and isinstance(parsed['data'], dict):
                cms_data = parsed['data']
                note = parsed.get('note', 'CMS 本地保存')
            else:
                cms_data = parsed
                note = 'CMS 本地保存'

            DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
            BACKUPS_DIR.mkdir(parents=True, exist_ok=True)

            time_str = datetime.now().strftime('%Y%m%d-%H%M%S')
            backup_file = BACKUPS_DIR / f'snapshot-{time_str}.json'

            formatted_json = json.dumps(cms_data, ensure_ascii=False, indent=2) + '\n'

            with open(backup_file, 'w', encoding='utf-8') as f:
                f.write(formatted_json)

            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                f.write(formatted_json)

            print(f"[{datetime.now().strftime('%H:%M:%S')}] [CMS] 已成功保存到 {DATA_FILE.relative_to(ROOT_DIR)}（快照备份: {backup_file.name}）")

            if sync_html_fallback:
                try:
                    sync_html_fallback(ROOT_DIR)
                except Exception as sync_err:
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] [CMS Warning] 同步 index.html 失败: {sync_err}", file=sys.stderr)

            self.send_json(200, {
                'success': True,
                'path': str(DATA_FILE.relative_to(ROOT_DIR)),
                'backup': backup_file.name,
                'time': datetime.now().isoformat()
            })
        except Exception as e:
            print(f"[CMS Error] {e}", file=sys.stderr)
            self.send_json(500, {'success': False, 'error': str(e)})

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('223.5.5.5', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return '127.0.0.1'

def run(port=8080, bind='0.0.0.0'):
    server_address = (bind, port)
    httpd = HTTPServer(server_address, BXKSRequestHandler)
    local_ip = get_local_ip()
    display_host = local_ip if bind in ('0.0.0.0', '') else bind
    print(f"=================================================")
    print(f" 不想看书 (bxks) 本地预览与管理服务")
    print(f" 本机访问:     http://127.0.0.1:{port}/")
    print(f" 局域网访问:   http://{display_host}:{port}/")
    print(f" 镜像管理CMS:  http://{display_host}:{port}/dtms/")
    print(f" 本地落盘接口: http://{display_host}:{port}/api/cms/save")
    print(f" 监听地址:     {bind}:{port}")
    print(f"=================================================")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n服务已停止")
        httpd.server_close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="不想看书 (bxks) 本地预览与 CMS 开发服务")
    parser.add_argument("port", nargs="?", type=int, default=8080, help="服务端口 (默认: 8080)")
    parser.add_argument("--bind", "-b", default="0.0.0.0", help="监听 IP (默认: 0.0.0.0，开放局域网访问)")
    args = parser.parse_args()
    run(port=args.port, bind=args.bind)
