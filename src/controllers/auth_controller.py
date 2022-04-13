import datetime
from src.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from src.models.user_model import User, db
from flask import Blueprint, request
from flask.json import  jsonify
from flask_jwt_extended import jwt_required , get_jwt_identity , create_access_token, create_refresh_token
from flask.views import MethodView
from werkzeug.security import check_password_hash

api_auth = Blueprint('auth_api', __name__)

class AuthAPI(MethodView):
    def post(self):
        username = request.json['username']
        password = request.json['password']


        user = User.query.filter_by(username=username).first()
        if user is None:
            return jsonify({
                'message': 'User not found'
            }), HTTP_400_BAD_REQUEST
            
        else:
            is_password_correct = check_password_hash(user.password, password)
            if is_password_correct:

                expires = datetime.timedelta(days=1)
                access = create_access_token(identity={'username': user.username, 'id': user.id, 'isAdmin': user.isAdmin}, expires_delta=expires)
                refresh = create_refresh_token(identity={'username': user.username, 'id': user.id, 'isAdmin': user.isAdmin})

                return jsonify({
                    'message': 'Logged in successfully',
                    'access_token' : access,
                'refresh_token' : refresh
                }), HTTP_201_CREATED
            else:
                return jsonify({
                    'message': 'Wrong password'
                }), HTTP_400_BAD_REQUEST
            

    #refresh token is used to get a new access token
    @jwt_required(refresh=True)
    def get(self):
        identity = get_jwt_identity()
        expires = datetime.timedelta(days=1)
        access = create_access_token(identity={'username': identity['username'], 'id': identity['id'], 'isAdmin': identity['isAdmin']}, expires_delta=expires)

        return jsonify({
            'message': True,
            'access_token': access
        }), HTTP_200_OK


auth_view = AuthAPI.as_view('auth_api')
api_auth.add_url_rule('/api/v1/auth', view_func=auth_view, methods=['POST', 'GET'])
        


        


    
    
