# -*- coding: utf-8 -*-
import credentials as creds
import get_wikipedia as gw
import pandas as pd
import ast
import gspread_dataframe as gd
import sys
# import func from another file in other directory
sys.path.insert(1, '../preparation/')




'''======= SETTINGS ======='''
# == MAIN FILE DRIVE ==
fileDriveName = "dummy-dataset-quran"
#fileDriveName = "dataset-quran"





'''============ 1. ============'''
'''
Desc    : Bikin unique word dari data, cukup lakukan sekali
'''
def createUniqueWords(fileName=fileDriveName,
                      wsNameCleanData="proceed-data",
                      wsNameUniqueWords="unique-words"
                      ):
    uWords = []
    dfClean = creds.getAsDataframe(fileName, wsNameCleanData)
    wsUniqueWords = creds.getWorksheet(
        creds.credentialGoogle(), fileName, wsNameUniqueWords)
    # convert dataframe ayat alquran to list
    listCleanToken = dfClean.iloc[:, 3].apply(ast.literal_eval)
    for terms in listCleanToken:
        for term in terms:
            if term not in uWords:
                uWords.append(term)
    dfUWords = pd.DataFrame(uWords, columns=["terms"])
    # Real data Already proceed then store in sheet "proceed-data"
    gd.set_with_dataframe(wsUniqueWords, dfUWords, allow_formulas=False)
    return dfUWords




'''============ 2. ============'''
'''
Desc    : Bikin unique word yang punya page di wikipedia, cukup lakukan sekali
'''
def createWikipediaUniqueWords(wikiUniqueWords,
                               fileName=fileDriveName,
                               wsWikiUniqueWords="wiki-unique-words",
                               ):
    wsWikiUniqueWords = creds.getWorksheet(
        creds.credentialGoogle(), fileName, wsWikiUniqueWords)
    dfWikiUniqueWords = pd.DataFrame(wikiUniqueWords, columns=["terms"])

    gd.set_with_dataframe(
        wsWikiUniqueWords, dfWikiUniqueWords, allow_formulas=False)
    return dfWikiUniqueWords




'''============ 3. ============'''
'''
Desc    : Menyimpan terms di google sheet, cukup lakukan sekali
'''
def saveTermsInSheet():
    # === Runing once only, to create unique words ===
    createUniqueWords()
    # === Runing sekali, untuk save unique word
    # yang ada pagenya di wikipedia ===
    termsList = gw.getListOfWiki()
    createWikipediaUniqueWords(termsList)




'''============ 4. ============'''
'''
Output  : terms dalam bentuk list
Desc    : untuk mengambil terms pada sheet dengan nama worksheet tertentu
'''
def getListTermsFromSheet(fileName=fileDriveName,
                          wsNameUniqueWords=""):
    wsUniqueWords = creds.getWorksheet(
        creds.credentialGoogle(), fileName, wsNameUniqueWords)
    dfUWords = gd.get_as_dataframe(wsUniqueWords, usecols=[0])
    # Convert word false and true as str
    booldict = {True: 'true', False: 'false'}
    dfUWords = dfUWords.replace(booldict)
    return dfUWords.values.ravel()




'''============ 5. ============'''
if __name__ == '__main__' :
#    terms = getListTermsFromSheet(wsNameUniqueWords = "wiki-unique-words")
#    print(terms)
#    print(len(terms))
    
    print(0)














