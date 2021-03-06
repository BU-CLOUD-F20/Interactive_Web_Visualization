import pandas as pd
from pandas import DataFrame
import json

class parse_affiliate:

    def getXLS():
        file_loc = './affiliatesheet/Hariri Faculty Affiliates.xlsx'

        data = pd.read_excel(file_loc)

        item_list = []

        full_name = data['Full Name ']
        department = data['Deparment']
        college = data['College']
        email = data['BU Email']
        interests = data[' Interests']
        domains = data['Domains']

        for n in range(len(full_name)):
            item = {
                "name": full_name[n].strip(),
                "department": department[n],
                "college": college[n],
                "email": email[n],
                "interests": interests[n],
                "domains": domains[n]
            }

            item_list.append(item)

        
        # print(len(item_list))

        return item_list
