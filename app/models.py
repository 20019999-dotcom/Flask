from app import db
from datetime import datetime


class Contato(db.Model):  # Modelo de dados `Contato` (tabela)
    id = db.Column(db.Integer, primary_key=True)  # Identificador do registro
    data_envio = db.Column(db.DateTime, default=datetime.utcnow)  # Data e hora do envio
    nome = db.Column(db.String, nullable=True)  # Nome do remetente
    email = db.Column(db.String, nullable=True)  # Email do remetente
    assunto = db.Column(db.String, nullable=True)  # Assunto da mensagem
    mensagem = db.Column(db.String, nullable=True)  # Corpo da mensagem
    respondido = db.Column(db.Integer, default=0)  # Flag indicando se já foi respondido