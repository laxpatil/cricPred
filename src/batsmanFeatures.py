
# @author laxmikant


from pymongo import MongoClient
import os
import sys
import json
from bson import json_util
import datetime
from time import mktime
import yaml
from _ast import Num


conn = MongoClient('mongodb://localhost:27017/')
database   = conn["ODI"]
collection = database["Stats"]


# to store the statistics
HOME_RUN_LIST={}
MILESTONE_LIST={}
BALLS_FACED={}
MATCHES_PLAYED={}

#HOME RUN HITTING ABILITY
for doc in collection.find():
    print doc['info']['outcome']
    if 'result' in doc['info']['outcome'].keys():
        print doc['info']['outcome']['result']
        if doc['info']['outcome']['result']=='no result':
            continue
    
    if doc['info']['match_type']=='ODI':
        print doc['innings'][0]['1st innings']['team']
        num_innings=len(doc['innings'])
        
        #iterate for both innings
        for i in range(num_innings):
            CURRENT_MATCH_RUNS={}
            if i==0:
                deliveries=doc['innings'][0]['1st innings']['deliveries']
            if i==1:
                deliveries=doc['innings'][1]['2nd innings']['deliveries']
                
                
            for ball in deliveries:
                #print ball
                for ball_attr in ball.keys():
                    #print ball[ball_attr]['runs']['total']
                    batsman=ball[ball_attr]['batsman']
                    run=ball[ball_attr]['runs']['batsman']
                    
                    # Add to CURRENT_MATCH_RUNS list
                    if batsman in CURRENT_MATCH_RUNS.keys():
                        CURRENT_MATCH_RUNS[batsman]=CURRENT_MATCH_RUNS[batsman]+run
                    else:
                        CURRENT_MATCH_RUNS[batsman]=run
                    
                    if batsman in BALLS_FACED.keys():
                        BALLS_FACED[batsman]=BALLS_FACED[batsman]+1
                    else:
                        BALLS_FACED[batsman]=1
                    
                    #add to Home RUN List
                    if run==4 or run==6:
                        print "It's HOME RUN!"
                        if batsman in HOME_RUN_LIST.keys():
                            HOME_RUN_LIST[batsman]=HOME_RUN_LIST[batsman]+1
                        else:
                            HOME_RUN_LIST[batsman]=1
            
            #add to MILESTONE List
            for player in CURRENT_MATCH_RUNS.keys():
                if CURRENT_MATCH_RUNS[player]>=50:
                    print "Adding to MILESTONE LIST"
                    if player in MILESTONE_LIST.keys():
                        MILESTONE_LIST[player]=MILESTONE_LIST[player]+1
                    else:
                        MILESTONE_LIST[player]=1
                        
            #No of matches played            
            for player in CURRENT_MATCH_RUNS.keys():
                if player in MATCHES_PLAYED.keys():
                    MATCHES_PLAYED[player]=MATCHES_PLAYED[player]+1
                else:
                    MATCHES_PLAYED[player]=1

    print "Printing List"
    for player in MILESTONE_LIST.keys():
        print player+ " "+ str(MILESTONE_LIST[player])



print "Writing to file"
openFile=open("F:\\Books\\Statistical Machine Learning (SML)\\Project\\Data\\Statistics\\batsmanFeatures.csv", "w")
fileHeader="Batsman,Home Run Hitting Ability,Milestone Reaching Ability,Matches Played"
openFile.write(fileHeader)
openFile.write("\n")

print "---------------Statistics-------------"
for player in HOME_RUN_LIST.keys():
    n=MATCHES_PLAYED[player]
    HRA=float(HOME_RUN_LIST[player])/n
    if player in MILESTONE_LIST.keys():
        MRA=float(MILESTONE_LIST[player])/n
    else:
        MRA=0
        
    feature="" + player + "," +str(HRA) + "," + str(MRA) + ","  + str(n)
    print feature
    openFile.write(feature)
    openFile.write("\n")             
                    