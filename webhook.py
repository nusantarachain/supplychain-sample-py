#!/usr/bin/env python
##
# Minimal webhook buat nge-handle notifikasi dari off-chain worker Nuchain
# ketika ada event yang berkaitan dengan tracking product.

from http.server import HTTPServer, BaseHTTPRequestHandler

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        self.wfile.write("{}")

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        # Doesn't do anything with posted data
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        print("post_body: %s" % (post_body))
        self._set_headers()
        self.wfile.write('{"result":"ok"}'.encode('utf-8'))


def run(server_class=HTTPServer, handler_class=S, addr="localhost", port=8000):
    server_address = (addr, port)
    httpd = server_class(server_address, handler_class)

    print(f"Starting httpd server on {addr}:{port}")
    httpd.serve_forever()


if __name__ == "__main__":
    run(port=3005)