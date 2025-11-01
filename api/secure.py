import os
import jwt
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

JWT_SECRET = os.getenv("JWT_SECRET", "segredo-dev")
JWT_ALGO = "HS256"
DURATION_MIN = 30
security_http= HTTPBearer(auto_error=False)

def create_access_token(email: str) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": email,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=DURATION_MIN)).timestamp())
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGO)
    return token

def validate_auth(authorization: str | None) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token de acesso ausente ou inválido")
    token = authorization.replace("Bearer ", "", 1).strip()
    try:
        details = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO])
        return details.get("sub", "")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token de acesso expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token de acesso inválido")

def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security_http)
) -> str:
    if credentials is None or (credentials.scheme or "").lower() != "bearer":
        raise HTTPException(status_code=401, detail="Token ausente")
    token = credentials.credentials
    try:
        details = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO])
        email = details.get("sub", "")
        if not email:
            raise HTTPException(status_code=401, detail="Usuário inválido")
        return email
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")