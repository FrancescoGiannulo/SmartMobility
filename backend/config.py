import os
import httpx
from supabase import create_client, Client
from supabase.lib.client_options import SyncClientOptions
from dotenv import load_dotenv
from database import engine, SessionLocal  # noqa: F401 — re-exported for legacy imports

load_dotenv()

SUPABASE_URL: str = os.environ["SUPABASE_URL"]
SUPABASE_KEY: str = os.environ["SUPABASE_KEY"]
SUPABASE_JWT_SECRET: str = os.environ["SUPABASE_JWT_SECRET"]
DATABASE_URL: str = os.environ["DATABASE_URL"]

def _ssl_funziona(url: str) -> bool:
    try:
        httpx.get(url, timeout=5)
        return True
    except Exception:
        return False

_verify = _ssl_funziona(SUPABASE_URL)
_options = None if _verify else SyncClientOptions(httpx_client=httpx.Client(verify=False))
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY, options=_options)
