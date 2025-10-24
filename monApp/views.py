from .app import app, db
from flask import render_template, redirect, url_for
from monApp.models import db,Client, Restauratrice, Type_plat
from flask_login import logout_user,login_user,login_required


@app.route('/')
@app.route('/index/')
def index() :
    lesTypeDePlats = Type_plat.query.all()
    return render_template("index.html", TypeDePlats=lesTypeDePlats)

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

@app.route('/connection/', methods=("GET","POST",))
def connection() :
    from .forms import LoginForm
    connection_form = LoginForm()
    unUser = None
    if connection_form.validate_on_submit():
        unUser = connection_form.get_authenticated_user()
        if unUser:
            login_user(unUser)
            # if isinstance(unUser, Client):
            #     session['user_type'] = 'client'
            #     return redirect(url_for('index'))
            # elif isinstance(unUser, Restauratrice):
            #     session['user_type'] = 'restauratrice'
                # return redirect(url_for('admin'))
            return redirect(url_for('index')) # remplacer par admin lorsque implémenté
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
@app.route('/admin/')
def admin() :
    return render_template("admin.html")
@app.route('/modif_plats/')
def modif_plats() :
    return "page de modif des plats"
    
if __name__== "__main__" :
    app.run()
