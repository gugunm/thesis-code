# -*- coding: utf-8 -*-
import sys
# import func from another file in other directory
sys.path.insert(1, '../preparation/')
# convert google sheet to dataframe
import pandas as pd

'''
Input   : jumlah windowing dan ayat alquran
Output  : return array sebanyak windownya
Problem : - untuk data yang kurang dari jumlah window yang saat itu digunakan ?
          - cek dengan print dokumen dummy
'''
def windowing(doc, n_window):
    test = 1
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
    # Ambil target word dari hasil return func windowing()
    # Looping satu-persatu
    # Lakukan proses weighting disetiap pages untuk setiap termsnya
    # weight untuk target word (rumusnya ada di dokumen / catetan)
    # setiap term akan memiliki weight dalam vector (concept vector) dengan panjang |wiki pages|
    
if __name__ == '__main__':
    '''
    # Get unique words from google sheet
    df = getUniqueWords()
    for val in df.iloc[:,0].values:
        if val == True:
            print(val)
    '''
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    