from fastapi import FastAPI
from app.routers import (
    livros,
    emprestimos, categorias, autores, exemplares, editoras, usuarios,
)

app = FastAPI(
    title="Sistema de Biblioteca",
    description="API para gerenciamento de biblioteca com persistência relacional.",
    version="1.0.0",
)

app.include_router(livros.router)
app.include_router(emprestimos.router)
app.include_router(categorias.router)
app.include_router(autores.router)
app.include_router(exemplares.router)
app.include_router(usuarios.router)
app.include_router(editoras.router)
