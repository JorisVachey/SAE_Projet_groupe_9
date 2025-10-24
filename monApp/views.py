import os
from .app import app, db
from flask import render_template, redirect, url_for
from flask_login import login_user, logout_user, login_required
from monApp.models import db,Client, Restauratrice, Type_plat, Plat


@app.route('/')
@app.route('/index/')
def index() :
    lesTypeDePlats = Type_plat.query.all()
    return render_template("index.html", TypeDePlats=lesTypeDePlats)

@app.route('/propos/')
def propos() :
    return "page a propos"

@app.route('/menu/')
def menu():
    lesTypeDePlats = Type_plat.query.all()
    lesPlats = Plat.query.all()
    for plat in lesPlats:
        if plat.cheminImg:
            chemin_complet = os.path.join(app.root_path, 'static', plat.cheminImg)
            if not os.path.isfile(chemin_complet):
                plat.cheminImg = 'img/base/image_defaut.png'
        else:
            plat.cheminImg = 'img/base/image_defaut.png'
    
    return render_template('menu.html', plats=lesPlats, TypeDePlats=lesTypeDePlats)
    

@app.route('/contact/')
def contact() :
    return render_template("contact.html")


@app.route('/nouvautes/')
def nouvautes() :
    return "page nouvautes"

@app.route('/admin/')
def admin() :
    return "page admin"

@app.route('/connection/', methods=("GET","POST",))
def connection() :
    from .forms import LoginForm
    connection_form = LoginForm()
    unUser = None
    if connection_form.validate_on_submit():
        unUser = connection_form.get_authenticated_user()
        if unUser:
            login_user(unUser)
            if isinstance(unUser, Client):
                return redirect(url_for('index'))
            if isinstance(unUser, Restauratrice):
                return redirect(url_for('admin'))
    return render_template("connection.html", form=connection_form)

@app.route('/deconnection/')
def deconnection() :
    logout_user()
    return redirect(url_for('index'))

@app.route('/inscription/', methods=("GET","POST",))
def inscription():
    from .forms import RegisterForm
    inscription_form = RegisterForm()
    newUser = None
    if inscription_form.validate_on_submit():
        newUser = inscription_form.get_registered_user()
        if newUser:
            db.session.add(newUser)
            db.session.commit()
            return redirect(url_for('connection'))
    return render_template("inscription.html", form=inscription_form)

if __name__== "__main__" :
    app.run()
