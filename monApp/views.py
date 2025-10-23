from .app import app
from flask import render_template
from monApp.models import db,Client


@app.route('/')
@app.route('/index/')
def index() :
    return render_template("index.html", name="Cricri")

@app.route('/propos/')
def propos() :
    return "page a propos"

@app.route('/menu/')
def menu() :
    return "page menu"

@app.route('/contact/')
def contact() :
    return "page contact"

@app.route('/nouvautes/')
def nouvautes() :
    return "page nouvautes"

@app.route('/connection/')
def connection() :
    return "page connection"

@app.route('/inscritpion/')
def inscritpion() :
    return "page inscritpion"
    
if __name__== "__main__" :
    app.run()