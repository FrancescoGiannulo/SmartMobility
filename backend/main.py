import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers.login_controller import router as login_router
from controllers.utente_controller import router as auth_router, mappa_router
from controllers.mezzo_operatore_controller import router as mezzo_op_router
from controllers.zona_operatore_controller import router as zona_op_router
from controllers.prenotazione_utente_controller import router as corsa_router
from controllers.ap_controller import router as ap_router
from controllers.pricing_controller import router as pricing_router

app = FastAPI(title="SmartMobility API")

_origins_env = os.getenv("FRONTEND_URL", "http://localhost:5173")
_allowed_origins = [o.strip() for o in _origins_env.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=_allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(login_router)
app.include_router(auth_router)
app.include_router(mappa_router)
app.include_router(mezzo_op_router)
app.include_router(zona_op_router)
app.include_router(corsa_router)
app.include_router(ap_router)
app.include_router(pricing_router)


@app.get("/")
def root():
    return {"status": "ok", "message": "SmartMobility API attiva"}
