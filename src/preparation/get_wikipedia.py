# -*- coding: utf-8 -*-
import os
import sys
import warnings
warnings.filterwarnings("ignore")
# import func from another file in other directory
sys.path.insert(1, '../processing/')
# import get unique words
import create_terms as ct
import wikipedia
import wikipediaapi
from glob import glob
from pathlib import Path

def getPageNameList(someWord):
    pageTitles = wikipedia.search(someWord)
    titleList = []
    for title in pageTitles:
        try:
            wikipedia.page(title)
            titleList.append(title)
        except wikipedia.exceptions.DisambiguationError: # as e:
            continue
            # CUKUP LEVEL 1 AJA
            #for disamTitle in e.options:
            #    if ('disambiguation' not in disamTitle.lower()):
            #        titleList.append(disamTitle)
        except wikipedia.exceptions.PageError:
            continue
    return titleList

def createDir(dirName, path= "../../data/wiki/"):
    try:
        os.mkdir(path+dirName) 
        print("Directory '%s' created" %dirName) 
        return str(path+dirName)
    except FileExistsError:
        print("Directory " , dirName ,  " already exists")
        return str(path+dirName)

def saveSummaryToTxt(title, summary, pathDir):
    # di encoding='utf-8' biar semua format str bisa di masukin ke file
    fileName = open(pathDir+"/"+str(title)+".txt", "w+", encoding='utf-8')
    fileName.write(summary)
    fileName.close()


def getArticleByWord(someWord, errwords):
    try:
        # Create dir for someWord
        pathDir = createDir(someWord)
        # get list of page related to someWord
        titleList = getPageNameList(someWord)
        # Remove duplicate page title in list
        titleList = list(dict.fromkeys(titleList))
        for t in titleList:
            try:
                wiki = wikipediaapi.Wikipedia('en')
                summaryPage = wiki.page(t).text
                #print(len(summaryPage), " -- Type : ", type(summaryPage), " -- Titile : ", t, "\n", summaryPage)
                if summaryPage:
                    saveSummaryToTxt(t, summaryPage, pathDir)
            except:
                continue
    except:
        errwords.write(someWord+"\n")
        

def collectWikiArticle(uWords, loop):
    errWordsPath = open("../../data/raw/unlistTermsError("+str(loop)+").txt", "w+", encoding='utf-8')
    for i, word in enumerate(uWords):
        # get a wikipedia page per term
        getArticleByWord(str(word), errWordsPath)
        print(i, ". {} - created.".format(str(word)))
    errWordsPath.close()

def getListOfWiki():
    folderName = glob("../../data/wiki/*/")
    gotTerms = [f[16:-1] for f in folderName]
    
    return gotTerms

def unlistTerms():
    listTerms = ct.getListTermsFromSheet(wsNameUniqueWords = "unique-words")
    wikiTerms = getListOfWiki()
    
    disjoinTerms = list(set(listTerms) - set(wikiTerms))
    
    return disjoinTerms

def getListOfDirs(dirName = '../../data/wiki'):
    # Create a List    
    listOfDirs = list()
     
    # Iterate over the directory tree and check if directory is empty.
    for (dirpath, dirnames, filenames) in os.walk(dirName):
        listOfDirs.append(dirpath)   
    return listOfDirs

def getListOfEmptyDirs():
    dirName = '../../data/wiki';
    # Create a List    
    listOfEmptyDirs = list()
     
    # Iterate over the directory tree and check if directory is empty.
    for (dirpath, dirnames, filenames) in os.walk(dirName):
        if len(dirnames) == 0 and len(filenames) == 0 :
            listOfEmptyDirs.append(dirpath)   
    return listOfEmptyDirs

def removeEmptyDirs(listOfEmptyDirs): 
    
    for eachDir in listOfEmptyDirs:
        dir_path = Path(eachDir)
        try:
            dir_path.rmdir()
        except OSError as e:
            print("Error: %s : %s" % (dir_path, e.strerror))      

def main():
    termsList = getListOfWiki()
#    termSheet = ct.getListTermsFromSheet(wsNameUniqueWords = "wiki-unique-words")

#    print(len(termsList))
#    
#    listOfDirs = getListOfDirs()
#    
#    print(len(listOfDirs))
#    listOfEmptyDirs = getListOfEmptyDirs()
#    
#    print(len(listOfEmptyDirs))
#    print(listOfEmptyDirs)
#    removeEmptyDirs(listOfEmptyDirs)
#    
#    print(unlistTerms)
#
#    collectWikiArticle(unlistTerms, 0) 
#    
#    ratioAwal = 0
#    ratio = 100
#    i = 0
#    
#    while i < 12:
#        collectWikiArticle(unlistTerms[ratioAwal:ratio], i) 
#        ratioAwal = ratio
#        ratio += 100
#        i += 1
      
if __name__ == '__main__' :
    main()
    
    







