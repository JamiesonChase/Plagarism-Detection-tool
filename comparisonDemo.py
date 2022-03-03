import itertools
from modules.preprocessing.process import process
from modules.hashingFingerprinting.hashFingerprint import hashingFunction
from modules.winnowing.winnowing import winnow
import os
from prettytable import PrettyTable
from modules.comparison.comparison import *

t = PrettyTable(['doc pairs', 'Pair Similarity'])

def inverted_index_create(s):
    inverted = {}
    for index, hash in s:
        locations = inverted.setdefault(hash, [])
        for i in index:
            if i not in locations:
                locations.append(i)
    return inverted

def getStripped(fileName):
    strippedFileName = fileName + "_Stripped"
    return strippedFileName

def load_documents(d):
    k = os.listdir(d)
    k.sort()
    i=1
    docs = {}
    for file in k:
        if file.endswith(".py"):
            item = docs.setdefault("doc" + str(i),""+d+file)
            i = i + 1
    return docs

def file_setup(document):

    # function to do the initial setup of the file
    s = process(document)
    print("processing document: \n", s)
    s = hashingFunction(s, 7)
    print("hashing document: \n", s)
    ws = winnow(4, s)
    print("winnowing document: \n", ws)
    ws = inverted_index_create(ws)
    return ws

def main():
    directory = "testing/WorkFolder/testfiles/"  # directory for testfiles
    documents = load_documents(directory)  # find documents inside testfiles directory
    print("documents: ", documents)
    queryHighlights = []
    inputFile = 'testing/WorkFolder/input.py'
    for val in documents.values():
        next = val
        print("next: ", next)
        # table = query(corpus, documents, file)
        # this table is comparing doc2 and doc3, shouldn't all the corpus documents be compared to only the input document?
        # why are we comparing docs in the corpus with other docs in the corpus
        queryHighlights.append(highlightedBlocks(file_setup(inputFile), file_setup(next), getStripped(inputFile), getStripped(next), inputFile, next))

main()