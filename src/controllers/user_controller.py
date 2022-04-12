from flask import Blueprint , request
from flask.json import jsonify
from flask.views import MethodView
from src.constants.http_status_codes import HTTP_200_OK,HTTP_201_CREATED, HTTP_404_NOT_FOUND , HTTP_401_UNAUTHORIZED
from src.models.user_model import User, db
from flask_jwt_extended import get_jwt_identity, jwt_required

from src.helpers.decorators import admin_required


api_user = Blueprint('user_api', __name__)


class UserAPI(MethodView):
    @admin_required()
    def get(self, id):
        if id is None:
            user = User.query.all()
            user_formated = [user.format() for user in user]
            return jsonify({
                'message': True,
                'user':user_formated
            }), HTTP_200_OK
        else:
            user = User.query.get(id)
            if user is None:
                return jsonify({
                    'message': False,
                    'error': 'User not found'
                }), HTTP_404_NOT_FOUND
            else:
                return jsonify({
                    'message': True,
                    'user': user.format()
                }), HTTP_200_OK

    def post(self):
        username = request.json['username']
        password = request.json['password']
        flag = False

        new_user = User(username=username, password=password, flag=flag)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            'message': "User created",
            'user': {
                'username': new_user.username,
                'password': new_user.password
            }
        }), HTTP_201_CREATED

    @jwt_required()
    def put(self, id):
        current_user = get_jwt_identity()
        user = User.query.get(id)
        if user is None:
            return jsonify({
                'message': False,
                'error': 'User not found'
            }), HTTP_404_NOT_FOUND
        else:
            #admin or this user can update this user
            if current_user['flag'] or current_user['id'] == user.id:
                user.username = request.json['username']
                user.password = request.json['password']
                db.session.commit()

                return jsonify({
                    'success':True,
                    'message': "User updated",
                    'user': {
                        'username': user.username,
                        'password': user.password
                    }
                })
            else:
                return jsonify({
                    'message': False,
                    'error': 'Unauthorized'
                }), HTTP_401_UNAUTHORIZED

    @jwt_required()
    def delete(self, id):
        current_user = get_jwt_identity()
        if current_user['flag'] == True:
            user = User.query.get(id)
            if user is None:
                return jsonify({
                    'message': False,
                    'error': 'User not found'
                }), HTTP_404_NOT_FOUND
            else:
                db.session.delete(user)
                db.session.commit()

                return jsonify({
                    'message': "User deleted"
                }), HTTP_200_OK
        else:
            return jsonify({
                'message': "You are not authorized to delete this user"
            }), HTTP_401_UNAUTHORIZED
        

user_view = UserAPI.as_view('user_api')
api_user.add_url_rule('/api/v1/user/register', view_func=user_view, methods=['POST'])
api_user.add_url_rule('/api/v1/user', defaults={'id':None}, view_func=user_view, methods=['GET', 'POST'])
api_user.add_url_rule('/api/v1/user/<int:id>', view_func=user_view, methods=['GET','PUT', 'DELETE'])
