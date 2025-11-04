from .app import app, db
from .models import *
import yaml
from flask.cli import with_appcontext
import click
from datetime import datetime
from hashlib import sha256

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

    click.echo("Insertion des utilisateurs...")
    for u in data.get("users", []):
        user = User(
            idUser=u["idUser"],
            numtelUser=u["numtelUser"],
            pseudonyme=u["pseudonyme"],
            mdp=u["mdp"],
            est_banni=u["est_banni"],
            pts_fidelite=u.get("pts_fidelite", 0),
            est_admin=u.get("est_admin", False)
        )
        db.session.add(user)
    db.session.commit()


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
            idP=p["idP"],
            nomP=p["nomP"],
            idTp=p["idTp"],
            prixP=p["prixP"],
            stock=p["stock"],
            stockInit=p["stockInit"],
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
            prixF=f["prixF"]
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
            idR=r["idR"],
            numtelUser=r["numtelUser"],
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
