"""Start a lab's Flask app on a random loopback port for the duration of a test."""

import socket
import threading
from collections.abc import Iterator
from contextlib import closing
from socketserver import ThreadingMixIn
from wsgiref.simple_server import WSGIServer, make_server

import pytest
import requests


class ThreadingWSGIServer(ThreadingMixIn, WSGIServer):
    """A real app serves concurrent requests; lab 01 and lab 03 depend on it."""

    daemon_threads = True


def _free_port() -> int:
    with closing(socket.socket()) as probe:
        probe.bind(("127.0.0.1", 0))
        return probe.getsockname()[1]


class RunningApp:
    def __init__(self, server: WSGIServer, port: int) -> None:
        self._server = server
        self.base_url = f"http://127.0.0.1:{port}"

    def wait_until_ready(self) -> None:
        for _ in range(50):
            try:
                requests.get(self.base_url, timeout=0.5)
                return
            except requests.RequestException:
                threading.Event().wait(0.05)
        raise RuntimeError("app did not start")


@pytest.fixture
def run_app() -> Iterator:
    servers: list[WSGIServer] = []

    def start(app) -> RunningApp:
        port = _free_port()
        server = make_server("127.0.0.1", port, app, server_class=ThreadingWSGIServer)
        servers.append(server)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        running = RunningApp(server, port)
        running.wait_until_ready()
        return running

    yield start
    for server in servers:
        server.shutdown()
