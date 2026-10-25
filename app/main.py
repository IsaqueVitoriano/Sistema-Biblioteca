from fastapi import FastAPI
from app.routers import (
    livro,
    emprestimo,
)

app = FastAPI(
    title="Sistema de Biblioteca",
    description="API para gerenciamento de biblioteca com persistência relacional.",
    version="1.0.0",
)

app.include_router(livro.router)
app.include_router(emprestimo.router)
