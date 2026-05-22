import os
import ssl
from supabase import create_client, Client
from dotenv import load_dotenv
from database import engine, SessionLocal  # noqa: F401 — re-exported for legacy imports

load_dotenv()

# University network does SSL inspection with a non-RFC-5280-compliant CA;
# neither certifi nor the Windows store can verify the chain cleanly.
_orig_ssl_ctx = ssl.create_default_context
def _ssl_no_verify(*args, **kwargs):
    ctx = _orig_ssl_ctx(*args, **kwargs)
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx
ssl.create_default_context = _ssl_no_verify

SUPABASE_URL: str = os.environ["SUPABASE_URL"]
SUPABASE_KEY: str = os.environ["SUPABASE_KEY"]
SUPABASE_JWT_SECRET: str = os.environ["SUPABASE_JWT_SECRET"]
DATABASE_URL: str = os.environ["DATABASE_URL"]

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
