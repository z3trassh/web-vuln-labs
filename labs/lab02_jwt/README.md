# Lab 02: JWT algorithm confusion

The API signs its tokens with RS256 and publishes its public key. Only a token
with `"role": "admin"` can read `/admin`.

## The bug

The verifier trusts the `alg` field from the token header, which the client
controls. When `alg` is `HS256`, it reuses the published public key as the HMAC
secret. Because that key is public, anyone can produce a valid HMAC over a token
of their choosing.

## The exploit

`exploit.py` downloads the PEM file, builds an admin token with `alg: HS256`, and
signs it with the PEM bytes as the secret.

## The fix

`fixed.py` accepts RS256 only and rejects every other header value before
checking the signature. A key should have a single purpose, and the server, not
the token, decides the algorithm.
