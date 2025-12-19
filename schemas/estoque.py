from pydantic import BaseModel
from datetime import datetime


class RespostaEstoqueSchema(BaseModel):
    id: int
    quantidade_disponivel: int
    data_entrada: datetime

    class Config:
        orm_mode = True
