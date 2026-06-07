from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField, FileField
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    ValidationError,
    Length
)

import os
from werkzeug.utils import secure_filename

from app import db, bcrypt, app
from app.models import Contato, User, Post, Comentarios


class UserForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    sobrenome = StringField('Sobrenome', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(min=8)])
    confirmacao_senha = PasswordField(
        'Confirmar Senha',
        validators=[DataRequired(), EqualTo('senha', message='As senhas devem ser iguais.')]
    )
    submit = SubmitField('Cadastrar')

    def validate_email(self, email):
        usuario = User.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('Este email já está em uso.')

    def save(self):
        senha_hash = bcrypt.generate_password_hash(self.senha.data).decode('utf-8')

        user = User(
            nome=self.nome.data,
            sobrenome=self.sobrenome.data,
            email=self.email.data,
            senha=senha_hash
        )

        db.session.add(user)
        db.session.commit()
        return user


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('login')

    def login(self):
        user = User.query.filter_by(email=self.email.data).first()

        if user:
            if bcrypt.check_password_hash(user.senha, self.senha.data.encode('utf-8')):
                return user
            else:
                raise Exception('Senha incorreta.')
        else:
            raise Exception('Usuario não encontrado.')


class ContatoForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    assunto = StringField('Assunto', validators=[DataRequired(), Length(min=2, max=200)])
    mensagem = TextAreaField('Mensagem', validators=[DataRequired(), Length(min=2, max=1000)])
    submit = SubmitField('Enviar')

    def save(self):
        contato = Contato(
            nome=self.nome.data,
            email=self.email.data,
            assunto=self.assunto.data,
            mensagem=self.mensagem.data
        )

        db.session.add(contato)
        db.session.commit()
        return contato


class PostForm(FlaskForm):
    mensagem = StringField("Enviar mensagem", validators=[DataRequired()])
    imagem = FileField('Imagem', validators=[DataRequired()])  # ← adicionado validators
    submit = SubmitField('Enviar')

    def save(self, user_id):
        # CORRIGIDO: variável imagem estava errada
        arquivo_imagem = self.imagem.data  # ← mudado de 'imagens' para 'arquivo_imagem'
        nome_seguro = secure_filename(arquivo_imagem.filename)
        
        post = Post(
            mensagem=self.mensagem.data,
            user_id=user_id,
            imagem=nome_seguro
        )

        # CORRIGIDO: caminho do arquivo
        caminho = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            app.config['UPLOAD_FILES'],
            'post',
            nome_seguro  # ← removido espaço extra
        )
        
        # Criar diretório se não existir
        os.makedirs(os.path.dirname(caminho), exist_ok=True)
        
        arquivo_imagem.save(caminho)

        db.session.add(post)
        db.session.commit()


class ComentariosForm(FlaskForm):
    comentario = StringField("Comentário", validators=[DataRequired()])
    submit = SubmitField("Enviar")

    def save(self, post_id):
        comentario = Comentarios(
            comentario=self.comentario.data,
            post_id=post_id
        )

        db.session.add(comentario)
        db.session.commit()