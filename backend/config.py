import os
from supabase import create_client, Client
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL: str = os.environ["SUPABASE_URL"]
SUPABASE_KEY: str = os.environ["SUPABASE_KEY"]
SUPABASE_JWT_SECRET: str = os.environ["SUPABASE_JWT_SECRET"]
DATABASE_URL: str = os.environ["DATABASE_URL"]

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
