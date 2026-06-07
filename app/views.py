from flask import render_template, url_for, request, redirect, flash
from app import app, db
from app.models import Contato, Post, Comentarios
from app.forms import ContatoForm, UserForm, LoginForm, PostForm, ComentariosForm
from flask_login import login_user, logout_user, current_user, login_required


@app.route("/", methods=["GET", "POST"])
def home():
    form = LoginForm()

    if form.validate_on_submit():
        user = form.login()
        login_user(user, remember=True)
        flash(f"Bem-vindo, {user.nome}!", "success")

    return render_template("index.html", form=form)


@app.route("/form/", methods=["GET", "POST"])
@login_required
def form():
    context = {}

    if request.method == "GET":
        pesquisar = request.args.get("pesquisar", "")
        context["pesquisar"] = pesquisar

    elif request.method == "POST":
        context["nome"] = request.form.get("nome", "")
        context["email"] = request.form.get("email", "")
        context["assunto"] = request.form.get("assunto", "")

    return render_template("form.html", **context)


@app.route("/cadastro/", methods=["GET", "POST"])
def cadastro():
    form = UserForm()

    if form.validate_on_submit():
        user = form.save()
        login_user(user, remember=True)
        flash("Cadastro realizado com sucesso!", "success")
        return redirect(url_for("home"))

    return render_template("cadastro.html", form=form)


@app.route("/sair/")
@login_required
def logout():
    logout_user()
    flash("Você saiu do sistema.", "info")
    return redirect(url_for("home"))


# ---------------- CONTATO ----------------

@app.route("/contato/", methods=["GET", "POST"])
@login_required
def contato():
    form = ContatoForm()

    if form.validate_on_submit():
        contato = Contato()
        form.populate_obj(contato)
        db.session.add(contato)
        db.session.commit()
        flash("Contato enviado com sucesso!", "success")
        return redirect(url_for("listacontato"))

    return render_template("contato.html", form=form)


@app.route("/contato/listar/")
@login_required
def listacontato():
    dados = Contato.query.all()
    return render_template("contatolista.html", dados=dados)


# ---------------- POSTS ----------------

@app.route("/post/novo/", methods=["GET", "POST"])
@login_required
def post():
    # CORRIGIDO: adicionado o form e a lógica de salvamento
    if current_user.id == 1:
        flash("Você não tem permissão para criar posts!", "danger")
        return redirect(url_for("home"))
    
    form = PostForm()

    if form.validate_on_submit():
        form.save(current_user.id)
        flash("Post criado com sucesso!", "success")
        return redirect(url_for("postlista"))

    return render_template("post.html", form=form)


@app.route("/post/lista/")
@login_required
def postlista():
    posts = Post.query.all()
    return render_template("postlista.html", posts=posts)


# ---------------- COMENTÁRIOS ----------------

@app.route("/novo/comentario/", methods=["GET", "POST"])
@login_required
def comentar():
    form = ComentariosForm()
    
    post_id = request.args.get("post_id", type=int)
    
    if not post_id:
        flash("Nenhum post selecionado para comentar!", "warning")
        return redirect(url_for("postlista"))

    if form.validate_on_submit():
        form.save(post_id)
        flash("Comentário adicionado com sucesso!", "success")
        return redirect(url_for("postlista"))

    return render_template("comentar.html", form=form, post_id=post_id)


