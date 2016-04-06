
# @author laxmikant


from _ast import Num
import datetime
import json
import os
import sys
from time import mktime

from bson import json_util
from pymongo import MongoClient
import yaml


conn = MongoClient('mongodb://localhost:27017/')
database   = conn["ODI"]
collection = database["Stats"]


# to store the statistics
#HOME_RUN_LIST={}
#MILESTONE_LIST={}
#BALLS_FACED={}
#MATCHES_PLAYED={}



# ball_match=0
# 
# counter=0
REMOVE_TEAMS={'Kenya','Bermuda','Scotland','Netherlands','Canada','Africa XI','Asia XI','United Arab Emirates', 'Hong Kong', 'Afghanistan'}

#File writing
#***************************CHANGE SEGMENT *********************************************************************
segment=10
#********************************************************************************
filename="F:\\Books\\Statistical Machine Learning (SML)\\Project\\Data\\Statistics\\Segment"
filename= filename+str(segment)+".csv"
openFile=open(filename, "w")
fileHeader="Batsman,Total Runs Scored,Home Runs,Non Home Runs,Balls Faced,R0,W0,R1,W1,Target,Team"
openFile.write(fileHeader)
openFile.write("\n")

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
            PLAYER_NON_HOME_RUNS={}
            PLAYER_HOME_RUNS={}
            TEAMS={}
            BALLS_FACED_TILL_NOW={}
            CURRENT_SEGMENT_BATSMAN=[]
            target=0
            wickets=0
            r0=0
            r1=0
            w0=0
            w1=0
            
            if i==0:
                deliveries=doc['innings'][0]['1st innings']['deliveries']
                team = doc['innings'][0]['1st innings']['team']
            if i==1:
                deliveries=doc['innings'][1]['2nd innings']['deliveries']
                team=doc['innings'][1]['2nd innings']['team']
            
            # for each ball    
            for ball in deliveries:
                
                over=float(str(ball.keys()[0]))
#
                
                '''
                For Segment 1 : keep segment=1, lower =0.0 
                For Segment 2 : keep segment=2, lower=0.0
                etc.
                '''
                ######## Segment bounds
                lower= 0.0
                higher=5.0 * segment
                #***********************
                if over>=lower and over<higher:     
                    for ball_attr in ball.keys():
                        #print ball[ball_attr]['runs']['total']
                        
                        batsman=ball[ball_attr]['batsman']
                        run=ball[ball_attr]['runs']['batsman']
                        
                        #Current segment batsman
                        if (over>=(segment-1)*5.0) and (over<segment*5.0):
                            if batsman not in CURRENT_SEGMENT_BATSMAN:
                                CURRENT_SEGMENT_BATSMAN.append(batsman)
                        
                        if batsman in CURRENT_MATCH_RUNS.keys():
                            CURRENT_MATCH_RUNS[batsman]=CURRENT_MATCH_RUNS[batsman]+run
                        else:
                            CURRENT_MATCH_RUNS[batsman]=run
                        
                        #update target for 2nd Inning
                        if(i==1):
                            target=target+run
                        
                        
                        #Wickets
                        seg0=segment-2;  # till segment n-2
                        seg1=segment-1;  # for segment n-1
                        
                        if segment==1 or segment==2:
                            seg0=0
                            r0=0
                            w0=0
                        
                        # wickets till segment n-2
                        if (over<seg0*5.0) and ('wicket' in ball[ball_attr].keys()):
                            w0=w0+1
                        
                        #runs till segment n-2
                        if over<seg0*5.0:
                            r0=r0+run
                        
                        #wickets in segment n-1
                        if (over>=seg0*5.0) and (over<seg1*5.0) and ('wicket' in ball[ball_attr].keys()):
                            w1=w1+1
                            #print "wicket at " +ball_attr  
                            
                        #runs in segment n-1
                        if (over>=seg0*5.0) and (over<seg1*5.0):
                            r1=r1+run
                            
                        #ball faced till the segment
                        if batsman in BALLS_FACED_TILL_NOW.keys():
                            BALLS_FACED_TILL_NOW[batsman]=BALLS_FACED_TILL_NOW[batsman]+1
                        else:
                            BALLS_FACED_TILL_NOW[batsman]=1
                            
                        if batsman in TEAMS.keys():
                            pass
                        else:
                            TEAMS[batsman]=team
                        
                        #add to Home RUNs & NON HOME RUNS
                        if run==4 or run==6:
                            #print "It's HOME RUN!"
                            
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
        
            
                #if ball is not in the segment still add to TARGET
                else:
                    for ball_attr in ball.keys():
                        run=ball[ball_attr]['runs']['batsman']
                        
                        #update target for 2nd Inning
                        if(i==1):
                            target=target+run
                    
            #Write to file for each batsman till the segment
            for player in CURRENT_SEGMENT_BATSMAN:
                
                if player in PLAYER_NON_HOME_RUNS.keys():
                    non_home_runs=PLAYER_NON_HOME_RUNS[player]
                else:
                    non_home_runs=0
                
                if player in PLAYER_HOME_RUNS.keys():
                    home_runs=PLAYER_HOME_RUNS[player]
                else:
                    home_runs=0
                        
                runs=home_runs+non_home_runs
                team=TEAMS[player]
                
                if i==0:
                    target=0
                else:
                    target=target+1        
                
                if player in BALLS_FACED_TILL_NOW.keys():
                    balls_faced=BALLS_FACED_TILL_NOW[player]
                else:
                    balls_faced=0
                
                feature="" + player + "," + str(runs) + ","  +str(home_runs) + "," +str(non_home_runs) + "," +str(balls_faced)+ "," +str(r0)+ ","+ str(w0)+","+ str(r1)+","+  str(w1)+","+ str(target) + ","  + str(team)
                print feature
                openFile.write(feature)
                openFile.write("\n")   
    

  
 
'''
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
'''    