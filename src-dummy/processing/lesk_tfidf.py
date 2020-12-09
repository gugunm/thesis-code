# -*- coding: utf-8 -*-
# == ORIGINAL PACKAGES ==
import pandas as pd
import codecs
import pickle
import math
# == FILE AS PACKAGES ==
import common_function as cf           # file processing/common_function



'''======= SETTINGS ======='''
### for dummy data ###
dum_TfResultPath = "../../data/dum_TfResultPath.bin.txt"
dum_DfResultPath = "../../data/dum_DfResultPath.bin.txt"
dum_TfIdfResultPath = "../../data/dum_TfIdfResultPath.bin.txt"

### for real data ###
TfResultPath = "../../data/TfResultPath.bin.txt"
DfResultPath = "../../data/DfResultPath.bin.txt"
TfIdfResultPath = "../../data/TfIdfResultPath.bin.txt"




'''=========== 1. ============='''
'''
Desc    : TF PERCOBAAN
Input   : -
Output  : matrix terms document yang isinya jumlah kemunculan terms dalam doc.
'''
def tf_dummy(outputPath= dum_TfResultPath):
    # definisikan terms dengan --- function getTerms() ---
    listTerms = cf.getTerms()
    # definisikan concepts
    listConceptsNameOld , listConceptsPathOld = cf.getConcepts()
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
        fileConcept = cf.readFileBin(conceptPath)
        for idxTerm, term in enumerate(listTerms):
            freq = fileConcept.count(term)
            dfTermsFreq.loc[term, listConceptsName[idxConceptPath]] = freq
            print('{}/{} : {}[{}] \u2713'.format(idxTerm, len(listTerms)-1, term, dfTermsFreq.loc[term, listConceptsName[idxConceptPath]]))
    
    with codecs.open(outputPath, 'wb') as outfile:
        pickle.dump(dfTermsFreq, outfile) 
        
    return 0





'''=========== 2. ============='''
'''
Desc    : DUMMY DOCUMENT FREQUENCY PERCOBAAN
Input   : -
Output  : matrix terms document yang isinya jumlah kemunculan terms dalam doc.
DONE Date: 17/09/2020
'''
def df_dummy(outputPath = dum_DfResultPath):
    # definisikan terms dengan --- function getTerms() ---
    listTerms = cf.getTerms()
    # definisikan concepts
    listConceptsNameOld , listConceptsPathOld = cf.getConcepts()
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
            fileConcept = cf.readFileBin(conceptPath)
            freq = fileConcept.count(term)
            if freq >= 1:
                dfOfTerm += 1
        dfDocFreq.loc[term, 'docfreq'] = math.log10(sizeDoc/dfOfTerm) 
        print('{}/{} : {}[{}] \u2713'.format(idxTerm, len(listTerms)-1, term, dfOfTerm))
    
    with codecs.open(outputPath, 'wb') as outfile:
        pickle.dump(dfDocFreq, outfile) 
    
    return 0





'''=========== 3. ============='''    
'''
Desc    : CALON TF YANG REAL
Input   : -
Output  : matrix terms document yang isinya jumlah kemunculan terms dalam doc.
'''
def tf(outputPath = TfResultPath):
    print('- Creating DF Terms Frequency...')
    # definisikan concepts
    listConceptsName , listConceptsPath = cf.getConcepts()
    # definisikan terms dengan --- function getTerms() ---
    listTerms = cf.getTerms()
    # inisialisasi matrix kosongnya dulu
    dfTermsFreq = pd.DataFrame(0, index=listTerms, columns=listConceptsName)
    
    countPage = 0
    for idxConceptPath, conceptPath in enumerate(listConceptsPath):
        countPage += 1
        # print(conceptPath[20:])
        fileConcept = cf.readFileBin(conceptPath)
        for idxTerm, term in enumerate(listTerms):
            freq = fileConcept.count(term)
            dfTermsFreq.loc[term, listConceptsName[idxConceptPath]] = freq
            # print('{}/{} : {}[{}] \u2713'.format(countPage, len(listConceptsPath), term, dfTermsFreq.loc[term, listConceptsName[idxConceptPath]]))
        print('{}/{} \u2713'.format(countPage, len(listConceptsPath)))
    with codecs.open(outputPath, 'wb') as outfile:
        pickle.dump(dfTermsFreq, outfile) 
    
    return 0



       

'''============ 4. ============'''
'''
Desc    : DOCUMENT FREQUENCY FOR PRODUCTION
Input   : -
Output  : matrix terms document yang isinya jumlah kemunculan terms dalam doc.
'''
def df(outputPath = DfResultPath):
    # definisikan terms dengan --- function getTerms() ---
    listTerms = cf.getTerms()
    print(len(listTerms))
    # definisikan concepts
    listConceptsName , listConceptsPath = cf.getConcepts()
    
    print(len(listConceptsPath))
    
    print("check")
        
    # inisialisasi matrix kosongnya dulu
    dfDocFreq = pd.DataFrame(0, index=listTerms, columns=['docfreq'])
    
    print("check 2")
    
    sizeDoc = len(listConceptsPath)
    for idxTerm, term in enumerate(listTerms):
        # print("Idx Term : {}/{}".format(idxTerm, len(listTerms)))
        dfOfTerm = 0
        for idxConceptPath, conceptPath in enumerate(listConceptsPath):
            fileConcept = cf.readFileBin(conceptPath)
            freq = fileConcept.count(term)
            if freq >= 1:
                dfOfTerm += 1
        if dfOfTerm == 0:
            dfOfTerm += 1
        dfDocFreq.loc[term, 'docfreq'] = math.log10(sizeDoc/dfOfTerm) 
        print('{}/{} : {}[{}] \u2713'.format(idxTerm, len(listTerms)-1, term, dfOfTerm))
    
    with codecs.open(outputPath, 'wb') as outfile:
        pickle.dump(dfDocFreq, outfile) 
    
    return 0




'''============ 5. ============'''
'''
Desc    : IDF
Input   : -
Output  : matrix idf.
DONE Date: 21/10/2020
'''
def tf_idf(dfTfWithOverlaps, dfDocFreq, outputPath):
    # get terms
    terms = dfTfWithOverlaps.index
    # get docs
    docs  = dfTfWithOverlaps.columns
    # create dataframe for tfidf
    dfTfIdf = dfTfWithOverlaps.copy()
    
    for i, doc in enumerate(docs):
        for j, term in enumerate(terms):
            # overwrite tfidf dataframe dengan hasil perhitungan tfidf
#            print(doc, ' - ', term)
            dfTfIdf.loc[term, doc] = dfTfWithOverlaps.loc[term, doc]*dfDocFreq.loc[term, 'docfreq']
            
    with codecs.open(outputPath, 'wb') as outfile:
        pickle.dump(dfTfIdf, outfile) 
    
    return dfTfIdf




'''=========== 6. ============='''
def get_tf(path):
    tf = cf.readFileBin(path)
    return tf

def get_df(path):
    df = cf.readFileBin(path)
    return df




'''=========== 7. ============='''
def main_dummy():
    # build dummy
    tf_dummy()
    df_dummy()
    
    tf_result = get_tf(dum_TfResultPath)
    df_result = get_df(dum_DfResultPath)
    tfIdf_result = tf_idf(tf_result, df_result, dum_TfIdfResultPath)
    
    return tfIdf_result

def main_actual():
    # build actual
    tf()
    df()
    
    tf_result = get_tf(TfResultPath)
    df_result = get_df(DfResultPath)
    tfIdf_result = tf_idf(tf_result, df_result, TfIdfResultPath)
    return tfIdf_result




'''=========== 8. ============='''
if __name__ == '__main__':
    # tf()
    # df()
    tf_result = get_tf(TfResultPath)
    df_result = get_df(DfResultPath)
    # print(tf_result)
    ### get creds
#    gClient = creds.credentialGoogle()
    ### file sheet name
#    fileName = "dataset-quran"
    
    #sudah pernah dirunning
    # dum_tfidf = main_dummy()
    print(0)












