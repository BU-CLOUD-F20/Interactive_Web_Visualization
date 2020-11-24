from flask_sqlalchemy import SQLAlchemy
from resources.memberapi import base
from sqlalchemy import Column, String, Integer, Float

class InfoItem(base):
    __tablename__ = 'affiliate_info'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    department = Column(String(100))
    college = Column(String(50))
    email = Column(String(50))
    interests = Column(String(1000))
    domains = Column(String(1000))