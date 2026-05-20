from fastapi import APIRouter

router = APIRouter(prefix="/flotta/mezzi", tags=["Flotta"])

# [IF-OP.04] Modifica Stato Mezzo
# [IF-OP.12] Aggiunge Mezzo
# [IF-OP.13] Dismette Mezzo
