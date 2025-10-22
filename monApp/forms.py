from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField , FloatField, PasswordField
from wtforms.validators import DataRequired
from .models import Client, Restauratrice
from hashlib import sha256

class RegisterForm(FlaskForm):
    numtel = StringField('Numéro de téléphone', validators=[DataRequired()])
    pseudonyme = StringField('Pseudonyme', validators=[DataRequired()])
    password = StringField('Mot de passe', validators=[DataRequired()])
    
    def get_registered_user(self):
        user = Client.query.get(self.numtel.data)
        if user is not None:
            return None
        m = sha256()
        m.update(self.mdp.data.encode())
        passwd = m.hexdigest()
        newClient = Client(numtel=self.numtel.data, pseudonyme=pseudonyme, mdp=passwd)
        return newClient

class LoginForm(FlaskForm):
    numtel = StringField('Numéro de téléphone', validators=[DataRequired()])
    password = StringField('Mot de passe', validators=[DataRequired()])
    
    def get_authenticated_user(self):
        user = Client.query.get(self.numtelCli.data) or Restauratrice.query.get(self.numtelRest.data)
        if not user:
            return None
        m = sha256()
        m.update(self.password.data.encode())
        passwd = m.hexdigest()
        return user if passwd == user.mdp else None
