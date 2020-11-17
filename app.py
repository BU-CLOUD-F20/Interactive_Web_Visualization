from flask import Blueprint
from flask_restful import Api
from resources.memberapi import MemberAPI


api_bp = Blueprint('api', __name__)
api = Api(api_bp)

api.add_resource(MemberAPI, '/v1/members') 

