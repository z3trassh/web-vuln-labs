"""Lab 03, fixed: the check and the write happen under one lock."""

import threading
import time

from flask import Flask, abort, jsonify

GRANT = "lab03-reward-granted"


def create_app() -> Flask:
    app = Flask(__name__)
    coupon = {"used": False}
    lock = threading.Lock()

    @app.post("/redeem")
    def redeem():
        with lock:
            if coupon["used"]:
                abort(409)
            coupon["used"] = True
        time.sleep(0.05)  # real work can happen outside the critical section
        return jsonify(status=GRANT)

    return app


if __name__ == "__main__":
    create_app().run(host="127.0.0.1", port=5000, threaded=True)
