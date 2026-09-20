#!/usr/bin/env python3
"""Serve the Bug Manager demo: a static site, no dependencies.

Only the ./public directory is served, directory listings are off, and a
strict Content-Security-Policy is sent (the page needs no network calls).
"""
import argparse, os
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

CSP = ("default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; font-src 'self'; "
       "connect-src 'none'; frame-ancestors 'none'; base-uri 'none'; form-action 'none'")

class Handler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache')            # revalidate, so updates show up right away
        self.send_header('Content-Security-Policy', CSP)
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('Referrer-Policy', 'strict-origin-when-cross-origin')
        super().end_headers()
    def list_directory(self, path):                               # no directory listings
        self.send_error(404, 'Not found')
        return None
    def log_message(self, fmt, *args):
        super().log_message(fmt, *args)

def main():
    root = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'public')
    ap = argparse.ArgumentParser()
    ap.add_argument('--host', default='0.0.0.0'); ap.add_argument('--port', type=int, default=8430)
    a = ap.parse_args()
    handler = lambda *args, **kw: Handler(*args, directory=root, **kw)
    with ThreadingHTTPServer((a.host, a.port), handler) as srv:
        print(f'Bug Manager demo on http://{a.host}:{a.port}/  (serving {root})', flush=True)
        srv.serve_forever()

if __name__ == '__main__':
    main()
