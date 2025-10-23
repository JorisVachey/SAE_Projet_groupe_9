from .app import app
from flask import render_template
from monApp.models import db,Client


@app.route('/')
@app.route('/index/')
def index() :
    return render_template("index.html", name="Cricri")

@app.route('/propos/')
def propos() :
    return "page a propos"

@app.route('/menu/')
def menu() :
    return "page menu"

@app.route('/contact/')
def contact() :
    return "page contact"

@app.route('/nouvautes/')
def nouvautes() :
    return "page nouvautes"

@app.route('/connection/')
def connection() :
    from .forms import LoginForm
    connection_form = LoginForm()
    return render_template("connection.html", form=connection_form)

@app.route('/inscription/')
def inscription():
    from .forms import RegisterForm
    inscription_form = RegisterForm()
    return render_template("inscription.html", form=inscription_form)
    
if __name__== "__main__" :
    app.run()
