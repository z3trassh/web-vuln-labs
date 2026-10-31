# Lab 01: SSRF allowlist bypass

An image-preview endpoint only accepts URLs from a trusted CDN. The app also has
an internal route that answers loopback clients only.

## The bug

```python
if not url.startswith("http://cdn.lab.test"):
    abort(403)
```

The check reads the URL as text, while the HTTP client reads it as a URL. In
`http://cdn.lab.test@127.0.0.1:PORT/internal/secret`, the part before `@` is
userinfo, and the real host is `127.0.0.1`.

## The exploit

`exploit.py` sends that URL to `/preview`. The server fetches it itself, so the
internal route sees a loopback client and returns the secret.

## The fix

`fixed.py` parses the URL, then:

1. rejects userinfo and any scheme other than HTTP(S);
2. compares the parsed hostname with the allowlist exactly;
3. rejects hostnames that resolve to a non-public address;
4. disables redirects, so an allowed host cannot forward the request elsewhere.

## Remaining limit

Resolving a name and connecting to it are two separate lookups, so DNS rebinding
can still change the answer in between. A production fix connects to the
validated address or routes requests through an egress proxy.
