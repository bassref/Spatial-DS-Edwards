import pymongo
import sys
from pymongo import MongoClient
'''
class MongoHelper(object):
    def _init_(self):
        self.db_airports = MongoClient().geo.db_airports
        self.db_states = MongoClient().geo.db_states

    def get_all_airports(self,db, type="International"):
        all_airports = self.db_airports.find({"type":type})

        results = []
        for ap in all_airports:
            results.append(ap)

        return results
    
    def get_doc_by_keyword(self,field,key):
        #filter on text in an object
        #pass in the dictionary and a regex of what I'm searching for
        result = self.db_airports.find({field:{'$regex':'.*'+key+'.*'}})

        # the result is a python result set so we need to put it in a list
        res_list = []
        for r in result:
            res_list.append(r)

        return res_list

    def get_state_poly(self,code):
        state = self.db_states.find_one({"code":code})

        return state

 '''   

def main():
    #mh = MongoHelper()
    #gaa = mh.get_all_airports("International")
    #print(gaa)

    #county_stuff = mh.get_doc_by_keyword("name", "County")
    #print(county_stuff,flush=True)

    print("My name is Christopher.", flush = True)
    dummy = input()


