"""Lab 01, fixed: the parsed host is validated and redirects are disabled."""

import ipaddress
import socket
from collections.abc import Callable
from urllib.parse import urlsplit

import requests
from flask import Flask, abort, request

SECRET = "lab01-internal-secret"
ALLOWED_HOSTS = {"cdn.lab.test"}


def resolve_host(hostname: str) -> list[str]:
    return [info[4][0] for info in socket.getaddrinfo(hostname, None)]


def is_allowed(url: str, resolver: Callable[[str], list[str]] = resolve_host) -> bool:
    try:
        parts = urlsplit(url)
        hostname = parts.hostname
    except ValueError:
        return False
    if parts.scheme not in {"http", "https"} or parts.username or parts.password:
        return False
    if hostname not in ALLOWED_HOSTS:
        return False
    try:
        addresses = resolver(hostname)
    except OSError:
        return False
    return bool(addresses) and all(ipaddress.ip_address(a).is_global for a in addresses)


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
        if not is_allowed(url):
            abort(403)
        try:
            upstream = requests.get(url, timeout=3, allow_redirects=False)
        except requests.RequestException:
            abort(502)
        return upstream.text, upstream.status_code

    return app


if __name__ == "__main__":
    create_app().run(host="127.0.0.1", port=5000)
