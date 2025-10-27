from fastapi import APIRouter, Depends, HTTPException
from ..modelos import UsuarioLogin, TokenAcesso
from ..seguranca import criar_token_acesso, obter_usuario_atual

rota_autenticacao = APIRouter(prefix="/api/v1/auth", tags=["autenticacao"])

USUARIO_FIXO = {"email": "teste@exemplo.com", "senha": "123456"}

@rota_autenticacao.post("/login", response_model=TokenAcesso)
def login(dados: UsuarioLogin):
    if dados.email == USUARIO_FIXO["email"] and dados.senha == USUARIO_FIXO["senha"]:
        token = criar_token_acesso(dados.email)
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Credenciais inválidas")

@rota_autenticacao.get("/eu")
def quem_sou(autor: str = Depends(obter_usuario_atual)):
    return {"email": autor}