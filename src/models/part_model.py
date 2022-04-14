from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.config.config import db

from sqlalchemy import event


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
            'isUsed': self.isUsed,
        }

#update the price of pc builds while price of part changed
@event.listens_for(Part.price, 'set')
def receive_set(target, value, oldvalue, initiator):
    from src.models.pc_model import PC
    
    if type(value) != int or type(oldvalue) != int: #fix: value or oldvalue is symbol
        value = 0
        oldvalue = 0
    else:
        new_value = value - oldvalue
        all_pc_value = PC.query.all()
        for pc in all_pc_value:
            pc.price += new_value




    
