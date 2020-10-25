# -*- coding: utf-8 -*-
# == ORIGINAL PACKAGES ==
import pandas as pd
import random
import codecs
import pickle
import math
# == FILE AS PACKAGES ==
import feature_lesk as fl



''' 
### ON PROCESS Date: 25/10/2020 ###
Input   : train data & test data
Output  : nilai probablitas test data menggunakan SNB untuk kelas 0 dan 1
Problem : -
''' 
def calculateSNB(currentBinaryLabel, train_data, test_data):
    
    return 0



''' 
### ON PROCESS Date: 22/10/2020 ###
Input   : train data & test data
Output  : train data yang udah di filter sama 
          terms yang ada di test data
Problem : -
''' 
#def removeTermsOfTestData():
#    return 0



''' 
### DONE Date: 25/10/2020 ###
Input   : train data & test data
Output  : hasil prediksi data test
Problem : -
''' 
def predictDataTest(predResult, currentBinaryLabel, train_data, test_data):
    for i, current_test_data in enumerate(test_data):    
        # hitung nilai semantic naive bayes, sampai return label untuk current data test pada current binary label
        predLabel = calculateSNB(currentBinaryLabel, train_data, current_test_data)

        # jadikan index data test string
        str_i = str(i)
        # append prediction label ke tabung hasil prediksi
        predResult.setdefault(str_i, []).append(predLabel)
    
    return predResult



''' 
### ON PROCESS Date: 22/10/2020 ###
Input   : train data & test data
Output  : multilabel yang sudah dipecah menjadi binary relevance
Problem : -
''' 
#def transformToBinaryRelevance(labelName, train_data, test_data):
#    for data in train_data:
#        data["currentBinaryLabel"] = labelName
#    
#    return train_data, test_data


''' 
### DONE Date: 22/10/2020 ###
Input   : listWeightedAyat
Output  : train data & test data
Problem : -
''' 
def splitData(listWeightedAyat):
    # Shuffle ayat agar yang dijadikan data test adalah random
    random.shuffle(listWeightedAyat)

    # ambil train data
    train_data = listWeightedAyat[:13]
    # ambil test data
    test_data = listWeightedAyat[13:]
    
    return train_data, test_data
    


''' 
### ON PROCESS Date: 25/10/2020 ###
Input   : train and test data
Output  : hasil klasifikasi
Problem : -
''' 
#def mainClassification(listWeightedAyat):
#    # ambil hasil dari split data
#    train_data, test_data = splitData(listWeightedAyat)




if __name__ == '__main__':
    #listWeightedAyat = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
    # load data terms-by-concept matriks dari file bin
    listWeightedAyat = fl.readFileBin(path='../../data/terms_by_concept_dummy.bin.txt')
    # panggill fungsi main / entar pake ini
    #mainClassification(listWeightedAyat)
    train_data, test_data = splitData(listWeightedAyat)
    # nama label untuk dataset
    labelsName = list(range(16))
    # inisialisasi dict untuk prediction result
    predResult = dict()
    for currentBinaryLabel in labelsName:
        # Lakukan prediksi untuk tiap data test dengan currentBinaryLabel
        predResult = predictDataTest(predResult, currentBinaryLabel, train_data, test_data)
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    