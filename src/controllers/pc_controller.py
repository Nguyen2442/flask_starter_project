from operator import and_
from flask import Blueprint , request
from flask.json import jsonify
from flask.views import MethodView
from src.constants.http_status_codes import HTTP_200_OK,HTTP_201_CREATED , HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND
from src.models.pc_model import PC, db , Component
from src.models.part_model import Part

from flask_jwt_extended import get_jwt_identity, jwt_required



api_pc = Blueprint('pc_api', __name__)


class PcAPI(MethodView):
    @jwt_required()
    def get(self, id):
        current_user = get_jwt_identity()

        #show name of list components in pc by pc_id
        # for component in Component.query.filter_by(pc_id=id).all():
        #     print(component.name)
        
        if id is None:
            args = request.args
            name = args.get('name')

            if name is None:
                if current_user['isAdmin'] == True:
                    pc = PC.query.all()
                    pc_formated = [pc.format() for pc in pc]
                    return jsonify({
                        'message': True,
                        'pc': pc_formated
                    }), HTTP_200_OK
                else:
                    pc = PC.query.filter_by(userId_created=current_user['id']).all()
                    pc_formated = [pc.format() for pc in pc]
                    return jsonify({
                        'message': True,
                        'pc': pc_formated
                    }), HTTP_200_OK

            else:
                if current_user['isAdmin'] == True:
                    pc = PC.query.filter_by(name=name).first()
                    return jsonify({
                        'message': True,
                        'pc': pc.format()
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
            if current_user['isAdmin'] == True:
                pc = PC.query.get(id)
                #get components of pc by pc_id
                components = Component.query.filter_by(pc_id=id).all()

                if pc is None:
                    return jsonify({
                        'message': False,
                        'error': 'Pc not found'
                    }),HTTP_404_NOT_FOUND

                else:
                    return jsonify({
                        'message': True,
                        'pc': pc.format(),
                        'components': [component.format() for component in components]
                    }), HTTP_200_OK
            else:
                pc = PC.query.filter(
                    PC.userId_created == current_user['id'],
                    PC.id == id
                )
                #get components of pc by pc_id
                components = Component.query.filter_by(pc_id=id).all()

                if pc is None:
                    return jsonify({
                        'message': False,
                        'error': 'Pc not found'
                    }),HTTP_404_NOT_FOUND

                else:
                    return jsonify({
                        'message': True,
                        'pc': pc.format(),
                        'components': [component.format() for component in components]
                    }), HTTP_200_OK



    @jwt_required()
    def post(self):
        name = request.json['name']
        current_user = get_jwt_identity()
        userId_created = current_user['id']
        components = request.json['components']


        #sum of price of list of part_id
        price = 0
        for comp in components:
            comp_all_values = Part.query.filter_by(id=comp['part_id']).first()
            price = price + comp_all_values.price * comp['quantity']

        #show name of list component in response
        components_name = []
        for comp in components:
            comp_all_values = Part.query.filter_by(id=comp['part_id']).first()
            components_name.append(comp_all_values.name)

        #set isUsed to true while part is used
        for comp in components:
            comp_all_values = Part.query.filter_by(id=comp['part_id']).first()
            comp_all_values.isUsed = True

        
        new_pc = PC(name=name, price=price, userId_created=userId_created)
        db.session.add(new_pc)
        db.session.flush()
        
        #Add components (part_id, quantity, pc_id) to table components
        for component in components:
            part_id = component['part_id']
            quantity = component['quantity']
            new_component = Component(part_id=part_id, quantity=quantity, pc_id=new_pc.id)
            db.session.add(new_component)

        db.session.commit()

        return jsonify({
            'message': "Pc created",
            'pc': {
                'name': new_pc.name,
                'price': new_pc.price,
                'components': components_name,
                'userId_created': userId_created
            }
        }), HTTP_201_CREATED

    #update pc
    @jwt_required()
    def put(self, id):
        current_user = get_jwt_identity()
        pc = PC.query.get(id)
        if pc is None:
            return jsonify({
                'message': False,
                'error': 'Pc not found'
            }),HTTP_404_NOT_FOUND
        else:
            if pc.userId_created != current_user['id'] or current_user['isAdmin'] == False:
                return jsonify({
                    'message': False,
                    'error': 'You are not the owner of this pc'
                }),HTTP_401_UNAUTHORIZED
            else:
                pc.name = request.json['name']
                components = request.json['components']

                Component.query.filter_by(pc_id=id).delete()

                for component in components:
                    part_id = component['part_id']
                    quantity = component['quantity']
                    new_component = Component(part_id=part_id, quantity=quantity, pc_id=id)
                    db.session.add(new_component)

                price=0
                for comp in components:
                    comp_all_values = Part.query.filter_by(id=comp['part_id']).first()
                    price = price + comp_all_values.price * comp['quantity']

                #show name of list component in response
                components_name = []
                for comp in components:
                    comp_all_values = Part.query.filter_by(id=comp['part_id']).first()
                    components_name.append(comp_all_values.name)

                db.session.commit()
                
                return jsonify({
                    'message': True,
                    'pc': {
                        'name': pc.name,
                        'price': pc.price,
                        'components': components_name,
                        'userId_created': pc.userId_created
                    }
                })

    # @jwt_required()
    # def put(self, id):
    #     current_user = get_jwt_identity()
    #     pc = PC.query.get(id)
    #     components = Component.query.filter_by(pc_id=id).all()
    #     for component in components:
    #         print("component.part_id before", component.part_id)
            
    #         db.session.delete(component.part_id)
    #         print("component.part_id after", component.part_id)
    #         component.quantity = None

    #     print(components)

    #     if pc is None:
    #         return jsonify({
    #             'message': False,
    #             'error': 'Pc not found'
    #         }), HTTP_404_NOT_FOUND
    #     else:
    #         if pc.userId_created == current_user['id'] or current_user['isAdmin']==True:
    #             pc.name = request.json['name']
    #             #update components 
                
    #             components = request.json['components']
    #             for component in components:
    #                 comp = Component.query.filter_by(pc_id=id, part_id=component['part_id']).first()
    #                 comp.quantity = component['quantity']
                
                

    #             db.session.commit()
    #         else:
    #             return jsonify({
    #                 'message': "You are not authorized to update this pc"
    #             }), HTTP_401_UNAUTHORIZED

    #     return jsonify({
    #         'message': "Pc updated",
    #         # 'pc': {
    #         #     'name': pc.name,
    #         #     'price': pc.price,
    #         #     # 'components': [],
    #         #     'userId_created': pc.userId_created
    #         # }
    #     }), HTTP_200_OK

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
            if pc.userId_created == current_user['id'] or current_user['isAdmin']==True:
                db.session.delete(pc)
                db.session.commit()

            return jsonify({
                'message': "Pc deleted"
            }), HTTP_200_OK

pc_view = PcAPI.as_view('pc_api')
api_pc.add_url_rule('/api/v1/pc', defaults={'id': None},view_func=pc_view, methods=['GET',])
api_pc.add_url_rule('/api/v1/pc' ,view_func=pc_view, methods=['POST',])
api_pc.add_url_rule('/api/v1/pc/<int:id>', view_func=pc_view, methods=['GET','PUT', 'DELETE'])


