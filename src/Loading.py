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
    database   = conn["CricketData"]
    collection = database["Statistics"]
    c=0
    for f in os.listdir("C:\\Users\\Aarav\\Downloads\\odis"):
        print f
        with open("C:\\Users\\Aarav\\Downloads\\odis\\"+ f, 'r') as stream:
            try:
                match = yaml.load(stream)
                j = json.dumps(match, default=date_handler)
                jObject= json.loads(j)
                #print jObject['innings'][0]['1st innings']['deliveries'][0]['0.1']
                collection.insert(jObject,check_keys=False)
                #print("Resond Inserted!")
            except yaml.YAMLError as exc:
                print(exc)
        c=c+1
        #if(c==3):
        #    break            
LoadData()


conn = MongoClient('mongodb://localhost:27017/')
database   = conn["CricketData"]
collection = database["Statistics"]

for i in collection.find({'innings':'1st innings'}):
    print i
        