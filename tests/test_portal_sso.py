"""Portal SSO validation with real RS256 tokens (2026-10-22 fix)."""
from __future__ import annotations

import base64
import hashlib
import hmac
import json
from datetime import datetime, timedelta, timezone

import httpx
import jwt
import pytest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from backend.app import portal_sso

KEY = rsa.generate_private_key(public_exponent=65537, key_size=2048)
PUB = KEY.public_key().public_bytes(
    serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo).decode()


@pytest.fixture(autouse=True)
def _setup(monkeypatch):
    monkeypatch.setenv("PORTAL_APP_SLUG", "fla")
    monkeypatch.setattr(portal_sso, "_get_public_key", lambda: PUB)
    yield


def _claims(**over):
    now = datetime.now(timezone.utc)
    c = {"iss": "https://portal.kolektif360.com", "sub": "16", "aud": "fla",
         "iat": int(now.timestamp()), "exp": int((now + timedelta(hours=2)).timestamp()),
         "tenant_slug": "testa", "role": "user"}
    c.update(over)
    return {k: v for k, v in c.items() if v is not None}


def test_valid_portal_token_passes():
    assert portal_sso.validate_token(jwt.encode(_claims(), KEY, algorithm="RS256"))["tenant_slug"] == "testa"


@pytest.mark.parametrize("over", [{"aud": "other-app"}, {"iss": "https://evil.example"}, {"sub": None},
                                  {"exp": int((datetime.now(timezone.utc) - timedelta(minutes=5)).timestamp())}])
def test_claim_violations_rejected(over):
    with pytest.raises(jwt.PyJWTError):
        portal_sso.validate_token(jwt.encode(_claims(**over), KEY, algorithm="RS256"))


def _b64(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode()


def test_hs256_forgery_with_public_key_rejected():
    body = f"{_b64(json.dumps({'alg': 'HS256', 'typ': 'JWT'}).encode())}.{_b64(json.dumps(_claims()).encode())}"
    sig = hmac.new(PUB.encode(), body.encode(), hashlib.sha256).digest()
    with pytest.raises(jwt.PyJWTError):
        portal_sso.validate_token(f"{body}.{_b64(sig)}")


def test_missing_app_slug_refuses(monkeypatch):
    monkeypatch.delenv("PORTAL_APP_SLUG")
    with pytest.raises(portal_sso.SSOConfigError):
        portal_sso.validate_token(jwt.encode(_claims(), KEY, algorithm="RS256"))


def test_key_endpoint_json_and_pem_bodies():
    j = httpx.Response(200, json={"public_key": PUB})
    p = httpx.Response(200, text=PUB)
    assert portal_sso._key_from_response(j) == PUB
    assert portal_sso._key_from_response(p).startswith("-----BEGIN PUBLIC KEY-----")
    with pytest.raises(ValueError):
        portal_sso._key_from_response(httpx.Response(200, json={"error": "x"}))
