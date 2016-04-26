
# @author Chinu


from _ast import Num
import datetime
import json
import os
import sys
from time import mktime

from bson import json_util
from pymongo import MongoClient
import yaml
import csv


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


VENUES={}
fileVenue=open("F:\\Books\\Statistical Machine Learning (SML)\\Project\\Data\\venues.csv",'r')
reader=csv.reader(fileVenue,delimiter=',')
for row in reader:
    if row[0] in VENUES.keys():
        pass
    else:
        VENUES[row[0]]=row[1]

# for key,value in VENUES.iteritems():
#     print key," : ",value
#     
docCount=0
testInn=0
trainInn=0
trainFolder="F:\\Books\\Statistical Machine Learning (SML)\\Project\\Data\\Split\\Train\\"
testFolder="F:\\Books\\Statistical Machine Learning (SML)\\Project\\Data\\Split\\Test\\"


testFile=testFolder+"Segment"+str(segment)+".csv"
testWriter=open(testFile, "w")
fileHeader="Match Index,Batsman,Player Total Runs ,Player Home Runs,Player Non Home Runs,Balls Faced,R0,W0,R1,W1,Current_HR,Current_NHR,Total Runs in Segment, Total HR till Segment, Total NHR till Segment,Total Runs Till Segment,Target,Final Runs Made,Extras,Team,Home,Segment,Opponent Runs"
testWriter.write(fileHeader)
testWriter.write("\n")


trainFile=trainFolder+"Segment"+str(segment)+".csv"
trainWriter=open(trainFile, "w")
fileHeader="Match Index,Batsman,Player Total Runs ,Player Home Runs,Player Non Home Runs,Balls Faced,R0,W0,R1,W1,Current_HR,Current_NHR,Total Runs in Segment, Total HR till Segment, Total NHR till Segment,Total Runs Till Segment,Target,Final Runs Made,Extras,Team,Home,Segment,Opponent Runs"
trainWriter.write(fileHeader)
trainWriter.write("\n")


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
    
        docCount+=  1
        
        if docCount%10==0:
            testInn+=1
        else:
            trainInn+=1
            
            
        
        
        
        if doc['info']['teams'][0] in REMOVE_TEAMS or doc['info']['teams'][1] in REMOVE_TEAMS:
            continue
        
        #print doc['info']['teams'][0] , doc['info']['teams'][1]
    
        venue=doc['info']['venue']
        venue=venue.replace(",", "")

        home_country=VENUES[venue]
        
        #print venue, " : ",home_country
        target1=0
        target2=0
        target=0
        #iterate for both innings
        for i in range(num_innings):
            CURRENT_MATCH_RUNS={}
            PLAYER_NON_HOME_RUNS={}
            PLAYER_HOME_RUNS={}
            TEAMS={}
            BALLS_FACED_TILL_NOW={}
            CURRENT_SEGMENT_BATSMAN=[]
            CURRENT_HR={}
            CURRENT_NHR={}
            
            wickets=0
            r0=0
            r1=0
            w0=0
            w1=0
            nhr=0
            hr=0
            runs_made=0
            hr_till_segment=0
            nhr_till_segment=0
            extras=0
            firstInnRuns=0
            secondInnRuns=0
            if i==0:
                deliveries=doc['innings'][0]['1st innings']['deliveries']
                team = doc['innings'][0]['1st innings']['team']

                secondDeliveries=doc['innings'][1]['2nd innings']['deliveries']
                
                for ball in secondDeliveries:
                    for ball_attr in ball.keys():
                        run=ball[ball_attr]['runs']['batsman']
                        print "secoond run ", run
                        secondInnRuns+=run

                
            if i==1:
                deliveries=doc['innings'][1]['2nd innings']['deliveries']
                team=doc['innings'][1]['2nd innings']['team']
                
                firstDeliveries=doc['innings'][0]['1st innings']['deliveries']
                
                for ball in firstDeliveries:
                    for ball_attr in ball.keys():
                        run=ball[ball_attr]['runs']['batsman']
                        firstInnRuns+=run
            
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
                for ball_attr in ball.keys():
                    run=ball[ball_attr]['runs']['total']
                    runs_made+=run
                
                
                if over>=lower and over<higher:     
                    for ball_attr in ball.keys():
                        #print ball[ball_attr]['runs']['total']
                        
                        batsman=ball[ball_attr]['batsman']
                        run=ball[ball_attr]['runs']['batsman']
                        
                        if(run==4 or run==6):
                            hr_till_segment+=run
                        else:
                            nhr_till_segment+=run
                        
                        extras+=ball[ball_attr]['runs']['extras']
                        
                        
                        #Match batsman to Team
                        if batsman not in TEAMS.keys():
                            TEAMS[batsman]=team
                            
                        #Current segment batsman
                        if (over>=(segment-1)*5.0) and (over<segment*5.0):
                            if batsman not in CURRENT_SEGMENT_BATSMAN:
                                CURRENT_SEGMENT_BATSMAN.append(batsman)
                        
                        if batsman in CURRENT_MATCH_RUNS.keys():
                            CURRENT_MATCH_RUNS[batsman]=CURRENT_MATCH_RUNS[batsman]+run
                        else:
                            CURRENT_MATCH_RUNS[batsman]=run
                        
                        #update target for 2nd Inning
                        if(i==0):
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
                        
                        #CURRENT SEGMENT HOME RUNS & NON HOME RUNS
                        if(over>=seg1*5.0) and (over<segment*5.0):
                            if run==4 or run==6:
                                
                                
                                hr=hr+run
                                if batsman in CURRENT_HR.keys():
                                    CURRENT_HR[batsman]=CURRENT_HR[batsman]+run
                                else:
                                    CURRENT_HR[batsman]=run
                            else:
                                
                                nhr=nhr+run
                                if batsman in CURRENT_NHR.keys():
                                    CURRENT_NHR[batsman]=CURRENT_NHR[batsman]+run
                                else:
                                    CURRENT_NHR[batsman]=run
                            
                        #ball faced till LAST segment(n-1), Since we want to predict for Segment n, we need not worry about the suns in current segment
                        if over<seg1*5.0:
                            if batsman in BALLS_FACED_TILL_NOW.keys():
                                BALLS_FACED_TILL_NOW[batsman]=BALLS_FACED_TILL_NOW[batsman]+1
                            else:
                                BALLS_FACED_TILL_NOW[batsman]=1
                                
                            
                            
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
                        if(i==0):
                            target=target+run
            
            #Set TARGET
            if i==0:
                target2=runs_made+1
                target=0
            else:
                target=target2
            
            
            #print "HR " , hr
            #print "NHR ", nhr        
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
                
                       
                
                if player in BALLS_FACED_TILL_NOW.keys():
                    balls_faced=BALLS_FACED_TILL_NOW[player]
                else:
                    balls_faced=0
                
                if team==home_country:
                    home_or_away=1
                else:
                    home_or_away=0
                
                
                if player in CURRENT_HR.keys():
                    current_hr=CURRENT_HR[player]
                else:
                    current_hr=0
                
                if player in CURRENT_NHR.keys():
                    current_nhr=CURRENT_NHR[player]
                else:
                    current_nhr=0
                
                total_runs_till_segment=nhr_till_segment+hr_till_segment
                
                
                total_runs_in_seg=hr+nhr
                
                
                if docCount%10==0:
                    if i==0:
                        oppRuns=secondInnRuns
                    else:
                        oppRuns=firstInnRuns
                    feature=str(testInn)+"," + player + "," + str(runs)+ ".0" + ","  +str(home_runs) +".0" + "," +str(non_home_runs) + ".0" + "," +str(balls_faced)+ "," +str(r0)+ ".0" + ","+ str(w0)+","+ str(r1)+".0" +","+  str(w1)+","+ str(hr)+".0"+","+str(nhr)+".0" + ","+ str(total_runs_in_seg) +","+ str(hr_till_segment)+"," + str(nhr_till_segment) +"," + str(total_runs_till_segment)+ "," + str(target) + "," +str(runs_made) +"," +str(extras)+"," +str(team)+ ","  + str(home_or_away)+","+str(segment)+","+str(oppRuns)
                    print "TEST --> " ,feature
                    testWriter.write(feature)
                    testWriter.write("\n")
                else:
                    if i==0:
                        oppRuns=secondInnRuns
                    else:
                        oppRuns=firstInnRuns                  
                    feature=str(trainInn)+"," + player + "," + str(runs)+ ".0" + ","  +str(home_runs) +".0" + "," +str(non_home_runs) + ".0" + "," +str(balls_faced)+ "," +str(r0)+ ".0" + ","+ str(w0)+","+ str(r1)+".0" +","+  str(w1)+","+ str(hr)+".0"+","+str(nhr)+".0" + ","+ str(total_runs_in_seg) +","+ str(hr_till_segment)+"," + str(nhr_till_segment) +"," + str(total_runs_till_segment)+ "," + str(target) + "," +str(runs_made) +"," +str(extras)+"," +str(team)+ ","  + str(home_or_away)+","+str(segment)+","+str(oppRuns)
                    print "TRAIN --> ", feature
                    trainWriter.write(feature)
                    trainWriter.write("\n")   
