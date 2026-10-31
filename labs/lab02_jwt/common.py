"""Minimal JWT helpers, written by hand so the lab owns its verifier."""

import base64
import json

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa


class InvalidToken(Exception):
    pass


def b64encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def b64decode(data: str) -> bytes:
    return base64.urlsafe_b64decode(data + "=" * (-len(data) % 4))


def new_keypair() -> tuple[rsa.RSAPrivateKey, bytes]:
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_pem = private_key.public_key().public_bytes(
        serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return private_key, public_pem


def sign_rs256(private_key: rsa.RSAPrivateKey, claims: dict) -> str:
    header = b64encode(json.dumps({"alg": "RS256", "typ": "JWT"}).encode())
    payload = b64encode(json.dumps(claims).encode())
    signing_input = f"{header}.{payload}".encode()
    signature = private_key.sign(signing_input, padding.PKCS1v15(), hashes.SHA256())
    return f"{header}.{payload}.{b64encode(signature)}"


def split_token(token: str) -> tuple[dict, dict, bytes, bytes]:
    """Return header, claims, signing input and signature."""
    try:
        header, payload, signature = token.split(".")
        return (
            json.loads(b64decode(header)),
            json.loads(b64decode(payload)),
            f"{header}.{payload}".encode(),
            b64decode(signature),
        )
    except ValueError as error:
        raise InvalidToken from error
