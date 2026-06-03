from flask_wtf import FlaskForm  # WTForms base class
from wtforms import StringField, TextAreaField, SubmitField  # Field types
from wtforms.validators import DataRequired, Email, Length  # Field validators
from app.models import Contato  # Modelo usado para criar registro

class ContatoForm(FlaskForm):  # Formulário de contato
    nome = StringField('Nome', validators=[DataRequired(), Length(min=2, max=100)])  # Campo nome
    email = StringField('Email', validators=[DataRequired(), Email()])  # Campo email
    assunto = StringField('Assunto', validators=[DataRequired(), Length(min=2, max=200)])  # Campo assunto
    mensagem = TextAreaField('Mensagem', validators=[DataRequired(), Length(min=2, max=1000)])  # Campo mensagem
    submit = SubmitField('Enviar')  # Botão enviar

    def save(self):  # Cria e retorna um objeto Contato (não faz commit)
        return Contato(  # Instância pronta para ser adicionada e commitada
            nome=self.nome.data,
            email=self.email.data,
            assunto=self.assunto.data,
            mensagem=self.mensagem.data,
        )
