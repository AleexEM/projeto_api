from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Usuario(Base):
    __tablename__ = "usuario"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(128), nullable=False)
    email = Column(String(64), nullable=False, unique=True)
    senha = Column(String(128), nullable=False)
    telefone = Column(String(11), nullable=True)
    tipo = Column(String(20), nullable=False)  # Para discriminar entre Cliente e Funcionario

    __mapper_args__ = {
        'polymorphic_identity': 'usuario',
        'polymorphic_on': tipo
    }

class Cliente(Usuario):
    __tablename__ = "cliente"

    id = Column(Integer, ForeignKey('usuario.id'), primary_key=True)
    cpf = Column(String(11), nullable=False, unique=True)
    data_nascimento = Column(String(10), nullable=True)
    endereco = Column(String(256), nullable=True)

    # Relacionamento com Emprestimo
    emprestimos = relationship("Emprestimo", back_populates="cliente")

    __mapper_args__ = {
        'polymorphic_identity': 'cliente',
    }

class Funcionario(Usuario):
    __tablename__ = "funcionario"

    id = Column(Integer, ForeignKey('usuario.id'), primary_key=True)
    cargo = Column(String(64), nullable=False)
    departamento = Column(String(64), nullable=True)
    data_contratacao = Column(String(10), nullable=False)
    salario = Column(Float, nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': 'funcionario',
    } 