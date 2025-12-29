
# file: app.py
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import logging
import sys

# Console-only logging to stdout
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("widget-api")

ROUTES = {
    "/v1": {
        "service": "widget_api",
        "version": "1.0.0",
        "active": True,
        "requests_today": 21,
    },
    "/v2": {
        "service": "widget_api",
        "version": "2.1.4",
        "active": True,
        "requests_today": 34,
    },
    "/v3": {
        "service": "widget_api",
        "version": "3.0.0-beta",
        "active": False,
        "requests_today": 7,
    },
}

class SimpleHandler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        # Route BaseHTTPRequestHandler messages through our logger to stdout
        logger.info("%s - - %s" % (self.address_string(), fmt % args))

    def _send_json(self, obj, status=200):
        body = json.dumps(obj).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        # Optional: allow CORS for simple testing in browsers/tools
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/":
            index = {
                "message": "Widget API versions",
                "routes": list(ROUTES.keys()),
                "example": "curl http://127.0.0.1:8080/v1"
            }
            self._send_json(index)
            # Access-style log line to console
            self.log_message('"%s %s" %s', "GET", self.path, 200)
            return

        if self.path in ROUTES:
            self._send_json(ROUTES[self.path])
            self.log_message('"%s %s" %s', "GET", self.path, 200)
            return

        # Not found
        self._send_json({"error": "Not Found"}, status=404)
        self.log_message('"%s %s" %s', "GET", self.path, 404)
        return

def run(host="127.0.0.1", port=8080):
    server = HTTPServer((host, port), SimpleHandler)
    logger.info(f"Serving on http://{host}:{port}")
    server.serve_forever()

if __name__ == "__main__":
    run()
