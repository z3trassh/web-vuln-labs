"""Lab 01, vulnerable: the allowlist is a string-prefix check."""

import requests
from flask import Flask, abort, request

SECRET = "lab01-internal-secret"
ALLOWED_PREFIX = "http://cdn.lab.test"


def create_app() -> Flask:
    app = Flask(__name__)

    @app.get("/internal/secret")
    def internal_secret():
        if request.remote_addr != "127.0.0.1" or request.headers.get("X-Public-Client"):
            abort(403)
        return SECRET

    @app.get("/preview")
    def preview():
        url = request.args.get("url", "")
        if not url.startswith(ALLOWED_PREFIX):
            abort(403)
        try:
            upstream = requests.get(url, timeout=3)
        except requests.RequestException:
            abort(502)
        return upstream.text, upstream.status_code

    return app


if __name__ == "__main__":
    create_app().run(host="127.0.0.1", port=5000)
