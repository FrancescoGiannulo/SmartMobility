"""
Crea utenti di test OP e AP su Supabase + inserisce nei rispettivi ruoli.
Eseguire una sola volta: cd backend && uv run python scripts/seed_test_users.py
"""
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

url = os.environ["SUPABASE_URL"]
key = os.environ["SUPABASE_KEY"]
supabase = create_client(url, key)

UTENTI = [
    {
        "email": "operatore@smartmobility.test",
        "password": "Operatore123!",
        "ruolo": "OP",
        "nome": "Mario Rossi",
    },
    {
        "email": "admin@smartmobility.test",
        "password": "Admin123!",
        "ruolo": "AP",
        "nome": "Comune Zootropolis",
    },
]

for u in UTENTI:
    print(f"Creo {u['ruolo']}: {u['email']} ...", end=" ")
    try:
        try:
            res = supabase.auth.admin.create_user({
                "email": u["email"],
                "password": u["password"],
                "email_confirm": True,
            })
            uid = res.user.id
        except Exception:
            users = supabase.auth.admin.list_users()
            uid = next(u2.id for u2 in users if u2.email == u["email"])

        from sqlalchemy import create_engine, text
        db_engine = create_engine(os.environ["DATABASE_URL"])
        with db_engine.connect() as conn:
            if u["ruolo"] == "OP":
                conn.execute(
                    text("INSERT INTO operatori (id, nome) VALUES (:id, :nome) ON CONFLICT DO NOTHING"),
                    {"id": uid, "nome": u["nome"]},
                )
            else:
                conn.execute(
                    text("INSERT INTO amministratori (id, nome) VALUES (:id, :nome) ON CONFLICT DO NOTHING"),
                    {"id": uid, "nome": u["nome"]},
                )
            conn.commit()

        print(f"OK (id={uid})")
    except Exception as e:
        print(f"ERRORE: {e}")

print("\nCredenziali utenti di test:")
for u in UTENTI:
    print(f"  [{u['ruolo']}] {u['email']} / {u['password']}")
