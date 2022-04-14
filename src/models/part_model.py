from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.config.config import db

from sqlalchemy import event
import logging



class Part(db.Model):
    __tablename__= 'parts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    type = db.Column(db.String(100))
    price = db.Column(db.Integer, default=0)
    isUsed = db.Column(db.Boolean, default=False)
    
    def __init__(self, name, type, price, isUsed):
        self.name = name
        self.type = type
        self.price = price
        self.isUsed = isUsed
    
    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'price': self.price,
            'isUsed': self.isUsed
        }



# @event.listens_for(Part.price, 'set')
# def receive_set(target, value, oldvalue, initiator):
#     new_value = value - oldvalue
#     for pc in target.pcs:
#         pc.price += new_value
    




    
