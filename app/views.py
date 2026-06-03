# Handlers de rotas (views) da aplicação
from flask import render_template, url_for, request, redirect  # Funções do Flask
from app import app, db  # App Flask e instância SQLAlchemy
from app.models import Contato  # Modelo Contato
from app.forms import ContatoForm  # Formulário de contato


@app.route("/")
def home():
    return render_template("index.html")  # Rende a página inicial

@app.route("/contato/", methods=["GET", "POST"])
def contato():
    # Exibe o formulário de contato e processa submissões
    form = ContatoForm()  # Instancia o formulário
    context = {}  # Contexto adicional (vazio por enquanto)
    if form.validate_on_submit():  # Se método POST e validação ok
        contato_registro = form.save()  # Cria objeto Contato com os dados
        db.session.add(contato_registro)  # Adiciona à sessão do DB
        db.session.commit()  # Persiste no banco
        return redirect(url_for("form"))  # Redireciona após salvar

    return render_template("contato.html", context=context, form=form)  # Exibe o formulário



@app.route("/form/", methods=["GET", "POST"])
def form():
    # Rota de exemplo `form` que demonstra leitura de GET/POST
    context = {}  # Contexto para a página `form`
    if request.method == "GET":
        pesquisar = request.args.get("pesquisar")  # Parâmetro de busca opcional
        context.update({"pesquisar": pesquisar})
        print("GET", pesquisar)  # Log simples
    if request.method == "POST":
        nome = request.form.get("nome")  # Recebe campo nome via POST
        email = request.form.get("email")  # Recebe campo email via POST
        assunto = request.form.get("assunto")  # Recebe campo assunto via POST

    return render_template("form.html", context=context)  # Rende a página `form`

