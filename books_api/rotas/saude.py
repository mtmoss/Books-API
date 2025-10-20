from fastapi import APIRouter

rota_saude = APIRouter(prefix="/api/v1/health", tags=["saude"])

@rota_saude.get("")
def verificar_saude():
    return {"status": "ok"}