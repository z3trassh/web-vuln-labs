"""Lab 02, fixed: the server pins RS256 and ignores any other header value."""

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
        if header.get("alg") != "RS256":
            raise InvalidToken
        try:
            public_key.verify(signature, signing_input, padding.PKCS1v15(), hashes.SHA256())
        except InvalidSignature as error:
            raise InvalidToken from error
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
