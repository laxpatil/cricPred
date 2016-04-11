#  @author laxmikant


import graphlab as gl


def getHRModels(train_data):
    models = []
    
    KNNfeatures=['Runs Scored', 'Target', 'R1']
    #KNNfeatures=['Runs Scored','Wickets Lost','Got All Out', 'Runs Conceded','Opponent Wickets Taken','Opponent All Out','Player Total Runs','Balls Faced', 'R0','W0','R1','W1','Target','ClusterID','Player Home Runs','Home']
    
    #-------------------if want RANDOM then--------------------
    '''
    randomF= random.sample(KNNfeatures, 3)
    KNNfeatures=randomF
    '''
    #-------------------------------------------------------------------
    
    for i in range(10):
        knnModel= gl.nearest_neighbors.create(train_data[i], features=KNNfeatures)
        models.append(knnModel)
    
    return models



def getPredictedHomeRun(models, train_data, segment, test_data):
    knn = 5
    nearestPoints = models[segment-1].query(test_data, k=knn)
    currentNN = nearestPoints
    k=0
    s=0
    lAvg = []
    for j in range(len(currentNN)):
        s = s + train_data[segment-1][currentNN[j]['reference_label']]['Current_HR']
        k = k + 1
        if(k == knn):
            lAvg.append(float(s) / knn)
            s = 0
            k = 0
        
    
    return gl.SFrame({"Predicted_HR": lAvg})