#  @author laxmikant


import graphlab as gl



def getNHRModels(train_data):
    
    #get all 10 models
    models=[]
    for i in range(10):
        linearModel= gl.regression.create(train_data[i], target='Current_NHR' , validation_set=None)
        models.append(linearModel)
        
    #print Summary
    for i in range(10):
        print models[i].summary()
    
    return models



def getPredictedNHR(models, segment, test_data):
    predicted_NHR=models[segment-1].predict(test_data)
    
    return gl.SFrame({"Predicted_NHR": predicted_NHR})