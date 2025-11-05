from .app import app, db, mail
from flask import render_template, redirect, url_for,request,flash, abort
from flask_login import login_user, logout_user, login_required, current_user
from monApp.models import db, User, Type_plat, Plat, Reservation, ContenirP, ContenirF, Formule
from flask_mail import Mail,Message
from datetime import date
import os
from functools import wraps


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Vérifie si le user est connecté
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
            if unUser.est_admin:
                return redirect(url_for('admin'))
            else:
                return redirect(url_for('index'))
    return render_template("connection.html", form=connection_form)

@app.route('/deconnection/')
def deconnection() :
    logout_user()
    return redirect(url_for('index'))

@login_required
def get_or_create_panier(numtelUser):
    panier = Reservation.query.filter_by(numtelUser=numtelUser, statut="panier").first()
    if not panier:
        panier = Reservation(
            idR=None,
            numtelUser=numtelUser,
            dateR=None,
            nb_couverts=1,
            sur_place=False,
            statut="panier"
        )
        db.session.add(panier)
        db.session.commit()
    return panier


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


@login_required
@app.route('/panier/')
def afficher_panier():
    numtel = current_user.numtelUser
    panier = get_or_create_panier(numtel)
    plats = ContenirP.query.filter_by(idR=panier.idR).all()
    formules = ContenirF.query.filter_by(idR=panier.idR).all()
    return render_template("panier.html", panier=panier, plats=plats, formules=formules)

@login_required
@app.route("/panier/ajouter-plat", methods=["POST"])
def ajouter_panier(idP):
    """créé un panier ou le recupere par rapport a l'utilisateur connecté

    Args:
        idP (_type_): _description_

    Returns:
        _type_: _description_
    """
    reservation = Reservation.query.filter_by(numtelUser=current_user.numtelUser, statut="en attente").first()
    if not reservation:
        reservation = Reservation(
            idR=None,
            numtelUser=current_user.numtelUser,
            dateR=date.today(),
            nb_couverts=1,
            sur_place=False,
            statut="en attente"
        )
        db.session.add(reservation)
        db.session.commit()
    plat = Plat.query.get(idP)
    if not plat:
        flash("Ce plat n’existe pas.", "error")
        return redirect(url_for("menu"))
    item = ContenirP.query.filter_by(idR=reservation.idR, idP=idP).first()
    if item:
        item.quantiteP += 1
    else:
        item = ContenirP(idR=reservation.idR, idP=idP, quantiteP=1)
        db.session.add(item)

    db.session.commit()
    flash(f"{plat.nomP} ajouté au panier !", "success")
    return redirect(url_for("voir_panier"))

@login_required
@app.route("/ajouter_formule/<int:idF>", methods=["POST"])
def ajouter_formule(idF):
    reservation = Reservation.query.filter_by(numtelUser=current_user.numtelUser, statut="en attente").first()
    if not reservation:
        reservation = Reservation(
            idR=None,
            numtelUser=current_user.numtelUser,
            dateR=date.today(),
            nb_couverts=1,
            sur_place=False,
            statut="en attente"
        )
        db.session.add(reservation)
        db.session.commit()
    formule = Formule.query.get(idF)
    if not formule:
        flash("Cette formule n’existe pas.", "error")
        return redirect(url_for("menu"))
    item = ContenirF.query.filter_by(idR=reservation.idR, idF=idF).first()
    if item:
        item.quantiteF += 1
    else:
        item = ContenirF(idR=reservation.idR, idF=idF, quantiteF=1)
        db.session.add(item)

    db.session.commit()
    flash(f"{formule.nomF} ajoutée au panier !", "success")
    return redirect(url_for("voir_panier"))

@app.route("/panier/modifier-plat", methods=["POST"])
@login_required
def modifier_plat():
    data = request.get_json()
    idP = int(data["idP"])
    quantite = int(data["quantite"])

    panier = get_or_create_panier(current_user.numtelUser)
    cp = ContenirP.query.filter_by(idR=panier.idR, idP=idP).first()

    if not cp:
        return jsonify({"error": "Plat non présent dans le panier"}), 404

    if quantite <= 0:
        db.session.delete(cp)
    else:
        cp.quantiteP = quantite

    db.session.commit()
    return jsonify({"success": True})

@login_required
@app.route("/modifier_quantite_plat/<int:idP>/<action>", methods=["POST"])
def modifier_quantite_plat(idP, action):
    """commande pour interagir avec les bouton + et - du panier

    Args:
        idP (_type_): _description_
        action (_type_): _description_

    Returns:
        _type_: _description_
    """
    reservation = Reservation.query.filter_by(
        numtelUser=current_user.numtelUser, statut="en attente"
    ).first()
    if not reservation:
        flash("Aucune réservation en cours.", "error")
        return redirect(url_for("voir_panier"))

    item = ContenirP.query.filter_by(idR=reservation.idR, idP=idP).first()
    if not item:
        flash("Ce plat n’est pas dans votre panier.", "error")
        return redirect(url_for("voir_panier"))

    plat = Plat.query.get(idP)
    variableChoixCom = 1
    if not reservation.sur_place :
        variableChoixCom= 0.8

    if action == "ajouter":
        nouvelle_quantite = item.quantiteP + 1
        if nouvelle_quantite > plat.stock or nouvelle_quantite > plat.stockInit * variableChoixCom:
            flash(f"Pas assez de stock pour '{plat.nomP}'", "error")
            return redirect(url_for("voir_panier"))
        item.quantiteP = nouvelle_quantite

    elif action == "diminuer":
        item.quantiteP -= 1
        if item.quantiteP <= 0:
            db.session.delete(item)  # supprime le plat si la quantité est 0

    db.session.commit()
    return redirect(url_for("voir_panier"))

@login_required
@app.route("/modifier_quantite_formule/<int:idF>/<action>", methods=["POST"])
def modifier_quantite_formule(idF, action):
    """commande pour interagir avec les bouton + et - du panier

    Args:
        idP (_type_): _description_
        action (_type_): _description_

    Returns:
        _type_: _description_
    """
    reservation = Reservation.query.filter_by(
        numtelUser=current_user.numtelUser, statut="en attente"
    ).first()
    if not reservation:
        flash("Aucune réservation en cours.", "error")
        return redirect(url_for("voir_panier"))

    item = ContenirF.query.filter_by(idR=reservation.idR, idF=idF).first()
    if not item:
        flash("Cette formule n’est pas dans votre panier.", "error")
        return redirect(url_for("voir_panier"))

    formule = Formule.query.get(idF)
    variableChoixCom = 1
    if not reservation.sur_place :
        variableChoixCom= 0.8

    if action == "ajouter":
        nouvelle_quantite = item.quantiteF + 1
        for c in formule.plats:
            plat = Plat.query.get(c.idP)
            qte_totale = (item.quantiteF + 1) * c.quantiteC
            if qte_totale > plat.stock or qte_totale > plat.stockInit * variableChoixCom:
                flash(f"Pas assez de stock pour le plat '{plat.nomP}' de la formule '{formule.nomF}'", "error")
                return redirect(url_for("voir_panier"))
        item.quantiteF = nouvelle_quantite

    elif action == "diminuer":
        item.quantiteF -= 1
        if item.quantiteF <= 0:
            db.session.delete(item)

    db.session.commit()
    return redirect(url_for("voir_panier"))



@app.route("/panier/valider", methods=["POST"])
@login_required
def valider_panier():
    """modifie le stock et change le status de la reservation

    Returns:
        _type_: _description_
    """
    panier = Reservation.query.filter_by(numtelUser=current_user.numtelUser, statut="panier").first()
    for cp in panier.plats:
        cp.plat.stock -= cp.quantiteP
    for cf in panier.formules:
        for c in cf.formule.plats:
            c.plat.stock -= cf.quantiteF * c.quantiteC
    panier.statut = "confirmée"
    db.session.commit()
    flash("Réservation validée !", "success")
    return redirect(url_for("mes_reservations"))

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

@app.route('/admin/gestion_compte/')
@admin_required
def gestion_compte():
    return "page de gestion du compte admin"
    
if __name__== "__main__" :
    app.run()
