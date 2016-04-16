#  @author laxmikant


import graphlab as gl



def getNHRModels(train_data):
    
    #get all 10 models
    
    selected_NHR_features=['Runs Scored','Wickets Lost','Got All Out', 'Runs Conceded','Opponent Wickets Taken','Opponent All Out','Player Total Runs','Balls Faced', 'R0','W0','R1','W1','Target','ClusterID','Player Non Home Runs','Home'] 

    
    models=[]
    for i in range(10):
        linearModel= gl.linear_regression.create(train_data[i],target='Current_NHR' , features=selected_NHR_features, validation_set=None)
        models.append(linearModel)
        
    #print Summary
    for i in range(10):
        print models[i].summary()
    
    return models



def getPredictedNHR(models, segment, test_data):
    predicted_NHR=models[segment-1].predict(test_data)
    
    return gl.SFrame({"Predicted_NHR": predicted_NHR})