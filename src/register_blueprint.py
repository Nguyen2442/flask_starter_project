from src.controllers.pc_controller import api_pc
from src.controllers.user_controller import api_user
from src.controllers.auth_controller import api_auth
from src.controllers.part_controller import api_part

def register_blueprint(app):
    app.register_blueprint(api_pc)
    app.register_blueprint(api_user)
    app.register_blueprint(api_auth)
    app.register_blueprint(api_part)
    