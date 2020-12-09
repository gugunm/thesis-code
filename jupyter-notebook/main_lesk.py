# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import pickle
import math
import re
import ast
import sys
import gzip

np.set_printoptions(threshold=sys.maxsize)

from nltk.corpus import wordnet as wn

import nltk
nltk.download('wordnet')

#real dataset
datapath = './dataset/dataset-quran.xlsx'

#concept path buat di drive
conceptpath = './assets/conceptInDrive.xlsx' 

### for real data ###
TfResultPath = "./assets/CompressedTfResultPath.bin"
DfResultPath = "./assets/CompressedDfResultPath.bin"
TfIdfResultPath = "./assets/TfIdfResultPath.bin.txt"

# wordembedLeskPath = "./assets/realTrainWordembedModel.bin.txt"

# GANTI KALO CW nya BEDA
leskOutputPath = './assets/leskOutput_cw_5/ayat'


'''=== PARALEL RUNNING ==='''
# Running Ke-1
# startAyat = 0
# endAyat = 1000

# Running Ke-2
# startAyat = 1000
# endAyat = 2000

# Running Ke-3
# startAyat = 2000
# endAyat = 3000

# Running Ke-4
# startAyat = 3000
# endAyat = 4000

# Running Ke-5
startAyat = 4118
endAyat = 5000

# # Running Ke-6
# startAyat = 5000
# endAyat = 5300

# # Running Ke-7
# startAyat = 5300
# endAyat = 5600

# # Running Ke-8
# startAyat = 5600
# endAyat = 5900

# Running Ke-9 - terakhir
# startAyat = 7000


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


'''=== LOAD TF AND IDF FILE ==='''
# RUBAH TYPENYA AGAR LEBIH KECIL SIZE-NYA
#*** ubah path ini kalo dipake buat data real
tf = load_zipped_pickle(TfResultPath)
tf = tf.astype('uint8')
#*** ubah path ini kalo dipake buat data real
dfDocFreq = load_zipped_pickle(DfResultPath)
dfDocFreq = dfDocFreq.astype('float16')
# docs = tf.columns

# UNTUK NORMALIZE LESK ALGORITHM
def tf_idf(dictTermsWindowingConcepts):
    listOfTerms = dfDocFreq.index
    # Iterating over keys 
    for state in dictTermsWindowingConcepts: 
        if state in listOfTerms:
            dictTermsWindowingConcepts[state] = np.array(dictTermsWindowingConcepts[state])*dfDocFreq.loc[state, 'docfreq']
        else:
            # kalo wordnya ga ada, defaultnya 1
            dictTermsWindowingConcepts[state] = np.array(dictTermsWindowingConcepts[state])* math.log10(40147/1)
    return dictTermsWindowingConcepts



'''=== LESK ALGORITHM ==='''
# INI YANG BARU DIUBAAAAAHAHHHHH
def calculateTargetTermConceptVector(dictNormalizedWindowingConcepts, targetWord):
    # milai concept windows
    '''Ada Kesalahan, Nilai Vector Targetnya Belum Dibagi Jumlah Concept Windows'''
    cw = len(dictNormalizedWindowingConcepts)
    # inisiasi untuk target vector
    vectorTargetWord = []

    for i, state in enumerate(dictNormalizedWindowingConcepts):
        if i == 0:
            vectorTargetWord = dictNormalizedWindowingConcepts[state]
        else:
            vectorTargetWord = np.add(vectorTargetWord, dictNormalizedWindowingConcepts[state])
    
    # print(targetWord, "\n")
    # display(vectorTargetWord)
    
    return vectorTargetWord


# INI YANG BARU DIUBAAAAAHAHHHHH
def countOverlapsConcept(windowingWords, countOverlapsContext):
    listOfPages = tf.columns
    
    listOfTerms = tf.index
    
    dictTermsWindowingConcepts = {}
    
    # print("countOverlapsContext : ", countOverlapsContext)
    for word in windowingWords:        
        windowWordVector = []
        for page in listOfPages:
            # Cell diisi jumlah term frequency + jumlah overlaps
            if word in listOfTerms:
                windowWordVector.append(tf.loc[word, page] + next(item for item in countOverlapsContext if item["word"] == word)['overlap'])
            else:
                windowWordVector.append(0 + next(item for item in countOverlapsContext if item["word"] == word)['overlap'])
        dictTermsWindowingConcepts[word] = windowWordVector
    
    # data = {'row_1': [3, 2, 1, 0], 'row_2': ['a', 'b', 'c', 'd']}
    # Normalize Matriks Term Frequency using IDF
    dictNormalizedWindowingConcepts = tf_idf(dictTermsWindowingConcepts)

    return dictNormalizedWindowingConcepts


def countOverlapDefinition(windowingWords, windowingWordsDef):
    windowOverlaps = []
    for word in windowingWords:
        # nntinya buat dihapus bergantian, sesuai word saat ini
        listWindowingWords = windowingWords.tolist().copy()
        # ambil element windowingDef berdasarkan kata saat ini
        wordDef = next(item for item in windowingWordsDef if item["word"] == word)
        # hitung overlaps concept window dengan definisi kata-nya
        countOverlap = 0
        listWindowingWords.remove(word)
        for el in listWindowingWords:
            # cari string word di definition, ambil panjang arraynya
            countSearchRegex = len(re.findall("{}".format(el), wordDef['def']))
            countOverlap += countSearchRegex
        windowOverlaps.append({
            "word": word,
            "overlap": countOverlap
        })
    return windowOverlaps


def tokenizeWordnetDefinition(word):
    listOfDefinition = []
    # ngambil list definition dari suatu word
    definitions = wn.synsets(word)
    for d in definitions:
        # clean def dari non-alphabet
        strDef = re.sub('[^A-Za-z]+',' ', d.definition())
        listOfDefinition.append(strDef)
    # join semua definisi ke satu str
    ravelListOfDefinition = " ".join(listOfDefinition)
    return ravelListOfDefinition


 
def termByConceptMatrixWeighted(windowingWords, targetWord):
    # Count Overlaps Context
    windowingWordsDef = []
    for w in windowingWords:
        # tokenizedDef harusnya bentuknya dict, nyimpe wordnya apa, dan token definisinya
        tokenizedDef = tokenizeWordnetDefinition(w)
        wordDef = {
            "word": w,
            "def": tokenizedDef
        }
        windowingWordsDef.append(wordDef)

    # print("## WORD DEF ", windowingWordsDef)
        
    # Count Overlaps WordNet
    # windowingWordsDef = [{'word': 'name', 'def': 'merciful beneficent beneficent a language unit by which a person or thing is known a person s reputation family based on male descent a well known or notable person by the sanction or authority of a defamatory or abusive word or phrase assign a specified usually proper proper name to give the name or identifying characteristics of refer to by name or some other identifying characteristic property charge with a function charge to be create and charge with a task or function mention and identify by name make reference to identify as in botany or biology for example give or make a list of name individually give the names of determine or distinguish the nature of a problem or an illness through a diagnostic analysis'}, {'word': 'allah', 'def': 'Muslim name for the one and only God'}, {'word': 'beneficent', 'def': 'doing or producing good generous in assistance to the poor'}, {'word': 'merciful', 'def': 'showing or giving mercy  used conventionally of royalty and high nobility gracious allah'}]
    # windowingWords = ['name', 'allah', 'beneficent', 'merciful']
    print('       - Count Overlaps...')
    countOverlapsContext = countOverlapDefinition(windowingWords, windowingWordsDef)
    # print(countOverlapsContext)
        
    print('       - Normalized Concept...')
    # Count Overlaps Concept
    dictNormalizedWindowingConcepts = countOverlapsConcept(windowingWords, countOverlapsContext)
    
    # print(dictNormalizedWindowingConcepts)
       
    print('       - Target Word Vector...')
    # hitung vector term concept untuk target word
    # return isi vector buat yang target word aja dalam bentuk dictionary
    targetWordVector = calculateTargetTermConceptVector(dictNormalizedWindowingConcepts, targetWord)
    
    #******* PRINT
    # print("TARGET WORD VECTOR : ", targetWordVector)

    return targetWordVector



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
    # delete word yang duplikat ketika berada dalam satu window
    # kasusnya ayat ke-5 word "thee" 
    windowingWordsClean = np.unique(np.array(windowingWords))
    
    #print('{} - {} - target : {} '.format(leftWords, rightWords, tokenAyat[idxTarget]))
    return windowingWordsClean



# INI BARU DIUBAAAAAAAAAAAAAHHHH
def weighting(tokenAyat, n_window):    
    '''Bikin list page yang ada di dummy, delete line ini kalo buat real'''
    # pageDummyList = []
    # for pageName in dfConcept.name:
    # if re.split("\_", pageName)[0] in listTerms:
    #     pageDummyList.append(pageName)

    print('- Creating DataFrame Terms Concept...')
    # inisialisasi matrix kosongnya dulu untuk matriks terms-by-concept, untuk yang real
    dfTermsConcepts = pd.DataFrame(0, index=list(range(len(dfConcept.name))) , columns=listTerms)
    dictTermsConcepts = {}

    '''pake column yang dummy, delete line ini kalo buat real'''
    # dfTermsConcepts = pd.DataFrame(0, index=listTerms, columns=pageDummyList)


    print('- Windowing & Weighting...')
    # looping for every word as target words
    for idxTarget, targetWord in enumerate(tokenAyat):
        print('  # Terget Word {}/{}'.format(idxTarget, len(tokenAyat)-1))
        print('    Target Word : {}'.format(targetWord))
        # --- function windowing() ---
        print('    - Windowing...')
        windowingWords = windowing(idxTarget, tokenAyat, n_window)
        print('      Windowing Words : {}'.format(windowingWords))
        # --- function termByConceptMatrixWeighted() ---
        print('    - Weighting...')
        # looping recursive buat ngisi nilai si dfTermsConcepts-nya
        targetWordVector = termByConceptMatrixWeighted(windowingWords, targetWord)

        dictTermsConcepts[targetWord] = targetWordVector
        # #*** Nyoba 1 target word
        #return dfTermsConcepts

    # print("dictTermsConcepts : ", dictTermsConcepts)
    
    # ===== CATATAAAAAN ====
    # replace column di dictTermsConcepts yang ada di token ayat
    for term in dictTermsConcepts:
        # dfTermsConcepts.iloc[listTerms.index(term)] = dictTermsConcepts[term]
        dfTermsConcepts[term] = dictTermsConcepts[term]
    
    # Rubah dtypes biar ga terlalu gede sizenya
    dfTermsConcepts = dfTermsConcepts.astype('float16')
    
    # display(dfTermsConcepts)
      
    return dfTermsConcepts 




def leskAlgorithm(n_window = 2):
    # declare list buat nampung ayat yang udah di weighted
    # listWeightedAyat = []
    
    # AYAT YANG INGIN DIGUNAKAN
    # ambil data dari drive
    ayatInString = pd.read_excel(datapath, sheet_name='proceed-data').Terjemahan.values[startAyat : endAyat]
    labelsAllAyat = pd.read_excel(datapath, sheet_name='proceed-data').iloc[:,4:20].values[startAyat : endAyat]
    
    
    # Looping datanya
    for idx, ayat in enumerate(ayatInString):
        # create dictionary for every ayat
        dictPerAyat = dict()

        # insert label ayat to dict
        dictPerAyat["labelsPerAyat"] = np.uint8(labelsAllAyat[idx]) # labelsAllAyat[idx]
        
        idx = idx + startAyat

        print('==== AYAT - {}/{} ===='.format(idx, endAyat-1))
        # ubah string ke bentuk array
        tokenAyat = ast.literal_eval(ayat)

        # --- weighting pake function weighting() ---
        print('# Lesk Algorithm...')
        weightedAyat = weighting(tokenAyat, n_window)


        # insert weighted ayat ke dictionary per ayat
        # dibalik column dan indexnya
        dictPerAyat["weightedAyat"] = weightedAyat

        # append weighted ayat ke list
        # listWeightedAyat.append(dictPerAyat)
        
        
        save_zipped_pickle(dictPerAyat, idx, leskOutputPath)

        #*** Nyoba 1 Ayat
        # return weightedAyat
  
    return 0 # listWeightedAyat



    # idx = 0

    # ayat = ayatInString[idx]
    # # create dictionary for every ayat
    # dictPerAyat = dict()

    # # insert label ayat to dict
    # dictPerAyat["labelsPerAyat"] = labelsAllAyat[idx]
    
    # print(np.uint8(labelsAllAyat[idx]))
    # print(labelsAllAyat[idx])

    # print('==== AYAT - {}/{} ===='.format(idx, len(ayatInString)-1))
    # # ubah string ke bentuk array
    # tokenAyat = ast.literal_eval(ayat)

    # # --- weighting pake function weighting() ---
    # print('# Lesk Algorithm...')
    # weightedAyat = weighting(tokenAyat, n_window)

    # # insert weighted ayat ke dictionary per ayat
    # # dibalik column dan indexnya
    # dictPerAyat["weightedAyat"] = weightedAyat
    
    
    # save_zipped_pickle(dictPerAyat, idx, leskOutputPath)

    # # append weighted ayat ke list
    # # listWeightedAyat.append(dictPerAyat)
  
    # # print(listWeightedAyat)
    # # listWeightedAyat
    # return 0


n_window = 5
leskAlgorithm(n_window)

