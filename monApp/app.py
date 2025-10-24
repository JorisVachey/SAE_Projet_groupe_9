from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap5 import Bootstrap
from flask_mail import Mail,Message
#from flask_login import LoginManager
app=Flask(__name__)
# mise en place de la configuration avec config.py
app.config.from_object('config')
# Creation de la base pour le moment pas initialiser
db = SQLAlchemy()
db.init_app(app)
# initialisation du module Bootstrap
Bootstrap(app)
#initialisation mail
mail = Mail(app)


from flask_login import LoginManager
from monApp.models import Client, Restauratrice

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    if user_id.startswith("client-"):
        numtel = user_id.split("-", 1)[1]
        return Client.query.get(numtel)
    elif user_id.startswith("resto-"):
        id_restauratrice = user_id.split("-", 1)[1]
        return Restauratrice.query.get(id_restauratrice)
    return None