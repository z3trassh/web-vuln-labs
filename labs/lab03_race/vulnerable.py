"""Lab 03, vulnerable: the coupon is checked and then marked used, with a gap."""

import time

from flask import Flask, abort, jsonify

GRANT = "lab03-reward-granted"


def create_app() -> Flask:
    app = Flask(__name__)
    coupon = {"used": False}

    @app.post("/redeem")
    def redeem():
        if coupon["used"]:
            abort(409)
        time.sleep(0.05)  # stands in for a DB write or payment call
        coupon["used"] = True
        return jsonify(status=GRANT)

    return app


if __name__ == "__main__":
    create_app().run(host="127.0.0.1", port=5000, threaded=True)
