from datetime import datetime
from flask_login import UserMixin
from app import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    sobrenome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)

    posts = db.relationship('Post', backref='user', lazy=True)


class Contato(db.Model):
    __tablename__ = 'contato'

    id = db.Column(db.Integer, primary_key=True)
    data_envio = db.Column(db.DateTime, default=datetime.utcnow)
    nome = db.Column(db.String(100))
    email = db.Column(db.String(120))
    assunto = db.Column(db.String(200))
    mensagem = db.Column(db.Text)
    respondido = db.Column(db.Integer, default=0)


class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    mensagem = db.Column(db.Text)
    imagem = db.Column(db.Text, default='default.png')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    comentarios = db.relationship(
        'Comentarios',
        backref='post',
        lazy=True,
        cascade="all, delete-orphan"
    )

    def mensagem_resumo(self):
        return f"{self.mensagem[:30]}..."


class Comentarios(db.Model):
    __tablename__ = 'comentarios'

    id = db.Column(db.Integer, primary_key=True)
    comentario = db.Column(db.Text, nullable=False)

    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    def comentario_resumo(self):
        return f"{self.comentario[:30]}..."