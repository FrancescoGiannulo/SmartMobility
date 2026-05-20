from fastapi import APIRouter

router = APIRouter(prefix="/pagamenti", tags=["Pagamenti"])

# [IF-UT.12] Salva Metodi Pagamento
# [IF-UT.20] Effettua Pagamento
# [IF-UT.21] Imposta Metodo Predefinito
