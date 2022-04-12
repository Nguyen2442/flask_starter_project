from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.config.config import db
from src.models.part_model import Part

from sqlalchemy import event

components = db.Table('components',
    db.Column('part_id', db.Integer, db.ForeignKey('parts.id'), primary_key=True),
    db.Column('pc_id', db.Integer, db.ForeignKey('pcs.id'), primary_key=True)
)


class PC(db.Model):
    __tablename__ = 'pcs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Integer)
    components = db.relationship('Part', secondary=components, lazy='subquery',
        backref=db.backref('pcs', lazy=True, uselist=True))  
    userId_created = db.Column(db.Integer, db.ForeignKey('users.id'))
    

    def __init__(self, name, components, price, userId_created):
        self.name = name
        self.price = price
        self.userId_created = userId_created


        self.components 
        for comp in components:
            part = Part.query.get(comp)
            self.components.append(part)


    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'components': [component.format() for component in self.components],
            'price': self.price,
            'userId_created': self.userId_created
        }


# @event.listens_for(PC.price, 'set')
# def receive_set(target, value, oldvalue, initiator):
#     try:
#         for component in target.components:
#             print(component)
#             component.price += (value - oldvalue)

#     except Exception as e:
#         pass

