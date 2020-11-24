from flask_restful import Resource
from flask import jsonify, request, Response

# from run import preset
import json
import os.path
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

db_string = os.getenv('DB_PASS')
db = create_engine(db_string)
base = declarative_base()

class InfoAPI(Resource):
    # with open(os.path.dirname(__file__) + '/demo.json') as j:
    
    
    from models.infoitem import InfoItem
    Session = sessionmaker(db)
    session = Session()
    # memberlist = Affiliate_Member

    base.metadata.create_all(db)
    members = session.query(InfoItem)
    memberlist = []
    for member in members:
        memberlist.append({
            "id": member.id,
            "name": member.name,
            "department": member.department,
            "college": member.college,
            "email": member.email,
            "interests": member.interests,
            "domains": member.domains
        })


    def get(self):
        # print(self.memberlist)
        return self.memberlist

    #admin use only
    def post(self):
        if not request:
            return {"message": "no input"}, 400

        # member = MemberItem(**request.get_json()) #change the pointer in the production for security reason
        # self.memberlist.append(member.toJson())
        
        return {"message": "post success"}, 201

    def put(self):
        item = request.get_json()

        for member in self.memberlist:
            if member['id'] == item['id']:
                for field in item:
                    member[field] = item[field]

                return {"message": "update success"}, 201

        return {"message": "item not found"}, 404