import itertools
from modules.preprocessing.process import process
from modules.hashingFingerprinting.hashFingerprint import hashingFunction
from modules.winnowing.winnowing import winnow
import os
from prettytable import PrettyTable
from modules.comparison.comparison import *

t = PrettyTable(['doc pairs', 'Pair Similarity'])


def inverted_index_create(s):
    # creates a inverted index of a list
    inverted = {}
    for index, hash in s:
        locations = inverted.setdefault(hash, [])
        for i in index:
            if i not in locations:
                locations.append(i)
    return inverted


def getStripped(fileName):
    # adds "_Stripped" to end of a filename
    strippedFileName = fileName + "_Stripped"
    return strippedFileName


def load_documents(d):
    # searches a directory for files*.py and returns a dictionary of key:docID value: fileName.py
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
    # calls each module to prepare input document for comparisons
        # modules called: process, hashingFunction, and winnow

    s = process(document)
    #print("processing document: \n", s)
    s = hashingFunction(s, 7)
    #print("hashing document: \n", s)
    ws = winnow(4, s)
    #print("winnowing document: \n", ws)
    ws = inverted_index_create(ws)
    return ws



def main():
    # demonstrates the comparison tool by outputting:
        # inputFile processed blocks of lines with found matches
        # compared document processed blocks with found matches
        # inputFile original code blocks
            # - this is the translated processed blocks of the original source file
        # compared document original code blocks
        # similarity percentage (needs fixed?)

    directory = "testing/WorkFolder/testfiles/"  # directory for testfiles
    documents = load_documents(directory)  # find documents inside testfiles directory
    print("documents: ", documents)
    queryHighlights = []
    inputFile = 'testing/WorkFolder/input.py'
    for val in documents.values():
        next = val
        print("compared document: ", next)
        queryHighlights.append(highlightedBlocks(file_setup(inputFile), file_setup(next), getStripped(inputFile), getStripped(next), inputFile, next))

main()