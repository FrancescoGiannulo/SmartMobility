from fastapi import APIRouter

router = APIRouter(prefix="/operatore/zone", tags=["Zone Operatore"])

# [IF-OP.03] Definisce Zona Operativa
# [IF-OP.07] Definisce Tariffa
# [IF-OP.08] Modifica Tariffa
# [IF-OP.14] Definisce Regole Fine Corsa
