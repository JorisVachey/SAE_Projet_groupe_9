import random, string, os
import mariadb
#>>>"".join([random.choice(string.printable) for _ in os.urandom(24) ] )
from dotenv import load_dotenv
load_dotenv()
user = os.getenv("DB_USER") 
password = os.getenv("DB_PASSWORD") 
host = os.getenv("DB_HOST") 
database = os.getenv("DB_NAME")

SECRET_KEY = "2lzUl{$*D6#`8uXqlU."
ABOUT = "Bienvenue sur la page à propos de Flask !"
CONTACT = "page de contact"
BOOTSTRAP_SERVE_LOCAL = True
#basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = f"mariadb+mariadbconnector://{user}:{password}@{host}/{database}"