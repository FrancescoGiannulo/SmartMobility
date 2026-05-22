from uuid import UUID
import jwt
from jwt import PyJWKClient
from fastapi import Request, HTTPException
from config import SUPABASE_JWT_SECRET, SUPABASE_URL
from dal.attore_repository import AttoreRepository, AttoreNonTrovatoException

_jwks_client: PyJWKClient | None = None


def _get_jwks_client() -> PyJWKClient:
    global _jwks_client
    if _jwks_client is None:
        _jwks_client = PyJWKClient(f"{SUPABASE_URL}/auth/v1/.well-known/jwks.json")
    return _jwks_client


def _decode_token(token: str) -> dict:
    """Decodifica JWT Supabase: supporta HS256 (test) e ES256 (produzione)."""
    # Inspect header to choose algorithm
    try:
        header = jwt.get_unverified_header(token)
    except jwt.InvalidTokenError:
        raise jwt.InvalidTokenError("Header non valido")

    alg = header.get("alg", "HS256")

    if alg == "HS256":
        return jwt.decode(
            token,
            SUPABASE_JWT_SECRET,
            algorithms=["HS256"],
            options={"verify_aud": False},
        )
    else:
        # ES256 (o altri algoritmi asimmetrici) — usa JWKS
        signing_key = _get_jwks_client().get_signing_key_from_jwt(token)
        return jwt.decode(
            token,
            signing_key.key,
            algorithms=["ES256"],
            options={"verify_aud": False},
        )


def verify_token(required_roles: list[str] | None = None):
    """Dependency factory. Verifica JWT Supabase e ruolo. Inietta {id, ruolo, email} nella request."""

    def _inner(request: Request) -> dict:
        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Token non valido o scaduto")

        token = auth.removeprefix("Bearer ")

        try:
            payload = _decode_token(token)
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token non valido o scaduto")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Token non valido o scaduto")
        except Exception:
            raise HTTPException(status_code=401, detail="Token non valido o scaduto")

        user_id = UUID(payload["sub"])
        email = payload.get("email", "")

        try:
            _, ruolo = AttoreRepository().trova_per_id(user_id)
        except AttoreNonTrovatoException:
            raise HTTPException(status_code=401, detail="Token non valido o scaduto")

        if required_roles and ruolo not in required_roles:
            raise HTTPException(status_code=403, detail="Accesso non autorizzato")

        request.state.utente_id = user_id
        request.state.ruolo = ruolo
        request.state.email = email
        return {"id": user_id, "ruolo": ruolo, "email": email}

    return _inner
