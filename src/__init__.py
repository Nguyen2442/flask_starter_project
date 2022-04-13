from calendar import c
from distutils.command.config import config
from flask import Flask
from src.register_blueprint import register_blueprint
from src.config.config import setup_db
from flask_jwt_extended import JWTManager
import os




def create_app():
    app = Flask(__name__)
    

    setup_db(app)

    register_blueprint(app)

    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    
    JWTManager(app)
    
    return app
