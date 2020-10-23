# -*- coding: utf-8 -*-
# == ORIGINAL PACKAGES ==
from nltk.corpus import wordnet as wn
from nltk.tokenize import RegexpTokenizer
import pandas as pd
import numpy as np
import codecs
import pickle
import math
import glob
import ast
import sys
import re
import os
# == FILE AS PACKAGES ==
sys.path.insert(1, '../preparation/')  # import func from another file in other directory
import get_wikipedia as gw             # file preparation/get_wikipedia.py
import credentials as creds            # file preparation/credentials.py
import create_terms as ct              # file processing/create_terms
import preprocess as pr                # file processing/preprocess
import lesk_tfidf as leskTfIdf         # file processing/lesk_tfidf
# == MAIN FILE DRIVE ==
fileDriveName = "dummy-dataset-quran"  # "dataset-quran"


'''
Input    : wiki file
Output   : clean wiki file
Problem  : remove all non word and convert doc to one line
'''
def cleanWikiFile(linesTxt):
    # membuat file menjadi satu baris
    mystr = '\t'.join([line.strip() for line in linesTxt])
    # replace yang berlebih menjadi 1
    mystr = " ".join(mystr.split())
    # hapus char kecuali huruf
    mystr = re.sub('[^A-Za-z]+',' ', mystr)
    return mystr


'''
Input   : path to directory wiki
Output  : return 1 directory with one file tiap termsnya
'''
def mergeTermsFiles():
    termsDirList = gw.getListOfDirs()
    # hapus dir ke wikinya, karena masuk di list
    termsDirList.pop(0)
    
    for i, termDir in enumerate(termsDirList):
        termName = termDir[16:]
        fileNameList = glob.glob("{}/*.txt".format(termDir))
        with codecs.open('../../data/merge_wiki/{}.bin.txt'.format(termName), 'wb') as outfile:
            for fname in fileNameList:
                with codecs.open(fname, 'r', 'utf-8') as infile:
                    lines = infile.readlines()
                    # clean dari whitespcae hingga hanya words saja
                    cleanTxt = cleanWikiFile(lines)
                    # clean sampai jadi list kayak ayat alquran
                    listCleanTxt = pr.cleaningData(cleanTxt)
                    # save list ke file txt, biar mudah pas di read
                    pickle.dump(listCleanTxt, outfile)
        print("{}/{} {} : done".format(i, len(termsDirList)-1, termName))


'''
Input   : nama main folder buat nampung outputnya
Output  : folder data/wiki_bin page concepts window ( mirip kayak mergeTermsFiles() )
Problem : create folder dengan bin per pages
'''
def createConceptsFiles(nameMainDir = 'wiki_bin'):   
    gw.createDir(nameMainDir, path='../../data/')
    # list path of dirs
    termsDirList = gw.getListOfDirs()
    # hapus dir ke wikinya, karena masuk di list
    termsDirList.pop(0)
    
    for i, termDir in enumerate(termsDirList):
        termName = termDir[16:]
        fileNameList = glob.glob("{}/*.txt".format(termDir))
        # create directorynya
        gw.createDir(termName, path= "../../data/{}/".format(nameMainDir))
        for j, fname in enumerate(fileNameList):
            with codecs.open('../../data/{}/{}/{}_page_{}.bin.txt'.format(nameMainDir, termName, termName, j), 'wb') as outfile:
                with codecs.open(fname, 'r', 'utf-8') as infile:
                    lines = infile.readlines()
                    # clean dari whitespcae hingga hanya words saja
                    cleanTxt = cleanWikiFile(lines)
                    # clean sampai jadi list kayak ayat alquran
                    listCleanTxt = pr.cleaningData(cleanTxt)
                    # save list ke file txt, biar mudah pas di read
                    pickle.dump(listCleanTxt, outfile)
            print("{}/{} from {}/{} {} : done".format(j, len(fileNameList)-1, i, len(termsDirList)-1, termName))


'''
Input   : path to binary file of wiki page
Output  : return type list of file binary
'''
def readFileBin(path = ''):
    file = open(path, 'rb')
    object_file = pickle.load(file)
    return object_file
    # file.close()


'''
Input   : jumlah windowing, ayat dan target word (indexnya)
Output  : return words berdasarkan windowsnya
Problem : - untuk data yang kurang dari jumlah window yang saat itu digunakan ? return semuanya
          - cek dengan print dokumen dummy
          - gimana kalo posisi target ada di (awal, tengah, ujung)
'''
def windowing(idxTarget, tokenAyat, n_window):
    # 0 kalau ada minus
    left = 0 if((idxTarget - n_window) < 0) else (idxTarget - n_window)
    # len target kalau lebih dari length nya
    right = (len(tokenAyat) - 1) if((idxTarget + n_window) > (len(tokenAyat) - 1)) else (idxTarget + n_window)
    
    # ambil kata-kata di kiri
    leftWords = tokenAyat[left : idxTarget]
    # ambil kata-kata dikanan
    rightWords = tokenAyat[idxTarget+1 : right + 1]

    # gabungkan jadi satu array
    windowingWords = [tokenAyat[idxTarget]] + leftWords + rightWords
    
    # ========= PERUBAHAN PENTING NIH ===========
    # delete word yang duplikat ketika beada lam satu window
    # kasusnya ayat ke-5 word "thee" 
    windowingWordsClean = np.unique(np.array(windowingWords))
    
    #print('{} - {} - target : {} '.format(leftWords, rightWords, tokenAyat[idxTarget]))
    return windowingWordsClean


'''
Input   : -
Output  : list of terms
Problem : ambil terms wiki di  google sheet
'''
def getTerms():
    # ambil data terms dari drive
    listTerms= ct.getListTermsFromSheet(fileName=fileDriveName, wsNameUniqueWords="wiki-unique-words")
    return listTerms


'''
Input   : -
Output  : list concepts
Problem : ambil list nama file dari wikipedia data/wiki_bin
'''
def setConceptsPagesList(mainDirName = 'wiki_bin', outputFileName = 'concepts'):
    concepts = []
    # dir buat ngambil nama pages setiap concepts-nya
    dirNameList = glob.glob("../../data/{}/*".format(mainDirName))
    for dirName in dirNameList:
        for file in os.listdir(dirName):
            if file.endswith(".bin.txt"):
                concept = pd.DataFrame({'path' : [os.path.join(dirName, file)],'name' : [file[:-8]] })
                concepts.append(concept)
    with codecs.open("../../data/{}.bin.txt".format(outputFileName), 'wb') as outfile:
        pickle.dump(concepts, outfile)
    print(concepts)
    print(concepts[0].name)


def getConcepts():
    # buka file picklenya yang isinya itu dict concepts
    path = '../../data/concepts.bin.txt'
    concepts = readFileBin(path)
    conceptsName = np.ravel([concept.name.values.tolist() for concept in concepts])
    conceptsPath = np.ravel([concept.path.values.tolist() for concept in concepts])
    return conceptsName, conceptsPath

'''
Input   : - hasil ravel of list of tokenization definition from wordnet
Output  : Count of overlap
Problem : - cara ngitungnya gimana
''' 
def countOverlapDefinition(windowingWordsDef):
    ravelWindowingWordsDef = [item for sublist in windowingWordsDef for item in sublist]
    uniqueWordDef = list(set(ravelWindowingWordsDef))
    count = 0
    for uniqueWord in uniqueWordDef:
        checkWord = True
        for wordDef in windowingWordsDef:
            if uniqueWord not in wordDef:
                checkWord = False
                break
        if checkWord:
            count += 1
            # print(uniqueWord)
    return count



''' ========== DONE Date: 21/10/2020 =========='''
'''
Input   : insert vector target word ke matriks dataframe ayat
Output  : matriks dataframe ayat
Problem : -
''' 
def insertTargetWordVectorToDf(dfTermsConcepts, dictTargetWordVector):
    # ambil target word sembari hapus key-nya
    targetWord = dictTargetWordVector.pop('target_kata', None)
    # dict dijadikan array - mempermudah looping
    dictItems = dictTargetWordVector.items()
    
    # looping tiap items dict target word
    for i, item in enumerate(dictItems):
        # ambil pageName dari tuple item
        pageName = item[0]
        if pageName in dfTermsConcepts.columns:
            dfTermsConcepts.loc[targetWord, pageName] = dictTargetWordVector[pageName]
        else:
            dfTermsConcepts.loc[targetWord, pageName] = 0.0
        #print('INSERTED : ', i, ' / ', dfTermsConcepts.loc[targetWord, pageName])
    
    return dfTermsConcepts



''' ========== DONE Date: 21/10/2020 =========='''
'''
Input   : hitung concept vector untuk target word
Output  : Vector of target terms by concepts
Problem : -
''' 
def calculateTargetTermConceptVector(dfNormalizedWindowingConcepts, targetWord):
    # milai concept windows
    cw = len(dfNormalizedWindowingConcepts.index)
    # inisiasi untuk target vector
    dictTargetWordVector = dict()
    # masukkan target word ke dict
    dictTargetWordVector['target_kata'] = targetWord
        
    # iterate dataframe through columns
    for (columnName, columnData) in dfNormalizedWindowingConcepts.iteritems():
        sumOfVectorPage = columnData.values.sum()
        # hitung nilai rata-rata dari vector terms
        avgValueOfTargetWord = sumOfVectorPage / cw
        # masukkan nilai avg ke dict
        dictTargetWordVector[columnName] = avgValueOfTargetWord
            
    return dictTargetWordVector



''' ========== DONE Date: 21/10/2020 =========='''
'''
Input   : - windowingWords
Output  : Vector of terms by concepts
Problem : - ngitungnya
''' 
def countOverlapsConcept(windowingWords, targetWord, countOverlapsContext):
    tf = leskTfIdf.get_tf()
    dfDocFreq = leskTfIdf.get_df()
    
    listOfPages = tf.columns
    
    dfTermsWindowingConcepts = pd.DataFrame(0, index=windowingWords, columns=listOfPages)
    for page in listOfPages:
        for word in windowingWords:
            # Cell diisi jumlah term frequency + jumlah overlaps
            dfTermsWindowingConcepts.loc[word, page] = tf.loc[word, page] + countOverlapsContext
    
    # Normalize Matriks Term Frequency using IDF
    dfNormalizedWindowingConcepts = leskTfIdf.tf_idf(dfTermsWindowingConcepts, dfDocFreq)
    
    #with codecs.open("../../data/countOverlapsConcept_dummy.bin.txt", 'wb') as outfile:
        #pickle.dump(dfNormalizedWindowingConcepts, outfile) 
                
    return dfNormalizedWindowingConcepts



'''
Input   : - word
Output  : hasil ravel of list of tokenization definition from wordnet
Problem : - remove punct
          - return ravel dari list of definition of word in tokenization
'''   
def tokenizeWordnetDefinition(word):
    listOfDefinition = []
    definitions = wn.synsets(word)
    tokenizer = RegexpTokenizer(r'\w+')
    for d in definitions:
        listOfDefinition.append(tokenizer.tokenize(d.definition()))
    ravelListOfDefinition = [item for sublist in listOfDefinition for item in sublist]
    return ravelListOfDefinition



'''
Input   : - matrix zero dengan index terms dan kolom concepts
          - windowing words
          - target word
Output  : matrix terms-by-concepts yang sudah ada weight-nya dari target word pada suatu ayat
Problem : - weighting dengan wordnet
          - hitung overlapping dengan lesk algorithm
          - normalize dengan tf-idf
'''     
def termByConceptMatrixWeighted(windowingWords, dfTermsConcepts, targetWord):
    # Count Overlaps Context
    windowingWordsDef = []
    for w in windowingWords:
        tokenizedDef = tokenizeWordnetDefinition(w)
        windowingWordsDef.append(tokenizedDef)
    countOverlapsContext = countOverlapDefinition(windowingWordsDef)
    
    # Count Overlaps Concept
    dfNormalizedWindowingConcepts = countOverlapsConcept(windowingWords, targetWord, countOverlapsContext)
    
    # hitung vector term concept untuk target word
    # return isi vector buat yang target word aja dalam bentuk dictionary
    dictTargetWordVector = calculateTargetTermConceptVector(dfNormalizedWindowingConcepts, targetWord)
    
    # function buat masukin vector target word ke dataframe terms concept ayat
    dfTermsConcepts = insertTargetWordVectorToDf(dfTermsConcepts, dictTargetWordVector)
    
    # print(windowingWordsDef)
    # Main Weighting
    # WordNet
    return dfTermsConcepts



'''
Input   : token ayat dan jumlah windowing
Output  : matrix terms-by-concepts dari suatu ayat
Problem : - jumlah overlaps menggunakan wordNet 
          - jumlah kata di page, sesuai dengan jumlah konsepnya
          - jumlah setiap term muncul di beberapa dokumen wikipedia (DF)
'''
def weighting(tokenAyat, n_window):
    print('- Creating DataFrame Terms Concept...')
    # definisikan concepts
    listConcepts, _ = getConcepts()
    # definisikan terms dengan --- function getTerms() ---
    listTerms = getTerms()
    # inisialisasi matrix kosongnya dulu
    dfTermsConcepts = pd.DataFrame(0, index=listTerms, columns=listConcepts)
    
    #print(dfTermsConcepts)
    
    print('- Windowing & Weighting...')
    # looping for every word as target words
    for idxTarget, targetWord in enumerate(tokenAyat):
        print('  # Terget Word {}/{}'.format(idxTarget, len(tokenAyat)-1))
        print('    Target Word : {}'.format(targetWord))
        # --- function windowing() ---
        print('    - Windowing...')
        windowingWords = windowing(idxTarget, tokenAyat, n_window)
        print('    Windowing Words : {}'.format(windowingWords))
        # --- function termByConceptMatrixWeighted() ---
        print('    - Weighting...')
        # looping recursive buat ngisi nilai si dfTermsConcepts-nya
        dfTermsConcepts = termByConceptMatrixWeighted(windowingWords, dfTermsConcepts, targetWord)
        
    return dfTermsConcepts

    # Lakukan proses weighting disetiap pages untuk setiap termsnya
    # weight untuk target word (rumusnya ada di dokumen / catetan)
    # setiap term akan memiliki weight dalam vector (concept vector) dengan panjang |wiki pages|



'''
Input   : file dataset
Output  : matrices of terms-by-concept sebanyak documents
Problem : - looping tiap ayat (doc)
          - untuk setiap ayatnya, lakukan weighting oleh def yg lain
'''
def leskAlgorithm(n_window = 2):
    # declare list buat nampung ayat yang udah di weighted
    listWeightedAyat = []
    # ambil data dari drive
    ayatInString = creds.getAsDataframe(fileDriveName, 'proceed-data').Terjemahan.values
    labelsAllAyat = creds.getAsDataframe(fileDriveName, 'proceed-data').iloc[:,4:20].values
    
    # Looping datanya
    for idx, ayat in enumerate(ayatInString):
        # create dictionary for every ayat
        dictPerAyat = dict()
        
        # insert label ayat to dict
        dictPerAyat["labelsPerAyat"] = labelsAllAyat[idx]
                        
        print('==== AYAT - {}/{} ===='.format(idx, len(ayatInString)-1))
        # ubah string ke bentuk array
        tokenAyat = ast.literal_eval(ayat)
        
        # --- weighting pake function weighting() ---
        print('# Lesk Algorithm...')
        weightedAyat = weighting(tokenAyat, n_window)
        
        # insert weighted ayat ke dictionary per ayat
        dictPerAyat["weightedAyat"] = weightedAyat
        
        # append weighted ayat ke list
        listWeightedAyat.append(dictPerAyat)

#        return weightedAyat
    
    return listWeightedAyat



''' ========== DONE Date: 21/10/2020 =========='''
'''
Input   : term by concept matrices
Output  : saved model in .bin.txt
Problem : -
''' 
def saveTermsByConceptMatrices(listWeightedAyat, outputFileName = 'terms_by_concept_dummy'):
    with codecs.open("../../data/{}.bin.txt".format(outputFileName), 'wb') as outfile:
        pickle.dump(listWeightedAyat, outfile) 



if __name__ == '__main__':
    # for word in wn.words():
    #     print(word)
    # print(syns[0].definition())
    # print(syns)
      
    n_window = 2
    listWeightedAyat = leskAlgorithm(n_window)
    saveTermsByConceptMatrices(listWeightedAyat)
    
#    listConcepts, _ = getConcepts()
#    # definisikan terms dengan --- function getTerms() ---
#    listTerms = getTerms()
#    # inisialisasi matrix kosongnya dulu
#    dfTermsConcepts = pd.DataFrame(0, index=listTerms, columns=listConcepts)
    
    
#    windowingWords = ['name', 'allah', 'beneficent']
#    windowingWords = ['thee', 'serve', 'thee', 'beseech', 'help']
#    targetWord = 'thee'
#    countOverlapsContext = 1
#    dfCountOverlapsConcept = countOverlapsConcept(windowingWords, targetWord, countOverlapsContext)
#    
#    targetWordDict = calculateTargetTermConceptVector(dfCountOverlapsConcept, targetWord)
    
#    dfTermsConceptsNew = insertTargetWordVectorToDf(dfTermsConcepts, targetWordDict)
      
    
    '''
    # Get unique words from google sheet
    df = getUniqueWords()
    for val in df.iloc[:,0].values:
        if val == True:
            print(val)
    '''
    
    
    
    
    
    
    
    
'''
def old_windowing(idxTarget, tokenAyat, n_window):
    # check n_window apakan ganjil atau genap
    # kalau genap, tambah 1 biar ganjil - dipaksakan
    if(n_window % 2) == 0:
        n_window += 1
    # kalau ganjil
    if(n_window % 2) == 1:
        half_window = math.floor(n_window/2)
        # 0 kalau ada minus
        left = 0 if((idxTarget - half_window) < 0) else (idxTarget - half_window)
        # len target kalau lebih dari length nya
        right = (len(tokenAyat) - 1) if((idxTarget + half_window) > (len(tokenAyat) - 1)) else (idxTarget + half_window)
        
        # ambil kata-kata di kiri
        leftWords = tokenAyat[left : idxTarget]
        # ambil kata-kata dikanan
        rightWords = tokenAyat[idxTarget+1 : right + 1]
    
        # gabungkan jadi satu array
        windowingWords = [tokenAyat[idxTarget]] + leftWords + rightWords
        
        #print('{} - {} - target : {} '.format(leftWords, rightWords, tokenAyat[idxTarget]))
        return windowingWords
'''