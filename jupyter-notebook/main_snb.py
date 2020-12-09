# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import codecs
import pickle
import random
import math
import re
import ast
import sys
import gzip

np.set_printoptions(threshold=sys.maxsize)

#real dataset
datapath = './dataset/dataset-quran.xlsx'

#concept path buat di drive
conceptpath = './assets/conceptInDrive.xlsx' 

### for real data ###
TfResultPath = "./assets/CompressedTfResultPath.bin"
DfResultPath = "./assets/CompressedDfResultPath.bin.txt"
TfIdfResultPath = "./assets/TfIdfResultPath.bin.txt"

wordembedLeskPath = "./assets/realTrainWordembedModel.bin.txt"

# GANTI KALO CW nya BEDA
leskOutputPath = './assets/leskOutput_cw_2/ayat'

'''=== COMMON FUNCTION ==='''
def readFileBin(path = ''):
    file = open(path, 'rb')
    object_file = pickle.load(file)
    return object_file


def save_zipped_pickle(obj, idx, filename, protocol=-1):
    with gzip.open("{}_{}".format(filename, idx), 'wb') as f:
        pickle.dump(obj, f, protocol)
        
        
def load_zipped_pickle(filename):
    with gzip.open(filename, 'rb') as f:
        loaded_object = pickle.load(f)
        return loaded_object


def getListTermsFromSheet(sheetname, datapath = datapath):
    dfUWords = pd.read_excel(datapath, sheet_name=sheetname)
    # Convert word false and true as str
    booldict = {True: 'true', False: 'false'}
    dfUWords = dfUWords.replace(booldict)
    return dfUWords.values.ravel()

def getTerms():
    # ambil data terms dari drive
    listTerms= getListTermsFromSheet('wiki-unique-words')
    return listTerms

def getConcepts():
    dfConcept = pd.read_excel(conceptpath)
    return dfConcept

'''=== LOAD CONCEPT AND TERMS ==='''
# definisikan concepts
dfConcept = getConcepts()
# definisikan terms dengan --- function getTerms() ---
listTerms = getTerms().tolist()


'''=== SEMANTIC NAIVE BAYES ==='''
def calculateProbabilityDataTest(probClass, testDataInClass):
    # sum all cell
    sumAllCell = np.ravel(testDataInClass.values).sum()
    # productAllCell = np.prod(testDataInClass.values)

    # jumlahkan dengan probability class-nya
    classProbForTest = np.log(probClass) + sumAllCell
    # classProbForTest = probClass * productAllCell

    return classProbForTest

def mapDataToClass(test_data, superMatrixClass):
    # ambil token ayat dari test data
    tokenAyat = test_data['token_ayat']
    
    # Ambil intersection termsnya, token di data test yang ada di list terms
    tokenAyat = list(set(listTerms) & set(tokenAyat))

    # ambil super matrix dengan index/terms yang ada di tokenAyat
    superMatrixTest = superMatrixClass[tokenAyat]

    return superMatrixTest


def calculateLogCell(cellValue):
    if cellValue == 0:
        return cellValue
    # hasil log(0.__) akan bernilai negatif, itu tidak apa-apa, hasilnya sama saja
    return np.log(cellValue)


'''============ 1. ============'''
''' 
### DONE Date: 25/10/2020 ###
Input   : dataPerClass
Output  : super matrix dari kelas tersebut
Problem : -
''' 
def createSuperMatrix(indexPerClass):
    # kalo datanya kosong untuk salah satu kelas-nya
    if len(indexPerClass) == 0:
        return 'empty'

    # inisialisasi df kosong untuk dataPerClass
    # ini bisa error kalo datanya kosong untuk salah satu kelas-nya, karena ada ini "dataPerClass[0]" > makanya cek dulu diatas
    dfAccumulatorDataPerClass = pd.DataFrame(0.0, columns=listTerms, index=range(len(dfConcept)))
    # inisiasi variable untuk total penjumlahan cell keseluruhan pada class tersebut
    accumulatorAllCells = 0
    
    # looping untuk tiap data di class tersebut
    for idx, i in enumerate(indexPerClass):
        print("data ke - {} / {}".format(idx, len(indexPerClass)-1))
        
        # LOAD DATA .BIN -> contoh path : './assets/leskOutput/ayat_0'
        pathToData = leskOutputPath + '_' + str(i)
        data = load_zipped_pickle(pathToData)        
        print('Loaded Data : ', pathToData)
        
        # jumahkan tiap cells di seluruh doc yang classnya sama rumusnya yang W*(t_i, s_j, c) -> matriks
        dfAccumulatorDataPerClass = dfAccumulatorDataPerClass.add(data["weightedAyat"], fill_value=0)
    
    print("  - Sum All Cells..")
    # jumlahkan keseluruhan cells di seleuruh doc yang classnya sama sigma_t . sigma_s W*(t, s, c) + |V||S| -> float 
    accumulatorAllCells += (dfAccumulatorDataPerClass.to_numpy().sum() / len(indexPerClass)) + (len(listTerms) * len(dfConcept))

    print("  - Devide Every Cell..")
    # bagi setiap cell-nya dengan jumlah data train di kelas itu
    dfAccumulatorDataPerClass = dfAccumulatorDataPerClass.div(len(indexPerClass))

    print("  - Devide Tiap Cell-nya dengan nilai total cell..")
    # bagi lagi tiap cell-nya dengan nilai accumulator | Pr(M_ij|c) + 1 -> rumus probability cell
    dfAccumulatorDataPerClass = dfAccumulatorDataPerClass.add(1).div(accumulatorAllCells)

    print("  - Log-kan tiap cell-nya..")
    # '''GAK PAKE LOG DULU'''
    # log-kan setiap cell-nya | logPr(M_ij|c) -> rumus prob. cell pakai log
    dfAccumulatorDataPerClass = dfAccumulatorDataPerClass.applymap(calculateLogCell)
    
    print("  - Rubah Data Menjadi Dataframe Lagi..")
    # dari bentuk tuple, rubah lagi ke dataframe, agar supaya gampang ngolahnya
    dfAccumulatorDataPerClass = pd.DataFrame(dfAccumulatorDataPerClass)
        
    return dfAccumulatorDataPerClass




def checkZero(arr):
    for i in arr:
        if i == 0:
            return True
    return False

# checkZero([1,2,4,3, 0])

'''============ 6. ============'''
''' 
### DONE Date: 25/10/2020 ###
Input   : train data & test data
Output  : hasil prediksi data test
Problem : -
''' 
def createProbabilityModel(listPredictionLabelTest, currentBinaryLabel, superMatrixClass0, superMatrixClass1, test_data, probClass0, probClass1):
    predictionLabelTest = list()
    # predictionLabelTest['label_number'] = currentBinaryLabel

    # |c| jumlah data belonging to the class c
    # totalDocClass0 = len(class0_train_index)
    # totalDocClass1 = len(class1_train_index)
    
    # # buat super matrix dan hitung probability tiap cell-nya | sampai ke rumus logPr(M_ij|c)
    # print("== creating super matrix class 0... ==")
    # superMatrixClass0 = createSuperMatrix(class0_train_index) 
    # print("== creating super matrix class 1... ==")
    # superMatrixClass1 = createSuperMatrix(class1_train_index)

    # display(superMatrixClass1)
    # print(checkZero(np.ravel(superMatrixClass1.values)))
    # '''
    
    print("\n")

    # looping untuk tiap-tiap testing data
    for i, dTest in enumerate(test_data):
        # mapping fitur data train ke data testing
        if type(superMatrixClass0) == str:
            # kalau matrix kelas 0 nya ga ada, otomatis di prediksi ke kelas 1
            predictionLabelTest.append(1)
            # predictionLabelTest[str(i)] = 1
            # listPredictionLabelTest.append(predictionLabelTest)
            continue # lanjut ke next data test
        elif type(superMatrixClass1) == str:
            # kalau matrix kelas 1 nya ga ada, otomatis di prediksi ke kelas 0
            predictionLabelTest.append(0)
            # predictionLabelTest[str(i)] = 0
            # listPredictionLabelTest.append(predictionLabelTest)
            continue # lanjut ke next data test

        testDataInClass0 = mapDataToClass(dTest, superMatrixClass0)
        testDataInClass1 = mapDataToClass(dTest, superMatrixClass1)

        print("# Testing Data ke : ", i+1)
        # display(testDataInClass0)
        # display(testDataInClass1)

        print("    - NILAI PROBABILITY")
        # hitung nilai probability untuk tiap kelasnya
        probabilityClass0 = calculateProbabilityDataTest(probClass0, testDataInClass0) 
        probabilityClass1 = calculateProbabilityDataTest(probClass1, testDataInClass1)

        # tampung prob di list
        listProb = [probabilityClass0, probabilityClass1]

        print("    - Nilai log(Prob) untuk Kelas 0 : ", probabilityClass0)
        print("    - Nilai log(Prob) untuk Kelas 1 : ", probabilityClass1)
        print("    > Max Value        : ", max(listProb))
        
        # tentuin classnya berdasarkan nomor indexnya
        classPrediction = listProb.index(max(listProb))
        predictionLabelTest.append(classPrediction)
        # predictionLabelTest[i] = classPrediction
        print("    @ Label Prediction : ", classPrediction)

    listPredictionLabelTest.append(predictionLabelTest)

    return listPredictionLabelTest
    # '''

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
def devideTrainDataByClass(train_index, currentBinaryLabel, data):
    class0_train_index, class1_train_index = list(), list()
    labelsAllAyat = data.iloc[:,4:20].values
    
    for i in train_index:      
        # print("Index Data Ke : ", i)
        # print("Label Datanya : ", labelsAllAyat[i])
        
        labelData = labelsAllAyat[i][currentBinaryLabel]
        # cek label datanya
        if labelData == 0:
            class0_train_index.append(i)
        else:
            class1_train_index.append(i)
    
    return class0_train_index, class1_train_index



'''============ 9. ============'''
''' 
### DONE Date: 22/10/2020 ###
Input   : listWeightedAyat
Output  : train data & test data
Problem : -
''' 
def splitData(data):
    totalData = 10 #dummy
    # totalData = len(data)
    # print("Jumlah Data : ", len(data))
    
    # ambil index ayat buat looping file
    listIndexData = list(range(totalData))
    # print(listIndexData)
    
    # Shuffle index ayat secara random
    # gunakan seed, agar hasil randomnya selalu sama
    random.seed(10)
    random.shuffle(listIndexData)
    # print(listIndexData)
    
    # jumlah data train
    percentValue = 0.8
    
    #index data train
    trainIndex = listIndexData[int(len(listIndexData) * 0) : int(len(listIndexData) * percentValue)]
    # print(trainIndex)
    
    # index data test
    testIndex = listIndexData[int(len(listIndexData) * percentValue) : int(len(listIndexData) * 1)]
    # print(testIndex)
    
    listAyatInString = data.Terjemahan.values[testIndex]
    labelsAllAyat = data.iloc[:,4:20].values[testIndex]
    
    # print(len(trainIndex))
    # print(len(testIndex))

    # list test data
    testData = []
    for i, ayat in enumerate(listAyatInString):
        testData.append({
          'token_ayat' : ast.literal_eval(listAyatInString[i]),
          'label_ayat' : labelsAllAyat[i]
        })
        
    # print(trainIndex)
    
    return trainIndex, testIndex, testData




#listWeightedAyat = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
# load data terms-by-concept matriks dari file bin
# selectedAyat = './assets/leskOutput/ayat_0'
# listWeightedAyat = readFileBin(leskOutputPath)

# ambil data terjemahannya dulu dari sheet
data = pd.read_excel(datapath, sheet_name='proceed-data')
# panggill fungsi main / entar pake ini
train_index, test_index, test_data = splitData(data)
print("test index : ", test_index)

# nama label untuk dataset
labelsName = list(range(16))
# inisialisasi dict untuk prediction result
listPredictionLabelTest = list()

# '''
# ALTERNATIF 1
for currentBinaryLabel in labelsName:
  print("Current Label : ", currentBinaryLabel)
  # kelompokkan data train berdasarkan kelasnya
  class0_train_index, class1_train_index = devideTrainDataByClass(train_index, currentBinaryLabel, data)
  
  print("class 0 train data : ", class0_train_index)
  print("class 1 train data : ", class1_train_index)

  # hitung probabilitas per kelasnya
  probClass0, probClass1 = calculateClassProbability(len(class0_train_index), len(class1_train_index), len(train_index))

  print("Prior Prob. Class 0 : ", probClass0)
  print("Prior Prob. Class 1 : ", probClass1)
  
  # buat super matrix dan hitung probability tiap cell-nya | sampai ke rumus logPr(M_ij|c)
  print("== creating super matrix class 0... ==")
  superMatrixClass0 = createSuperMatrix(class0_train_index) 
  print("== creating super matrix class 1... ==")
  superMatrixClass1 = createSuperMatrix(class1_train_index)

  # buat model probability menggunakan SNB untuk currentBinaryLabel
  listPredictionLabelTest = createProbabilityModel(listPredictionLabelTest, currentBinaryLabel, superMatrixClass0, superMatrixClass1, test_data, probClass0, probClass1)

  print("\n>>==============\n")

print("\nPrediction Label for Test Data : ", listPredictionLabelTest)
# '''


'''
# ALTERNATFIF 2
# ambil label ke-1 | diitung dari 0
currentBinaryLabel = 0 
print("Current Label : ", currentBinaryLabel)
# kelompokkan data train berdasarkan kelasnya
class0_train_index, class1_train_index = devideTrainDataByClass(train_index, currentBinaryLabel, data)

print("class 0 train data : ", class0_train_index)
print("class 1 train data : ", class1_train_index)

# # hitung probabilitas per kelasnya
probClass0, probClass1 = calculateClassProbability(len(class0_train_index), len(class1_train_index), len(train_index))

print("Prior Prob. Class 0 : ", probClass0)
print("Prior Prob. Class 1 : ", probClass1)

# buat super matrix dan hitung probability tiap cell-nya | sampai ke rumus logPr(M_ij|c)
print("== creating super matrix class 0... ==")
superMatrixClass0 = createSuperMatrix(class0_train_index) 
print("== creating super matrix class 1... ==")
superMatrixClass1 = createSuperMatrix(class1_train_index)

# buat model probability menggunakan SNB untuk currentBinaryLabel
listPredictionLabelTest = createProbabilityModel(listPredictionLabelTest, currentBinaryLabel, superMatrixClass0, superMatrixClass1, test_data, probClass0, probClass1)

print("\n>>==============\n")

print("\nPrediction Label for Test Data : ", listPredictionLabelTest)
'''



# def createSuperMatrix(dataPerClass):
#     # kalo datanya kosong untuk salah satu kelas-nya
#     if len(dataPerClass) == 0:
#         return 'empty'

#     # inisialisasi df kosong untuk dataPerClass
#     # ini bisa error kalo datanya kosong untuk salah satu kelas-nya, karena ada ini "dataPerClass[0]" > makanya cek dulu diatas
#     dfAccumulatorDataPerClass = pd.DataFrame(0.0, columns=dataPerClass[0]["weightedAyat"].columns, index=dataPerClass[0]["weightedAyat"].index)
#     # inisiasi variable untuk total penjumlahan cell keseluruhan pada class tersebut
#     accumulatorAllCells = 0
    
#     # looping untuk tiap data di class tersebut
#     for i, data in enumerate(dataPerClass):
#         print("data ke - {} / {}".format(i, len(dataPerClass)-1))
#         # jumahkan tiap cells di seluruh doc yang classnya sama rumusnya yang W*(t_i, s_j, c) -> matriks
#         dfAccumulatorDataPerClass = dfAccumulatorDataPerClass.add(data["weightedAyat"], fill_value=0)
    
#     # jumlahkan keseluruhan cells di seleuruh doc yang classnya sama sigma_t . sigma_s W*(t, s, c) + |V||S| -> float 
#     accumulatorAllCells += (dfAccumulatorDataPerClass.to_numpy().sum() / len(dataPerClass)) + (len(dataPerClass[0]['weightedAyat'].index) * len(dataPerClass[0]['weightedAyat'].columns))

#     # bagi setiap cell-nya dengan jumlah data train di kelas itu
#     dfAccumulatorDataPerClass = dfAccumulatorDataPerClass.div(len(dataPerClass))

#     # bagi lagi tiap cell-nya dengan nilai accumulator | Pr(M_ij|c) + 1 -> rumus probability cell
#     dfAccumulatorDataPerClass = dfAccumulatorDataPerClass.add(1).div(accumulatorAllCells)

#     # '''GAK PAKE LOG DULU'''
#     # log-kan setiap cell-nya | logPr(M_ij|c) -> rumus prob. cell pakai log
#     dfAccumulatorDataPerClass = dfAccumulatorDataPerClass.applymap(calculateLogCell)
#     # dari bentuk tuple, rubah lagi ke dataframe, agar supaya gampang ngolahnya
#     dfAccumulatorDataPerClass = pd.DataFrame(dfAccumulatorDataPerClass)
        
#     return dfAccumulatorDataPerClass
