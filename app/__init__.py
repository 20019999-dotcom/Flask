"""Inicialização da aplicação Flask, configuração e extensões."""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)  # Instância da aplicação Flask

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # URL do banco SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Desativa warnings de rastreamento
app.config['SECRET_KEY'] = 'wtww4twdweeeeeeeeeeeeeeeeee'  # Chave secreta para formulários

db = SQLAlchemy(app)  # ORM SQLAlchemy
migrate = Migrate(app, db)  # Flask-Migrate para migrações de esquema

from app.models import Contato  # Importa modelos (registra tabelas)
from app import views  # Importa views (registra rotas)