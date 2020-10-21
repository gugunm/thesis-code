# -*- coding: utf-8 -*-
# == ORIGINAL PACKAGES ==
import pandas as pd
import numpy as np
import codecs
import pickle
import math
# == FILE AS PACKAGES ==
import feature_lesk as fl


'''
Desc    : TF PERCOBAAN
Input   : -
Output  : matrix terms document yang isinya jumlah kemunculan terms dalam doc.
'''
def tf_dummy(outputFileName = 'lesk_tf_dummy'):
    # definisikan terms dengan --- function getTerms() ---
    listTerms = fl.getTerms()
    # definisikan concepts
    listConceptsNameOld , listConceptsPathOld = fl.getConcepts()
    listConceptsName = []
    listConceptsPath = []
    for i, cName in enumerate(listConceptsNameOld):
        listConceptsName.append(cName) if (cName[: -7] in listTerms) else print('Concept Name Failed : ' + cName)
        pathName = listConceptsPathOld[i]
        cNameInPath = pathName[ pathName.rfind('\\', 1)+1 : -15 ]
        listConceptsPath.append(pathName) if (cNameInPath in listTerms) else print('Concept Path Failed : ' + cName)
        
    # inisialisasi matrix kosongnya dulu
    dfTermsFreq = pd.DataFrame(0, index=listTerms, columns=listConceptsName)
    
    for idxConceptPath, conceptPath in enumerate(listConceptsPath):
        fileConcept = fl.readFileBin(conceptPath)
        for idxTerm, term in enumerate(listTerms):
            freq = fileConcept.count(term)
            dfTermsFreq.loc[term, listConceptsName[idxConceptPath]] = freq
            print('{}/{} : {}[{}] \u2713'.format(idxTerm, len(listTerms)-1, term, dfTermsFreq.loc[term, listConceptsName[idxConceptPath]]))
    
    with codecs.open("../../data/{}.bin.txt".format(outputFileName), 'wb') as outfile:
        pickle.dump(dfTermsFreq, outfile) 
        
        
'''
Desc    : CALON TF YANG REAL
Input   : -
Output  : matrix terms document yang isinya jumlah kemunculan terms dalam doc.
'''
def tf(outputFileName = 'lesk_tf'):
    print('- Creating DF Terms Frequency...')
    # definisikan concepts
    listConceptsName , listConceptsPath = fl.getConcepts()
    # definisikan terms dengan --- function getTerms() ---
    listTerms = fl.getTerms()
    # inisialisasi matrix kosongnya dulu
    dfTermsFreq = pd.DataFrame(0, index=listTerms, columns=listConceptsName)
    
    for idxConceptPath, conceptPath in enumerate(listConceptsPath):
        fileConcept = fl.readFileBin(conceptPath)
        for idxTerm, term in enumerate(listTerms):
            freq = fileConcept.count(term)
            dfTermsFreq.loc[term, listConceptsName[idxConceptPath]] = freq
            print('{}/{} : {}[{}] \u2713'.format(idxTerm, len(listTerms)-1, term, dfTermsFreq.loc[term, listConceptsName[idxConceptPath]]))
    
    with codecs.open("../../data/{}.bin.txt".format(outputFileName), 'wb') as outfile:
        pickle.dump(dfTermsFreq, outfile) 


def get_tf(path = '../../data/lesk_tf_dummy.bin.txt'):
    tf = fl.readFileBin(path)
    return tf


''' ========== DONE Date: 17/09/2020 =========='''
'''
Desc    : DOCUMENT FREQUENCY PERCOBAAN
Input   : -
Output  : matrix terms document yang isinya jumlah kemunculan terms dalam doc.
'''
def df_dummy(outputFileName = 'lesk_df_dummy'):
    # definisikan terms dengan --- function getTerms() ---
    listTerms = fl.getTerms()
    # definisikan concepts
    listConceptsNameOld , listConceptsPathOld = fl.getConcepts()
    listConceptsName = []
    listConceptsPath = []
    for i, cName in enumerate(listConceptsNameOld):
        listConceptsName.append(cName) if (cName[: -7] in listTerms) else print('Concept Name Failed : ' + cName)
        pathName = listConceptsPathOld[i]
        cNameInPath = pathName[ pathName.rfind('\\', 1)+1 : -15 ]
        listConceptsPath.append(pathName) if (cNameInPath in listTerms) else print('Concept Path Failed : ' + cName)
        
    # inisialisasi matrix kosongnya dulu
    dfDocFreq = pd.DataFrame(0, index=listTerms, columns=['docfreq'])
    
    sizeDoc = len(listConceptsPath)
    for idxTerm, term in enumerate(listTerms):
        dfOfTerm = 0
        for idxConceptPath, conceptPath in enumerate(listConceptsPath):
            fileConcept = fl.readFileBin(conceptPath)
            freq = fileConcept.count(term)
            if freq >= 1:
                dfOfTerm += 1
        dfDocFreq.loc[term, 'docfreq'] = math.log10(sizeDoc/dfOfTerm) 
        print('{}/{} : {}[{}] \u2713'.format(idxTerm, len(listTerms)-1, term, dfOfTerm))
    
    with codecs.open("../../data/{}.bin.txt".format(outputFileName), 'wb') as outfile:
        pickle.dump(dfDocFreq, outfile) 
        
def get_df(path = '../../data/lesk_df_dummy.bin.txt'):
    df = fl.readFileBin(path)
    return df


''' ========== ON PROCESS Date: 21/10/2020 =========='''
'''
Desc    : IDF
Input   : -
Output  : matrix idf.
'''
def tf_idf(dfTfWithOverlaps, dfDocFreq):
    terms = dfTfWithOverlaps.index
    docs  = dfTfWithOverlaps.columns
#    tfidf = np.zeros((len(terms), len(docs)), dtype=float)
    dfTfIdf = dfTfWithOverlaps.copy()
    for i, doc in enumerate(docs):
        for j, term in enumerate(terms):
            dfTfIdf.loc[term, doc] = dfTfWithOverlaps.loc[term, doc]*dfDocFreq.loc[term, 'docfreq']
    return dfTfIdf


if __name__ == '__main__':
    # get creds
#    gClient = creds.credentialGoogle()
#    # file sheet name
#    fileName = "dataset-quran"
#    tf_dummy()
#    tf = get_tf()
#     df = df_dummy()
#     df = get_df()
    
#    tf_result = get_tf()
#    df_result = get_df()
#    tfIdf_result = tf_idf(tf_result, df_result)




#def idf(all_fitur, size_doc):
#    for fitur in all_fitur:
#        all_fitur[fitur] = math.log10(size_doc/all_fitur[fitur])
#    return all_fitur
#
#def tf_idf(tf, idf, bow):
#    tfidf = np.zeros((len(tf), len(idf)), dtype=float)
#    for i in range(len(tf)):
#        for j, fitur in enumerate(bow):
#            tfidf[i,j] = tf[i,j]*idf[fitur]
#    return tfidf
#
## Save to CSV
#def save_tocsv(data_array, nfile):
#    df = pd.DataFrame(data_array)
#    df.to_csv(nfile,  sep=',', encoding='utf-8', index=False)
#       
#
## Main Program
#def main(fitur_onedoc, fitur_alldoc, result_tfidf):
#    bow = bagofword(fitur_alldoc)
#    tfreq = tf(bow, fitur_onedoc)
#    tidf = idf(fitur_alldoc, len(fitur_onedoc))
#    tfidf = tf_idf(tfreq, tidf, bow)
#    save_tocsv(tfidf, result_tfidf)
#    return tfidf, bow
















