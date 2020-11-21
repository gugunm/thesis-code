# -*- coding: utf-8 -*-
from glob import glob
import sys
import warnings
warnings.filterwarnings("ignore")
# import func from another file in other directory
sys.path.insert(1, '../processing/')
# import get unique words
import feature_lesk as fl


def getListOfWiki():
    folderName = glob("../../data/wiki/*/")
    gotTerms = [f[16:-1] for f in folderName]
    
    return gotTerms

def unlistTerms():
    listTerms = fl.getUniqueWords().values.ravel()
    wikiTerms = getListOfWiki()
    
    disjoinTerms = list(set(listTerms) - set(wikiTerms))
    
    return disjoinTerms

if __name__ == '__main__':
    print(unlistTerms())

