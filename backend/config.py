import os
from supabase import create_client, Client
from dotenv import load_dotenv
from database import engine, SessionLocal  # noqa: F401 — re-exported for legacy imports

load_dotenv()

SUPABASE_URL: str = os.environ["SUPABASE_URL"]
SUPABASE_KEY: str = os.environ["SUPABASE_KEY"]
SUPABASE_JWT_SECRET: str = os.environ["SUPABASE_JWT_SECRET"]
DATABASE_URL: str = os.environ["DATABASE_URL"]

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
