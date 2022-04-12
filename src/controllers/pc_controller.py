from operator import and_
from flask import Blueprint , request
from flask.json import jsonify
from flask.views import MethodView
from src.constants.http_status_codes import HTTP_200_OK,HTTP_201_CREATED , HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND
from src.models.pc_model import PC, db, components 
from src.models.part_model import Part

from flask_jwt_extended import get_jwt_identity, jwt_required



api_pc = Blueprint('pc_api', __name__)


class PcAPI(MethodView):
    @jwt_required()
    
    def get(self, id):
        current_user = get_jwt_identity()
        
        if id is None:
            args = request.args
            name = args.get('name')

            if name is None:
                pc = PC.query.filter_by(userId_created=current_user['id']).all()
                pc_formated = [pc.format() for pc in pc]
                return jsonify({
                    'message': True,
                    'pc': pc_formated
                }), HTTP_200_OK
            else:
                pc = PC.query.filter(
                    PC.userId_created == current_user['id'],
                    PC.name == name
                )
                pc_formated = [pc.format() for pc in pc]
                return jsonify({
                    'message': True,
                    'pc': pc_formated
                }), HTTP_200_OK
        else:
            pc = PC.query.get(id)
            if pc is None:
                return jsonify({
                    'message': False,
                    'error': 'Pc not found'
                }),HTTP_404_NOT_FOUND

            else:
                return jsonify({
                    'message': True,
                    'pc': pc.format()
                }), HTTP_200_OK



    @jwt_required()
    def post(self):
        name = request.json['name']
        components = request.json['components']
        
        current_user = get_jwt_identity()
        userId_created = current_user['id']

        #sum of price of list of part
        price = 0
        for comp in components:
            comp_all_values = Part.query.filter_by(id=comp).first()
            price = price + comp_all_values.price


        #show name of list component in response
        list_component_name = []
        for item in components:
            comp_all_values = Part.query.filter_by(id=item).first()
            list_component_name.append(comp_all_values.name)

        #set isUsed to true while part is used
        for item in components:
            comp_all_values = Part.query.filter_by(id=item).first()
            comp_all_values.isUsed = True

        new_pc = PC(name=name, components=components,  price=price, userId_created=userId_created)
        db.session.add(new_pc)
        db.session.commit()

        return jsonify({
            'message': "Pc created",
            'pc': {
                'name': new_pc.name,
                'price': new_pc.price,
                'components': list_component_name,
                'userId_created': userId_created
            }
        }), HTTP_201_CREATED

    @jwt_required()
    def put(self, id):
        current_user = get_jwt_identity()
        pc = PC.query.get(id)
        if pc is None:
            return jsonify({
                'message': False,
                'error': 'Pc not found'
            }), HTTP_404_NOT_FOUND
        else:
            if pc.userId_created == current_user['id'] or current_user['flag']==True:
                pc.name = request.json['name']
                
                
                new_components= []
                for comp in pc.components:
                    new_components.append(comp)



                ###NEW test
                #sum of price of list of part
                price = 0
                for comp in new_components:
                    comp_all_values = Part.query.filter_by(id=comp).first()
                    price = price + comp_all_values.price

                #show name of list component in response
                list_component_name = []
                for item in new_components:
                    comp_all_values = Part.query.filter_by(id=item).first()
                    list_component_name.append(comp_all_values.name)

                #set isUsed to true while part is used
                for item in new_components:
                    comp_all_values = Part.query.filter_by(id=item).first()
                    comp_all_values.isUsed = True


                # #sum of price of list of part
                # price = 0
                # for comp in components:
                #     comp_all_values = Part.query.filter_by(id=comp).first()
                #     price = price + comp_all_values.price

                # #show name of list component in response
                # list_component_name = []
                # for item in components:
                #     comp_all_values = Part.query.filter_by(id=item).first()
                #     list_component_name.append(comp_all_values.name)

                # #set isUsed to true while part is used
                # for item in components:
                #     comp_all_values = Part.query.filter_by(id=item).first()
                #     comp_all_values.isUsed = True

                db.session.commit()
            else:
                return jsonify({
                    'message': "You are not authorized to update this pc"
                }), HTTP_401_UNAUTHORIZED

        return jsonify({
            'message': "Pc updated",
            'pc': {
                'name': pc.name,
                'price': pc.price,
                'components': list_component_name,
                'userId_created': pc.userId_created
            }
        }), HTTP_200_OK

    @jwt_required()
    def delete(self, id):
        current_user = get_jwt_identity()
        if id is None:
            return jsonify({
                'message': False,
                'error': 'Pc not found'
            }), HTTP_404_NOT_FOUND
        else:
            pc = PC.query.get(id)
            if pc.userId_created == current_user['id'] or current_user['flag']==True:
                db.session.delete(pc)
                db.session.commit()

            return jsonify({
                'message': "Pc deleted"
            }), HTTP_200_OK

pc_view = PcAPI.as_view('pc_api')
api_pc.add_url_rule('/api/v1/pc', defaults={'id': None},view_func=pc_view, methods=['GET',])
api_pc.add_url_rule('/api/v1/pc' ,view_func=pc_view, methods=['POST',])
api_pc.add_url_rule('/api/v1/pc/<int:id>', view_func=pc_view, methods=['GET','PUT', 'DELETE'])


