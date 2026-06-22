import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers.login_controller import router as login_router
from controllers.utente_controller import router as auth_router, gdpr_router
from controllers.homepage_utente_controller import router as homepage_utente_router
from controllers.segnalazione_utente_controller import router as segnalazione_ut_router
from controllers.segnalazione_op_controller import router as segnalazione_op_router
from controllers.mezzo_operatore_controller import router as mezzo_op_router
from controllers.tariffa_controller import router as tariffa_router
from controllers.zona_operatore_controller import router as zona_op_router
from controllers.corsa_controller import router as corsa_router
from controllers.ap_controller import router as ap_router
from controllers.pagamenti_controller import router as pagamenti_router
from controllers.offerta_controller import router as offerta_router
from controllers.regola_fine_corsa_controller import router as regola_fine_corsa_router
from controllers.pricing_controller import router as pricing_router
from controllers.abbonamento_controller import router as abbonamento_router
from controllers.configurazione_controller import router as configurazione_router, router_sicurezza
from controllers.suggerimento_controller import router as suggerimento_router
from controllers.recensione_controller import router as recensione_router
from controllers.utenti_op_controller import router as utenti_op_router

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
app.include_router(homepage_utente_router)
app.include_router(gdpr_router)
app.include_router(mezzo_op_router)
app.include_router(tariffa_router)
app.include_router(zona_op_router)
app.include_router(corsa_router)
app.include_router(ap_router)
app.include_router(segnalazione_ut_router)
app.include_router(segnalazione_op_router)
app.include_router(pagamenti_router)
app.include_router(offerta_router)
app.include_router(regola_fine_corsa_router)
app.include_router(pricing_router)
app.include_router(abbonamento_router)
app.include_router(configurazione_router)
app.include_router(router_sicurezza)
app.include_router(suggerimento_router)
app.include_router(recensione_router)
app.include_router(utenti_op_router)


@app.get("/")
def root():
    return {"status": "ok", "message": "SmartMobility API attiva"}
