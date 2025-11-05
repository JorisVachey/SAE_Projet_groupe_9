from hashlib import sha256
from .app import app, db, mail
from flask import render_template, redirect, url_for,request,flash, abort
from flask_login import login_user, logout_user, login_required, current_user
from monApp.models import db, User, Type_plat, Plat
from flask_mail import Mail,Message
import os
from functools import wraps


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Vérifie si le user est connecté
        print(current_user)
        if not current_user.is_authenticated:
            flash("Veuillez vous connecter pour accéder à cette page.", "warning")
            return redirect(url_for('connection'))
        # Vérifie si l user est l'admin
        if not current_user.est_admin:
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
@app.route('/index/')
def index() :
    lesTypeDePlats = Type_plat.query.all()
    return render_template("index.html", TypeDePlats=lesTypeDePlats)

@app.route('/propos/')
@app.route('/propos')
def propos() :
    return render_template("apropos.html")

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
    

@app.route('/contact/',methods = ["GET","POST"])
def contact() :
    if request.method == "POST":
        email = request.form["email"]
        message = request.form["message"]
        msg = Message(
            subject=f"Nouveau message de {email or 'anonyme'}",
            sender=app.config["MAIL_DEFAULT_SENDER"], # fonctionne car on s'envoie le mail a nous meme pas besion de verif l'adresse de l'auteur
            recipients=[app.config["MAIL_USERNAME"]],  # adresse qui reçoit les messages
            body=f"Email: {email}\n\nMessage:\n{message}")
        
        if email:
            msg.reply_to = email
        try:
            mail.send(msg)
            print("message envoyé")
            flash("Message envoyé avec succès !", "success")
        except Exception as e:
            import traceback
            print("Erreur lors de l'envoi du mail :")
            traceback.print_exc()
            flash(f"Erreur lors de l'envoi : {e}", "danger")
        if email:
             msg_confirmation = Message(
                subject="Confirmation : votre message a été envoyé",
                sender=app.config["MAIL_USERNAME"],  # toujours ton SMTP
                recipients=[email],
                body="Merci ! Nous avons bien reçu votre message envoyer sur notre site."
            )
        try:
            mail.send(msg_confirmation)
            print("Mail de confirmation envoyé à l'utilisateur")
        except Exception as e:
            print("Erreur lors de l'envoi au user :", e)

        flash("Message envoyé avec succès !", "success")
    return render_template("contact.html")


@app.route('/nouveautes/')
def nouveautes() :
    return render_template("nouveautes.html")

@app.route('/connection/', methods=("GET","POST",))
def connection() :
    from .forms import LoginForm
    connection_form = LoginForm()
    unUser = None
    if connection_form.validate_on_submit():
        unUser = connection_form.get_authenticated_user()
        if unUser:
            login_user(unUser)
            print(current_user)
            if unUser.est_admin:
                return redirect(url_for('admin'))
            else:
                return redirect(url_for('index'))
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
@admin_required
def admin():
    return render_template("admin.html")

@app.route('/admin/gestion_plats/')
@admin_required
def gestion_plats():
    return "page de modif des plats"

@app.route('/admin/gestion_formules/')
@admin_required
def gestion_formules():
    return "page de gestion des formules"

@app.route('/admin/gestion_cli/')
@admin_required
def gestion_cli():
    return "page de gestion des clients"

@app.route('/admin/voir_comm/')
@admin_required
def voir_comm():
    return "page de visionnage des commandes"

@app.route('/admin/gestion_compte/', methods=("GET","POST",))
@admin_required
def gestion_compte():
    return render_template("admin_compte.html", user=current_user)

@app.route('/admin/modifier_pseudo', methods=['POST'])
@admin_required
def modifier_pseudo():
    nouveau_pseudo = request.form.get('pseudonyme')
    if nouveau_pseudo:
        current_user.pseudonyme = nouveau_pseudo
        db.session.commit()
        flash('Pseudonyme mis à jour avec succès.', 'success')
    return redirect(url_for('gestion_compte'))


@app.route('/admin/modifier_numtel', methods=['POST'])
@admin_required
def modifier_numtel():
    nouveau_numtel = request.form.get('numtel')
    if nouveau_numtel:
        current_user.numtelUser = nouveau_numtel
        db.session.commit()
        flash('Numéro de téléphone mis à jour avec succès.', 'success')
    return redirect(url_for('gestion_compte'))


@app.route('/admin/modifier_mdp', methods=['POST'])
@admin_required
def modifier_mdp():
    ancien_mdp = request.form.get('ancien_mdp')
    nouveau_mdp = request.form.get('nouveau_mdp')

    # Vérification de l'ancien mot de passe
    hash_ancien = sha256(ancien_mdp.encode('utf-8')).hexdigest()
    if current_user.mdp != hash_ancien:
        flash("L'ancien mot de passe est incorrect.", "danger")
        return redirect(url_for('mon_compte'))

    # Hachage du nouveau mot de passe
    hash_nouveau = sha256(nouveau_mdp.encode('utf-8')).hexdigest()
    current_user.mdp = hash_nouveau
    db.session.commit()

    flash('Mot de passe mis à jour avec succès.', 'success')
    return redirect(url_for('gestion_compte'))

    
if __name__== "__main__" :
    app.run()
