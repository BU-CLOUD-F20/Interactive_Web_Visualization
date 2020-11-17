from sqlalchemy import create_engine  
from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy.orm import sessionmaker
import os
from algorithms.parsescival import parse_scival as ps

db_string = "postgres://postgres:ec528password@database-1.cs5w0p0igzwb.us-east-1.rds.amazonaws.com"

db = create_engine(db_string)  
base = declarative_base()

class Affiliate_Member(base):  
    __tablename__ = 'affiliates'

    id = Column(Integer, primary_key=True)
    title = Column(String(1000))
    authors = Column(String(200))
    scopusIds = Column(String(200))
    year = Column(Integer)
    citations = Column(Integer)
    weight = Column(Float) 

Session = sessionmaker(db)  
session = Session()

base.metadata.create_all(db)

current_path = os.path.dirname((os.path.realpath(__file__)))
sheet_path = current_path + '/' + 'scivalsheets/'
preset = []
for filename in os.listdir(sheet_path):
    preset += (ps().getXLS(os.path.join(sheet_path, filename)))

# Create 

for n in range(len(preset)):
    item = Affiliate_Member(
        title=preset[n]['title'],
        authors=preset[n]['authors'],
        scopusIds=preset[n]['scopus_ids'],
        year=preset[n]['year'],
        citations=preset[n]['citations'],
        weight=preset[n]['weight']
    )  
    session.add(item)  
    session.commit()


# Read
members = session.query(Affiliate_Member)  
for member in members:  
    print(member.title)