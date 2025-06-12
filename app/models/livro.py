from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Livro(Base):
    __tablename__ = "livro"

    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(256), nullable=False)
    autor = Column(String(128), nullable=False)
    editora = Column(String(128), nullable=False)
    isbn = Column(String(13), nullable=False, unique=True)
    ano_publicacao = Column(Integer, nullable=False)
    edicao = Column(String(32), nullable=True)
    categoria = Column(String(64), nullable=False)
    quantidade_total = Column(Integer, nullable=False)
    quantidade_disponivel = Column(Integer, nullable=False)
    localizacao = Column(String(32), nullable=False)  # Ex: "Prateleira A-12"
    descricao = Column(String(512), nullable=True)
    preco_compra = Column(Float, nullable=True)
    data_aquisicao = Column(DateTime, nullable=True)
    status = Column(String(20), nullable=False)  # 'disponivel', 'emprestado', 'manutencao'
    observacoes = Column(String(256), nullable=True)

    # Relacionamentos
    emprestimos = relationship("Emprestimo", back_populates="livro") 