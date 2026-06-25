import pytest
import httpx

BASE = "http://localhost:8000"


def _login(email: str, password: str) -> str:
    r = httpx.post(f"{BASE}/auth/login", json={"email": email, "password": password})
    assert r.status_code == 200, r.text
    return r.json()["access_token"]


@pytest.mark.integration
def test_posizione_demo_403_se_non_account_demo(db, utente_test):
    # utente_test ha email ut_test@example.com != DEMO_ACCOUNT_EMAIL
    token = _login(utente_test["email"], utente_test["password"])
    import uuid as _uuid
    corsa_fittizia = str(_uuid.uuid4())
    r = httpx.patch(
        f"{BASE}/utente/corse/{corsa_fittizia}/demo/posizione",
        json={"lat": 41.1093, "lng": 16.8791},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 403, r.text
