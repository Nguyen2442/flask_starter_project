from flask import Blueprint
from src.controllers.pc_controller import api_pc

def register_blueprint(app):
    app.register_blueprint(api_pc)