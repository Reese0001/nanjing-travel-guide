import http.server
import socketserver
import webbrowser
import os
import sys
import time
import threading

DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class TravelGuideHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        super().end_headers()

    def log_message(self, format, *args):
        pass

def open_browser_delayed(port):
    time.sleep(1.5)
    url = f'http://localhost:{port}/index.html'
    webbrowser.open(url)
    print(f'\n  浏览器已打开: {url}\n')

def start_server(port):
    os.chdir(DIRECTORY)
    handler = TravelGuideHandler

    try:
        with socketserver.TCPServer(("", port), handler) as httpd:
            print('=' * 55)
            print('  南京3天劳动节旅行攻略 - Web服务已启动')
            print('=' * 55)
            print(f'  服务地址: http://localhost:{port}/index.html')
            print(f'  服务目录: {DIRECTORY}')
            print('=' * 55)

            browser_thread = threading.Thread(target=open_browser_delayed, args=(port,), daemon=True)
            browser_thread.start()

            print('  按 Ctrl+C 停止服务\n')
            httpd.serve_forever()
    except KeyboardInterrupt:
        print('\n  服务已停止。祝您旅途愉快！\n')
        sys.exit(0)
    except OSError as e:
        if 'address already in use' in str(e).lower() or '10048' in str(e):
            print(f'\n  端口 {port} 已被占用，尝试备用端口 {port + 1}...')
            start_server(port + 1)
        else:
            print(f'\n  启动失败: {e}\n')
            sys.exit(1)

if __name__ == '__main__':
    start_server(8080)