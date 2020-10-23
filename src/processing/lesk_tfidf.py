# -*- coding: utf-8 -*-
# == ORIGINAL PACKAGES ==
import pandas as pd
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
Desc    : DUMMY DOCUMENT FREQUENCY PERCOBAAN
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
        
        
        
'''
Desc    : DOCUMENT FREQUENCY FOR PRODUCTION
Input   : -
Output  : matrix terms document yang isinya jumlah kemunculan terms dalam doc.
'''
def df(outputFileName = 'lesk_df'):
    # definisikan terms dengan --- function getTerms() ---
    listTerms = fl.getTerms()
    print(len(listTerms))
    # definisikan concepts
    listConceptsName , listConceptsPath = fl.getConcepts()
        
    # inisialisasi matrix kosongnya dulu
    dfDocFreq = pd.DataFrame(0, index=listTerms, columns=['docfreq'])
    
    sizeDoc = len(listConceptsPath)
    for idxTerm, term in enumerate(listTerms):
        print("Idx Term : {}/{}".format(idxTerm, len(listTerms)))
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


''' ========== DONE Date: 21/10/2020 =========='''
'''
Desc    : IDF
Input   : -
Output  : matrix idf.
'''
def tf_idf(dfTfWithOverlaps, dfDocFreq):
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
    
    return dfTfIdf


if __name__ == '__main__':
    ### get creds
#    gClient = creds.credentialGoogle()
    ### file sheet name
#    fileName = "dataset-quran"
    
    ### Proses TF
    '''
    tf_dummy()
    tf = get_tf()
    '''
    
    ### Proses DF
    '''
    df()
    df_result = get_df()
    '''
    
    ### Proses TF-IDF
    '''
    tf_result = get_tf()
    df_result = get_df()
    tfIdf_result = tf_idf(tf_result, df_result)
    '''












