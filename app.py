from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from sqlalchemy.exc import IntegrityError
from datetime import datetime


from model import Session, Cadastro, Solicitacao, Estoque, Base, engine
from schemas import *
from flask_cors import CORS


# -----------------------------------------------------------------------------
# API INFO
# -----------------------------------------------------------------------------


info = Info(title="Estoca ae!", version="1.0.0", description="API de Cadastro, Solicitação e Estoque")
app = OpenAPI(__name__, info=info)
CORS(app)


# -----------------------------------------------------------------------------
# TAGS
# -----------------------------------------------------------------------------


home_tag = Tag(name="Home", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
cadastro_tag = Tag(name="Cadastro", description="Adição, visualização e remoção de materiais à base")
solicitacao_tag = Tag(name="Solicitação", description="Realização de pedido de material")
estoque_tag = Tag(name="Estoque", description="Controle de estoque após atendimento da solicitação")


# -----------------------------------------------------------------------------
# HOME
# -----------------------------------------------------------------------------

@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')

# -----------------------------------------------------------------------------
# CADASTRO
# -----------------------------------------------------------------------------

@app.post("/cadastros", tags=[cadastro_tag])
def criar_cadastro(body: CriacaoCadastroSchema):
    """Cria um novo cadastro"""
    session = Session()

    cadastro = Cadastro(**body.dict())

    try:
        session.add(cadastro)
        session.commit()
        return RespostaCadastroSchema.from_orm(cadastro)

    except IntegrityError:
        session.rollback()
        return {"message": "Cadastro já existente"}, 409

    finally:
        session.close()


@app.get("/cadastros", tags=[cadastro_tag])
def listar_cadastros():
    """Lista todos os cadastros"""
    session = Session()
    cadastros = session.query(Cadastro).all()
    session.close()

    return [RespostaCadastroSchema.from_orm(c) for c in cadastros]


@app.delete("/cadastros/{id}", tags=[cadastro_tag])
def deletar_cadastro(path: IdPathSchema):
    session = Session()

    cadastro = session.get(Cadastro, path.id)
    if not cadastro:
        session.close()
        return {"message": "Cadastro não encontrado"}, 404

    if cadastro.solicitacoes:
        session.close()
        return {
            "message": "Cadastro possui solicitações associadas"
        }, 400


    session.delete(cadastro)
    session.commit()
    session.close()

    return {"message": "Cadastro removido com sucesso"}


# -----------------------------------------------------------------------------
# SOLICITAÇÃO
# -----------------------------------------------------------------------------

@app.post("/solicitacoes", tags=[solicitacao_tag])
def criar_solicitacao(body: CriacaoSolicitacaoSchema):
    """Cria uma solicitação"""
    session = Session()

    cadastro = session.get(Cadastro, body.cadastro_id)
    if not cadastro:
        session.close()
        return {"message": "Cadastro não encontrado"}, 404

    solicitacao = Solicitacao(
        quantidade=body.quantidade,
        cadastro=cadastro
    )

    session.add(solicitacao)
    session.commit()
    session.refresh(solicitacao)
    session.close()

    return RespostaSolicitacaoSchema.from_orm(solicitacao)


@app.put("/solicitacoes/{id}/atender", tags=[solicitacao_tag])
def atender_solicitacao(path: IdPathSchema):
    """Atende uma solicitação e gera estoque"""
    session = Session()

    solicitacao = session.get(Solicitacao, path.id)
    if not solicitacao:
        session.close()
        return {"message": "Solicitação não encontrada"}, 404

    try:
        gerar_estoque_da_solicitacao(solicitacao)
        session.commit()
        session.refresh(solicitacao)
        return RespostaSolicitacaoSchema.from_orm(solicitacao)

    except ValueError as e:
        session.rollback()
        return {"message": str(e)}, 400

    finally:
        session.close()


@app.delete("/solicitacoes/{id}", tags=[solicitacao_tag])
def deletar_solicitacao(path: IdPathSchema):
    session = Session()

    solicitacao = session.get(Solicitacao, path.id)
    if not solicitacao:
        session.close()
        return {"message": "Solicitação não encontrada"}, 404

    if solicitacao.status == "ATENDIDA":
        session.close()
        return {
            "message": "Não é possível excluir solicitação atendida"
        }, 400

    session.delete(solicitacao)
    session.commit()
    session.close()

    return {"message": "Solicitação removida com sucesso"}


# -----------------------------------------------------------------------------
# ESTOQUE
# -----------------------------------------------------------------------------

@app.get("/estoque", tags=[estoque_tag])
def listar_estoque():
    """Lista o estoque"""
    session = Session()
    estoque = session.query(Estoque).all()
    session.close()

    return [RespostaEstoqueSchema.from_orm(e) for e in estoque]


@app.delete("/estoque/{id}", tags=[estoque_tag])
def deletar_estoque(path: IdPathSchema):
    session = Session()

    estoque = session.get(Estoque, path.id)
    if not estoque:
        session.close()
        return {"message": "Estoque não encontrado"}, 404

    session.delete(estoque)
    session.commit()
    session.close()

    return {"message": "Estoque removido com sucesso"}


# -----------------------------------------------------------------------------
# SERVICE (REGRA DE NEGÓCIO)
# -----------------------------------------------------------------------------

def gerar_estoque_da_solicitacao(solicitacao: Solicitacao):
    if solicitacao.status == "ATENDIDA":
        raise ValueError("Solicitação já atendida")

    if solicitacao.estoque:
        raise ValueError("Estoque já gerado")

    solicitacao.estoque = Estoque(
        quantidade=solicitacao.quantidade
    )
    solicitacao.data_atendimento = datetime.now()
    solicitacao.status = "ATENDIDA"

# -----------------------------------------------------------------------------
# START
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    app.run(debug=True)
