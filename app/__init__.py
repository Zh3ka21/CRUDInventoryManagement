from flask import Flask
from pymongo import MongoClient
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

client = MongoClient('mongodb://localhost:27017/')
db = client.im

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
csrf = CSRFProtect(app)

bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login_view'

from . import routes