
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.config.config import db

class Part(db.Model):
    __tablename__= 'parts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    type = db.Column(db.String(100))
    price = db.Column(db.Integer)
    
    def __init__(self, name, type, price):
        self.name = name
        self.type = type
        self.price = price
    
    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'price': self.price
        }
