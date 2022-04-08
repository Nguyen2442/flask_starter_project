from flask_sqlalchemy import SQLAlchemy
from src.config import database
from flask_migrate import Migrate
import os

db = SQLAlchemy()


def setup_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = database.DATABASE_CONNECTION_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
    
    db.app = app
    db.init_app(app)

    migrate = Migrate(app, db)

    return db
