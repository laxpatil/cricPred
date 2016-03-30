from pymongo import MongoClient
import os
import sys
import json
from bson import json_util
import datetime
from time import mktime
import yaml


def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj


def LoadData():
    conn = MongoClient('mongodb://localhost:27017/')
    database   = conn["AllCricketData"]
    collection = database["Stats"]
    count=0
    for f in os.listdir("F:\\Books\\Statistical Machine Learning (SML)\\Project\\Data\\All Matches"):
        print f
        with open("F:\\Books\\Statistical Machine Learning (SML)\\Project\\Data\\All Matches\\"+ f, 'r') as stream:
            try:
                match = yaml.load(stream)
                j = json.dumps(match, default=date_handler)
                jObject= json.loads(j)
                print jObject['info']   #just printing info
                collection.insert(jObject,check_keys=False)
                print("Recond Inserted!")
                count=count+1
                print "Doc count: "+ str(count)
            except yaml.YAMLError as exc:
                print(exc)
            
          
            
LoadData()


'''
conn = MongoClient('mongodb://localhost:27017/')
database   = conn["CricketData"]
collection = database["Statistics"]

print collection.count()
#print collection.find_one({'bowler':'B Lee'})
for entry in collection.find({'info.outcome.by.runs': 38}):
    print entry['info'].keys()

cursor=collection.aggregate(
                     [
                      {"$group": {"$_id" :  {}"$sum":{"$info.outcome.by"}}}
                      ]
                     )

for document in cursor:
    print(document)

print collection.find({'info.city': 'Jaipur'}).count()
'''       