from .app import app, db
import sys
from .models import (
    User,
    Type_plat,
    Plat,
    Restriction,
    ContenirR,
    Formule,
    Composer,
    Reservation,
    ContenirF,
    ContenirP,
)
import yaml
from flask.cli import with_appcontext
import click
import logging as lg
from datetime import datetime
from hashlib import sha256


# fonction utilitaire
def create_user(num_tel, pseudonyme, mdp, admin, est_bannie, pts_fidelite):
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
    un_user = User(num_tel, pseudonyme, m.hexdigest(), est_bannie, pts_fidelite,
                   admin)
    db.session.add(un_user)
    db.session.commit()
    return un_user


# partie commands flask
@click.command("loaddb")
@click.option("--file",
              default="monApp/data/data.yaml",
              help="Chemin du fichier YAML à charger")
@with_appcontext
def loaddb(file):
    """Charge les données initiales depuis data.yaml dans la base."""
    try:
        with open(file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except FileNotFoundError:
        click.echo("Le fichier data.yaml est introuvable.")
        return

    for key in [
            "users", "type_plats", "plats", "restrictions", "contenir_R",
            "formules", "composer", "reservations", "contenir_f", "contenir_p"
    ]:
        if data.get(key) is None:
            data[key] = []

    click.echo("Insertion des utilisateurs...")
    for u in data.get("users", []):
        create_user(num_tel=u["numtelUser"],
                    pseudonyme=u["pseudonyme"],
                    mdp=u["mdp"],
                    admin=u.get("est_admin", False),
                    est_bannie=u.get("est_banni", False),
                    pts_fidelite=u.get("pts_fidelite", 0))

    click.echo("Insertion des types de plats...")
    for t in data.get("type_plats", []):
        type_plat = Type_plat(idTp=t["idTp"],
                              nomTp=t["nomTp"],
                              descriptionTp=t["descriptionTp"],
                              cheminImg=t["cheminImg"])
        db.session.add(type_plat)
    db.session.commit()

    click.echo("Insertion des plats...")
    for p in data.get("plats", []):
        plat = Plat(nomP=p["nomP"],
                    idTp=p["idTp"],
                    prixP=p["prixP"],
                    stockInit=p["stockInit"],
                    descriptionP=p["descriptionP"],
                    cheminImg=p["cheminImg"])
        db.session.add(plat)

    click.echo("Insertion des restrictions...")
    for r in data.get("restrictions", []):
        restriction = Restriction(nomA=r["nomA"])
        db.session.add(restriction)
    db.session.commit()

    click.echo("Insertion des associations plat <-> restrictions...")
    for ca in data.get("contenir_R", []):
        contenir_a = ContenirR(idP=ca["idP"], nomA=ca["nomA"])
        db.session.add(contenir_a)
    db.session.commit()

    click.echo("Insertion des formules...")
    for f in data.get("formules", []):
        form = Formule(idF=f["idF"],
                       nomF=f["nomF"],
                       prixF=f["prixF"],
                       cheminImg=f.get("cheminImg",
                                       "img/base/image_defaut.png"))
        db.session.add(form)

    db.session.commit(
    )  #on fait un commit pour eviter les erreurs de clé etrangere

    click.echo("Insertion des compositions de formules...")
    for c in data.get("composer", []):
        comp = Composer(idF=c["idF"], idP=c["idP"], quantiteC=c["quantiteC"])
        db.session.add(comp)

    db.session.commit()

    click.echo("Insertion des réservations...")
    for r in data.get("reservations", []):
        date_r = datetime.strptime(r["dateR"], "%Y-%m-%d").date()
        resa = Reservation(idUser=r["idUser"],
                           dateR=date_r,
                           nb_couverts=r["nb_couverts"],
                           sur_place=r["sur_place"],
                           statut=r["statut"])
        db.session.add(resa)

    db.session.commit()

    print("Insertion des formules dans les réservations...")
    for cf in data["contenir_f"]:
        contenir_f = ContenirF(idR=cf["idR"],
                               idF=cf["idF"],
                               quantiteF=cf["quantiteF"])
        db.session.add(contenir_f)
        db.session.flush()  # Important pour MariaDB
    db.session.commit()

    click.echo("Insertion des plats dans les réservations...")
    for cp in data.get("contenir_p", []):
        contain_p = ContenirP(idR=cp["idR"],
                              idP=cp["idP"],
                              quantiteP=cp["quantiteP"])
        db.session.add(contain_p)

    db.session.commit()

    click.echo("Base de données remplie avec succès !")


app.cli.add_command(loaddb)


@app.cli.command()
@click.argument("num_tel")
@click.argument("pseudonyme")
@click.argument("pwd")
@click.option("--admin",
              is_flag=True,
              help="Définit l'utilisateur comme administrateur")
@click.option("--banni", is_flag=True, help="Définit l'utilisateur comme banni")
def newuser(num_tel, pseudonyme, pwd, admin, banni):
    """Créer un nouvel utilisateur via CLI"""
    create_user(num_tel, pseudonyme, pwd, admin, banni, 0)
    lg.warning("User %s created! (Admin: %s)", num_tel, admin)

app.cli.add_command(newuser)

@app.cli.command()
@with_appcontext
def init_db():
    """Créer toutes les tables."""
    db.create_all()
    lg.warning("Tables creer avec succès")
app.cli.add_command(init_db)

@app.cli.command()
@with_appcontext
def drop_db():
    """Supprime toutes les tables"""
    db.drop_all()
    lg.warning("Tables supprimer")
app.cli.add_command(drop_db)

@app.cli.command()
@with_appcontext
def exist_db():
    """Vérifie si les tables existe déjà"""
    existing_tables = db.inspect(db.engine).get_table_names()
    for table in db.metadata.tables.keys():
        if not(table in existing_tables):
            sys.exit(1)# il n'y a pas les tables 
    sys.exit(0)# il y a les tables 
app.cli.add_command(exist_db)