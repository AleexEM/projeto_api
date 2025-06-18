from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from database import get_db
from app.models.emprestimo import Emprestimo

router = APIRouter(prefix="/emprestimos", tags=["emprestimos"])

# Schemas
class EmprestimoBase(BaseModel):
    cliente_id: int
    livro_id: int
    data_emprestimo: str | None = None  # ISO format
    data_devolucao_prevista: str
    data_devolucao_real: str | None = None
    status: str
    multa: float | None = None
    observacoes: str | None = None

class EmprestimoCreate(EmprestimoBase):
    pass

class EmprestimoResponse(EmprestimoBase):
    id: int

    class Config:
        from_attributes = True

# Rotas
@router.post("/", response_model=EmprestimoResponse)
def criar_emprestimo(emprestimo: EmprestimoCreate, db: Session = Depends(get_db)):
    db_emprestimo = Emprestimo(**emprestimo.model_dump())
    db.add(db_emprestimo)
    db.commit()
    db.refresh(db_emprestimo)
    return db_emprestimo

@router.get("/", response_model=List[EmprestimoResponse])
def listar_emprestimos(db: Session = Depends(get_db)):
    emprestimos = db.query(Emprestimo).all()
    return emprestimos

@router.get("/{emprestimo_id}", response_model=EmprestimoResponse)
def obter_emprestimo(emprestimo_id: int, db: Session = Depends(get_db)):
    emprestimo = db.query(Emprestimo).filter(Emprestimo.id == emprestimo_id).first()
    if emprestimo is None:
        raise HTTPException(status_code=404, detail="Empréstimo não encontrado")
    return emprestimo

@router.put("/{emprestimo_id}", response_model=EmprestimoResponse)
def atualizar_emprestimo(emprestimo_id: int, emprestimo: EmprestimoCreate, db: Session = Depends(get_db)):
    db_emprestimo = db.query(Emprestimo).filter(Emprestimo.id == emprestimo_id).first()
    if db_emprestimo is None:
        raise HTTPException(status_code=404, detail="Empréstimo não encontrado")
    for key, value in emprestimo.model_dump().items():
        setattr(db_emprestimo, key, value)
    db.commit()
    db.refresh(db_emprestimo)
    return db_emprestimo

@router.delete("/{emprestimo_id}")
def deletar_emprestimo(emprestimo_id: int, db: Session = Depends(get_db)):
    db_emprestimo = db.query(Emprestimo).filter(Emprestimo.id == emprestimo_id).first()
    if db_emprestimo is None:
        raise HTTPException(status_code=404, detail="Empréstimo não encontrado")
    db.delete(db_emprestimo)
    db.commit()
    return {"message": "Empréstimo deletado com sucesso"} 