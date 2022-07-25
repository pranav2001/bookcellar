from flask import Flask
from wtforms.validators import Email
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY']='334bfc0d25abe431c88e6a1692f44857'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'


db=SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager=LoginManager(app)
login_manager.login_view='login'
login_manager.login_message_category='info'
from bookcellar_pkg import routes
