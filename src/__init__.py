from calendar import c
from distutils.command.config import config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from src.register_blueprint import register_blueprint
import os 
from src.config import config
from src.models.pc_model import db



def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_CONNECTION_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    register_blueprint(app)
    
    return app
