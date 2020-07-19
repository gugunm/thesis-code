# -*- coding: utf-8 -*-
import pandas as pd
import sys
# import func from another file in other directory
sys.path.insert(1, '../preparation/')
# file get_wikipedia
import get_wikipedia as gw
# file credentials
import credentials as creds
# file preprocess
import preprocess as pr
# file create_terms
import create_terms as ct
import codecs
import pickle
import glob
import re
import ast
import math
import os

# NAMA FILE DRIVE
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
def createConceptsFiles(nameMainDir = 'bin_wikipedia'):   
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
def readWikiPage(path = '../../data/merge_wiki/aba.bin.txt'):
    file = open(path, 'rb')
    object_file = pickle.load(file)
    print(object_file)
    # file.close()


'''
Input   : jumlah windowing, ayat dan target word (indexnya)
Output  : return words berdasarkan windowsnya
Problem : - untuk data yang kurang dari jumlah window yang saat itu digunakan ? return semuanya
          - cek dengan print dokumen dummy
          - posisi target ada di (awal, tengah, ujung)
'''
def windowing(idxTarget, tokenAyat, n_window):
    # check n_window apakan ganjil atau genap
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
        arrWindowing = [tokenAyat[idxTarget]] + leftWords + rightWords
        
        #print('{} - {} - target : {} '.format(leftWords, rightWords, tokenAyat[idxTarget]))
        print(arrWindowing)


'''
Input   : - matrix zero dengan index terms dan kolom concepts
          - windowing words
Output  : matrix terms-by-concepts yang sudah ada weight-nya
Problem : - weighting dengan wordnet
          - hitung overlapping dengan lesk algorithm
          - normalize dengan tf-idf
'''
def termByConceptMatrixWeighted(windowingWords, dfTermsConcepts):     
    print('termByConceptMatrixWeighted')


'''
Input   : -
Output  : list of terms
Problem : ambil terms wiki di  google sheet
'''
def getTerms():
    # ambil data terms dari drive
    listTerms= ct.getListTermsFromSheet(fileName=fileDriveName, wsNameUniqueWords="wiki-unique-words")
    print(listTerms)


'''
Input   : -
Output  : list concepts
Problem : ambil list nama file dari wikipedia data/wiki_bin
'''
def setConceptsPagesList(mainDirName = 'wiki_bin', outputFileName = 'concepts'):
    concepts = []
    dirNameList = glob.glob("../../data/{}/*".format(mainDirName))
    for dirName in dirNameList:
        for file in os.listdir(dirName):
            if file.endswith(".bin.txt"):
                concepts.append({
                        "path" : os.path.join(dirName, file), #print(os.path.join(dirName, file))
                        "name" : file #print(file)
                        })
    with codecs.open("../../data/{}.bin.txt".format(outputFileName), 'wb') as outfile:
        pickle.dump(concepts, outfile)
    print(concepts)


def getConcepts():
    # buka file picklenya yang isinya itu dict concepts
    print('ok')


'''
Input   : token ayat dan jumlah windowing
Output  : matrix terms-by-concepts dari suatu ayat
Problem : - jumlah overlaps menggunakan wordNet 
          - jumlah kata di page, sesuai dengan jumlah konsepnya
          - jumlah setiap term muncul di beberapa dokumen wikipedia (DF)
'''
def weighting(tokenAyat, n_window):
    # definisikan concepts
    listConcepts = [1, 2, 3]
    # definisikan terms dengan --- function getTerms() ---
    listTerms = getTerms()
    # inisialisasi matrix kosongnya dulu
    dfTermsConcepts = pd.DataFrame(0, index=listTerms, columns=listConcepts)
    
    print(dfTermsConcepts)
    
    # looping for every word as target words
    for idxTarget, targetWord in enumerate(tokenAyat):
        # --- function windowing() ---
        windowingWords = windowing(idxTarget, tokenAyat, n_window)
#        return windowingWords
    # Ambil target word dari hasil return func windowing()
    # Looping satu-persatu
    # Lakukan proses weighting disetiap pages untuk setiap termsnya
    # weight untuk target word (rumusnya ada di dokumen / catetan)
    # setiap term akan memiliki weight dalam vector (concept vector) dengan panjang |wiki pages|

'''
Input   : file dataset
Output  : matrices of terms-by-concept sebanyak documents
Problem : - looping tiap ayat (doc)
          - untuk setiap ayatnya, lakukan weighting oleh def yg lain
'''
def leskAlgorithm(n_window = 5):
    # ambil data dari drive
    ayatInString = creds.getAsDataframe(fileDriveName, 'proceed-data').Terjemahan.values
    
    # Looping datanya
    for ayat in ayatInString:
        tokenAyat = ast.literal_eval(ayat)
        # --- weighting pake function weighting() ---
        weightedAyat = weighting(tokenAyat, n_window)
        # return matrix of ayat
#        print(weightedAyat)
        print("====")
#        break
    


if __name__ == '__main__':
    setConceptsPagesList()
#    n_window = 5
#    leskAlgorithm(n_window)
    
    '''
    # Get unique words from google sheet
    df = getUniqueWords()
    for val in df.iloc[:,0].values:
        if val == True:
            print(val)
    '''