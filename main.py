import uvicorn
from fastapi import FastAPI
from database import engine, Base
from app.routers import empresa as empresa_router
from app.routers import livro as livro_router
from app.routers import funcionario as funcionario_router
from app.routers import emprestimo as emprestimo_router
from app.routers import usuario as usuario_router
from app.routers import cliente as cliente_router

from app.models import empresa, emprestimo, usuario, livro

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def check_api():
    return {"response": "Api Online!"}

app.include_router(empresa_router.router)
app.include_router(livro_router.router)
app.include_router(funcionario_router.router)
app.include_router(emprestimo_router.router)
app.include_router(usuario_router.router)
app.include_router(cliente_router.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, reload=True)   