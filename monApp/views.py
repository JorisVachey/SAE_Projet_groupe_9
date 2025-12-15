from hashlib import sha256
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

@app.route('/connection/', methods=("GET","POST"))
def connection() :
    from .forms import LoginForm
    connection_form = LoginForm()
    unUser = None
    next_page = request.form.get('next') or request.args.get('next')
    if connection_form.validate_on_submit():
        unUser = connection_form.get_authenticated_user()
        if unUser:
            login_user(unUser)
            if unUser.est_admin:
                return redirect(url_for('admin'))
            else:
                if next_page == "menu":
                    return redirect(url_for(next_page))
                else:
                    return redirect(url_for('index'))
    return render_template("connection.html", form=connection_form, next_page=next_page)

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

@login_required
@app.route('/panier/')
def voir_panier():
    idU = current_user.idUser
    panier = get_or_create_panier(idU)
    plats = ContenirP.query.filter_by(idR=panier.idR).all()
    formules = ContenirF.query.filter_by(idR=panier.idR).all()
    return render_template("panier.html",user=current_user, panier=panier, plats=plats, formules=formules, prix_total=panier.get_total())


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
    qte_actuelle = item.quantiteP if item else 0
    if qte_actuelle + 1 > plat.stock:
        flash(f"Plus de stock disponible pour {plat.nomP}", "error")
        return redirect(url_for("menu"))

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
    """
    reservation = get_or_create_panier(current_user.idUser)
    formule = Formule.query.get(idF)
    if not formule:
        flash("Cette formule n’existe pas.", "error")
        return redirect(url_for("menu"))
    
    item = ContenirF.query.filter_by(idR=reservation.idR, idF=idF).first()
    qte_formule_future = (item.quantiteF + 1) if item else 1
    
    for c in formule.plats:
        plat = Plat.query.get(c.idP)
        if plat.stock < c.quantiteC * qte_formule_future:
            flash(f"Pas assez de stock pour le plat {plat.nomP} dans cette formule.", "error")
            return redirect(url_for("menu"))

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
        if nouvelle_quantite > plat.stock or nouvelle_quantite > plat.stockInit * variableChoixCom:
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
@app.route("/modifier_quantite_formule/<int:idF>/<action>", methods=["POST"])
def modifier_quantite_formule(idF, action):
    """commande pour interagir avec les bouton + et - du panier
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
            qte_totale = nouvelle_quantite * c.quantiteC
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
        else:
            reservation.nb_couverts += 1


    elif action == "diminuer":
        reservation = Reservation.query.get(idR)
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
    idR = data.get("idR")
    sur_place = data.get("sur_place")

    resa = Reservation.query.filter_by(idR=idR, idUser=current_user.idUser).first()
    if not resa:
        return jsonify({"error": "Réservation introuvable"}), 404

    for cp in ContenirP.query.filter_by(idR=idR).all():
        cp.quantiteP = 1

    for cf in ContenirF.query.filter_by(idR=idR).all():
        cf.quantiteF = 1
    success = False
    message = ""

    if sur_place:
        places_prises = nb_couvert_jour(resa.dateR)
        places_restantes = 12 - places_prises
        if places_prises + resa.nb_couverts <= 12:
            resa.sur_place = True
            message = "Réservation mise à jour : sur place"
            success = True
        elif places_restantes > 0:
            resa.nb_couverts = places_restantes
            resa.sur_place = True
            message = f"Réservation ajustée à {places_restantes} couverts (capacité max atteinte)."
            success = True
        else:
            resa.sur_place = False
            message = "Impossible de réserver sur place : complet (limite de 12 couverts)."
            success = False

    else:
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


@app.route("/panier/valider", methods=["POST"])
@login_required
def valider_panier():
    """change le status de la reservation ,quand un utilisateur a fini de construire son panier

    Returns:
        _type_: _description_
    """
    panier = Reservation.query.filter_by(idUser=current_user.idUser, statut="en attente").first()
    panier.statut = "confirmée"
    db.session.commit()
    flash("Réservation validée !", "success")
    return redirect(url_for("mes_reservations"))

@app.route("/panier/annuler", methods=["POST"])
@login_required
def supprimer_panier():
    """supprime le panier

    Returns:
        _type_: _description_
    """
    panier = Reservation.query.filter_by(idUser=current_user.idUser, statut="en attente").first()
    db.session.delete(panier)
    db.session.commit()
    flash("Réservation annulée !", "success")
    return redirect(url_for("menu"))

@login_required
@app.route('/mesreservation/')
def mes_reservations() :
    reservations = Reservation.query.filter_by(idUser=current_user.idUser).order_by(Reservation.dateR.desc()).all()
    return render_template("reservation.html", user=current_user, reservations=reservations)


@app.route('/admin/')
@admin_required
def admin():
    return render_template("admin.html")

from flask import request, redirect, url_for, render_template, jsonify
from .models import db, Plat, Type_plat

@app.route('/admin/gestion_plats/', methods=['GET', 'POST'])
@admin_required
def gestion_plats():

    if request.method == 'POST':
        try:
            nom_plat = request.form.get('nomP')
            type_plat_id = request.form.get('idTp')
            prix_plat = request.form.get('prixP')
            stock = request.form.get("stock")
            desc= request.form.get("desc")

            if not nom_plat or not prix_plat or not type_plat_id or not stock or not desc:
                return jsonify({'success': False, 'error': 'Champs manquants'}), 400
            
            plat_existant = Plat.query.filter_by(nomP=nom_plat).first()
            if plat_existant:
                return jsonify({'success': False, 'error': 'Un plat avec ce nom existe déjà.'}), 400

            try:
                prix_decimal = float(prix_plat)
                type_id_int = int(type_plat_id)
                stock_int = int(stock)
            except ValueError:
                return jsonify({'success': False, 'error': 'Format de prix ou ID invalide'}), 400

            nouveau_plat = Plat(
                nomP=nom_plat,
                idTp=type_id_int,
                prixP=prix_decimal,
                stock=stock_int,
                cheminImg="",
                descriptionP=desc
            )

            db.session.add(nouveau_plat)
            db.session.commit()
            
            type_associe = Type_plat.query.get(type_id_int)
            type_nom = type_associe.nomTp if type_associe else 'Inconnu'

            return jsonify({
                'success': True,
                'plat': {
                    'id': nouveau_plat.idP,
                    'nomP': nouveau_plat.nomP,
                    'prixP': nouveau_plat.prixP,
                    'type_nom': type_nom,
                    'stock': nouveau_plat.stock,
                    'stockInit': nouveau_plat.stockInit
                }
            })

        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'error': str(e)}), 500

    plats = Plat.query.all()
    types = Type_plat.query.all()
    return render_template("gestion_plat.html", plats=plats, types=types)

@app.route('/admin/gestion_formules/')
@admin_required
def gestion_formules():
    return "page de gestion des formules"

@app.route('/admin/gestion_cli/')
@admin_required
def gestion_cli():
    clients = User.query.filter_by(est_admin=False).all()
    return render_template("admin_gestion-client.html", clients=clients)

@app.route('/admin/bannir-cli/<int:client_id>')
@admin_required
def bannir_cli(client_id):
    client = User.query.filter_by(idUser=client_id).first()
    client.bannir()
    return redirect(url_for('gestion_cli'))
    
@app.route('/admin/debannir-cli/<int:client_id>')
@admin_required
def debannir_cli(client_id):
    client = User.query.filter_by(idUser=client_id).first()
    client.debannir()
    return redirect(url_for('gestion_cli'))

@app.route('/admin/voir_comm/')
@admin_required
def voir_comm():
    commandes = Reservation.query.all()
    return render_template("commandes.html", commandes=commandes)


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
    from sqlite3 import IntegrityError
    nouveau_numtel = request.form.get('numtel')

    if not nouveau_numtel:
        flash("Veuillez entrer un numéro de téléphone.", "warning")
        return redirect(url_for('gestion_compte'))

    utilisateur_existant = User.query.filter_by(numtelUser=nouveau_numtel).first()

    # Vérifie si le numéro de téléphone est déjà utilisé
    if utilisateur_existant and utilisateur_existant.idUser != current_user.idUser:
        flash("Ce numéro de téléphone est déjà utilisé.", "danger")
        return redirect(url_for('gestion_compte'))

    try:
        current_user.numtelUser = nouveau_numtel
        db.session.commit()
        flash("Numéro de téléphone mis à jour avec succès.", "success")
    except IntegrityError:
        db.session.rollback()
        flash("Erreur : ce numéro existe déjà ou la mise à jour a échoué.", "danger")

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
        return redirect(url_for('gestion_compte'))

    # Hachage du nouveau mot de passe
    hash_nouveau = sha256(nouveau_mdp.encode('utf-8')).hexdigest()
    current_user.mdp = hash_nouveau
    db.session.commit()

    flash('Mot de passe mis à jour avec succès.', 'success')
    return redirect(url_for('gestion_compte'))

@app.route('/supprimer-plat/<string:nom_plat>', methods=['DELETE'])
@admin_required
def supprimer_plat(nom_plat): 
    try:
        plat_a_supprimer = Plat.query.filter_by(nomP=nom_plat).first()

        if plat_a_supprimer:
            db.session.delete(plat_a_supprimer)
            db.session.commit()
            
            return jsonify({'success': True}), 200
        else:
            return jsonify({'success': False, 'error': 'Plat introuvable'}), 404

    except Exception as e:
        db.session.rollback()
        print(f"Erreur lors de la suppression : {e}") 
        return jsonify({'success': False, 'error': 'Erreur interne du serveur.'}), 500
    
if __name__== "__main__" :
    app.run()
