from .app import app
# from config import ABOUT,CONTACT
from flask import render_template,request,redirect,url_for
# from flask_login import logout_user,login_user,login_required
# from monApp.forms import *
@app.route('/')
@app.route('/index/')
def index():
    if len(request.args)==0:
        return render_template("index.html",name="")
    else :
        param_name = request.args.get('name')
        return render_template("index.html",name=param_name)