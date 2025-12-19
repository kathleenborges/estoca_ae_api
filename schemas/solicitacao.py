from pydantic import BaseModel
from datetime import datetime
from typing import Optional


from schemas.estoque import RespostaEstoqueSchema


class CriacaoSolicitacaoSchema(BaseModel):
    cadastro_id: int
    quantidade: int


class SolicitacaoUpdateStatusSchema(BaseModel):
    status: str  # PENDENTE | ATENDIDA


class RespostaSolicitacaoSchema(BaseModel):
    id: int
    quantidade: int
    status: str
    data_solicitacao: datetime
    data_necessidade: Optional[datetime]
    data_atendimento: Optional[datetime]
    estoque: Optional[RespostaEstoqueSchema]

    class Config:
        orm_mode = True