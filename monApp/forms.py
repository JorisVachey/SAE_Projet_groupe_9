from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField , FloatField , PasswordField
from wtforms.validators import DataRequired
from .models import *
from hashlib import sha256

class clientForm(FlaskForm):
    numtelCli = StringField('Numéro de téléphone', validators=[DataRequired()])
    pseudonyme = StringField('Pseudonyme', validators=[DataRequired()])
    mdp = PasswordField('Mot de passe', validators=[DataRequired()])
    
    def get_authenticated_user(self):
        user = Client.query.get(self.numtelCli.data)
        if user is None:
            return None
        m = sha256()
        m.update(self.mdp.data.encode())
        passwd = m.hexdigest()
        return user if passwd == user.mdp else None
