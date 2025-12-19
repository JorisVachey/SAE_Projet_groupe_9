from .app import app, db
from .models import *
import yaml
from flask.cli import with_appcontext
import click, logging as lg
from datetime import datetime
from hashlib import sha256

# fonction utilitaire
def create_user(num_tel, pseudonyme, mdp, admin, est_bannie,pts_fidelite):
    """
    Créer un nouvel utilisateur
    
    Args:
        num_tel (str): numéro de téléphone de l'utilisateur
        pseudonyme (str): pseudo de l'utilisateur
        mdp (str): mot de passe de l'utilisateur
        admin (bool): True si l'utilisateur est administrateur, False sinon
        est_bannie (bool): True si l'utilisateur est bannie, False sinon
        pts_fidelite (int): les points de fidelite de l'utilisateur

    Returns:
        User: l'utilisateur crée
    """
    m = sha256()
    m.update(mdp.encode())
    unUser = User(num_tel, pseudonyme,m.hexdigest() , admin, est_bannie,pts_fidelite)
    db.session.add(unUser)
    db.session.commit()
    return unUser 

# partie commands flask
@click.command("loaddb")
@click.option("--file", default="monApp/data/data.yaml", help="Chemin du fichier YAML à charger")
@with_appcontext
def loaddb(file):
    """Charge les données initiales depuis data.yaml dans la base."""
    try:
        with open(file, 'r') as f:
            data = yaml.safe_load(f)
    except FileNotFoundError:
        click.echo("Le fichier data.yaml est introuvable.")
        return

    for key in ["users", "type_plats", "plats", "restrictions",
                "contenir_R", "formules", "composer",
                "reservations", "contenir_f", "contenir_p"]:
        if data.get(key) is None:
            data[key] = []

    click.echo("Insertion des utilisateurs...")
    for u in data.get("users", []):
        create_user(
            u["numtelUser"],
            u["pseudonyme"],
            u["mdp"],
            u["est_banni"],
            u.get("pts_fidelite", 0),
            u.get("est_admin", False)
        )

    click.echo("Insertion des types de plats...")
    for t in data.get("type_plats", []):
        type_plat = Type_plat(
            idTp=t["idTp"],
            nomTp=t["nomTp"],
            descriptionTp=t["descriptionTp"],
            cheminImg=t["cheminImg"]
        )
        db.session.add(type_plat)
    db.session.commit()

    click.echo("Insertion des plats...")
    for p in data.get("plats", []):
        plat = Plat(
            nomP=p["nomP"],
            idTp=p["idTp"],
            prixP=p["prixP"],
            stock=p["stock"],
            descriptionP=p["descriptionP"],
            cheminImg=p["cheminImg"]
        )
        db.session.add(plat)

    click.echo("Insertion des restrictions...")
    for r in data.get("restrictions", []):
        restriction = Restriction(
            nomA=r["nomA"]
        )
        db.session.add(restriction)
    db.session.commit()

    click.echo("Insertion des associations plat <-> restrictions...")
    for ca in data.get("contenir_R", []):
        contenir_a = ContenirR(
            idP=ca["idP"],
            nomA=ca["nomA"]
        )
        db.session.add(contenir_a)
    db.session.commit()

    click.echo("Insertion des formules...")
    for f in data.get("formules", []):
        form = Formule(
            idF=f["idF"],
            nomF=f["nomF"],
            prixF=f["prixF"],
            cheminImg=f.get("cheminImg", "img/base/image_defaut.png")
        )
        db.session.add(form)

    db.session.commit()  #on fait un commit pour eviter les erreurs de clé etrangere

    click.echo("Insertion des compositions de formules...")
    for c in data.get("composer", []):
        comp = Composer(
            idF=c["idF"],
            idP=c["idP"],
            quantiteC=c["quantiteC"]
        )
        db.session.add(comp)

    db.session.commit()

    click.echo("Insertion des réservations...")
    for r in data.get("reservations", []):
        date_r = datetime.strptime(r["dateR"], "%Y-%m-%d").date()
        resa = Reservation(
            idUser=r["idUser"],
            dateR=date_r,
            nb_couverts=r["nb_couverts"],
            sur_place=r["sur_place"],
            statut=r["statut"]
        )
        db.session.add(resa)

    db.session.commit()

    print("Insertion des formules dans les réservations...")
    for cf in data['contenir_f']:
        contenir_f = ContenirF(
            idR=cf['idR'],
            idF=cf['idF'],
            quantiteF=cf['quantiteF']
        )
        db.session.add(contenir_f)
        db.session.flush()  # Important pour MariaDB
    db.session.commit()

    click.echo("Insertion des plats dans les réservations...")
    for cp in data.get("contenir_p", []):
        containP = ContenirP(
            idR=cp["idR"],
            idP=cp["idP"],
            quantiteP=cp["quantiteP"]
        )
        db.session.add(containP)

    db.session.commit()

    click.echo("Base de données remplie avec succès !")

app.cli.add_command(loaddb)

@app.cli.command()
@click.argument('num_tel')
@click.argument('pseudonyme')
@click.argument('pwd')
@click.option("--admin", default=False, help="l'utilisateur est administrateur")
@click.option("--est_bannie", default=False, help="Creer un nouvel utilisateur bannie")
def newuser(num_tel, pseudonyme, pwd, admin, est_bannie,pts_fidelite):
    """Créer un nouvel utilisateur via CLI"""
    create_user(num_tel, pseudonyme, pwd, admin, est_bannie,pts_fidelite)
    lg.warning('User ' + num_tel + ' created!')

app.cli.add_command(newuser)




