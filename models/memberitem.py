from flask_sqlalchemy import SQLAlchemy
from resources.memberapi import base
from sqlalchemy import Column, String, Integer, Float

class MemberItem(base):
    __tablename__ = 'affiliates'

    id = Column(Integer, primary_key=True)
    title = Column(String(200))
    authors = Column(String(200))
    scopusIds = Column(String(200))
    year = Column(Integer)
    citations = Column(Integer)
    weight = Column(Float) 

    # def __init__(self, title, authors, scopusIds, year, citations, weight):
    #     self.title = title
    #     self.authors = authors
    #     self.scopusIds = scopusIds
    #     self.year = year
    #     self.citations = citations
    #     self.weight = weight
