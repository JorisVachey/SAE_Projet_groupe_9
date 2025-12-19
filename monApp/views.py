from hashlib import sha256
from .app import app, db, mail
from flask import render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from monApp.models import db, User, Type_plat, Plat, Reservation, ContenirP, ContenirF, Formule, Composer
from flask_mail import Message
from datetime import datetime
import os
import time
import re
from werkzeug.utils import secure_filename
from functools import wraps
from sqlite3 import IntegrityError
from .forms import LoginForm, RegisterForm
import traceback
from sqlalchemy import update



def admin_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Vérifie si le user est connecté
        print(current_user)
        if not current_user.is_authenticated:
            flash("Veuillez vous connecter pour accéder à cette page.",
                  "warning")
            return redirect(url_for("connection"))
        # Vérifie si l user est l'admin
        if not current_user.est_admin:
            return redirect(url_for("index"))
        return f(*args, **kwargs)

    return decorated_function



ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}

def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS

def _slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\-_. ]+", "", text)
    text = re.sub(r"[\s]+", "_", text)
    return text or "image"

def save_image(file_storage, base_name: str, folder="imgP") -> str:
    """Save uploaded image into static/img/{folder} and return relative path like 'img/{folder}/xxx.jpg'"""
    if not file_storage or not allowed_file(file_storage.filename):
        return ""

    upload_dir = os.path.join(app.static_folder, "img", folder)
    os.makedirs(upload_dir, exist_ok=True)

    filename = secure_filename(file_storage.filename)
    _, ext = os.path.splitext(filename)
    unique = int(time.time())
    safe_base = _slugify(base_name)
    final_name = f"{safe_base}_{unique}{ext.lower()}"
    abs_path = os.path.join(upload_dir, final_name)
    file_storage.save(abs_path)
    return f"img/{folder}/{final_name}"



ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}

def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS

def _slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\-_. ]+", "", text)
    text = re.sub(r"[\s]+", "_", text)
    return text or "image"

def save_image(file_storage, base_name: str, folder="imgP") -> str:
    """Save uploaded image into static/img/{folder} and return relative path like 'img/{folder}/xxx.jpg'"""
    if not file_storage or not allowed_file(file_storage.filename):
        return ""

    upload_dir = os.path.join(app.static_folder, "img", folder)
    os.makedirs(upload_dir, exist_ok=True)

    filename = secure_filename(file_storage.filename)
    _, ext = os.path.splitext(filename)
    unique = int(time.time())
    safe_base = _slugify(base_name)
    final_name = f"{safe_base}_{unique}{ext.lower()}"
    abs_path = os.path.join(upload_dir, final_name)
    file_storage.save(abs_path)
    return f"img/{folder}/{final_name}"


@app.route("/")
@app.route("/index/")
def index():
    les_type_de_plats = Type_plat.query.all()
    return render_template("index.html", TypeDePlats=les_type_de_plats)


@app.route("/propos/")
@app.route("/propos")
def propos():
    return render_template("apropos.html")


@app.route("/menu/")
def menu():
    les_type_de_plats = Type_plat.query.all()
    les_plats = Plat.query.all()
    les_formules = Formule.query.all()

    for formule in les_formules:
        formule.details_plats = db.session.query(Plat, Composer.quantiteC).join(
            Composer,
            Plat.idP == Composer.idP).filter(Composer.idF == formule.idF).all()

    for plat in les_plats:
        if plat.cheminImg:
            chemin_complet = os.path.join(app.root_path, "static",
                                          plat.cheminImg)
            if not os.path.isfile(chemin_complet):
                plat.cheminImg = "img/base/image_defaut.png"
        else:
            plat.cheminImg = "img/base/image_defaut.png"

    return render_template("menu.html",
                           plats=les_plats,
                           TypeDePlats=les_type_de_plats,
                           formules=les_formules)


@app.route("/contact/", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        email = request.form["email"]
        message = request.form["message"]
        msg = Message(
            subject=f"Nouveau message de {email or "anonyme"}",
            sender=app.config[
                "MAIL_DEFAULT_SENDER"],
                # fonctionne car on s'envoie le mail a nous meme
                # pas besion de verif l'adresse de l'auteur
            recipients=[app.config["MAIL_USERNAME"]
                       ],  # adresse qui reçoit les messages
            body=f"Email: {email}\n\nMessage:\n{message}")

        if email:
            msg.reply_to = email
        try:
            mail.send(msg)
            print("message envoyé")
            flash("Message envoyé avec succès !", "success")
        except Exception as e:
            print("Erreur lors de l'envoi du mail :")
            traceback.print_exc()
            flash(f"Erreur lors de l'envoi : {e}", "danger")
        if email:
            msg_confirmation = Message(
                subject="Confirmation : votre message a été envoyé",
                sender=app.config["MAIL_USERNAME"],
                recipients=[email],
                body=
                "Merci ! Nous avons bien reçu votre message envoyer sur notre site."
            )
        try:
            mail.send(msg_confirmation)
            print("Mail de confirmation envoyé à l'utilisateur")
        except Exception as e:
            print("Erreur lors de l'envoi au user :", e)

        flash("Message envoyé avec succès !", "success")
    return render_template("contact.html")


@app.route("/nouveautes/")
def nouveautes():
    return render_template("nouveautes.html")


@app.route("/connection/", methods=("GET", "POST"))
def connection():
    connection_form = LoginForm()
    un_user = None
    next_page = request.form.get("next") or request.args.get("next")
    if connection_form.validate_on_submit():
        un_user = connection_form.get_authenticated_user()
        if un_user:
            login_user(un_user)
            if un_user.est_admin:
                return redirect(url_for("admin"))
            else:
                if next_page == "menu":
                    return redirect(url_for(next_page))
                else:
                    return redirect(url_for("index"))
    return render_template("connection.html",
                           form=connection_form,
                           next_page=next_page)


@app.route("/deconnection/")
def deconnection():
    logout_user()
    return redirect(url_for("index"))


@app.route("/inscription/", methods=(
    "GET",
    "POST",
))
def inscription():
    inscription_form = RegisterForm()
    new_user = None
    if inscription_form.validate_on_submit():
        new_user = inscription_form.get_registered_user()
        if new_user:
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for("connection"))
    return render_template("inscription.html", form=inscription_form)


def nb_couvert_jour(date):
    couverts_journalier = 0
    for reservation in Reservation.query.filter_by(dateR=date).all():
        if reservation.sur_place:
            couverts_journalier += reservation.nb_couverts
    return couverts_journalier


def get_or_create_panier(id_user):
    """créé ou recupere la panier en cour

    Args:
        idUser (_type_): _description_

    Returns:
        _type_: _description_
    """
    panier = Reservation.query.filter_by(idUser=id_user,
                                         statut="EN ATTENTE").first()
    if not panier:
        panier = Reservation(idUser=id_user,
                             dateR=datetime.now(),
                             nb_couverts=1,
                             sur_place=False,
                             statut="EN ATTENTE")
        db.session.add(panier)
        print(datetime.now())
        db.session.commit()
    return panier


@login_required
@app.route("/panier/")
def voir_panier():
    id_user = current_user.idUser
    panier = get_or_create_panier(id_user)
    plats = ContenirP.query.filter_by(idR=panier.idR).all()
    formules = ContenirF.query.filter_by(idR=panier.idR).all()
    return render_template("panier.html",
                           user=current_user,
                           panier=panier,
                           plats=plats,
                           formules=formules,
                           prix_total=panier.get_total())


@login_required
@app.route("/ajouter_plat/<int:id_p>", methods=["POST"])
def ajouter_plat(id_p):
    """ajoute un plat depuis le menu, créé un panier si il n'y en a pas
    """
    reservation = get_or_create_panier(current_user.idUser)
    plat = Plat.query.get(id_p)
    if not plat:
        flash("Ce plat n’existe pas.", "error")
        return redirect(url_for("menu"))

    item = ContenirP.query.filter_by(idR=reservation.idR, idP=id_p).first()
    qte_actuelle = item.quantiteP if item else 0

    variable_choix_com = 1
    if not reservation.sur_place:
        variable_choix_com = 0.8

    if qte_actuelle + 1 > plat.stock or qte_actuelle + 1 > plat.stockInit * variable_choix_com or plat.stock <=plat.stockInit * variable_choix_com:
        flash(f"Plus de stock disponible pour {plat.nomP}", "error")
        return redirect(url_for("menu"))

    if item:
        item.quantiteP += 1
    else:
        item = ContenirP(idR=reservation.idR, idP=id_p, quantiteP=1)
        db.session.add(item)

    db.session.commit()
    flash(f"{plat.nomP} ajoutée au panier !", "success")
    return redirect(url_for("menu"))


@login_required
@app.route("/ajouter_formule/<int:id_f>", methods=["POST"])
def ajouter_formule(id_f):
    """ajoute une formule depuis le menu, créé la panier si besoin
    """
    reservation = get_or_create_panier(current_user.idUser)
    formule = Formule.query.get(id_f)
    if not formule:
        flash("Cette formule n’existe pas.", "error")
        return redirect(url_for("menu"))

    item = ContenirF.query.filter_by(idR=reservation.idR, idF=id_f).first()
    qte_formule_future = (item.quantiteF + 1) if item else 1

    variable_choix_com = 1
    if not reservation.sur_place:
        variable_choix_com = 0.8

    for c in formule.plats:
        plat = Plat.query.get(c.idP)
        if plat.stock < c.quantiteC * qte_formule_future or c.quantiteC * qte_formule_future > plat.stockInit * variable_choix_com or plat.stock <=plat.stockInit * variable_choix_com:
            flash(
                f"Pas assez de stock pour le plat {plat.nomP} dans cette formule.",
                "error")
            return redirect(url_for("menu"))

    if item:
        item.quantiteF += 1
    else:
        item = ContenirF(idR=reservation.idR, idF=id_f, quantiteF=1)
        db.session.add(item)

    db.session.commit()
    flash(f"{formule.nomF} ajoutée au panier !", "success")
    return redirect(url_for("menu"))


@login_required
@app.route("/modifier_quantite_plat/<int:id_p>/<action>", methods=["POST"])
def modifier_quantite_plat(id_p, action):
    """commande pour interagir avec les bouton + et - du panier
    """
    reservation = Reservation.query.filter_by(idUser=current_user.idUser,
                                              statut="en attente").first()
    if not reservation:
        flash("Aucune réservation en cours.", "error")
        return redirect(url_for("voir_panier"))

    item = ContenirP.query.filter_by(idR=reservation.idR, idP=id_p).first()
    if not item:
        flash("Ce plat n’est pas dans votre panier.", "error")
        return redirect(url_for("voir_panier"))

    plat = Plat.query.get(id_p)
    variable_choix_com = 1
    if not reservation.sur_place:
        variable_choix_com = 0.8

    if action == "ajouter":
        nouvelle_quantite = item.quantiteP + 1
        if nouvelle_quantite > plat.stock or nouvelle_quantite > plat.stockInit * variable_choix_com:
            flash(f"Pas assez de stock pour '{plat.nomP}'", "error")
            return redirect(url_for("voir_panier"))
        item.quantiteP = nouvelle_quantite

    elif action == "diminuer":
        item.quantiteP -= 1
        if item.quantiteP <= 0:
            db.session.delete(item)

    db.session.commit()
    return redirect(url_for("voir_panier"))


@login_required
@app.route("/modifier_quantite_formule/<int:id_f>/<action>", methods=["POST"])
def modifier_quantite_formule(id_f, action):
    """commande pour interagir avec les bouton + et - du panier
    """
    reservation = Reservation.query.filter_by(idUser=current_user.idUser,
                                              statut="en attente").first()
    if not reservation:
        flash("Aucune réservation en cours.", "error")
        return redirect(url_for("voir_panier"))

    item = ContenirF.query.filter_by(idR=reservation.idR, idF=id_f).first()
    if not item:
        flash("Cette formule n’est pas dans votre panier.", "error")
        return redirect(url_for("voir_panier"))

    formule = Formule.query.get(id_f)
    variable_choix_com = 1
    if not reservation.sur_place:
        variable_choix_com = 0.8

    if action == "ajouter":
        nouvelle_quantite = item.quantiteF + 1
        for c in formule.plats:
            plat = Plat.query.get(c.idP)
            qte_totale = nouvelle_quantite * c.quantiteC
            if qte_totale > plat.stock or qte_totale > plat.stockInit * variable_choix_com:
                flash(
                    f"Pas assez de stock pour le plat '{plat.nomP}' de la formule '{formule.nomF}'",
                    "error")
                return redirect(url_for("voir_panier"))
        item.quantiteF = nouvelle_quantite

    elif action == "diminuer":
        item.quantiteF -= 1
        if item.quantiteF <= 0:
            db.session.delete(item)

    db.session.commit()
    return redirect(url_for("voir_panier"))


@app.route("/modifier_nb_couvert/<int:id_r>/<action>", methods=["POST"])
@login_required
def modifier_nb_couvert(id_r, action):
    if action == "ajouter":
        reservation = Reservation.query.get(id_r)
        if reservation.sur_place:
            if not nb_couvert_jour(reservation.dateR) + 1 > 12:
                reservation.nb_couverts += 1
        else:
            reservation.nb_couverts += 1

    elif action == "diminuer":
        reservation = Reservation.query.get(id_r)
        if reservation.nb_couverts > 1:
            reservation.nb_couverts -= 1

    db.session.commit()
    return redirect(url_for("voir_panier"))


@app.route("/update_checkbox", methods=["POST"])
def update_checkbox():
    """Change le statut sur place/emporter et réinitialise les quantités à 1
    pour éviter les conflits de limites, SANS toucher au stock.
    """
    data = request.get_json()
    id_r = data.get("idR")
    sur_place = data.get("sur_place")

    resa = Reservation.query.filter_by(idR=id_r,
                                       idUser=current_user.idUser).first()
    if not resa:
        return jsonify({"error": "Réservation introuvable"}), 404

    for cp in ContenirP.query.filter_by(idR=id_r).all():
        cp.quantiteP = 1

    for cf in ContenirF.query.filter_by(idR=id_r).all():
        cf.quantiteF = 1
    if sur_place and nb_couvert_jour(resa.dateR) + resa.nb_couverts <= 12:
        resa.sur_place = sur_place
        message = "Réservation mise à jour : sur place "
        success = True
    elif sur_place and nb_couvert_jour(resa.dateR) + resa.nb_couverts > 12:
        message = "Réservation mise à jour : sur place "
        success = True
        resa.nb_couverts = 12-nb_couvert_jour(resa.dateR)
        resa.sur_place = sur_place
    elif not sur_place:
        resa.sur_place = False
        message = "Réservation mise à jour : à emporter"
        success = True

    db.session.commit()

    return jsonify({
        "success": success,
        "message": message,
        "sur_place": resa.sur_place,
        "nb_couverts": resa.nb_couverts
    })


@login_required
@app.route("/admin/update_statut_preparation", methods=["POST"])
def update_statut_preparation():
    """
    Passe le statut de la commande à 'EN PREPARATION'
    dès qu'une case est cochée.
    """
    data = request.get_json()
    id_r = data.get("idR")

    reservation = Reservation.query.get(id_r)
    if not reservation:
        return jsonify({"success": False, "error": "Commande introuvable"}), 404
    reservation.statut = "EN PRÉPARATION"
    db.session.commit()
    return jsonify({"success": True, "statut": reservation.statut})


@app.route("/panier/valider", methods=["POST"])
@login_required
def valider_panier():
    """change le status de la reservation ,quand un utilisateur a fini de construire son panier

    Returns:
        _type_: _description_
    """
    panier = Reservation.query.filter_by(idUser=current_user.idUser,
                                         statut="EN ATTENTE").first()
    panier.statut = "CONFIRMÉE"
    db.session.commit()
    flash("Réservation validée !", "success")
    return redirect(url_for("mes_reservations"))


def getbesoin(reservation):
    """renvoi la liste des plats d'une reservation, avec leur nombre

    Args:
        reservation (Reservation): _description_

    Returns:
        dict: _description_
    """
    contenu_p = ContenirP.query.filter_by(idR=reservation.idR).all()
    contenu_f = ContenirF.query.filter_by(idR=reservation.idR).all()
    besoins_stock = {}  #on regroupe les plats uniques et les formules
    for item in contenu_p:
        besoins_stock[item.idP] = besoins_stock.get(item.idP,
                                                    0) + item.quantiteP
    for item in contenu_f:
        formule = Formule.query.get(item.idF)
        for c in formule.plats:
            qte_necessaire = c.quantiteC * item.quantiteF
            besoins_stock[c.idP] = besoins_stock.get(c.idP, 0) + qte_necessaire
    return besoins_stock


@app.route("/admin/preparer_panier/<int:id_r>/<action>", methods=["POST"])
@login_required
def preparer_panier(id_r, action):
    """ -> quand l'admin prend en compte une commande 
    Valide le panier et décrémente les stocks 
    ou refuse et chage l'attribut
    """
    reservation = Reservation.query.get(id_r)

    if not reservation:
        flash("Aucune réservation à traiter.", "error")
        return redirect(url_for("menu"))
    if action == "valider":
        besoins_stock = getbesoin(reservation)
        for id_p, quantite_totale in besoins_stock.items():
            plat = Plat.query.get(id_p)
            if plat.stock < quantite_totale:
                flash(
                    f"Stock insuffisant pour {plat.nomP} (Demandé: {quantite_totale}, Dispo: {plat.stock}). Veuillez modifier votre panier.",
                    "error")
                return redirect(url_for("voir_panier"))
        for id_p, quantite_totale in besoins_stock.items():
            plat = Plat.query.get(id_p)
            plat.stock -= quantite_totale

        reservation.statut = "VENIR CHERCHER"

    elif action == "supprimer":
        reservation.statut = "REFUSÉ"

    db.session.commit()
    flash("La commande a etais traité avec succès !", "success")
    return redirect(url_for("voir_comm"))


@app.route("/panier/annuler", methods=["POST"])
@login_required
def supprimer_panier():
    """supprime le panier

    Returns:
        _type_: _description_
    """
    panier = Reservation.query.filter_by(idUser=current_user.idUser,
                                         statut="EN ATTENTE").first()
    db.session.delete(panier)
    db.session.commit()
    flash("Réservation annulée !", "success")
    return redirect(url_for("menu"))


@login_required
@app.route("/mesreservation/")
def mes_reservations():
    reservations = Reservation.query.filter_by(
        idUser=current_user.idUser).order_by(Reservation.dateR.desc()).all()
    return render_template("reservation.html",
                           user=current_user,
                           reservations=reservations)


@app.route("/admin/")
@admin_required
def admin():
    return render_template("admin.html")


@app.route("/admin/gestion_plats/", methods=["GET", "POST"])
@admin_required
def gestion_plats():

    if request.method == "POST":
        try:
            nom_plat = request.form.get("nomP")
            type_plat_id = request.form.get("idTp")
            prix_plat = request.form.get("prixP")
            stock = request.form.get("stock")
            desc = request.form.get("desc")
            image_file = request.files.get('image')

            if not nom_plat or not prix_plat or not type_plat_id or not stock or not desc:
                return jsonify({
                    "success": False,
                    "error": "Champs manquants"
                }), 400

            plat_existant = Plat.query.filter_by(nomP=nom_plat).first()
            if plat_existant:
                return jsonify({
                    "success": False,
                    "error": "Un plat avec ce nom existe déjà."
                }), 400

            try:
                prix_decimal = float(prix_plat)
                type_id_int = int(type_plat_id)
                stock_int = int(stock)
            except ValueError:
                return jsonify({
                    "success": False,
                    "error": "Format de prix ou ID invalide"
                }), 400

            nouveau_plat = Plat(nomP=nom_plat,
                                idTp=type_id_int,
                                prixP=prix_decimal,
                                stock=stock_int,
                                cheminImg="",
                                descriptionP=desc)

            db.session.add(nouveau_plat)
            db.session.flush()

            nouveau_plat.stockInit = stock_int

            if image_file and allowed_file(image_file.filename):
                rel_path = save_image(image_file, nom_plat or f"plat_{nouveau_plat.idP or ''}")
                if rel_path:
                    nouveau_plat.cheminImg = rel_path

            db.session.commit()

            type_associe = Type_plat.query.get(type_id_int)
            type_nom = type_associe.nomTp if type_associe else "Inconnu"

            return jsonify({
                "success": True,
                "plat": {
                    "id": nouveau_plat.idP,
                    "nomP": nouveau_plat.nomP,
                    "prixP": nouveau_plat.prixP,
                    "type_nom": type_nom,
                    "stock": nouveau_plat.stock,
                    "stockInit": nouveau_plat.stockInit
                }
            })

        except Exception as e:
            db.session.rollback()
            return jsonify({"success": False, "error": str(e)}), 500

    plats = Plat.query.all()
    types = Type_plat.query.all()
    return render_template("gestion_plat.html", plats=plats, types=types)


@app.route("/admin/gestion_formules/", methods=["GET", "POST"])
@admin_required
def gestion_formules():
    if request.method == "POST":
        try:
            nom_formule = request.form.get("nomF")
            prix_formule = request.form.get("prixF")
            plats_ids = request.form.getlist("plats")

            if not nom_formule or not prix_formule:
                return jsonify({
                    "success": False,
                    "error": "Champs manquants"
                }), 400

            if not plats_ids:
                return jsonify({
                    "success": False,
                    "error": "Aucun plat sélectionné"
                }), 400

            if Formule.query.filter_by(nomF=nom_formule).first():
                return jsonify({
                    "success": False,
                    "error": "Une formule avec ce nom existe déjà"
                }), 400

            max_id = db.session.query(db.func.max(Formule.idF)).scalar()
            new_id = (max_id or 0) + 1

            image_file = request.files.get('image')
            chemin_img = "img/base/image_defaut.png"
            if image_file:
                saved_path = save_image(image_file, nom_formule, folder="imgF")
                if saved_path:
                    chemin_img = saved_path

            nouvelle_formule = Formule(idF=new_id,
                                       nomF=nom_formule,
                                       prixF=float(prix_formule), cheminImg=chemin_img)
            db.session.add(nouvelle_formule)
            db.session.flush()

            for pid in plats_ids:
                quantite = request.form.get(f"quantite_{pid}", 1)
                composer = Composer(idF=nouvelle_formule.idF,
                                    idP=int(pid),
                                    quantiteC=int(quantite))
                db.session.add(composer)

            db.session.commit()
            return jsonify({"success": True})

        except Exception as e:
            db.session.rollback()
            return jsonify({"success": False, "error": str(e)}), 500

    formules = Formule.query.all()
    types = Type_plat.query.all()
    plats = Plat.query.all()
    return render_template("gestion_formules.html",
                           formules=formules,
                           types=types,
                           plats=plats)


@app.route("/admin/supprimer-formule/<int:id_formule>", methods=["DELETE"])
@admin_required
def supprimer_formule(id_formule):
    try:
        formule = Formule.query.get(id_formule)
        if formule:
            db.session.delete(formule)
            db.session.commit()
            return jsonify({"success": True})
        else:
            return jsonify({
                "success": False,
                "error": "Formule introuvable"
            }), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/admin/modifier_prix_formule", methods=["POST"])
@admin_required
def modifier_prix_formule():
    data = request.get_json()
    id_formule = data.get("idF")
    nouveau_prix = data.get("prixF")

    if not id_formule or not nouveau_prix:
        return jsonify({"success": False, "error": "Données manquantes"}), 400

    try:
        formule = Formule.query.get(id_formule)
        if not formule:
            return jsonify({
                "success": False,
                "error": "Formule introuvable"
            }), 404

        formule.prixF = float(nouveau_prix)
        db.session.commit()
        return jsonify({"success": True}), 200

    except ValueError:
        return jsonify({"success": False, "error": "Prix invalide"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/admin/modifier_image_formule', methods=['POST'])
@admin_required
def modifier_image_formule():
    try:
        id_formule = request.form.get('idF')
        image_file = request.files.get('image')

        if not id_formule or not image_file:
            return jsonify({'success': False, 'error': 'Données manquantes'}), 400

        formule = Formule.query.get(id_formule)
        if not formule:
            return jsonify({'success': False, 'error': 'Formule introuvable'}), 404

        db.session.refresh(formule)

        saved_path = save_image(image_file, formule.nomF, folder="imgF")
        if saved_path:
            db.session.execute(
                update(Formule)
                .where(Formule.idF == id_formule)
                .values(cheminImg=saved_path)
            )
            db.session.commit()
            return jsonify({'success': True, 'cheminImg': saved_path}), 200
        else:
            return jsonify({'success': False, 'error': 'Erreur lors de l\'enregistrement de l\'image'}), 400

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route("/admin/gestion_cli/")
@admin_required
def gestion_cli():
    clients = User.query.filter_by(est_admin=False).all()
    return render_template("gestion_clients.html", clients=clients)


@app.route("/admin/bannir-cli/<int:client_id>")
@admin_required
def bannir_cli(client_id):
    client = User.query.filter_by(idUser=client_id).first()
    client.bannir()
    return redirect(url_for("gestion_cli"))


@app.route("/admin/debannir-cli/<int:client_id>")
@admin_required
def debannir_cli(client_id):
    client = User.query.filter_by(idUser=client_id).first()
    client.debannir()
    return redirect(url_for("gestion_cli"))


@app.route("/admin/voir_comm/")
@admin_required
def voir_comm():
    commandes = Reservation.query.filter(
        Reservation.statut.in_(["CONFIRMÉE", "EN PRÉPARATION"])).all()
    return render_template("gestion_commandes.html", commandes=commandes)


@app.route("/admin/gestion_compte/", methods=(
    "GET",
    "POST",
))
@admin_required
def gestion_compte():
    return render_template("admin_compte.html", user=current_user)


@app.route("/admin/modifier_pseudo", methods=["POST"])
@admin_required
def modifier_pseudo():
    nouveau_pseudo = request.form.get("pseudonyme")
    if nouveau_pseudo:
        current_user.pseudonyme = nouveau_pseudo
        db.session.commit()
        flash("Pseudonyme mis à jour avec succès.", "success")
    return redirect(url_for("gestion_compte"))


@app.route("/admin/modifier_numtel", methods=["POST"])
@admin_required
def modifier_numtel():
    nouveau_numtel = request.form.get("numtel")

    if not nouveau_numtel:
        flash("Veuillez entrer un numéro de téléphone.", "warning")
        return redirect(url_for("gestion_compte"))

    utilisateur_existant = User.query.filter_by(
        numtelUser=nouveau_numtel).first()

    if utilisateur_existant and utilisateur_existant.idUser != current_user.idUser:
        flash("Ce numéro de téléphone est déjà utilisé.", "danger")
        return redirect(url_for("gestion_compte"))

    try:
        current_user.numtelUser = nouveau_numtel
        db.session.commit()
        flash("Numéro de téléphone mis à jour avec succès.", "success")
    except IntegrityError:
        db.session.rollback()
        flash("Erreur : ce numéro existe déjà ou la mise à jour a échoué.",
              "danger")

    return redirect(url_for("gestion_compte"))


@app.route("/admin/modifier_mdp", methods=["POST"])
@admin_required
def modifier_mdp():
    ancien_mdp = request.form.get("ancien_mdp")
    nouveau_mdp = request.form.get("nouveau_mdp")


    hash_ancien = sha256(ancien_mdp.encode("utf-8")).hexdigest()
    if current_user.mdp != hash_ancien:
        flash("L'ancien mot de passe est incorrect.", "danger")
        return redirect(url_for("gestion_compte"))


    hash_nouveau = sha256(nouveau_mdp.encode("utf-8")).hexdigest()
    current_user.mdp = hash_nouveau
    db.session.commit()

    flash("Mot de passe mis à jour avec succès.", "success")
    return redirect(url_for("gestion_compte"))


@app.route("/supprimer-plat/<string:nom_plat>", methods=["DELETE"])
@admin_required
def supprimer_plat(nom_plat):
    try:
        plat_a_supprimer = Plat.query.filter_by(nomP=nom_plat).first()

        if plat_a_supprimer:
            db.session.delete(plat_a_supprimer)
            db.session.commit()

            return jsonify({"success": True}), 200
        else:
            return jsonify({"success": False, "error": "Plat introuvable"}), 404

    except Exception as e:
        db.session.rollback()
        print(f"Erreur lors de la suppression : {e}")
        return jsonify({
            "success": False,
            "error": "Erreur interne du serveur."
        }), 500


@app.route("/admin/modifier_prix_plat", methods=["POST"])
@admin_required
def modifier_prix_plat():
    data = request.get_json()
    id_plat = data.get("idP")
    nouveau_prix = data.get("prixP")

    if not id_plat or not nouveau_prix:
        return jsonify({"success": False, "error": "Données manquantes"}), 400

    try:
        plat = Plat.query.get(id_plat)
        if not plat:
            return jsonify({"success": False, "error": "Plat introuvable"}), 404

        plat.prixP = float(nouveau_prix)
        db.session.commit()
        return jsonify({"success": True}), 200

    except ValueError:
        return jsonify({"success": False, "error": "Prix invalide"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/admin/modifier_quantite_plat", methods=["POST"])
@admin_required
def admin_modifier_quantite_plat():
    data = request.get_json()
    id_plat = data.get("idP")
    nouvelle_quantite = data.get("stockInit")

    if not id_plat or not nouvelle_quantite:
        return jsonify({"success": False, "error": "Données manquantes"}), 400

    try:
        plat = Plat.query.get(id_plat)
        if not plat:
            return jsonify({"success": False, "error": "Plat introuvable"}), 404

        # On met à jour le stock initial et le stock courant
        # Si on veut juste changer le stock initial (capacité totale) :
        plat.stockInit = int(nouvelle_quantite)
        # Si on veut réinitialiser le stock courant à la nouvelle capacité :
        # plat.stock = int(nouvelle_quantite)

        db.session.commit()
        return jsonify({"success": True}), 200

    except ValueError:
        return jsonify({"success": False, "error": "Quantité invalide"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/admin/modifier_image_plat', methods=['POST'])
@admin_required
def modifier_image_plat():
    try:
        id_plat = request.form.get('idP')
        image_file = request.files.get('image')

        if not id_plat or not image_file:
            return jsonify({'success': False, 'error': 'Données manquantes'}), 400

        plat = Plat.query.get(id_plat)
        if not plat:
            return jsonify({'success': False, 'error': 'Plat introuvable'}), 404

        if not allowed_file(image_file.filename):
            return jsonify({'success': False, 'error': 'Format d\'image non autorisé'}), 400

        rel_path = save_image(image_file, plat.nomP or f"plat_{plat.idP}")
        if not rel_path:
            return jsonify({'success': False, 'error': 'Échec de l\'enregistrement de l\'image'}), 500

        plat.cheminImg = rel_path
        db.session.commit()
        return jsonify({'success': True, 'cheminImg': rel_path}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500
    
if __name__ == "__main__":
    app.run()
