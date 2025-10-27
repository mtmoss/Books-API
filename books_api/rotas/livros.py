from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from ..modelos import Livro, RespostaLivros
from ..repositorio import listar_livros, listar_generos, obter_livro_por_id
from ..servicos import filtrar_livros

rota_livros = APIRouter(prefix="/api/v1", tags=["livros"])

@rota_livros.get("/books", response_model=RespostaLivros)
def listar_todos_os_livros():
    itens = listar_livros()
    return {"total": len(itens), "itens": itens}

@rota_livros.get("/books/search", response_model=RespostaLivros)
def buscar_livros(
    titulo: Optional[str] = Query(default=None),
    genero: Optional[str] = Query(default=None)
):
    itens = listar_livros()
    itens_filtrados = filtrar_livros(itens, titulo=titulo, genero=genero)
    return {"total": len(itens_filtrados), "itens": itens_filtrados}

@rota_livros.get("/books/{id}", response_model=Livro)
def detalhar_livro(id: int):
    livro = obter_livro_por_id(id)
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return livro

@rota_livros.get("/generos", response_model=List[str])
def obter_generos():
    return listar_generos()