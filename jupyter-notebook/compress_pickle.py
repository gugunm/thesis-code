# -*- coding: utf-8 -*-
# import cPickle
import gzip
import pickle

# def readFileBin(path = ''):
#     file = open(path, 'rb')
#     object_file = pickle.load(file)
#     return object_file

# def save_zipped_pickle(obj, filename, protocol=-1):
#     with gzip.open(filename, 'wb') as f:
#         pickle.dump(obj, f, protocol)


path = './assets/leskOutput/ayat_0'


# data = readFileBin(path)

# save_zipped_pickle(data, 'zip_ayat_0')

def load_zipped_pickle(filename):
    with gzip.open(filename, 'rb') as f:
        loaded_object = pickle.load(f)
        return loaded_object
    
    
print(load_zipped_pickle(path)['weightedAyat']['name'])