
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
database   = conn["AllCricketData"]
collection = database["Stats"]


# to store the statistics
HOME_RUN_LIST={}
MILESTONE_LIST={}
BALLS_FACED={}
MATCHES_PLAYED={}
PLAYER_NON_HOME_RUNS={}
PLAYER_HOME_RUNS={}
TEAMS={}
# ball_match=0
# 
# counter=0
REMOVE_TEAMS={'Kenya','Bermuda','Scotland','Netherlands','Canada','Africa XI','Asia XI','United Arab Emirates', 'Hong Kong', 'Afghanistan'}

#HOME RUN HITTING ABILITY
for doc in collection.find():
    #counter=counter+1
    #print doc['info']['outcome']
    if 'result' in doc['info']['outcome'].keys():
        #print doc['info']['outcome']['result']
        if doc['info']['outcome']['result']=='no result':
            continue
    
    if doc['info']['match_type']=='ODI':
        #print doc['innings'][0]['1st innings']['team']
        num_innings=len(doc['innings'])
        if(num_innings>2):
            continue
    
        
        if doc['info']['teams'][0] in REMOVE_TEAMS or doc['info']['teams'][1] in REMOVE_TEAMS:
            continue
        
        #print doc['info']['teams'][0] , doc['info']['teams'][1]
        
        #iterate for both innings
        for i in range(num_innings):
            CURRENT_MATCH_RUNS={}
           
           
            if i==0:
                deliveries=doc['innings'][0]['1st innings']['deliveries']
                team = doc['innings'][0]['1st innings']['team']
            if i==1:
                deliveries=doc['innings'][1]['2nd innings']['deliveries']
                team=doc['innings'][1]['2nd innings']['team']
                
            for ball in deliveries:
                #if ball.keys()[0]<5.0:
                    
                #print type(ball.keys()[0])
                #print type(str(ball.keys()[0]))
                #print str(ball.keys()[0])
                over=float(str(ball.keys()[0]))
#                        
                
                if over>=45.0 and over<50.0:     
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
                            
                        if batsman in TEAMS.keys():
                            pass
                        else:
                            TEAMS[batsman]=team
                        
                        #add to Home RUN List
                        if run==4 or run==6:
                            #print "It's HOME RUN!"
                            if batsman in HOME_RUN_LIST.keys():
                                HOME_RUN_LIST[batsman]=HOME_RUN_LIST[batsman]+1
                            else:
                                HOME_RUN_LIST[batsman]=1
                                
                            if batsman in PLAYER_HOME_RUNS.keys():
                                if run ==4:
                                    PLAYER_HOME_RUNS[batsman]=PLAYER_HOME_RUNS[batsman]+4
                                else:
                                    PLAYER_HOME_RUNS[batsman]=PLAYER_HOME_RUNS[batsman]+6
                            else:
                                if run ==4:
                                    PLAYER_HOME_RUNS[batsman]=4
                                else:
                                    PLAYER_HOME_RUNS[batsman]=6
                                
                           
                        else:
                                                            
                            if batsman in PLAYER_NON_HOME_RUNS.keys():
                                PLAYER_NON_HOME_RUNS[batsman]=PLAYER_NON_HOME_RUNS[batsman]+run
                            else:
                                PLAYER_NON_HOME_RUNS[batsman]=run
        
            #add to MILESTONE List
            for player in CURRENT_MATCH_RUNS.keys():
                if CURRENT_MATCH_RUNS[player]>=50:
                    #print "Adding to MILESTONE LIST"
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

    #print "Printing List"
    #for player in MILESTONE_LIST.keys():
        #print player+ " "+ str(MILESTONE_LIST[player])



print "Writing to file"
openFile=open("C:\\Users\\Aarav\\Desktop\\UpdatedSegmentFeatures\\Segment10.csv", "w")
fileHeader="Batsman,Total Runs Scored,Home Run Hitting Ability,Home Runs,Non Home Runs,Number of Milestones Reached,Average Balls Faced,Team"
openFile.write(fileHeader)
openFile.write("\n")

print "---------------Statistics-------------"
for player in HOME_RUN_LIST.keys():
    
    if player in PLAYER_NON_HOME_RUNS.keys():
        non_home_runs=PLAYER_NON_HOME_RUNS[player]
    else:
        non_home_runs=0
        
    if player in PLAYER_HOME_RUNS.keys():
        home_runs=PLAYER_HOME_RUNS[player]
    else:
        home_runs=0
        
    runs=home_runs+non_home_runs
    n=float(float(BALLS_FACED[player])/float(MATCHES_PLAYED[player]))
    tm=TEAMS[player]
    HRA=float(HOME_RUN_LIST[player])
    
    if player in MILESTONE_LIST.keys():
        MRA=float(MILESTONE_LIST[player])
    else:
        MRA=0
        
    feature="" + player + "," + str(runs) + "," +str(HRA) + "," +str(home_runs) + "," +str(non_home_runs) + "," + str(MRA) + ","  + str(n) + ","  + str(tm) 
    print feature
    openFile.write(feature)
    openFile.write("\n")
    