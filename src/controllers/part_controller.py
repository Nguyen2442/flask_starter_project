from flask import Blueprint , request
from flask.json import jsonify
from flask.views import MethodView
from src.constants.http_status_codes import HTTP_200_OK,HTTP_201_CREATED , HTTP_401_UNAUTHORIZED
from src.models.part_model import Part, db

from flask_jwt_extended import get_jwt_identity, jwt_required


api_part = Blueprint('part_api', __name__)


class PartAPI(MethodView):
    def get(self , id):
        if id is None:
            args = request.args
            name = args.get('name')
            type = args.get('type')

            if name is None and type is None:
                part = Part.query.all()
                part_formated = [part.format() for part in part]
                return jsonify({
                    'message': True,
                    'part':part_formated
                })
            elif name is not None and type is None:
                part = Part.query.filter_by(name=name).first()
                return jsonify({
                    'message': True,
                    'part': part.format()
                })
            elif name is None and type is not None:
                part = Part.query.filter_by(type=type).first()
                return jsonify({
                    'message': True,
                    'part': part.format()
                })
            
        else:
            part = Part.query.get(id)
            return jsonify({
                'message': True,
                'part': part.format()
            })
    

    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()

        if current_user['flag'] == True:
            name = request.json['name']
            type = request.json['type']
            price = request.json['price']

            new_part = Part(name=name, type=type, price=price)
            db.session.add(new_part)
            db.session.commit()

            return jsonify({
                'message': "Part created",
                'part': {
                    'name': new_part.name,
                    'type': new_part.type,
                    'price': new_part.price
                }
            }), HTTP_201_CREATED

        else:
            return jsonify({
                'message': "You are not authorized to create a part"
            }), HTTP_401_UNAUTHORIZED

    @jwt_required()
    def put(self, id):
        current_user = get_jwt_identity()

        if current_user['flag'] == True:
            part = Part.query.get(id)
            part.name = request.json['name']
            part.type = request.json['type']
            part.price = request.json['price']
            db.session.commit()

            return jsonify({
                'message': "Part updated",
                'part': {
                    'name': part.name,
                    'type': part.type,
                    'price': part.price
                }
            })

        else:
            return jsonify({
                'message': "You are not authorized to update a part"
            }), HTTP_401_UNAUTHORIZED

    @jwt_required()
    def delete(self, id):
        current_user = get_jwt_identity()

        if current_user['flag'] == True:
            part = Part.query.get(id)
            db.session.delete(part)
            db.session.commit()

            return jsonify({
                'message': "Part deleted"
            })

        else:
            return jsonify({
                'message': "You are not authorized to delete a part"
            }), HTTP_401_UNAUTHORIZED


part_view = PartAPI.as_view('part_api')
api_part.add_url_rule('/api/v1/part', defaults={'id':None} ,view_func=part_view, methods=['GET',])
api_part.add_url_rule('/api/v1/part',view_func=part_view, methods=['POST',])
api_part.add_url_rule('/api/v1/part/<int:id>',view_func=part_view, methods=['GET','PUT','DELETE'])
