"""Portal SSO service for Foreign Language Assessment.

Validates RS256 JWTs issued by portal.kolektif360.com using httpx (sync)
so it can be used from regular FastAPI endpoints without async overhead.

2026-10-22 fixes (found by the AIAssay Web component scan follow-up):
- The portal key endpoint returns JSON ``{"public_key": "<PEM>"}``; the old code used the
  raw response text as the key, so no token could ever verify.
- Portal tokens always carry ``aud`` (the app slug). The old code passed no ``audience``,
  so PyJWT rejected every token with InvalidAudienceError. ``PORTAL_APP_SLUG`` is now
  required; without it validation refuses instead of skipping the audience check.
- ``iss`` and the presence of ``exp/iat/aud/iss/sub`` are now checked as well.
"""
from __future__ import annotations

import logging
import os
from functools import lru_cache

import httpx
import jwt

logger = logging.getLogger(__name__)

PORTAL_PUBLIC_KEY_URL = os.environ.get(
    "PORTAL_PUBLIC_KEY_URL",
    "https://portal.kolektif360.com/api/.well-known/jwt-public-key.pem",
)
PORTAL_ISSUER = os.environ.get("PORTAL_ISSUER", "https://portal.kolektif360.com")


class SSOConfigError(RuntimeError):
    """SSO is not configured (e.g. PORTAL_APP_SLUG missing)."""


def _key_from_response(resp: httpx.Response) -> str:
    """The endpoint returns JSON ``{"public_key": PEM}``; a bare PEM body is accepted too."""
    body = resp.text.strip()
    if body.startswith("-----BEGIN"):
        return body
    key = resp.json().get("public_key", "")
    if not key.startswith("-----BEGIN"):
        raise ValueError("portal public key response has no PEM key")
    return key


@lru_cache(maxsize=1)
def _get_public_key() -> str:
    """Fetch and cache the Portal RS256 public key PEM."""
    resp = httpx.get(PORTAL_PUBLIC_KEY_URL, timeout=10)
    resp.raise_for_status()
    return _key_from_response(resp)


def _app_slug() -> str:
    slug = os.environ.get("PORTAL_APP_SLUG", "").strip()
    if not slug:
        raise SSOConfigError("PORTAL_APP_SLUG is not set; refusing to validate portal tokens without an audience")
    return slug


def validate_token(token: str) -> dict:
    """Validate a Portal-issued RS256 JWT and return its payload.

    Raises jwt.PyJWTError on invalid / expired tokens.
    Raises SSOConfigError if PORTAL_APP_SLUG is not configured.
    Raises httpx.HTTPError if the public key cannot be fetched.
    """
    audience = _app_slug()
    public_key = _get_public_key()
    payload = jwt.decode(
        token,
        public_key,
        algorithms=["RS256"],                 # RS256 only: no HS/none confusion
        audience=audience,
        issuer=PORTAL_ISSUER,
        options={"require": ["exp", "iat", "aud", "iss", "sub"]},
        leeway=10,
    )
    return payload


def clear_key_cache() -> None:
    """Invalidate the cached public key (e.g., after a key rotation)."""
    _get_public_key.cache_clear()
