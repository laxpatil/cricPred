

#  @author laxmikant


import HRModel
import NHRModel
import LoadData 


def updateHRFeatures(test_data,predicted_HR):
    test_data['Actual HR in Segment'] = test_data['Current_HR']
    test_data['Predicted HR in Segment']= predicted_HR['Predicted_HR']
    test_data['R0']=test_data['R0']+predicted_HR['Predicted_HR']
    test_data['R1']= predicted_HR['Predicted_HR']
    test_data['Current_HR']= predicted_HR['Predicted_HR']
    return test_data

def updateNHRFeatures(test_data,predicted_NHR):
    test_data['Actual NHR in Segment'] = test_data['Current_NHR']
    test_data['Predicted NHR in Segment']= predicted_NHR['Predicted_NHR']
    test_data['R0']=test_data['R0'] + predicted_NHR['Predicted_NHR']
    test_data['R1']+= predicted_NHR['Predicted_NHR']
    test_data['Current_NHR']= predicted_NHR['Predicted_NHR']
    test_data['Predicted Total runs till Segment']= test_data['R0']+test_data['R1']
    return test_data


def main():
    
    #---------------------------PUT THE SEGMENT YOU WANT TO START PREDICTING FROM----------------------
    CURRENT_SEGMENT=5
    #-----------------------------------------------------
    
    train_data=LoadData.getTraindata()
    test_data=LoadData.getTestData(CURRENT_SEGMENT)
    
    HRMods= HRModel.getHRModels(train_data)
    NHRMods= NHRModel.getNHRModels(train_data)
    
    
    #Start predicting for each segment

    while CURRENT_SEGMENT<=10:
        print "--------------Segment "+ str(CURRENT_SEGMENT)+" Started-----------------"  
        predict_HR= HRModel.getPredictedHomeRun(HRMods, train_data, CURRENT_SEGMENT, test_data)
        predict_NHR= NHRModel.getPredictedNHR(NHRMods, CURRENT_SEGMENT, test_data)
        
        test_data=updateHRFeatures(test_data, predict_HR)
        test_data=updateNHRFeatures(test_data, predict_NHR)
        
        #write to FILE
        filename="../Predict EOI/Results/Segment5/HR_NHR"+str(CURRENT_SEGMENT)+".csv"
        test_data.save(filename, format='csv')
        
        CURRENT_SEGMENT=CURRENT_SEGMENT+1
        
        
    return 


if __name__ == "__main__":
    main()