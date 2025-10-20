from typing import List, Optional, Dict
from .modelos import Livro

_livros_memoria: List[Dict] = [
    {
        "id": 1,
        "titulo": "A Light in the Attic",
        "preco": 51.77,
        "nota": 3.0,
        "disponivel": 22,
        "genero": "Poetry",
        "imagem": "https://books.toscrape.com/media/cache/fe/72/fe72f0532301ec28892ae79a629a293c.jpg"
    },
    {
        "id": 2,
        "titulo": "Tipping the Velvet",
        "preco": 53.74,
        "nota": 1.0,
        "disponivel": 8,
        "genero": "Historical Fiction",
        "imagem": "https://books.toscrape.com/media/cache/08/e9/08e94f3731d7d6b760dfbfbc02ca5c62.jpg"
    }
]

def listar_livros() -> List[Livro]:
    return [Livro(**d) for d in _livros_memoria]

def obter_livro_por_id(identificador: int) -> Optional[Livro]:
    for d in _livros_memoria:
        if d["id"] == identificador:
            return Livro(**d)
    return None

def listar_generos() -> List[str]:
    generos = sorted({d["genero"] for d in _livros_memoria})
    return generos