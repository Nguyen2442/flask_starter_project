from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.config.config import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))
    flag = db.Column(db.Boolean, default=False) # True if user is admin, False if user is not admin

    def __init__(self, username, password, flag):
        self.username = username
        self.password = password
        self.flag = flag

    def format(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password,
            'flag': self.flag
        }
    