from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #tira quando fazer o deploy

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app.models import Contato
from app import views