from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.config.config import db
from werkzeug.security import generate_password_hash

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(500))
    isAdmin = db.Column(db.Boolean, default=False) # True if user is admin, False if user is not admin

    def __init__(self, username, password, isAdmin):
        self.username = username
        self.password = generate_password_hash(password)
        self.isAdmin = isAdmin

    def format(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password,
            'isAdmin': self.isAdmin
        }
    