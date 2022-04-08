from os import access
from src.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED
from src.models.user_model import User, db
from flask import Blueprint, request
from flask.json import  jsonify
from flask_jwt_extended import get_jwt_identity , create_access_token, create_refresh_token
from flask.views import MethodView

api_auth = Blueprint('auth_api', __name__)

class AuthAPI(MethodView):
    def post(self):
        username = request.json['username']
        password = request.json['password']

        user = User.query.filter_by(username=username, password=password).first()

        access = create_access_token(identity={'username': user.username, 'id': user.id, 'flag': user.flag})
        refresh = create_refresh_token(identity={'username': user.username, 'id': user.id, 'flag': user.flag})

        if not user:
            return jsonify({
                'message': 'Invalid credentials'
            }), HTTP_200_OK
        else:
            return jsonify({
                'message': 'Logged in successfully',
                'access_token' : access,
            'refresh_token' : refresh
            }), HTTP_201_CREATED



auth_view = AuthAPI.as_view('auth_api')
api_auth.add_url_rule('/api/v1/auth', view_func=auth_view, methods=['POST'])
        


        


    
    
