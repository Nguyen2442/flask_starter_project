from flask import Blueprint , request
from flask.json import jsonify
from flask.views import MethodView
from src.constants.http_status_codes import HTTP_200_OK,HTTP_201_CREATED
from src.models.pc_model import PC, db


api_pc = Blueprint('pc_api', __name__)


class PcAPI(MethodView):
    def get(self, id):
        if id is None:
            pc = PC.query.all()
            pc_formated = [pc.format() for pc in pc]
            return jsonify({
                'message': True,
                'pc':pc_formated
            })
        else:
            pc = PC.query.get(id)
            return jsonify({
                'message': True,
                'pc': pc.format()
            })


    def post(self):
        name = request.json['name']
        price = request.json['price']
        component = request.json['component']


        new_pc = PC(name=name, price=price, component=component)
        db.session.add(new_pc)
        db.session.commit()

        return jsonify({
            'message': "Pc created",
            'pc': {
                'name': new_pc.name,
                'price': new_pc.price,
                'component': new_pc.component

            }
        }), HTTP_201_CREATED

    def put(self, id):
        pc = PC.query.get(id)
        pc.name = request.json['name']
        pc.price = request.json['price']
        db.session.commit()

        return jsonify({
            'message': "Pc updated",
            'pc': {
                'name': pc.name,
                'price': pc.price
            }
        })

    def delete(self, id):
        pc = PC.query.get(id)
        db.session.delete(pc)

        return jsonify({
            'message': "Pc deleted"
        })

pc_view = PcAPI.as_view('pc_api')
api_pc.add_url_rule('/api/v1/pc', defaults={'id': None},view_func=pc_view, methods=['GET',])
api_pc.add_url_rule('/api/v1/pc' ,view_func=pc_view, methods=['POST',])
api_pc.add_url_rule('/api/v1/pc/<int:id>', view_func=pc_view, methods=['GET','PUT', 'DELETE'])


