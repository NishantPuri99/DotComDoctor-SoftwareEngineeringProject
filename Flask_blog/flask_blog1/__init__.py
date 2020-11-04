from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager # responsible for simplifying the login process

app = Flask(__name__)
app.config['SECRET_KEY'] = '6caa2c672d64ba7e2ba240bfdf6a009c'   #Use a random string of characters with secrets module. 
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from flask_blog1 import routes