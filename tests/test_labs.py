"""Each lab proves the exploit works against `vulnerable` and fails against `fixed`."""

from labs.lab01_ssrf import exploit as ssrf_exploit
from labs.lab01_ssrf import fixed as ssrf_fixed
from labs.lab01_ssrf import vulnerable as ssrf_vulnerable
from labs.lab02_jwt import exploit as jwt_exploit
from labs.lab02_jwt import fixed as jwt_fixed
from labs.lab02_jwt import vulnerable as jwt_vulnerable
from labs.lab03_race import exploit as race_exploit
from labs.lab03_race import fixed as race_fixed
from labs.lab03_race import vulnerable as race_vulnerable
from labs.lab04_bola import exploit as bola_exploit
from labs.lab04_bola import fixed as bola_fixed
from labs.lab04_bola import vulnerable as bola_vulnerable


def test_lab01_ssrf(run_app):
    assert ssrf_exploit.exploit(run_app(ssrf_vulnerable.create_app()).base_url) == ssrf_vulnerable.SECRET
    assert ssrf_exploit.exploit(run_app(ssrf_fixed.create_app()).base_url) is None


def test_lab02_jwt(run_app):
    assert jwt_exploit.exploit(run_app(jwt_vulnerable.create_app()).base_url) == jwt_vulnerable.SECRET
    assert jwt_exploit.exploit(run_app(jwt_fixed.create_app()).base_url) is None


def test_lab03_race(run_app):
    assert race_exploit.exploit(run_app(race_vulnerable.create_app()).base_url) > 1
    assert race_exploit.exploit(run_app(race_fixed.create_app()).base_url) == 1


def test_lab04_bola(run_app):
    assert bola_exploit.exploit(run_app(bola_vulnerable.create_app()).base_url)
    assert bola_exploit.exploit(run_app(bola_fixed.create_app()).base_url) == []
