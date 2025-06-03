from extensios import db
from models.Resultados import Resultados
from datetime import datetime

def criar_resultado(data): 
    tipo = data.get("tipo")
    data_realizacao = datetime.strptime(data.get("data_realizacao"), "%Y-%m-%d").date()

    resultado = Resultados(
        tipo=tipo,
        data_realizacao=data_realizacao,
        qtd_questoes=data.get("qtd_questoes"),
        qtd_acertos=data.get("qtd_acertos"),
    )

    if tipo == "prova":
        resultado.materia = data.get("materia")
    elif tipo == "simulado":
        resultado.materias_simulado = data.get("materias_simulado")
        resultado.descricao_erros = data.get("descricao_erros")
        resultado.nome_simulado = data.get("nome_simulado")

    db.session.add(resultado)
    db.session.commit()
    return resultado

def listar_resultados():
    return Resultados.query.all()

def obter_resultado_por_id(resultado_id):
    resultado = Resultados.query.get(resultado_id)
    if not resultado:
        raise ValueError("Resultado não encontrado")
    return resultado

def atualizar_resultado(resultado_id, data):
    resultado = Resultados.query.get(resultado_id)
    if not resultado:
        return None

    resultado.tipo = data.get("tipo", resultado.tipo)
    resultado.data_realizacao = datetime.strptime(data["data_realizacao"], "%Y-%m-%d").date()
    resultado.qtd_questoes = data.get("qtd_questoes", resultado.qtd_questoes)
    resultado.qtd_acertos = data.get("qtd_acertos", resultado.qtd_acertos)

    if resultado.tipo == "prova":
        resultado.materia = data.get("materia")
        resultado.materias_simulado = None
        resultado.descricao_erros = None
        resultado.nome_simulado = None
    elif resultado.tipo == "simulado":
        resultado.materias_simulado = data.get("materias_simulado")
        resultado.descricao_erros = data.get("descricao_erros")
        resultado.nome_simulado = data.get("nome_simulado")
        resultado.materia = None

    db.session.commit()
    return resultado

def deletar_resultado(resultado_id):
    resultado = Resultados.query.get(resultado_id)
    if not resultado:
        raise ValueError("Resultado não encontrado")
    db.session.delete(resultado)
    db.session.commit()
    return True
