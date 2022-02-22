import itertools
from preprocessing.process import process
from preprocessing.translate import TranslateLines
from hashingFingerprinting.hashFingerprint import hashingFunction
from winnowing.winnowing import winnow
import os
from prettytable import PrettyTable
from collections import Iterable
from one_to_one import *

t = PrettyTable(['doc pairs', 'Pair Similarity'])

def inverted_index_create(s):
    inverted = {}
    for index, hash in s:
        locations = inverted.setdefault(hash, [])
        for i in index:
            if i not in locations:
                locations.append(i)
    return inverted

def corpus_add_index(corpus,doc_id, s):
    for word, locations in s.items():
        indices = corpus.setdefault(word, {})
        indices[doc_id] = locations
    return corpus

def getStripped(fileName):
    strippedFileName = fileName + "_Stripped"
    return strippedFileName

def query(corpus, documents, inputFile):
    percentages = 0
    inputfile = inputFile
    inputFile = process(inputFile)
    inputFile = hashingFunction(inputFile, 7)
    inputFile = winnow(4, inputFile)
    inputFile = inverted_index_create(inputFile)

    for doc_id,path in documents.items():
        print("doc: ", doc_id, "path: ", path)
        for key,val in inputFile.items():
            if key in corpus.keys():
                if doc_id in corpus[key]:
                    percentages = percentages+1
        t.add_row([documents[doc_id] + " - " + inputfile,"{:05.2f}".format(percentages / len(inputFile) * 100)])
        percentages = 0
    return t


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

def create_corpus(documents):
    corpus = {}
    for doc_id,path in documents.items():
        s = process(path)
        s = hashingFunction(s, 7)
        s = winnow(4, s)
        s = inverted_index_create(s)
        corpus = corpus_add_index(corpus,doc_id,s)
    return corpus


def file_setup(document):

    # function to do the initial setup of the file
    s = process(document)
    s = hashingFunction(s, 7)
    ws = winnow(4, s)
    ws = inverted_index_create(ws)
    return ws

def main():
    directory = "testfiles/"  # directory for testfiles
    documents = load_documents(directory)  # find documents inside testfiles directory
    print("documents: ", documents)
    queryHighlights = []
    inputFile = 'input.py'
    for val in documents.values():
        next = val
        print("next: ", next)
        # table = query(corpus, documents, file)
        # this table is comparing doc2 and doc3, shouldn't all the corpus documents be compared to only the input document?
        # why are we comparing docs in the corpus with other docs in the corpus
        queryHighlights.append(highlightedBlocks(file_setup(inputFile), file_setup(next), getStripped(inputFile), getStripped(next), inputFile, next))

main()