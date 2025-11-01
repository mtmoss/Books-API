from fastapi import APIRouter, Depends, HTTPException
from ..models import UserLogin, AccessToken
from ..secure import create_access_token, get_current_user

route_auth = APIRouter(prefix="/api/v1/auth", tags=["auth"])

FIXED_USER = {"email": "test@example.com", "password": "123456"}

@route_auth.post("/login", response_model=AccessToken)
def login(details: UserLogin):
    if details.email == FIXED_USER["email"] and details.password == FIXED_USER["password"]:
        token = create_access_token(details.email)
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Credenciais inválidas")

@route_auth.get("/me")
def who_am_i(author: str = Depends(get_current_user)):
    return {"email": author}