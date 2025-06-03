from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.dialects.mysql import LONGTEXT
from extensios import db

class Resultados(db.Model):
    __tablename__ = 'resultados'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tipo = db.Column(db.String(10), nullable=False)

    data_realizacao = db.Column(db.Date, nullable=False)
    qtd_questoes = db.Column(db.Integer, nullable=False)
    qtd_acertos = db.Column(db.Integer, nullable=False)

    
    materia = db.Column(db.String(50), nullable=True)

    materias_simulado = db.Column(db.JSON, nullable=True)
    descricao_erros = db.Column(LONGTEXT, nullable=True)
    nome_simulado = db.Column(db.String(100), nullable=True)

    @property
    def qtd_erros(self):
        return self.qtd_questoes - self.qtd_acertos
