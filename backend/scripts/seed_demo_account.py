"""
Crea l'account demo UT usato per la demo movimento mezzi all'esame.
L'email deve coincidere con DEMO_ACCOUNT_EMAIL (backend) / VITE_DEMO_EMAIL (frontend).
Eseguire una sola volta: cd backend && uv run python scripts/seed_demo_account.py
Idempotente: se l'utente esiste gia, ne riusa l'id e fa upsert nella tabella utenti.
"""
import os
from dotenv import load_dotenv
from supabase import create_client
from sqlalchemy import create_engine, text

load_dotenv()

DEMO = {
    "email": "demo@smartmobility.it",
    "password": "DemoEsame2026!",
    "nome": "Demo",
    "cognome": "Esame",
}

supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

print(f"Creo account demo UT: {DEMO['email']} ...", end=" ")
try:
    try:
        res = supabase.auth.admin.create_user({
            "email": DEMO["email"],
            "password": DEMO["password"],
            "email_confirm": True,
        })
        uid = res.user.id
    except Exception:
        # gia esistente: recupera id e reimposta la password nota
        users = supabase.auth.admin.list_users()
        uid = next(u.id for u in users if u.email == DEMO["email"])
        supabase.auth.admin.update_user_by_id(uid, {"password": DEMO["password"]})

    db_engine = create_engine(os.environ["DATABASE_URL"])
    with db_engine.connect() as conn:
        conn.execute(
            text(
                "INSERT INTO utenti (id, nome, cognome, sospeso, consenso_privacy_at) "
                "VALUES (:id, :nome, :cognome, false, now()) "
                "ON CONFLICT (id) DO UPDATE SET sospeso = false, consenso_privacy_at = now()"
            ),
            {"id": uid, "nome": DEMO["nome"], "cognome": DEMO["cognome"]},
        )
        conn.commit()

    print(f"OK (id={uid})")
except Exception as e:
    print(f"ERRORE: {e}")
    raise

print("\n=== CREDENZIALI ACCOUNT DEMO (UT) ===")
print(f"  email:    {DEMO['email']}")
print(f"  password: {DEMO['password']}")
