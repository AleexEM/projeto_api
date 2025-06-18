from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from database import get_db
from app.models.livro import Livro

router = APIRouter(prefix="/livros", tags=["livros"])

# Schemas
class LivroBase(BaseModel):
    titulo: str
    autor: str
    editora: str
    isbn: str
    ano_publicacao: int
    edicao: str | None = None
    categoria: str
    quantidade_total: int
    quantidade_disponivel: int
    localizacao: str
    descricao: str | None = None
    preco_compra: float | None = None
    data_aquisicao: str | None = None  # ISO format
    status: str
    observacoes: str | None = None

class LivroCreate(LivroBase):
    pass

class LivroResponse(LivroBase):
    id: int

    class Config:
        from_attributes = True

# Rotas
@router.post("/", response_model=LivroResponse)
def criar_livro(livro: LivroCreate, db: Session = Depends(get_db)):
    db_livro = Livro(**livro.model_dump())
    db.add(db_livro)
    db.commit()
    db.refresh(db_livro)
    return db_livro

@router.get("/", response_model=List[LivroResponse])
def listar_livros(db: Session = Depends(get_db)):
    livros = db.query(Livro).all()
    return livros

@router.get("/{livro_id}", response_model=LivroResponse)
def obter_livro(livro_id: int, db: Session = Depends(get_db)):
    livro = db.query(Livro).filter(Livro.id == livro_id).first()
    if livro is None:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return livro

@router.put("/{livro_id}", response_model=LivroResponse)
def atualizar_livro(livro_id: int, livro: LivroCreate, db: Session = Depends(get_db)):
    db_livro = db.query(Livro).filter(Livro.id == livro_id).first()
    if db_livro is None:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    for key, value in livro.model_dump().items():
        setattr(db_livro, key, value)
    db.commit()
    db.refresh(db_livro)
    return db_livro

@router.delete("/{livro_id}")
def deletar_livro(livro_id: int, db: Session = Depends(get_db)):
    db_livro = db.query(Livro).filter(Livro.id == livro_id).first()
    if db_livro is None:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    db.delete(db_livro)
    db.commit()
    return {"message": "Livro deletado com sucesso"} 