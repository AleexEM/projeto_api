from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from database import get_db
from app.models.usuario import Funcionario

router = APIRouter(prefix="/funcionarios", tags=["funcionarios"])

# Schemas
class FuncionarioBase(BaseModel):
    nome: str
    email: str
    senha: str
    telefone: str | None = None
    cargo: str
    departamento: str | None = None
    data_contratacao: str
    salario: float | None = None
    tipo: str = "funcionario"

class FuncionarioCreate(FuncionarioBase):
    pass

class FuncionarioResponse(FuncionarioBase):
    id: int

    class Config:
        from_attributes = True

# Rotas
@router.post("/", response_model=FuncionarioResponse)
def criar_funcionario(funcionario: FuncionarioCreate, db: Session = Depends(get_db)):
    db_funcionario = Funcionario(**funcionario.model_dump())
    db.add(db_funcionario)
    db.commit()
    db.refresh(db_funcionario)
    return db_funcionario

@router.get("/", response_model=List[FuncionarioResponse])
def listar_funcionarios(db: Session = Depends(get_db)):
    funcionarios = db.query(Funcionario).all()
    return funcionarios

@router.get("/{funcionario_id}", response_model=FuncionarioResponse)
def obter_funcionario(funcionario_id: int, db: Session = Depends(get_db)):
    funcionario = db.query(Funcionario).filter(Funcionario.id == funcionario_id).first()
    if funcionario is None:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")
    return funcionario

@router.put("/{funcionario_id}", response_model=FuncionarioResponse)
def atualizar_funcionario(funcionario_id: int, funcionario: FuncionarioCreate, db: Session = Depends(get_db)):
    db_funcionario = db.query(Funcionario).filter(Funcionario.id == funcionario_id).first()
    if db_funcionario is None:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")
    for key, value in funcionario.model_dump().items():
        setattr(db_funcionario, key, value)
    db.commit()
    db.refresh(db_funcionario)
    return db_funcionario

@router.delete("/{funcionario_id}")
def deletar_funcionario(funcionario_id: int, db: Session = Depends(get_db)):
    db_funcionario = db.query(Funcionario).filter(Funcionario.id == funcionario_id).first()
    if db_funcionario is None:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")
    db.delete(db_funcionario)
    db.commit()
    return {"message": "Funcionário deletado com sucesso"} 