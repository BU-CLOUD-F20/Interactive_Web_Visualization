from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
db_string = os.getenv('DB_PASS')

db = create_engine(db_string)
base = declarative_base()

class Affiliate_INFO(base):
    __tablename__ = 'affiliate_info'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    department = Column(String(100))
    college = Column(String(50))
    email = Column(String(50))
    interests = Column(String(1000))
    domains = Column(String(1000))

Session = sessionmaker(db)
session = Session()

base.metadata.create_all(db)

# load data

from algorithms.parseaffiliate import parse_affiliate as pa

data = pa.getXLS()

for n in range(len(data)):
    item = Affiliate_INFO(
        name=data[n]['name'],
        department=data[n]['department'],
        college=data[n]['college'],
        email=data[n]['email'],
        interests=data[n]['interests'],
        domains=data[n]['domains']
    )
    session.add(item)
    session.commit()




