import pandas as pd
from pandas import DataFrame
from algorithms.parseaffiliate import parse_affiliate
import json

# this class scrapes the excel sheets in the 'sheets' folder to upload them to the db
# then goes through an algorithm that only selects the BU affiliates' publications

class parse_scival():

    def getXLS(self, file_loc):
        data = pd.read_excel(file_loc, skiprows = range(0, 15))
        affiliates = parse_affiliate.getXLS()

        titles = data['Title']
        authors = data['Authors']
        scopus_ids = data['Scopus Author Ids']
        year = data['Year']
        citations = data['Citations']
        weight = data['Field-Weighted Citation Impact']
        aff_namelist = []
        item_list = []

        # load and abbreviate affiliates
        for affiliate in affiliates:
            aff_namelist.append(self._abbreviate(affiliate['name']))
        
        # print(aff_namelist)

        # make 
        for n in range(len(titles)):
            author = self._separate(authors[n])
            scopus_id = self._separate(scopus_ids[n])
            trigger = False
            author_list = []
            id_list = []
            for i in range(len(author)):
                # print(len(aff_namelist))
                for j in range(len(affiliates)):
                    if (author[i] == aff_namelist[j]):
                        trigger = True
                        # print(j)
                        # print(affiliates[j]['name'])
                        author_list.append(affiliates[j]['name'])
                        id_list.append(scopus_id[i])

            if (trigger):
                item = {
                    "title": titles[n],
                    "authors": author_list,
                    "scopus_ids": id_list,
                    "year": year[n],
                    "citations": citations[n],
                    "weight": weight[n]
                }
                item_list.append(item)

        # mem_list = json.dumps(self.item_list)
        return json.loads(json.dumps(item_list))
  
        # print(data['Authors'])

    def _separate(self, obj):
        obj = json.dumps(obj)
        obj = obj.replace('"', '').replace(' ','').replace(',',', ')
        return obj.split('|')

    def _abbreviate(self, name):
        head, sep, tail = name.partition(', ')
        abb_name = head + sep + tail[0] + '.'
        return abb_name


# data = parse_scival()
# data.getXLS('./scivalsheets/PublicationsGroup5.xls')

# test = data.output_data()

# print(test)
