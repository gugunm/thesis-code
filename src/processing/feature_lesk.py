# -*- coding: utf-8 -*-
import pandas as pd
import sys
# import func from another file in other directory
sys.path.insert(1, '../preparation/')
# file get_wikipedia
import get_wikipedia as gw
# file preprocess
import preprocess as pr
import codecs
import pickle
import glob
import re

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
Input   : path to binary file of wiki page
Output  : return type list of file binary
'''
def readWikiPage(path = '../../data/merge_wiki/aba.bin.txt'):
    file = open(path, 'rb')
    object_file = pickle.load(file)
    print(object_file)
    file.close()

'''
Input   : jumlah windowing dan ayat alquran
Output  : return array sebanyak windownya
Problem : - untuk data yang kurang dari jumlah window yang saat itu digunakan ?
          - cek dengan print dokumen dummy
'''
def windowing(doc, n_window):
    test = 1
    print(test)
    # periksa dulu

'''
Input   : seluruh pages dan func winidowingPage
Output  : setiap window beserta weightnya per term
Problem : - jumlah overlaps menggunakan wordNet 
          - jumlah kata di page, sesuai dengan jumlah konsepnya
          - jumlah setiap term muncul di beberapa dokumen wikipedia (DF)
'''
def weighting():
    test = 1
    print(test)
    # Ambil target word dari hasil return func windowing()
    # Looping satu-persatu
    # Lakukan proses weighting disetiap pages untuk setiap termsnya
    # weight untuk target word (rumusnya ada di dokumen / catetan)
    # setiap term akan memiliki weight dalam vector (concept vector) dengan panjang |wiki pages|

if __name__ == '__main__':
    mergeTermsFiles()
    
    '''
    # Get unique words from google sheet
    df = getUniqueWords()
    for val in df.iloc[:,0].values:
        if val == True:
            print(val)
    '''
