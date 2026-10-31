"""Lab 04, vulnerable: authentication without an ownership check."""

from flask import Flask, abort, jsonify, request

TOKENS = {"token-alice": "alice", "token-bob": "bob"}
INVOICES = {
    1: {"owner": "alice", "amount": "12.00", "note": "alice invoice"},
    2: {"owner": "bob", "amount": "80.00", "note": "bob invoice"},
    3: {"owner": "carol", "amount": "999.00", "note": "carol invoice"},
}


def authenticate(token: str) -> str:
    user = TOKENS.get(token)
    if user is None:
        abort(401)
    return user


def create_app() -> Flask:
    app = Flask(__name__)

    @app.get("/invoices/<int:invoice_id>")
    def get_invoice(invoice_id: int):
        authenticate(request.headers.get("Authorization", "").removeprefix("Bearer "))
        invoice = INVOICES.get(invoice_id)
        if invoice is None:
            abort(404)
        return jsonify(invoice)

    return app


if __name__ == "__main__":
    create_app().run(host="127.0.0.1", port=5000)
