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


# def create_celery_app(app):

#     celery = Celery(app.import_name)

#     celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL")
#     celery.conf.result_backend = os.environ.get("CELERY_BROKER_URL")

#     class ContextTask(celery.Task):
#         def __call__(self, *args, **kwargs):
#             with app.app_context():
#                 return self.run(*args, **kwargs)

#     celery.Task = ContextTask

#     return celery
