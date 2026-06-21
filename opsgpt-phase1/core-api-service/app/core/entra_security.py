import time
from typing import Any

import httpx
from jose import jwk, jwt
from jose.exceptions import ExpiredSignatureError, JWKError, JWTClaimsError, JWTError

from app.core.config import settings

JWKS_CACHE_SECONDS = 3600
_jwks_cache: dict[str, Any] | None = None
_jwks_cached_at = 0.0


class EntraConfigurationError(Exception):
    pass


class EntraTokenValidationError(Exception):
    pass


class EntraRoleError(Exception):
    pass


def _missing_configuration() -> list[str]:
    required = {
        "AZURE_TENANT_ID": settings.azure_tenant_id,
        "AZURE_CLIENT_ID": settings.azure_client_id,
        "AZURE_API_AUDIENCE": settings.azure_api_audience,
    }
    return [name for name, value in required.items() if not value.strip()]


def _validate_configuration() -> None:
    missing = _missing_configuration()
    if missing:
        raise EntraConfigurationError(
            f"Microsoft Entra ID configuration is missing: {', '.join(missing)}"
        )

    if not settings.resolved_azure_issuer or not settings.resolved_azure_jwks_url:
        raise EntraConfigurationError("Microsoft Entra ID issuer or JWKS URL is not configured")


def _get_jwks() -> dict[str, Any]:
    global _jwks_cache, _jwks_cached_at

    now = time.monotonic()
    if _jwks_cache and now - _jwks_cached_at < JWKS_CACHE_SECONDS:
        return _jwks_cache

    try:
        response = httpx.get(settings.resolved_azure_jwks_url, timeout=10.0)
        response.raise_for_status()
        jwks = response.json()
    except (httpx.HTTPError, ValueError) as exc:
        raise EntraTokenValidationError("Unable to retrieve Microsoft Entra signing keys") from exc

    if not isinstance(jwks, dict) or not isinstance(jwks.get("keys"), list):
        raise EntraTokenValidationError("Microsoft Entra signing keys response is invalid")

    _jwks_cache = jwks
    _jwks_cached_at = now
    return jwks


def _get_signing_key(token: str) -> str:
    try:
        header = jwt.get_unverified_header(token)
    except JWTError as exc:
        raise EntraTokenValidationError("Invalid Microsoft Entra access token") from exc

    kid = header.get("kid")
    if not isinstance(kid, str) or not kid:
        raise EntraTokenValidationError("Microsoft Entra access token has no signing key identifier")

    matching_key = next((key for key in _get_jwks()["keys"] if key.get("kid") == kid), None)
    if not matching_key:
        raise EntraTokenValidationError("Microsoft Entra signing key was not found")

    try:
        return jwk.construct(matching_key, algorithm="RS256").to_pem().decode("utf-8")
    except (JWKError, ValueError, TypeError) as exc:
        raise EntraTokenValidationError("Microsoft Entra signing key is invalid") from exc


def validate_entra_access_token(token: str) -> dict[str, Any]:
    _validate_configuration()

    try:
        claims = jwt.decode(
            token,
            _get_signing_key(token),
            algorithms=["RS256"],
            audience=settings.azure_api_audience,
            issuer=settings.resolved_azure_issuer,
        )
    except ExpiredSignatureError as exc:
        raise EntraTokenValidationError("Microsoft Entra access token has expired") from exc
    except (JWTClaimsError, JWTError) as exc:
        raise EntraTokenValidationError("Invalid or expired Microsoft Entra access token") from exc

    if claims.get("tid") != settings.azure_tenant_id:
        raise EntraTokenValidationError("Microsoft Entra access token tenant is invalid")
    if not isinstance(claims.get("oid"), str) or not claims["oid"]:
        raise EntraTokenValidationError("Microsoft Entra access token has no user object identifier")
    return claims


def map_entra_role(claims: dict[str, Any]) -> str:
    token_roles = claims.get("roles")
    if not token_roles:
        raise EntraRoleError(
            "No OpsGPT app role found in token. Assign the user or group to an OpsGPT app role in Enterprise Applications."
        )

    if isinstance(token_roles, str):
        token_roles = [token_roles]
    if not isinstance(token_roles, list) or not all(isinstance(role, str) for role in token_roles):
        raise EntraRoleError("User is authenticated but has no OpsGPT app role assigned.")

    role_mapping = (
        (settings.entra_role_admin, "admin"),
        (settings.entra_role_senior, "senior_engineer"),
        (settings.entra_role_junior, "junior_engineer"),
    )
    for entra_role, opsgpt_role in role_mapping:
        if entra_role in token_roles:
            return opsgpt_role

    raise EntraRoleError("User is authenticated but has no OpsGPT app role assigned.")
