from fastapi import APIRouter

router = APIRouter(prefix="/prenotazioni", tags=["Prenotazione"])

# [IF-UT.02] Prenota Mezzo
# [IF-UT.04] Sblocca Mezzo
# [IF-UT.06] Termina Corsa
