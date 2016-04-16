

#  @author laxmikant

import graphlab as gl
import HRModel
import NHRModel
import LoadData 
import math
from graphlab.data_structures.sframe import SFrame
import pandas as pd
import numpy as np

def updateHRFeatures(test_data,predicted_HR):
    test_data['Actual HR in Segment'] = test_data['Current_HR']
    test_data['Predicted HR in Segment']= predicted_HR['Predicted_HR']
    test_data['R0']=test_data['R0']+predicted_HR['Predicted_HR']
    test_data['R1']= predicted_HR['Predicted_HR']
    test_data['Current_HR']= predicted_HR['Predicted_HR']
    test_data['Predicted Total HR till Segment']+=predicted_HR['Predicted_HR']
    
    return test_data

def updateNHRFeatures(test_data,predicted_NHR):
    test_data['Actual NHR in Segment'] = test_data['Current_NHR']
    test_data['Predicted NHR in Segment']= predicted_NHR['Predicted_NHR']
    test_data['R0']=test_data['R0'] + predicted_NHR['Predicted_NHR']
    test_data['R1']+= predicted_NHR['Predicted_NHR']
    test_data['Current_NHR']= predicted_NHR['Predicted_NHR']
    test_data['Predicted Total NHR till Segment']+=predicted_NHR['Predicted_NHR']
    test_data['Predicted Total runs till Segment']= test_data['R0']+test_data['R1']
    return test_data

def getStatistics(train_data,test_data, CURRENT_SEGMENT):
    mae=0
    seg_test = gl.SFrame("../Predict EOI/SegmentFeatures/Test/Segment" + str(CURRENT_SEGMENT) + ".csv")
    mae_hr_in_segment=0
    mae_nhr_in_segment=0
    total_mae_in_segment=0
    mae_hr_till_segment=0
    mae_nhr_till_segment=0
    for i in range(len(test_data)):
        if CURRENT_SEGMENT==10:
            mae+=math.fabs(test_data[i]['Final Runs Made'] - test_data[i]['Predicted Total runs till Segment'])
            mae_hr_in_segment+=math.fabs(test_data[i]['Actual HR in Segment'] - test_data[i]['Predicted HR in Segment'])
            mae_nhr_in_segment+=math.fabs(test_data[i]['Actual NHR in Segment'] - test_data[i]['Predicted NHR in Segment'])
            total_mae_in_segment+=math.fabs(test_data[i]['Actual HR in Segment'] + test_data[i]['Actual NHR in Segment']- (test_data[i]['Predicted HR in Segment']+test_data[i]['Predicted NHR in Segment']))
            mae_hr_till_segment+=math.fabs(seg_test[i]['Total HR till Segment']-test_data[i]['Predicted Total HR till Segment'])
            mae_nhr_till_segment+=math.fabs(seg_test[i]['Total NHR till Segment']-test_data[i]['Predicted Total NHR till Segment'])
        else:
            mae+=math.fabs(seg_test[i]['Total Runs Till Segment']  - test_data[i]['Predicted Total runs till Segment'])
            mae_hr_in_segment+=math.fabs(test_data[i]['Actual HR in Segment'] - test_data[i]['Predicted HR in Segment'])
            mae_nhr_in_segment+=math.fabs(test_data[i]['Actual NHR in Segment'] - test_data[i]['Predicted NHR in Segment'])
            total_mae_in_segment+=math.fabs(test_data[i]['Actual HR in Segment'] + test_data[i]['Actual NHR in Segment']- (test_data[i]['Predicted HR in Segment']+test_data[i]['Predicted NHR in Segment']))
            mae_hr_till_segment+=math.fabs(seg_test[i]['Total HR till Segment']-test_data[i]['Predicted Total HR till Segment'])
            mae_nhr_till_segment+=math.fabs(seg_test[i]['Total NHR till Segment']-test_data[i]['Predicted Total NHR till Segment'])
            
        
    mae=float(mae)/ len(test_data)
    mae_hr_in_segment=float(mae_hr_in_segment)/ len(test_data)
    mae_nhr_in_segment=float(mae_nhr_in_segment)/ len(test_data)
    mae_hr_till_segment=float(mae_hr_till_segment)/ len(test_data)
    mae_nhr_till_segment=float(mae_nhr_till_segment)/ len(test_data)
    
    mae_string=str(mae_hr_in_segment)+","+str(mae_nhr_in_segment)+","+str(mae_hr_till_segment)+","+str(mae_nhr_till_segment)+","+str(mae)
    return mae_string



def main():
    
    #---------------------------PUT THE SEGMENT YOU WANT TO START PREDICTING FROM----------------------
    CURRENT_SEGMENT=1
    inning=2
    
    #-----------------------------------------------------
    
    train_data=LoadData.getTraindata(inning)
    test_data=LoadData.getTestData(CURRENT_SEGMENT, inning)
    
    HRMods= HRModel.getHRModels(train_data)
    NHRMods= NHRModel.getNHRModels(train_data)
    
    
    #Start predicting for each segment
    fileFolder="../Predict EOI/Results/Final PPT/Inn"+str(inning)+"-StartSeg"+str(CURRENT_SEGMENT)+"-HR_NHR-"
    maeFile=fileFolder+"MAE.csv"
    fwriter=open(maeFile,"w")
    fwriter.write("Segment,HR MAE in Segment,NHR MAE in Segment,HR MAE till Segment,NHR MAE till Segment,Total MAE")
    fwriter.write("\n")
    
    df = pd.DataFrame(0, index=np.arange(len(test_data)), columns=['Predicted Total HR till Segment'])
    hr_runs = gl.SFrame(data=df)
    df = pd.DataFrame(0, index=np.arange(len(test_data)), columns=['Predicted Total NHR till Segment'])
    nhr_runs = gl.SFrame(data=df)
    
        
    while CURRENT_SEGMENT<=10:
        print "--------------Segment "+ str(CURRENT_SEGMENT)+" Started-----------------"  
        predict_HR= HRModel.getPredictedHomeRun(HRMods, train_data, CURRENT_SEGMENT, test_data)
        predict_NHR= NHRModel.getPredictedNHR(NHRMods, CURRENT_SEGMENT, test_data)
        
        test_data['Predicted Total HR till Segment']=hr_runs['Predicted Total HR till Segment']
        test_data['Predicted Total NHR till Segment']=nhr_runs['Predicted Total NHR till Segment']
        
        test_data=updateHRFeatures(test_data, predict_HR)
        test_data=updateNHRFeatures(test_data, predict_NHR)
        
        #write to FILE
        filename=fileFolder+str(CURRENT_SEGMENT)+".csv"
        test_data.save(filename, format='csv')
        
        
        mae_string=getStatistics(train_data, test_data, CURRENT_SEGMENT)
        
        print ""
        print "MAE = ", mae_string
        fwriter.write(str(CURRENT_SEGMENT)+","+mae_string)
        fwriter.write("\n")
        
        
        CURRENT_SEGMENT=CURRENT_SEGMENT+1
    
    print ""    
    print "-----------Prediction Done!---------------"   
    return 


if __name__ == "__main__":
    main()