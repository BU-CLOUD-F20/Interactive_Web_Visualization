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

class RelationAPI(Resource):
    from models.relationitem import RelationItem
    from models.infoitem import InfoItem

    Session = sessionmaker(db)
    session = Session()

    base.metadata.create_all(db)
    relations = session.query(RelationItem)
    names = session.query(InfoItem)
    relationlist = [] 
    namelist = []

    def __compute(self):
        self.namelist = [] # intialize
        self.relationlist = []
        for name in self.names:
            self.namelist.append({
                "id": name.name,
                "department": name.department,
                "college": name.college,
                "email": name.email,
                "interests": name.interests,
                "domains": name.domains
            })

        for relation in self.relations:
            source_id = self.__FindIndex(self.namelist, relation.source)
            target_id = self.__FindIndex(self.namelist, relation.target)
            self.relationlist.append({
                "source": source_id,
                "target": target_id,
                "value": relation.value
            })

    def __FindIndex(self, namelist, name):
        for x in range(len(namelist)):
            if name == namelist[x]['id']:
                return x


    def get(self):
        self.__compute()
        return {
            "nodes": self.namelist,
            "links": self.relationlist
            }