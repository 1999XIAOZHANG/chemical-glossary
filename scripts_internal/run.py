"""启动化学词汇表可视化页面"""

import http.server
import socketserver
import webbrowser
import os
import sys

PORT = 7888
MAX_PORT = 7998
DIRECTORY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        if self.path == "/":
            self.path = "/scripts_internal/index.html"
        super().do_GET()

    def log_message(self, format, *args):
        pass


def find_free_port(start, end):
    for port in range(start, end + 1):
        try:
            with socketserver.TCPServer(("", port), None) as s:
                return port
        except OSError:
            continue
    return None


def main():
    port = find_free_port(PORT, MAX_PORT)
    if port is None:
        print(f"错误：{PORT}-{MAX_PORT} 端口全部被占用")
        sys.exit(1)

    with socketserver.TCPServer(("", port), Handler) as httpd:
        url = f"http://localhost:{port}"
        print(f"化学词汇表可视化页面已启动")
        print(f"地址: {url}")
        print(f"按 Ctrl+C 停止")
        webbrowser.open(url)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n已停止")


if __name__ == "__main__":
    main()
