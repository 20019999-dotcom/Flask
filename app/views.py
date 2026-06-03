from flask import render_template, url_for
from app import app

@app.route("/")
def form():
    return render_template("form.html")