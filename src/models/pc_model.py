from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.config.config import db
from src.models.part_model import Part

components = db.Table('components',
    db.Column('part_id', db.Integer, db.ForeignKey('parts.id'), primary_key=True),
    db.Column('pc_id', db.Integer, db.ForeignKey('pcs.id'), primary_key=True)
)


class PC(db.Model):
    __tablename__ = 'pcs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    component = db.relationship('Components', secondary=components, lazy='subquery',
        backref=db.backref('pcs', lazy=True))
        
    price = db.Column(db.Integer)

    def __init__(self, name,price, component):
        self.name = name
        self.component = component
        self.price = price

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'component': [component.format() for component in self.component],
            'price': self.price
        }