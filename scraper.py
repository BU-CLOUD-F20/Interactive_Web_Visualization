import pandas as pd
from pandas import DataFrame, read_csv
import json

#this class scrapes the excel sheets in the 'sheets' folder to upload them to the db

class scraper():
    item_list = []

    def getXLS(self, file_loc):
        data = pd.read_excel(file_loc, skiprows = range(0, 15))

        titles = data['Title']
        authors = data['Authors']
        scopus_ids = data['Scopus Author Ids']

        # make 
        for n in range(len(titles)):
            author = self._separate(authors[n])
            scopus_id = self._separate(scopus_ids[n])
            item = {
                "title": titles[n],
                "authors": author,
                "scopus_ids": scopus_id
            }
            self.item_list.append(item)

        # mem_list = json.dumps(self.item_list)
        return json.loads(json.dumps(self.item_list))
  
        # print(data['Authors'])

    def _separate(self, obj):
        obj = json.dumps(obj)
        obj = obj.replace('"', '').replace(' ','').replace(',',', ')
        return obj.split('|')


# test = scraper().getXLS('./sheets/PublicationsGroup1.xls')

# print(test[0])