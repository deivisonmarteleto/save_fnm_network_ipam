#!/bin/python3

from datetime import datetime
import pymongo
from bson.son import SON

#VARIAVEIS

conn = pymongo.MongoClient(f'mongodb://127.0.0.1:27017/')

T_now = datetime.now()
database = conn['fnmdb']



class MongoSave:
    def __call__(self, collection, query: dict):
        return database[collection].insert_one(query)


class MongoQuerySubnet:
    def __call__(self):
        _list = []
        for x in database['customer'].find({}, {'_id':0, 'net':1}):
            _list.append(x['net'])        
        return _list

class MongoUpade:
    def __call__(self, collection, query: dict):
        myquery = {'value': 1}
        newquery = {"$set": query}
        return database[collection].update_one(myquery, newquery)


class MongoFindAsn:
    def __call__(self):
        
        y = database['customer'].find_one({'asn': '265066'}, {'_id':0, 'asn': 1, 'subnet':1, 'hop':1,'date':1,})
        pprint.pprint(y)


class MongoFindPrefix:
    def __call__(self, net):
        
        y = database['customer'].find_one({'net': net}, {'_id':0, 'asn': 1, 'net':1, 'hop':1, 'date':1,})
        if y == None:
            return False
        else:
            return True

class MongoDropPrefix:
    def __call__(self, net):
        
        return database['customer'].find_one_and_delete({'net': net}, {'_id':0, 'asn': 1, 'net':1, 'date':1,})


