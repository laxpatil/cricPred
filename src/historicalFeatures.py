
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
database   = conn["CricketData"]
collection = database["Statistics"]


'''
for entry in collection.find({'info.outcome.by.runs': 38}):
    print entry['info'].keys()
'''
loc="F:\\Books\\Statistical Machine Learning (SML)\\Project\\Data\\Statistics\\avgRunsInning.csv"

countries=[]

NUM_MATCHES={}
RUNS={}
WICKETS_LOST={}
GOT_ALL_OUT={}
CONCEDED_RUNS={}
OPPONENT_WICKETS_TAKEN={}
OPPONENT_ALL_OUT={}


openFile = open(loc, "w")
for doc in collection.find():
    if doc['info']['match_type']=='ODI':
        print doc['innings'][0]['1st innings']['team']
        num_innings=len(doc['innings'])
        
        
        
        print "TEAMS: ",
        team1= doc['info']['teams'][0]
        team2= doc['info']['teams'][1]
     
        print team1 + " vs "+ team2
        
        print "------------1st innings-------"
        
        deliveries=doc['innings'][0]['1st innings']['deliveries']
        
        #print deliveries[0]
        
        #Total runs
        runs=0
        wickets=0
        for ball in deliveries:
            #print ball
            for ball_attr in ball.keys():
                #print ball[ball_attr]['runs']['total']
                run=ball[ball_attr]['runs']['total']
                runs=runs+run
                if 'wicket' in ball[ball_attr].keys():
                    #print "WICKET LOST"
                    wickets=wickets+1
        
        print "Putting in RUNS dictionary for " + team1       
        if team1 in countries:
            RUNS[team1]=RUNS[team1]+runs
            NUM_MATCHES[team1]=NUM_MATCHES[team1]+1
            WICKETS_LOST[team1]=WICKETS_LOST[team1]+wickets
        else:
            countries.append(team1)
            RUNS[team1]=runs
            NUM_MATCHES[team1]=1
            WICKETS_LOST[team1]=wickets
            CONCEDED_RUNS[team1]=0
            OPPONENT_WICKETS_TAKEN[team1]=0
            GOT_ALL_OUT[team1]=0
            
        if wickets==10:
            print "ALL OUT"
            if team1 in GOT_ALL_OUT:
                GOT_ALL_OUT[team1]=GOT_ALL_OUT[team1]+1
            else:
                GOT_ALL_OUT[team1]=1
           
        print "Total runs in 1st inning : "+ str(runs) + "/" +  str(wickets) 
        
        print "UPDATING OPPONENT STATS"
        if team2 in countries:
            CONCEDED_RUNS[team2]=CONCEDED_RUNS[team2]+runs
            OPPONENT_WICKETS_TAKEN[team2]=OPPONENT_WICKETS_TAKEN[team2]+wickets
        else:
            countries.append(team2)
            CONCEDED_RUNS[team2]=runs
            OPPONENT_WICKETS_TAKEN[team2]=wickets
            RUNS[team2]=0
            NUM_MATCHES[team2]=1
            WICKETS_LOST[team2]=0
            OPPONENT_ALL_OUT[team2]=0
            
        if wickets==10:
            print "ALL OUT"
            if team2 in OPPONENT_ALL_OUT:
                OPPONENT_ALL_OUT[team2]=OPPONENT_ALL_OUT[team2]+1
            else:
                OPPONENT_ALL_OUT[team2]=1
        
        print "..........................................................................................................."
        
        if num_innings<2:
            continue
        print "-----------2nd Innings---------------"        
        
        deliveries=doc['innings'][1]['2nd innings']['deliveries']
        
        #Total runs
        runs=0
        wickets=0
        for ball in deliveries:
            #print ball
            for ball_attr in ball.keys():
                #print ball[ball_attr]['runs']['total']
                run=ball[ball_attr]['runs']['total']
                runs=runs+run
                if 'wicket' in ball[ball_attr].keys():
                    #print "WICKET LOST"
                    wickets=wickets+1
        
        print "Putting in RUNS dictionary for " + team2        
        if team2 in countries:
            RUNS[team2]=RUNS[team2]+runs
            NUM_MATCHES[team2]=NUM_MATCHES[team2]+1
            WICKETS_LOST[team2]=WICKETS_LOST[team2]+wickets
        else:
            countries.append(team2)
            RUNS[team2]=runs
            NUM_MATCHES[team2]=1
            WICKETS_LOST[team2]=wickets
            
        if wickets==10:
            print "ALL OUT"
            if team2 in GOT_ALL_OUT:
                GOT_ALL_OUT[team2]=GOT_ALL_OUT[team2]+1
            else:
                GOT_ALL_OUT[team2]=1
           
        print "Total runs in 2nd inning : "+ str(runs) + "/" +  str(wickets)     
        
        print "UPDATING OPPONENT STATS : team1"
        if team1 in countries:
            CONCEDED_RUNS[team1]=CONCEDED_RUNS[team1]+runs
            OPPONENT_WICKETS_TAKEN[team1]=OPPONENT_WICKETS_TAKEN[team1]+wickets
        else:
            countries.append(team1)
            CONCEDED_RUNS[team1]=runs
            OPPONENT_WICKETS_TAKEN[team1]=wickets
        
        if wickets==10:
            print "OPPONENT ALL OUT"
            if team1 in OPPONENT_ALL_OUT:
                OPPONENT_ALL_OUT[team1]=OPPONENT_ALL_OUT[team1]+1
            else:
                OPPONENT_ALL_OUT[team1]=1
        
        print "..........................................................................................................."   
        
        

## WRITING TO FILE
print "Writing to file"
openFile=open("F:\\Books\\Statistical Machine Learning (SML)\\Project\\Data\\Statistics\\HistoricalFeatures.csv", "w")
fileHeader="Team,Total Matches Played,Runs Scored,Wickets Lost,Got All Out,Runs Conceded,Opponent Wickets Taken,Opponent All Out "
openFile.write(fileHeader)
openFile.write("\n")
for team in countries:
    print team +" : "+ str(RUNS[team])
    n=NUM_MATCHES[team]
    print RUNS[team]
    print n
    feature="" + team + "," +str(n) + "," + str(float(RUNS[team])/n) + "," + str(float(WICKETS_LOST[team])/n) + "," + str(float(GOT_ALL_OUT[team])/n) + "," + str(float(CONCEDED_RUNS[team])/n) + "," + str(float(OPPONENT_WICKETS_TAKEN[team])/n) + "," + str(float(OPPONENT_ALL_OUT[team])/n) 
    openFile.write(feature)
    openFile.write("\n")               
        



