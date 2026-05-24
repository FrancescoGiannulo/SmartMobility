import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers.login_controller import router as login_router
from controllers.utente_controller import router as utente_router
from controllers.pagamenti_controller import router as pagamenti_router

app = FastAPI(title="SmartMobility API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL", "http://localhost:5173")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(login_router)
app.include_router(utente_router)
app.include_router(pagamenti_router)


@app.get("/")
def root():
    return {"status": "ok", "message": "SmartMobility API attiva"}
