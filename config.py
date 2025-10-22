import random, string, os
#>>>"".join([random.choice(string.printable) for _ in os.urandom(24) ] )
SECRET_KEY = "2lzUl{$*D6#`8uXqlU."
ABOUT = "Bienvenue sur la page à propos de Flask !"
CONTACT = "page de contact"
BOOTSTRAP_SERVE_LOCAL = True
basedir = os.path.abspath(os.path.dirname(__file__))
#SQLALCHEMY_DATABASE_URI = 'mariadb:///' + os.path.join(basedir, 'monApp.db')