from .app import app, db, mail
from flask import render_template, redirect, url_for,request,flash, abort, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from monApp.models import db, User, Type_plat, Plat, Reservation, ContenirP, ContenirF, Formule,Reservation
from flask_mail import Mail,Message
from datetime import datetime
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
                sender=app.config["MAIL_USERNAME"], 
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

def nb_couvert_jour(date):
    couverts_journalier = 0
    for reservationA in Reservation.query.filter_by(dateR=date).all():
        if reservationA.sur_place:
            couverts_journalier += reservationA.nb_couverts
    return couverts_journalier

def get_or_create_panier(idUser):
    """créé ou recupere la panier en cour

    Args:
        idUser (_type_): _description_

    Returns:
        _type_: _description_
    """
    panier = Reservation.query.filter_by(idUser=idUser, statut="en attente").first()
    if not panier:
        panier = Reservation(
            idUser=idUser,
            dateR=datetime.now(),
            nb_couverts=1,
            sur_place=False,
            statut="en attente"
        )
        db.session.add(panier)
        print(datetime.now())
        db.session.commit()
    return panier

@app.route("/reservation/<int:idR>/total")
@login_required
def get_total_panier(idR):
    """permet de calculer le cout total de la commande a partir d'un idR
    """
    total =0
    for cp in ContenirP.query.filter_by(idR=idR).all():
        plat = Plat.query.get(cp.idP)
        total += plat.prixP * cp.quantiteP
    for cf in ContenirF.query.filter_by(idR=idR).all():
        formule = Formule.query.get(cf.idF)
        total += formule.prixF * cf.quantiteF
    return total

@login_required
@app.route('/panier/')
def voir_panier():
    idU = current_user.idUser
    panier = get_or_create_panier(idU)
    plats = ContenirP.query.filter_by(idR=panier.idR).all()
    formules = ContenirF.query.filter_by(idR=panier.idR).all()
    return render_template("panier.html",user=current_user, panier=panier, plats=plats, formules=formules, prix_total=get_total_panier(panier.idR))


@login_required
@app.route("/ajouter_plat/<int:idP>", methods=["POST"])
def ajouter_plat(idP):
    """ajoute un plat depuis le menu, créé un panier si il n'y en a pas
    """
    reservation = get_or_create_panier(current_user.idUser)
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
    flash(f"{plat.nomP} ajoutée au panier !", "success")
    return redirect(url_for("voir_panier"))

@login_required
@app.route("/ajouter_formule/<int:idF>", methods=["POST"])
def ajouter_formule(idF):
    """ajoute une formule depuis le menu, créé la panier si besoin

    Args:
        idF (_type_): _description_

    Returns:
        _type_: _description_
    """
    reservation = get_or_create_panier(current_user.idUser)
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
        idUser=current_user.idUser, statut="en attente"
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
        if nouvelle_quantite > plat.stock+item.quantiteP or nouvelle_quantite > plat.stockInit * variableChoixCom:
            flash(f"Pas assez de stock pour '{plat.nomP}'", "error")
            #print('Pas assez de stock pour le plat')
            #print(nouvelle_quantite, plat.stock, plat.stockInit * variableChoixCom)
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
        idUser=current_user.idUser, statut="en attente"
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

@app.route("/modifier_nb_couvert/<int:idR>/<action>", methods=["POST"])
@login_required
def modifier_nb_couvert(idR, action):
    if action == "ajouter":
        reservation = Reservation.query.get(idR)
        if reservation.sur_place:
            if not nb_couvert_jour(reservation.dateR)+1>12:
                reservation.nb_couverts += 1

    elif action == "diminuer":
        reservation = Reservation.query.get(idR)
        if reservation.nb_couverts > 1:
            reservation.nb_couverts -= 1


    db.session.commit()
    return redirect(url_for("voir_panier"))

@app.route("/update_checkbox", methods=["POST"])
def update_checkbox():
    data = request.get_json()
    idR = data.get("idR")
    sur_place = data.get("sur_place")

    resa = Reservation.query.filter_by(idR=idR, idUser=current_user.idUser).first()
    for cp in ContenirP.query.filter_by(idR=idR).all():
        plat = Plat.query.get(cp.idP)
        plat.stock+=cp.quantiteP-1
        cp.quantiteP = 1
    for cf in ContenirF.query.filter_by(idR=idR).all():
        formule = Formule.query.get(cf.idF)
        for c in formule.plats:
            plat = Plat.query.get(c.idP)
            plat.stock+=c.quantiteC*cf.quantiteF-c.quantiteC
        cf.quantiteF = 1

    if sur_place and nb_couvert_jour(resa.dateR)+1<=12:
        resa.sur_place = sur_place
    else:
        resa.sur_place = False
    db.session.commit()
    return redirect(url_for("voir_panier"))


@app.route("/panier/valider", methods=["POST"])
@login_required
def valider_panier():
    """modifie le stock et change le status de la reservation

    Returns:
        _type_: _description_
    """
    panier = Reservation.query.filter_by(idUser=current_user.idUser, statut="en attente").first()
    panier.statut = "confirmée"
    db.session.commit()
    flash("Réservation validée !", "success")
    return redirect(url_for("mes_reservations"))

@login_required
@app.route('/mesreservation/')
def mes_reservations() :
    reservations = Reservation.query.filter_by(idUser=current_user.idUser).order_by(Reservation.dateR.desc()).all()
    return render_template("reservation.html", user=current_user, reservations=reservations)


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
    commandes = Reservation.query.all()
    prix_commande = 0 # TODO requete pour calculer le prix de la commande le 0 est une valeur temp
    return render_template("commande.html", commandes=commandes,prix_commande = prix_commande)


@app.route('/admin/gestion_compte/')
@admin_required
def gestion_compte():
    return "page de gestion du compte admin"
    
if __name__== "__main__" :
    app.run()
