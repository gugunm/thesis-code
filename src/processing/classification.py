# -*- coding: utf-8 -*-
# == ORIGINAL PACKAGES ==
import pandas as pd
import random
import codecs
import pickle
import math
# == FILE AS PACKAGES ==
import feature_lesk as fl




def splitData(listWeightedAyat):
    # Shuffle ayat agar yang dijadikan data test adalah random
    random.shuffle(listWeightedAyat)

    # ambil train data
    train_data = listWeightedAyat[:13]
    # ambil test data
    test_data = listWeightedAyat[13:]
    
    return train_data, test_data
    

if __name__ == '__main__':
    #listWeightedAyat = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
    # load data terms-by-concept matriks dari file bin
    listWeightedAyat = fl.readFileBin(path='../../data/terms_by_concept_dummy.bin.txt')
    # ambil hasil dari split data
    train_data, test_data = splitData(listWeightedAyat)