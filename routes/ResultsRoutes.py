from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from services.resultado_service import (
    criar_resultado,
    listar_resultados as listar_resultados_service,
    obter_resultado_por_id as obter_resultado_por_id_service,
    atualizar_resultado as atualizar_resultado_service,
    deletar_resultado as deletar_resultado_service
)

resultados_bp = Blueprint('resultados', __name__)

@resultados_bp.route('/resultados', methods=['POST'])
@jwt_required()
def registrar_resultado():
    data = request.get_json()
    try:
        resultado = criar_resultado(data)
        return jsonify({
            "id": resultado.id,
            "tipo": resultado.tipo,
            "qtd_questoes": resultado.qtd_questoes,
            "qtd_acertos": resultado.qtd_acertos,
            "qtd_erros": resultado.qtd_erros,
            "materia": resultado.materia,
            "materias_simulado": resultado.materias_simulado,
            "descricao_erros": resultado.descricao_erros,
            "nome_simulado": resultado.nome_simulado,
            "data_realizacao": resultado.data_realizacao.strftime("%Y-%m-%d")
        }), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 400

@resultados_bp.route('/resultados', methods=['GET'])
@jwt_required()
def listar_resultados():
    try:
        resultados = listar_resultados_service()
        return jsonify([{
            "id": resultado.id,
            "tipo": resultado.tipo,
            "qtd_questoes": resultado.qtd_questoes,
            "qtd_acertos": resultado.qtd_acertos,
            "qtd_erros": resultado.qtd_erros,
            "materia": resultado.materia,
            "materias_simulado": resultado.materias_simulado,
            "descricao_erros": resultado.descricao_erros,
            "nome_simulado": resultado.nome_simulado,
            "data_realizacao": resultado.data_realizacao.strftime("%Y-%m-%d")
        } for resultado in resultados]), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400

@resultados_bp.route('/resultados/<int:resultado_id>', methods=['GET'])
@jwt_required()
def obter_resultado(resultado_id):
    try:
        resultado = obter_resultado_por_id_service(resultado_id)
        return jsonify({
            "id": resultado.id,
            "tipo": resultado.tipo,
            "qtd_questoes": resultado.qtd_questoes,
            "qtd_acertos": resultado.qtd_acertos,
            "qtd_erros": resultado.qtd_erros,
            "materia": resultado.materia,
            "materias_simulado": resultado.materias_simulado,
            "descricao_erros": resultado.descricao_erros,
            "nome_simulado": resultado.nome_simulado,
            "data_realizacao": resultado.data_realizacao.strftime("%Y-%m-%d")
        }), 200
    except ValueError as e:
        return jsonify({"message": str(e)}), 404
    except Exception as e:
        return jsonify({"message": str(e)}), 400

@resultados_bp.route('/resultados/<int:resultado_id>', methods=['PUT'])
@jwt_required()
def atualizar_resultado_route(resultado_id):
    data = request.get_json()
    try:
        resultado = atualizar_resultado_service(resultado_id, data)
        if not resultado:
            return jsonify({"message": "Resultado não encontrado"}), 404
        
        return jsonify({
            "id": resultado.id,
            "tipo": resultado.tipo,
            "qtd_questoes": resultado.qtd_questoes,
            "qtd_acertos": resultado.qtd_acertos,
            "qtd_erros": resultado.qtd_erros,
            "materia": resultado.materia,
            "materias_simulado": resultado.materias_simulado,
            "descricao_erros": resultado.descricao_erros,
            "nome_simulado": resultado.nome_simulado,
            "data_realizacao": resultado.data_realizacao.strftime("%Y-%m-%d")
        }), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400

@resultados_bp.route('/resultados/<int:resultado_id>', methods=['DELETE'])
@jwt_required()
def deletar_resultado_route(resultado_id):
    try:
        deletar_resultado_service(resultado_id)
        return jsonify({"message": "Resultado deletado com sucesso"}), 204
    except ValueError as e:
        return jsonify({"message": str(e)}), 404
    except Exception as e:
        return jsonify({"message": str(e)}), 400
