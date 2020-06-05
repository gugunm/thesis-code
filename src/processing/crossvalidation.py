# -*- coding: utf-8 -*-
import sys
# import func from another file in other directory
sys.path.insert(1, '../preparation/')
# credential for GDrive and GSheet
import credentials as creds 
# k-fold cross validation
from sklearn.model_selection import KFold

def crossValidation(df):
    # initiation for kfold array
    foldList = []
    # data devided into 10 fold and 1 iteration
    kf = KFold(n_splits=10, shuffle=False)    
    # looping for each fold
    for train_index, test_index in kf.split(df.values): 
        foldList.append({'train_index':train_index, 'test_index':test_index})
        #dfTrain, dfTest = df.iloc[train_index], df.iloc[test_index] 
        #print("train : ", dfTrain, "-- test : ", dfTest)
    return foldList

def mainCrossValidation():
    # file sheet name
    fileName = "dataset-quran"
    # worksheet name
    worksheetName = "proceed-data"
    df = creds.getAsDataframe(fileName, worksheetName).iloc[:,3:]
    return crossValidation(df)

if __name__ == '__main__':
    foldLists = mainCrossValidation()
    
    
    
    
    
    
    
    
    


