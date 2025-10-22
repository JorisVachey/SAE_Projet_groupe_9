from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField , FloatField, PasswordField
from wtforms.validators import DataRequired
from .models import Client, Restauratrice
from hashlib import sha256

class RegisterForm(FlaskForm):
    numtel = StringField('Numéro de téléphone', validators=[DataRequired()])
    pseudonyme = StringField('Pseudonyme', validators=[DataRequired()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    
    def get_registered_user(self):
        user = Client.query.get(self.numtel.data)
        if user is not None:
            return None
        m = sha256()
        m.update(self.password.data.encode())
        passwd = m.hexdigest()
        newClient = Client(numtelCli=self.numtel.data, pseudonyme=self.pseudonyme.data, mdp=passwd)
        return newClient

class LoginForm(FlaskForm):
    numtel = StringField('Numéro de téléphone', validators=[DataRequired()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    
    def get_authenticated_user(self):
        user = Client.query.get(self.numtel.data)
        if not user:
            user = Restauratrice.query.filter_by(numtelRest=self.numtel.data).first()
        if not user:
            return None
        m = sha256()
        m.update(self.password.data.encode())
        passwd = m.hexdigest()
        return user if passwd == user.mdp else None
