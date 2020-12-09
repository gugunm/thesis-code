# -*- coding: utf-8 -*-
import pandas as pd
import pickle
import gzip
import fasttext.util


#real dataset
datapath = './dataset/dataset-quran.xlsx'

#concept path buat di drive
conceptpath = './assets/conceptInDrive.xlsx' 

### for real data ###
TfResultPath = "./assets/CompressedTfResultPath.bin"
DfResultPath = "./assets/CompressedDfResultPath.bin"


# GANTI KALO CW nya BEDA -> RUBAH JUGA CODINGAN DIBAWAH
leskOutput_cw_2 = './assets/leskOutput_cw_2/ayat'
leskFasttextOutput_2_cw_2 = './assets/leskFasttextOutput_2_cw_2/ayat'


'''== IMPORT FASTTEXT =='''
# fasttext.util.download_model('en', if_exists='ignore')
ft = fasttext.load_model('./model/crawl-300d-2M-subword.bin')


'''== COMMON FUNCTION =='''
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


'''FASTTEXT X LESK = 300 LENGTH VECTOR'''

'''== Multiply Terms by Concept Matrix dengan FastText =='''
# cell dengan nilai lesk nol, akan di ganti dengan vector nol sepanjang 300, karena itu hasil dari vector kata dikalikan dengan nilai lesk
# harus inisiasi dataframe baru dan diubah bentuk jadi object, karena dataframe biasa ga bisa nampung vector
def createWordEmbeddingModel(data):
  totalData = len(data)
  listIndexData = list(range(totalData))
  
  for idx, i in enumerate(listIndexData):
    #LOAD AYAT LESK MODEL .BIN
    pathToData = leskOutput_cw_2 + '_' + str(i)
    ayat = load_zipped_pickle(pathToData)        
    print('Loaded Data : ', pathToData)
      
    # ambil weightedayat untuk tiap ayatnya
    dfWeightedAyat = ayat['weightedAyat']
    # create dataframe buat nampung hasil rata-rata word embeddingnya
    dfWordEmbed = pd.DataFrame(columns=listTerms, index=list(range(len(dfConcept) + 300))) #.astype(object)

    # looping tiap terms
    for term in listTerms:
      # ambil vector terms-nya dari model fasttext
      wordVector = ft.get_word_vector(term)

      # ambil lesk vektor term
      leskVector = dfWeightedAyat[term].values
      
      # gabungkan lesk vektor dan fasttext vektor
      leskConcateFasttext = leskVector + wordVector

      # hitung vector rata-rata untuk suatu index/term nya
      dfWordEmbed[term] = leskConcateFasttext


    print("Ayat ke - {}/{} completed.".format(idx+1, totalData))
    ayat['weightedAyat'] = dfWordEmbed.astype('float16')

    save_zipped_pickle(ayat, idx, leskFasttextOutput_2_cw_2)
  
  return 0


# ambil data terjemahannya dulu dari sheet
data = pd.read_excel(datapath, sheet_name='proceed-data')
createWordEmbeddingModel(data)














