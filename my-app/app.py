import os
from http.server import BaseHTTPRequestHandler, HTTPServer

APP_NAME = os.getenv("APP_NAME", "MicroApp")
APP_PORT = int(os.getenv("APP_PORT", "8080"))
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")


class AppHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            status = 200
            message = "healthy"
        else:
            status = 200
            message = f"{APP_NAME} - version {APP_VERSION}"

        self.send_response(status)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(message.encode("utf-8"))

    def log_message(self, format, *args):
        print(f"{self.address_string()} - {format % args}")


server = HTTPServer(("0.0.0.0", APP_PORT), AppHandler)
print(f"{APP_NAME} v{APP_VERSION} démarre sur le port {APP_PORT}")
server.serve_forever()
