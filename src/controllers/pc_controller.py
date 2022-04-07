from flask import Blueprint , request
from flask.json import jsonify
from flask.views import MethodView
from src.constants.http_status_codes import HTTP_200_OK
from src.models.pc_model import PCs


api_pc = Blueprint('api', __name__)


class PcAPI(MethodView):
    def get(self):
        pc = PCs.query.all()
        return jsonify({'pc':pc})
        #return jsonify({'message': 'Server is running'}), HTTP_200_OK

pc_view = PcAPI.as_view('pc_api')
api_pc.add_url_rule('/api/v1/pc', view_func=pc_view, methods=['GET'])


