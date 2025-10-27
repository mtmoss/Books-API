import unicodedata
from typing import Optional, List
from .modelos import Livro

def normalizar_texto(valor: str) -> str:
    if not valor:
        return ""
    texto = valor.lower()
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(ch for ch in texto if not unicodedata.combining(ch))
    return texto

def filtrar_livros(
    livros: List[Livro],
    titulo: Optional[str] = None,
    genero: Optional[str] = None
) -> List[Livro]:
    titulo_n = normalizar_texto(titulo or "")
    genero_n = normalizar_texto(genero or "")
    resultado: List[Livro] = []

    for livro in livros:
        titulo_ok = True
        genero_ok = True

        if titulo_n:
            titulo_ok = titulo_n in normalizar_texto(livro.titulo)

        if genero_n:
            genero_ok = genero_n == normalizar_texto(livro.genero)

        if titulo_ok and genero_ok:
            resultado.append(livro)

    return resultado