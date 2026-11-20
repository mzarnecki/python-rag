"""Minimal HTTP server built on the standard library (plays the role of Apache + PHP in php-rag).
Serves static files from public/ and routes /process.py to process.process()."""
import json
import os
import traceback
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from process import process

PUBLIC_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_FILES = {
    '/': ('index.html', 'text/html; charset=utf-8'),
    '/index.html': ('index.html', 'text/html; charset=utf-8'),
    '/script.js': ('script.js', 'application/javascript'),
    '/spinner.gif': ('spinner.gif', 'image/gif'),
}


def flatten(query: dict) -> dict:
    return {key: values[0] for key, values in query.items()}


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        url = urlparse(self.path)
        if url.path == '/process.py':
            return self._process(flatten(parse_qs(url.query, keep_blank_values=True)), {})
        if url.path not in STATIC_FILES:
            return self._send(404, 'text/plain', b'Not found')
        file_name, content_type = STATIC_FILES[url.path]
        with open(os.path.join(PUBLIC_DIR, file_name), 'rb') as f:
            self._send(200, content_type, f.read())

    def do_POST(self):
        url = urlparse(self.path)
        if url.path != '/process.py':
            return self._send(404, 'text/plain', b'Not found')
        body = self.rfile.read(int(self.headers.get('Content-Length', 0))).decode('utf-8')
        if self.headers.get('Content-Type', '').startswith('application/json'):
            post = json.loads(body or '{}')
        else:
            post = flatten(parse_qs(body))
        self._process(flatten(parse_qs(url.query, keep_blank_values=True)), post)

    def _process(self, get: dict, post: dict):
        try:
            output = process(post, get)
        except Exception:
            traceback.print_exc()
            return self._send(500, 'text/plain', b'Internal server error, check logs.')
        content_type = 'application/json' if 'api' in get else 'text/html; charset=utf-8'
        self._send(200, content_type, output.encode('utf-8'))

    def _send(self, status: int, content_type: str, body: bytes):
        self.send_response(status)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == '__main__':
    # port from env, not argv - PromptResolver treats argv[1] as CLI prompt
    port = int(os.environ.get('PORT', 80))
    print(f'Listening on http://0.0.0.0:{port}')
    ThreadingHTTPServer(('0.0.0.0', port), RequestHandler).serve_forever()
