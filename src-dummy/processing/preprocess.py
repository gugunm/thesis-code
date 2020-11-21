# -*- coding: utf-8 -*-
# == ORIGINAL PACKAGES ==
import gspread_dataframe as gd                   # convert google sheet to dataframe
import sys
# == FILE AS PACKAGES ==
sys.path.insert(1, '../preparation/')            # import func from another file in other directory
import credentials as creds                      # credential for GDrive and GSheet




'''======= SETTINGS ======='''
# lib for lemmatization
from nltk.stem import WordNetLemmatizer #, PorterStemmer
# dict for stopword in english
from nltk.corpus import stopwords
# for tokenize and remove punctuation
from nltk.tokenize import RegexpTokenizer
# Initialize for preprocessing
wordnet_lemmatizer = WordNetLemmatizer()    # lemmatization
tokenizer = RegexpTokenizer(r'\w+')         # remove punctuatuion





'''=========== 1. ============='''
def cleaningData(sentence):
    lowcase_word = sentence.lower()                                                     # lowcase a sentence
    tokens = tokenizer.tokenize(lowcase_word)                                       # tokenize a sentence
    filtered_words = [w for w in tokens if not w in stopwords.words('english')]     # remove Stopwords
    output = []
    for word in filtered_words:
        #output.append(PorterStemmer().stem(word))                                   # if you wanna use only stemming
        output.append(wordnet_lemmatizer.lemmatize(word))                            # if you wanna use only lemmatization
    return output




'''=========== 2. ============='''
def mainPreprocessing():
    # get creds
    gClient = creds.credentialGoogle()
    # file sheet name
    fileName = "dataset-quran"
    # Take real (before process) all data using pandas
    real_sheet = creds.getWorksheet(gClient, fileName, "real-data")
    # Take a proceed sheet
    proc_sheet = creds.getWorksheet(gClient, fileName, "proceed-data")
    # Take a Data to be proccess
    data_df = gd.get_as_dataframe(real_sheet)
    ayat_df = data_df.iloc[:,3]   
    # Preprocessing data ayat
    for idx in ayat_df.index:
        ayat = ayat_df[idx]
        ayat_df[idx] = cleaningData(ayat)     # replace data to be tokenization result
    # Real data Already proceed then store in sheet "proceed-data" 
    gd.set_with_dataframe(proc_sheet, data_df)
    
    return 0




'''=========== 3. ============='''    
if __name__ == '__main__':
#    mainPreprocessing()
    print(0)





''' REMINDER CODES'''
# ''' 
# Input     : wikipedia page yang udah di download    
# Output    : Wikipedia page yang udah bersih dan siap di windowing
# '''
# def cleanWikiPages(wikiDir):
#     test = 1
#     print(test)
#     # Looping untuk setiap folder
#     # Baca setiap wikipedia pages
#         # Lakukan cleaning file .txt seperti biasa
#         # hapus enter di setiap dokumen
#         # hapus non-alphabetic
        
#     # Setelah ini selesai, masuk ke tahap windowing di file feature_lesk.py



