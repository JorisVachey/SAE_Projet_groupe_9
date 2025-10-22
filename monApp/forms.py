from flask_wtf import FlaskForm
from wtforms import Form, StringField
from wtforms.validators import DataRequired
# from .models import Client, Restauratrice

class RegisterForm(FlaskForm):
    numtel = StringField('Numéro de téléphone', validators=[DataRequired()])
    pseudonyme = StringField('Pseudonyme', validators=[DataRequired()])
    password = StringField('Mot de passe', validators=[DataRequired()])

class LoginForm(FlaskForm):
    numtel = StringField('Numéro de téléphone', validators=[DataRequired()])
    password = StringField('Mot de passe', validators=[DataRequired()])
