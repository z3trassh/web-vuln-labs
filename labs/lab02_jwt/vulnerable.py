"""Lab 02, vulnerable: the token header chooses the verification algorithm."""

import hashlib
import hmac

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from flask import Flask, abort, jsonify, request

from labs.lab02_jwt.common import InvalidToken, new_keypair, sign_rs256, split_token

SECRET = "lab02-admin-secret"


def create_app() -> Flask:
    app = Flask(__name__)
    private_key, public_pem = new_keypair()
    public_key = serialization.load_pem_public_key(public_pem)

    def verify(token: str) -> dict:
        header, claims, signing_input, signature = split_token(token)
        alg = header.get("alg")
        if alg == "RS256":
            try:
                public_key.verify(signature, signing_input, padding.PKCS1v15(), hashes.SHA256())
            except InvalidSignature as error:
                raise InvalidToken from error
        elif alg == "HS256":
            expected = hmac.new(public_pem, signing_input, hashlib.sha256).digest()
            if not hmac.compare_digest(expected, signature):
                raise InvalidToken
        else:
            raise InvalidToken
        return claims

    @app.get("/public.pem")
    def public_key_file():
        return public_pem, {"Content-Type": "application/x-pem-file"}

    @app.post("/login")
    def login():
        return jsonify(token=sign_rs256(private_key, {"sub": "guest", "role": "user"}))

    @app.get("/admin")
    def admin():
        token = request.headers.get("Authorization", "").removeprefix("Bearer ")
        try:
            claims = verify(token)
        except InvalidToken:
            abort(401)
        if claims.get("role") != "admin":
            abort(403)
        return SECRET

    return app


if __name__ == "__main__":
    create_app().run(host="127.0.0.1", port=5000)
