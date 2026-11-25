import json
import os
import ssl
import sys
import threading
import time
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer

SA_DIR = "/var/run/secrets/kubernetes.io/serviceaccount"
CONFIGMAP = "haven-config"
PORT = int(os.environ.get("PORT", "8080"))

state = {"config": None, "error": "config not loaded yet"}


def read(path):
    with open(path) as f:
        return f.read().strip()


def load_config():
    host = os.environ["KUBERNETES_SERVICE_HOST"]
    port = os.environ.get("KUBERNETES_SERVICE_PORT", "443")
    token = read(f"{SA_DIR}/token")
    namespace = read(f"{SA_DIR}/namespace")
    url = f"https://{host}:{port}/api/v1/namespaces/{namespace}/configmaps/{CONFIGMAP}"
    request = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    context = ssl.create_default_context(cafile=f"{SA_DIR}/ca.crt")
    with urllib.request.urlopen(request, context=context, timeout=5) as response:
        return json.load(response)["data"]


def refresh_forever():
    while True:
        try:
            state["config"] = load_config()
            state["error"] = None
        except urllib.error.HTTPError as e:
            body = e.read().decode(errors="replace")
            state["config"] = None
            state["error"] = f"HTTP {e.code} from the Kubernetes API: {body}"
        except Exception as e:
            state["config"] = None
            state["error"] = f"{type(e).__name__}: {e}"
        if state["error"]:
            print(f"config load failed: {state['error']}", file=sys.stderr, flush=True)
        time.sleep(5)


class Handler(BaseHTTPRequestHandler):
    def _send(self, status, payload):
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/healthz":
            self._send(200, {"status": "ok"})
        elif self.path == "/ready":
            if state["config"] is None:
                self._send(503, {"status": "not ready", "reason": state["error"]})
            else:
                self._send(200, {"status": "ready"})
        elif self.path == "/":
            if state["config"] is None:
                self._send(503, {"status": "not ready"})
            else:
                self._send(200, {"service": "photo-api", "config": state["config"]})
        else:
            self._send(404, {"status": "not found"})

    def log_message(self, fmt, *args):
        print(f"{self.address_string()} {fmt % args}", flush=True)


if __name__ == "__main__":
    threading.Thread(target=refresh_forever, daemon=True).start()
    print(f"photo-api listening on {PORT}", flush=True)
    HTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
