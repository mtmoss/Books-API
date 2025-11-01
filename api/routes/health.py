from fastapi import APIRouter

route_health = APIRouter(prefix="/api/v1/health", tags=["health"])

@route_health.get("")
def health_check():
    return {"status": "ok"}