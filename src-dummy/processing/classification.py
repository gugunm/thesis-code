# -*- coding: utf-8 -*-
# == ORIGINAL PACKAGES ==
import pandas as pd
import numpy as np
# == FILE AS PACKAGES ==
import common_function as cf           # file processing/common_function




'''============ 1. ============'''
''' 
### DONE Date: 25/10/2020 ###
Input   : dataPerClass
Output  : super matrix dari kelas tersebut
Problem : -
''' 
def createSuperMatrix(dataPerClass):
    # inisialisasi df kosong untuk dataPerClass
    dfAccumulatorDataPerClass = pd.DataFrame(0.0, columns=dataPerClass[0]["weightedAyat"].columns, index=dataPerClass[0]["weightedAyat"].index)
    # inisiasi variable untuk total penjumlahan cell keseluruhan pada class tersebut
    accumulatorAllCells = 0
    
    # looping untuk tiap data di class tersebut
    for i, data in enumerate(dataPerClass):
        print("data ke - {} / {}".format(i, len(dataPerClass)-1))
        # jumahkan tiap cells di seluruh doc yang classnya sama rumusnya yang W*(t_i, s_j, c) -> matriks
        dfAccumulatorDataPerClass = dfAccumulatorDataPerClass.add(data["weightedAyat"], fill_value=0)
        # jumlahkan keseluruhan cells di seleuruh doc yang classnya sama sigma_t . sigma_s W*(t, s, c) -> float
        accumulatorAllCells += data["weightedAyat"].to_numpy().sum()
        
    return dfAccumulatorDataPerClass, accumulatorAllCells





'''============ 2. ============'''
''' 
### DONE Date: 25/10/2020 ###
Input   : superMatrixSomeClass, sumAllCellSomeClass, current_test_data
Output  : updetan super matrix dan sumallcells karena ditambah dengan current data test
Problem : -
''' 
def updateSuperMatrix(superMatrixSomeClass, sumAllCellSomeClass, current_test_data, totalDocPerClass):
    # update matrix sebelumnya dengan menambahkan data test
    superMatrixSomeClass = superMatrixSomeClass.add(current_test_data["weightedAyat"], fill_value=0) 
    # devide setiap nilainya dengan jumlah data di class itu (plus 1 karena ditambah data test 1)
    superMatrixSomeClass = superMatrixSomeClass.div(totalDocPerClass + 1)
    
    # update sum cells dengan sum pada data test
    sumAllCellSomeClass += current_test_data["weightedAyat"].to_numpy().sum()
    # devide nilai sum per class dengan jumlah data di class itu (plus 1 karena ditambah data test 1)
    sumAllCellSomeClass = sumAllCellSomeClass / (totalDocPerClass + 1)
    
    return superMatrixSomeClass, sumAllCellSomeClass




'''============ 3. ============'''
''' 
### ON PROCESS Date: 25/10/2020 ###
Input   : superMatrixClass0, sumAllCellClass0, totalVocab, totalConcept -> Pr(Mij | C)
Output  : matrix probablity untuk kelas tertentu
Problem : -
''' 
def calculateProbability(superMatrixSomeClass, sumAllCellSomeClass, totalVocab, totalConcept):
    # tambah semua nilai dengan 1 untuk smoothing
    probMatrixSomeClass = superMatrixSomeClass.add(1) 
    # inisiasi untuk nilai pembaginya yaitu sumAllCellSomeClass + |V|.|S| -> untuk smoothing
    probabilityDivision = sumAllCellSomeClass + np.multiply(totalVocab, totalConcept)
    
    # untuk tiap cell-nya, bagi nilainya dengan probabilityDivision
    probMatrixSomeClass = probMatrixSomeClass.div(probabilityDivision)
    
    return probMatrixSomeClass




'''============ 4. ============'''
''' 
### ON PROCESS Date: 25/10/2020 ###
Input   : probClass0, probabilityMatrixClass0
Output  : nilai probablitas final untuk tiap kelasnya
Problem : -
''' 
def calculateFinalProbability(probClass, probabilityMatrixClass):
    # ini bagian sigma_|v|.sigma_|s|logPr(Mij|c)
    #sumOfProbCells = probabilityMatrixClass.to_numpy().sum()
    
    probNumpyArray = probabilityMatrixClass.to_numpy()

    accumulator = 0
    for i in probNumpyArray:
        for j in i:
            #probAccumulator = np.multiply(probAccumulator, j)
            accumulator += np.log(j)
    
    # ini rumus untuk argMax
    finalProbabiity = np.log(probClass) + accumulator
    
    return finalProbabiity




'''============ 5. ============'''
''' 
### ON PROCESS Date: 25/10/2020 ###
Input   : train data & test data
Output  : nilai probablitas test data menggunakan SNB untuk kelas 0 dan 1
Problem : -
''' 
def calculateSNB(
        currentBinaryLabel,  
        current_test_data,
        superMatrixClass0, 
        sumAllCellClass0,
        totalDocClass0,
        superMatrixClass1, 
        sumAllCellClass1,
        totalDocClass1,
        probClass0, 
        probClass1
        ):
    
    print("== updating super matrix class 0 with test data... ==")
    # update super matrix karena ditambah data test
    superMatrixClass0, sumAllCellClass0 = updateSuperMatrix(superMatrixClass0, sumAllCellClass0, current_test_data, totalDocClass0) 
    print("== updating super matrix class 1 with test data... ==")
    # update summ all cells karena ditambah data test
    superMatrixClass1, sumAllCellClass1 = updateSuperMatrix(superMatrixClass1, sumAllCellClass1, current_test_data, totalDocClass1)   
    
    # get total vocabulary and concept page for smoothing
    totalVocab = len(class0_train_data[0]["weightedAyat"].index)
    totalConcept = len(class0_train_data[0]["weightedAyat"].columns)
    
    # hitung nilai probabilitas untuk tiap cellnya
    probabilityMatrixClass0 = calculateProbability(superMatrixClass0, sumAllCellClass0, totalVocab, totalConcept)
    probabilityMatrixClass1 = calculateProbability(superMatrixClass1, sumAllCellClass1, totalVocab, totalConcept)
    
    # tampung seluruh final prob untuk tiap kelasnya
    finalProbToBeClass0 = calculateFinalProbability(probClass0, probabilityMatrixClass0)
    finalProbToBeClass1 = calculateFinalProbability(probClass1, probabilityMatrixClass1)
    
    print("Probabilitas Class 0 : ", finalProbToBeClass0)
    print("Probabilitas Class 1 : ", finalProbToBeClass1)
    
    # tampung di array argmax
    argMaxArray = [finalProbToBeClass0, finalProbToBeClass1]
    
    # tentuin classnya berdasarkan nomor indexnya
    classPrediction = argMaxArray.index(max(argMaxArray))
    
    return classPrediction





'''============ 6. ============'''
''' 
### DONE Date: 25/10/2020 ###
Input   : train data & test data
Output  : hasil prediksi data test
Problem : -
''' 
def predictDataTest(predResult, currentBinaryLabel, class0_train_data, class1_train_data, test_data, probClass0, probClass1):
    # |c| jumlah data belonging to the class c
    totalDocClass0 = len(class0_train_data)
    totalDocClass1 = len(class1_train_data)
    
    # buat super matrix
    print("== creating super matrix class 0... ==")
    superMatrixClass0, sumAllCellClass0 = createSuperMatrix(class0_train_data) 
    print("== creating super matrix class 1... ==")
    superMatrixClass1, sumAllCellClass1 = createSuperMatrix(class1_train_data)
    
    for i, current_test_data in enumerate(test_data):    
        # hitung nilai semantic naive bayes, sampai return label untuk current data test pada current binary label
        predLabel = calculateSNB(
                currentBinaryLabel,  
                current_test_data,
                superMatrixClass0, 
                sumAllCellClass0,
                totalDocClass0,
                superMatrixClass1, 
                sumAllCellClass1,
                totalDocClass1,
                probClass0,
                probClass1
                )

        # jadikan index data test string
        str_i = str(i)
        # append prediction label ke tabung hasil prediksi
        predResult.setdefault(str_i, []).append(predLabel)
        
        print("# Prediksi data test ke {} pada binary label ke {} : {}".format(i, currentBinaryLabel, predLabel))
        print("# Label faktual data test ke {} pada binary label ke {} : {}".format(i, currentBinaryLabel, current_test_data["labelsPerAyat"][currentBinaryLabel]))
    
    return predResult





'''============ 7. ============'''
''' 
### DONE Date: 25/10/2020 ###
Input   : class0_train_data, class1_train_data, number_train_data
Output  : class prob untuk tiap kelasnya
Problem : -
''' 
def calculateClassProbability(number_class0_train_data, number_class1_train_data, number_train_data):
    # probability class 0
    probClass0 = number_class0_train_data / number_train_data
    # probability class 1
    probClass1 = number_class1_train_data / number_train_data
        
    return probClass0, probClass1





'''============ 8. ============'''
''' 
### DONE Date: 25/10/2020 ###
Input   : train data
Output  : train data yang telah dikelompokkan berdasarkan kelasnya
Problem : -
''' 
def devideTrainDataByClass(train_data, currentBinaryLabel):
    class0_train_data, class1_train_data = list(), list()
    
    for i, data in enumerate(train_data):
        if data["labelsPerAyat"][currentBinaryLabel] == 0:
            class0_train_data.append(data)
        else:
            class1_train_data.append(data)
    
    return class0_train_data, class1_train_data





'''============ 9. ============'''
''' 
### DONE Date: 22/10/2020 ###
Input   : listWeightedAyat
Output  : train data & test data
Problem : -
''' 
def splitData(listWeightedAyat):
    # Shuffle ayat agar yang dijadikan data test adalah random
#    random.shuffle(listWeightedAyat)

    # ambil train data
    train_data = listWeightedAyat[:14]
    # ambil test data
    test_data = listWeightedAyat[14:]
    
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





'''============ 10. ============'''
if __name__ == '__main__':
    #listWeightedAyat = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
    # load data terms-by-concept matriks dari file bin
    listWeightedAyat = cf.readFileBin(path='../../data/terms_by_concept_dummy.bin.txt')
    # panggill fungsi main / entar pake ini
    #mainClassification(listWeightedAyat)
    train_data, test_data = splitData(listWeightedAyat)
    # nama label untuk dataset
    labelsName = list(range(16))
    # inisialisasi dict untuk prediction result
    predResult = dict()

#    '''
    # ALTERNATIF 1
    for currentBinaryLabel in labelsName:
        # kelompokkan data train berdasarkan kelasnya
        class0_train_data, class1_train_data = devideTrainDataByClass(train_data, currentBinaryLabel)
        
        # hitung probabilitas er kelasnya
        probClass0, probClass1 = calculateClassProbability(len(class0_train_data), len(class1_train_data), len(train_data))
        
        # Lakukan prediksi untuk tiap data test dengan currentBinaryLabel
        predResult = predictDataTest(predResult, currentBinaryLabel, class0_train_data, class1_train_data, test_data, probClass0, probClass1)
        #break
#    '''
        
    '''
    # ALTERNATFIF 2
    currentBinaryLabel = 2
    # kelompokkan data train berdasarkan kelasnya
    class0_train_data, class1_train_data = devideTrainDataByClass(train_data, currentBinaryLabel)
    
    # hitung probabilitas er kelasnya
    probClass0, probClass1 = calculateClassProbability(len(class0_train_data), len(class1_train_data), len(train_data))
    
    # Lakukan prediksi untuk tiap data test dengan currentBinaryLabel
    predResult = predictDataTest(predResult, currentBinaryLabel, class0_train_data, class1_train_data, test_data, probClass0, probClass1)
    '''
    
#    # Contoh perhitungan supermatrix (biar mudah diliat pake variable)
#    superMatrix, sumAllCells = createSuperMatrix(test_data)
#    
#    # get total vocabulary and concept page for smoothing
#    totalVocab = len(test_data[0]["weightedAyat"].index)
#    totalConcept = len(test_data[0]["weightedAyat"].columns)
#    
#    matriksprobabilitas = calculateProbability(superMatrix, sumAllCells, totalVocab, totalConcept)
        
#    print("probClass0 = ", probClass0)
#    print("probClass1 = ", probClass1)
        
    
    
    
    
    








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
### ON PROCESS Date: 22/10/2020 ###
Input   : train data & test data
Output  : train data yang udah di filter sama 
          terms yang ada di test data
Problem : -
''' 
#def removeTermsOfTestData():
#    return 0

    
    
    
    
    
    
    
    
    