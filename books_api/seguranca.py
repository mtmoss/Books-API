import os
import jwt
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

SEGREDO_JWT = os.getenv("JWT_SECRET", "segredo-dev")
ALGORITMO_JWT = "HS256"
DURACAO_MINUTOS = 30
seguranca_http = HTTPBearer(auto_error=False)

def criar_token_acesso(email: str) -> str:
    agora = datetime.now(timezone.utc)
    payload = {
        "sub": email,
        "iat": int(agora.timestamp()),
        "exp": int((agora + timedelta(minutes=DURACAO_MINUTOS)).timestamp())
    }
    token = jwt.encode(payload, SEGREDO_JWT, algorithm=ALGORITMO_JWT)
    return token

def validar_autorizacao(authorization: str | None) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token de acesso ausente ou inválido")
    token = authorization.replace("Bearer ", "", 1).strip()
    try:
        dados = jwt.decode(token, SEGREDO_JWT, algorithms=[ALGORITMO_JWT])
        return dados.get("sub", "")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token de acesso expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token de acesso inválido")
    
def obter_usuario_atual(
        credenciais: HTTPAuthorizationCredentials = Depends(seguranca_http)
) -> str:
    if credenciais is None or (credenciais.scheme or "").lower() != "bearer":
        raise HTTPException(status_code=401, detail="Token ausente")
    token = credenciais.credentials
    try:
        dados = jwt.decode(token, SEGREDO_JWT, algorithms=[ALGORITMO_JWT])
        email = dados.get("sub", "")
        if not email:
            raise HTTPException(status_code=401, detail="Usuário inválido")
        return email
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")