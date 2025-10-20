from pydantic import BaseModel
from typing import List

class Livro(BaseModel):
    id: int
    titulo: str
    preco: float
    nota: float
    disponivel: int
    genero: str
    imagem: str

class RespostaLivros(BaseModel):
    total: int
    itens: List[Livro]

class UsuarioLogin(BaseModel):
    email: str
    senha: str

class TokenAcesso(BaseModel):
    access_token: str
    token_type: str