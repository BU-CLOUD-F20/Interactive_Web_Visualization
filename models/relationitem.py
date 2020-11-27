from flask_sqlalchemy import SQLAlchemy
from resources.relationapi import base
from sqlalchemy import Column, String, Integer

class RelationItem(base):
    __tablename__ = 'relations'

    id = Column(Integer, primary_key=True)
    source = Column(String(50))
    target = Column(String(50))
    value = Column(Integer)