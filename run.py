from flask import Blueprint
from flask_restful import Api
from resources.memberapi import MemberAPI
from resources.infoapi import InfoAPI
from resources.relationapi import RelationAPI


api_bp = Blueprint('api', __name__)
api = Api(api_bp)

api.add_resource(MemberAPI, '/v1/members') 
api.add_resource(InfoAPI, '/v1/info')
api.add_resource(RelationAPI, '/v1/relations')