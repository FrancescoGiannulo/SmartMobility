from uuid import UUID
import jwt
from fastapi import Request, HTTPException
from config import SUPABASE_JWT_SECRET
from dal.attore_repository import AttoreRepository, AttoreNonTrovatoException


def verify_token(required_roles: list[str] | None = None):
    """Dependency factory. Verifica JWT Supabase e ruolo. Inietta {id, ruolo, email} nella request."""

    def _inner(request: Request) -> dict:
        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Token non valido o scaduto")

        token = auth.removeprefix("Bearer ")

        try:
            payload = jwt.decode(
                token,
                SUPABASE_JWT_SECRET,
                algorithms=["HS256"],
                options={"verify_aud": False},
            )
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token non valido o scaduto")
        except jwt.InvalidTokenError:
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
