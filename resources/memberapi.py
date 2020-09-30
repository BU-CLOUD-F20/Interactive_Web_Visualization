from flask_restful import Resource
from flask import jsonify, request, Response
from models.memberitem import MemberItem
import json
import os.path

class MemberAPI(Resource):
    with open(os.path.dirname(__file__) + '/demo.json') as j:
        memberlist = json.load(j)
    # memberlist = [
    #     {
    #         'id': 1, 
    #         'name': 'test',
    #         'department': 'ECE',
    #         'college': 'ENG',
    #         'email': 'test@test.te',
    #         'interests': 'cloud computing',
    #         'domains': 'cybersecurity'
    #     }
    # ] # this will be removed once db is set up

    def get(self):
        return self.memberlist

    #admin use only
    def post(self):
        if not request:
            return {"message": "no input"}, 400

        member = MemberItem(**request.get_json()) #change the pointer in the production for security reason
        self.memberlist.append(member.toJson())
        
        return {"message": "post success"}, 201

    def put(self):
        item = request.get_json()

        for member in self.memberlist:
            if member['id'] == item['id']:
                for field in item:
                    member[field] = item[field]

                return {"message": "update success"}, 201

        return {"message": "item not found"}, 404



        
