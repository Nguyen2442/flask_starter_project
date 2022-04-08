from flask import Blueprint , request
from flask.json import jsonify
from flask.views import MethodView
from src.constants.http_status_codes import HTTP_200_OK,HTTP_201_CREATED
from src.models.user_model import User, db


api_user = Blueprint('user_api', __name__)


class UserAPI(MethodView):
    def get(self, id):
        if id is None:
            user = User.query.all()
            user_formated = [user.format() for user in user]
            return jsonify({
                'message': True,
                'user':user_formated
            })
        else:
            user = User.query.get(id)
            return jsonify({
                'message': True,
                'user': user.format()
            })

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

    def put(self, id):
        user = User.query.get(id)
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

    def delete(self, id):
        user = User.query.get(id)
        db.session.delete(user)
        db.session.commit()

        return jsonify({
            'message': "User deleted"
        })

user_view = UserAPI.as_view('user_api')
api_user.add_url_rule('/api/v1/user/register', view_func=user_view, methods=['POST'])
api_user.add_url_rule('/api/v1/user', defaults={'id':None}, view_func=user_view, methods=['GET', 'POST'])
api_user.add_url_rule('/api/v1/user/<int:id>', view_func=user_view, methods=['GET','PUT', 'DELETE'])
