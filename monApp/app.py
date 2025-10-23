from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap5 import Bootstrap
#from flask_login import LoginManager
app=Flask(__name__)
# mise en place de la configuration avec config.py
app.config.from_object('config')
# Creation de la base pour le moment pas initialiser
db = SQLAlchemy()
db.init_app(app)
# initialisation du module Bootstrap
Bootstrap(app)