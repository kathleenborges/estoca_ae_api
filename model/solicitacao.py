from sqlalchemy import Column, Integer, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from datetime import datetime

from model.base import Base


class Solicitacao(Base):
    __tablename__ = "solicitacao"

    id = Column(Integer, primary_key=True)
    quantidade = Column(Integer, nullable=False)
    data_solicitacao = Column(DateTime, default=datetime.now)
    data_necessidade = Column(DateTime, default=datetime.now)
    data_atendimento = Column(DateTime, nullable=True)
    status = Column(String(20), default="PENDENTE",nullable=False)
    cadastro_id = Column(Integer, ForeignKey("cadastro.id"), nullable=False)

    # Relacionamento N:1 (muitas solicitações → um cadastro)
    cadastro = relationship("Cadastro", back_populates="solicitacoes")

    # Relacionamento 1:1 com Estoque
    estoque = relationship(
        "Estoque",
        back_populates="solicitacao",
        uselist=False,
        cascade="all, delete-orphan"
    )
