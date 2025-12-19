from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from model.base import Base


class Estoque(Base):
    __tablename__ = "estoque"

    id = Column(Integer, primary_key=True)
    quantidade_disponivel = Column(Integer, nullable=False)
    data_entrada = Column(DateTime, default=datetime.now)

    solicitacao_id = Column(
        Integer,
        ForeignKey("solicitacao.id"),
        unique=True,
        nullable=False
    )

    solicitacao = relationship("Solicitacao", back_populates="estoque")
