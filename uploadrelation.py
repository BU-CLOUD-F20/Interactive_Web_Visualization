from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())
db_string = os.getenv('DB_PASS')

db = create_engine(db_string)
base = declarative_base()

class Relations(base):
    __tablename__ = 'relations'

    id = Column(Integer, primary_key=True)
    source = Column(String(50))
    target = Column(String(50))
    value = Column(Integer)

Session = sessionmaker(db)
session = Session()

base.metadata.create_all(db)

from algorithms.parseaffiliate import parse_affiliate as pa
from algorithms.parsescival import parse_scival as ps

affiliates = pa.getXLS()

current_path = os.path.dirname((os.path.realpath(__file__)))
sheet_path = current_path + '/' + 'scivalsheets/'
papers = []
for filename in os.listdir(sheet_path):
    papers += (ps().getXLS(os.path.join(sheet_path, filename)))

# implementing queue
queue = []
relation_map = []

for n in range(len(affiliates)):
    queue.append(affiliates[n]['name'])

while queue:
    current_name = queue.pop(0) # set the oldest item in queue as current_name while removing it
    for i in range(len(queue)):
        target_name = queue[i]
        count = 0

        for j in range(len(papers)):
            if current_name in papers[j]['authors'] and target_name in papers[j]['authors']:
                if current_name == 'Li, Wen' and target_name == 'Li, Wenchao':
                    pass
                else:
                    print(current_name, target_name)
                    count += 1

        if count > 0:
            relation = Relations(
                source=current_name,
                target=target_name,
                value=count
            )
            # relation_map.append(relation)
            session.add(relation)
            session.commit()

# print(relation_map)

    
