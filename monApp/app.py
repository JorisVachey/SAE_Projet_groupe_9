from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap5 import Bootstrap
from flask_mail import Mail
from flask_apscheduler import APScheduler
from datetime import datetime
#from flask_login import LoginManager
app = Flask(__name__)
# mise en place de la configuration avec config.py
app.config.from_object('config')
# Creation de la base pour le moment pas initialiser
db = SQLAlchemy()
db.init_app(app)
# initialisation du module Bootstrap
Bootstrap(app)
#initialisation mail
mail = Mail(app)


app.config['SCHEDULER_TIMEZONE'] = "Europe/Paris"
app.config['SCHEDULER_API_ENABLED'] = True
scheduler = APScheduler()


def daily_restock():
    """Remplissage du Stock avec le stock initial tout les matins"""
    with app.app_context():
        from .models import Plat 
        db.session.query(Plat).update({Plat.stock: Plat.stockInit})
        db.session.commit()
        print(f"[{datetime.now()}] Restockage automatique effectué.")

scheduler.init_app(app)
scheduler.add_job(
    id='daily_restock',
    func=daily_restock,
    trigger='cron',
    hour=0, 
    minute=0  
)
scheduler.start()


from flask_login import LoginManager
from monApp.models import User

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
