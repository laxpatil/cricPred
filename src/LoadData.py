
#  @author laxmikant


import graphlab as gl



def getTraindata():
        batsman = gl.SFrame("../Instantaneous features/batsmanClusters.csv")
        
        historical = gl.SFrame("../Historical features/HistoricalFeatures.csv")
        
        train_data=[]
        
        for i in range(10):
            seg = gl.SFrame("../Predict EOI/SegmentFeatures/Train/Segment" + str(i+1) + ".csv")
            #print "Segment ",seg['R1'].dtype()
            combined = historical.join(seg, on='Team')
            combined = combined.join(batsman, on='Batsman')
            
            print "Training R1 Type: ",combined['R1'].dtype()
            train_data.append(combined)
            
            
        return train_data

#get TEST data
def getTestData(segment):
    
    batsman = gl.SFrame("../Instantaneous features/batsmanClusters.csv")
        
    historical = gl.SFrame("../Historical features/HistoricalFeatures.csv")
        
    seg = gl.SFrame("../Predict EOI/SegmentFeatures/Test/Segment" + str(segment) + ".csv")
            #print "Segment ",seg['R1'].dtype()
    combined = historical.join(seg, on='Team')
    combined = combined.join(batsman, on='Batsman')
            
    print "Test  R1 Type: ",combined['R1'].dtype()
    
    test_data=combined
            
            
    return test_data