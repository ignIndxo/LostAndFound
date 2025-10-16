from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os

app = Flask(__name__) # so Flask knows where to look for templates and static files

#with app.app_context():
file_path = os.path.abspath(os.getcwd())+"\site.db"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+file_path

app.config['SECRET_KEY'] = '0ebb980f435eef6cfaa76b5aebbff95d'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app) # for hashing passwords
login_manager = LoginManager(app)

from flaskapp import routes

# Need a secret key to protect against modifying cookies and cross site request forgery attacks
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dbdir/site.db'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'