from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List, Optional

class RespostaEstoqueSchema(BaseModel):
    id: int
    quantidade_disponivel: int
    data_entrada: datetime
    cadastro_id: Optional[int] = None
    nome: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class ListaEstoqueSchema(BaseModel):
    """ Define como a lista de itens em estoque será retornada """
    estoque: List[RespostaEstoqueSchema]
    
