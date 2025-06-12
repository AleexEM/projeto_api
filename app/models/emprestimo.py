from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Emprestimo(Base):
    __tablename__ = "emprestimo"

    id = Column(Integer, primary_key=True, autoincrement=True)
    cliente_id = Column(Integer, ForeignKey('cliente.id'), nullable=False)
    livro_id = Column(Integer, ForeignKey('livro.id'), nullable=False)
    data_emprestimo = Column(DateTime, default=datetime.now, nullable=False)
    data_devolucao_prevista = Column(DateTime, nullable=False)
    data_devolucao_real = Column(DateTime, nullable=True)
    status = Column(String(20), nullable=False)  # 'ativo', 'devolvido', 'atrasado'
    multa = Column(Float, nullable=True)
    observacoes = Column(String(256), nullable=True)

    # Relacionamentos
    cliente = relationship("Cliente", back_populates="emprestimos")
    livro = relationship("Livro", back_populates="emprestimos") 