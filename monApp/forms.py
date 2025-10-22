from flask_wtf import FlaskForm
from wtforms import Form, StringField
# from .models import Client, Restauratrice

class RegisterForm(FlaskForm):
    numtel = StringField('Numéro de téléphone')
    pseudonyme = StringField('Pseudonyme')
    password = StringField('Mot de passe')

class LoginForm(FlaskForm):
    numtel = StringField('Numéro de téléphone')
    password = StringField('Mot de passe')
    