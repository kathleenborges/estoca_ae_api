from pydantic import BaseModel, HttpUrl


class CriacaoCadastroSchema(BaseModel):
    """ Criar o cadastro """
    nome: str
    valor: float
    link: HttpUrl


class RespostaCadastroSchema(BaseModel):
    """ Resposta do cadastro """
    id: int
    nome: str
    valor: float
    link: str

    class Config:
        orm_mode = True
