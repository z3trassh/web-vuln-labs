# web-vuln-labs

Small, deliberately vulnerable web apps. Each lab ships the bug, a working
exploit, the fix, and a test proving that the exploit succeeds against the
vulnerable app and fails against the fixed one.

| Lab | Bug class | CWE | What it teaches |
| --- | --- | --- | --- |
| [01 SSRF allowlist bypass](labs/lab01_ssrf/README.md) | SSRF | CWE-918 | A string prefix is not a host check |
| [02 JWT algorithm confusion](labs/lab02_jwt/README.md) | Broken authentication | CWE-347 | The token must not choose its own verification algorithm |
| [03 Coupon race condition](labs/lab03_race/README.md) | Race condition | CWE-367 | Check-then-write breaks under concurrency |
| [04 Invoice BOLA](labs/lab04_bola/README.md) | Broken object-level authorization | CWE-639 | Authentication does not imply ownership |

## Run the proof

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/pytest
```

Every lab test starts both apps on a random `127.0.0.1` port, so nothing is
exposed to your network.

## Try a lab by hand

```bash
.venv/bin/python -m labs.lab04_bola.vulnerable
.venv/bin/python -m labs.lab04_bola.exploit http://127.0.0.1:5000
```

Swap `vulnerable` for `fixed` to see the same exploit fail.

## Scope

These apps are intentionally insecure and were written for this repository.
They do not reproduce a vulnerability in any real product. Keep them on
localhost, and use the exploits only against these labs.

## License

[MIT](LICENSE)
