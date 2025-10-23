from .app import app, db
from .models import *
import yaml
from flask.cli import with_appcontext
import click
from datetime import datetime

@click.command("loaddb")
@click.option("--file", default="data.yaml", help="Chemin du fichier YAML à charger")
@with_appcontext
def loaddb(file):
    """Charge les données initiales depuis data.yaml dans la base."""
    try:
        with open(file, 'r') as f:
            data = yaml.safe_load(f)
    except FileNotFoundError:
        click.echo("Le fichier data.yaml est introuvable.")
        return

    click.echo("Insertion des restauratrices...")
    for r in data.get("restauratrices", []):
        rest = Restauratrice(
            idRest=r["idRest"],
            nomRest=r["nomRest"],
            prenomRest=r["prenomRest"],
            numtelRest=r["numtelRest"],
            mdp=r["mdp"]
        )
        db.session.add(rest)

    click.echo("Insertion des clients...")
    for c in data.get("clients", []):
        cli = Client(
            numtelCli=c["numtelCli"],
            pseudonyme=c["pseudonyme"],
            mdp=c["mdp"],
            est_banni=c["est_banni"],
            pts_fidelite=c["pts_fidelite"]
        )
        db.session.add(cli)

    click.echo("Insertion des plats...")
    for p in data.get("plats", []):
        plat = Plat(
            idP=p["idP"],
            nomP=p["nomP"],
            typeP=p["typeP"],
            prixP=p["prixP"],
            stock=p["stock"],
            stockInit=p["stockInit"],
            descriptionP=p["descriptionP"],
            cheminImg=p["cheminImg"]
        )
        db.session.add(plat)

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

    click.echo("Insertion des réservations...")
    for r in data.get("reservations", []):
        date_r = datetime.strptime(r["dateR"], "%Y-%m-%d").date()
        resa = Reservation(
            idR=r["idR"],
            numtelCli=r["numtelCli"],
            dateR=date_r,
            nb_couverts=r["nb_couverts"],
            sur_place=r["sur_place"],
            statut=r["statut"]
        )
        db.session.add(resa)

    db.session.commit()

    click.echo("Insertion des formules dans les réservations...")
    for cf in data.get("contenir_f", []):
        containF = ContenirF(
            idR=cf["idR"],
            idF=cf["idF"],
            quantiteF=cf["quantiteF"]
        )
        db.session.add(containF)

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

#app.cli.add_command(loaddb)
