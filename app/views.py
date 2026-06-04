from flask import render_template, url_for, request, redirect

from app import app, db
from app.models import Contato
from app.forms import ContatoForm


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/contato/", methods=["GET", "POST"])
def contato():
    form = ContatoForm()

    if form.validate_on_submit():
        contato_registro = Contato()
        form.populate_obj(contato_registro)
        db.session.add(contato_registro)
        db.session.commit()
        return redirect(url_for("listacontato"))

    return render_template("contato.html", form=form)

@app.route("/contato/<int:id>/")
def contatoDetail(id):
    obj = Contato.query.get_or_404(id)

    return render_template("contato_detail.html", obj=obj)


@app.route("/contato/<int:id>/responder/", methods=["POST"])
def marcarRespondido(id):
    obj = Contato.query.get_or_404(id)
    obj.respondido = 1 if obj.respondido == 0 else 0
    db.session.commit()
    return redirect(url_for("contatoDetail", id=id))


@app.route("/contato/listar/")
def listacontato():
    pesquisar = request.args.get("pesquisar", "")
    query = Contato.query.order_by(Contato.nome)
    if pesquisar:
        query = query.filter(Contato.nome.ilike(f"%{pesquisar}%"))
    dados = query.all()

    return render_template("contatolista.html", dados=dados, pesquisar=pesquisar)


@app.route("/form/", methods=["GET", "POST"])
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

