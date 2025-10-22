from flask import Flask
app = Flask ( __name__ )
# Config options - Make sure you created a 'config.py' file.
app.config.from_object('config')
# To get one variable, tape app.config['MY_VARIABLE']
# Create database connection object
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
db.init_app(app)
from flask_bootstrap5 import Bootstrap
Bootstrap(app)
from flask_login import LoginManager
login_manager = LoginManager(app)
login_manager.login_view = "login"
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from monApp.modeles.base import Base

def ouvrir_connexion(user,passwd,host,database):
    """
    ouverture d'une connexion MySQL
    paramètres:
       user     (str) le login MySQL de l'utilsateur
       passwd   (str) le mot de passe MySQL de l'utilisateur
       host     (str) le nom ou l'adresse IP de la machine hébergeant le serveur MySQL
       database (str) le nom de la base de données à utiliser
    résultat: l'objet qui gère le connection MySQL si tout s'est bien passé
    """
    try:
        #creation de l'objet gérant les interactions avec le serveur de BD
        engine=sqlalchemy.create_engine('mysql://'+user+':'+passwd+'@'+host+'/'+database)
        #creation de la connexion
        cnx = engine.connect()
    except Exception as err:
        print(err)
        raise err
    print("connexion réussie")
    return engine

def loaddb(engine):
    """va permettere d'ajouter des elements

    Args:
        engine (_type_): _description_
    """
    session = Session(engine)
    session.commit()

if __name__ == '__main__':
	engine=ouvrir_connexion('audor','audor','localhost','DBaudor')
	loaddb(engine)