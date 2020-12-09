# -*- coding: utf-8 -*-
# == ORIGINAL PACKAGES ==
import numpy as np
import pickle
import re
# == FILE AS PACKAGES ==
import create_terms as ct              # file processing/create_terms




'''======= SETTINGS ======='''
# == MAIN FILE DRIVE ==
# fileDriveName = "dummy-dataset-quran"
fileDriveName = "dataset-quran"




'''============ 1. ============'''
'''
Input   : path to binary file of wiki page
Output  : return type list of file binary
'''
def readFileBin(path = ''):
    file = open(path, 'rb')
    object_file = pickle.load(file)
    return object_file
    # file.close()




'''============ 2. ============'''
'''
Input   : -
Output  : list of terms
Problem : ambil terms wiki di  google sheet
'''
def getTerms():
    # ambil data terms dari drive
    listTerms= ct.getListTermsFromSheet(fileName=fileDriveName, wsNameUniqueWords="wiki-unique-words")
    return listTerms



'''============ 3. ============'''
def getConcepts(): # for real data
    # buka file picklenya yang isinya itu dict concepts
    path = '../../data/concepts.bin.txt'
    concepts = readFileBin(path)
    conceptsName = np.ravel([concept.name.values.tolist() for concept in concepts])
    conceptsPath = np.ravel([concept.path.values.tolist() for concept in concepts])
    return conceptsName, conceptsPath

# def getConcepts(): #for dummy data
#     # buka file picklenya yang isinya itu dict concepts
#     path = '../../data/concepts.bin.txt'
#     concepts = readFileBin(path)
#     conceptsName = np.ravel([concept.name.values.tolist() for concept in concepts])  
#     conceptsPath = np.ravel([concept.path.values.tolist() for concept in concepts])
    
#     dummyConceptName = []
#     dummyConceptPath = []
#     terms = getTerms()
        
#     for i, c in enumerate(conceptsName):
#         if re.split("\_", c)[0] in terms:
#             dummyConceptName.append(c)
#             dummyConceptPath.append(conceptsPath[i])
    
#     return dummyConceptName, dummyConceptPath
