import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail



login_manager = LoginManager()


app=Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config.from_object(Config)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///" + os.path.join(basedir,"storage.db")
app.config['SQLALCHEMY_TRACK_MODIFICATION']= False
app.config['IMAGE_UPLOAD_FOLDER'] = os.path.join(basedir,'static/Images/')

db = SQLAlchemy(app)
migrate = Migrate(app,db)
login_manager.init_app(app)
login_manager.login_view = "login"
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'xxxxxxxxx'
app.config['MAIL_PASSWORD'] = 'xxxxxxxxxxx'
mail = Mail(app)
