# -*- coding: utf-8 -*-
'''
DISCLAIMER : FILE INI DIGUNAKAN SEBELUM MASUK KE LESK ALGORITHM, UNTUK MERAPIKAN DATA YANG DIPEROLEH DARI WIKIPEDIA PAGES
'''
# == ORIGINAL PACKAGES ==
import re
import glob
import sys
import codecs
import pickle
import os
import pandas as pd
# == FILE AS PACKAGES ==
sys.path.insert(1, '../preparation/')  # import func from another file in other directory
import get_wikipedia as gw             # file preparation/get_wikipedia.py
import preprocess as pr                # file processing/preprocess





'''============ 1. ============'''
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




'''============ 2. ============'''
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





'''============ 3. ============'''
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
    return 0





'''============ 4. ============'''
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





'''============ 5. ============'''
if __name__ == '__main__':
    print(0)













