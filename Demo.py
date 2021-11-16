from preprocessing.process import process
from hashingFingerprinting.hashFingerprint import hashingFunction
from winnowing.winnowing import winnow
import pprint as pp

def inverted_index_create(s): # create inverted index for particular document
    inverted = {}
    for index, hash in s:
        locations = inverted.setdefault(hash, [])
        for i in index:
            if i not in locations:
                locations.append(i)
    return inverted

def corpus_add_index(corpus,doc_id, s): # add an inverted index to corpus
    for word, locations in s.items():
        indices = corpus.setdefault(word, {})
        indices[doc_id] = locations
    return corpus

def main():

    corpus = {}
    documents = {'doc1':'testfiles/test.py', 'doc2':'testfiles/test2.py'} # add test files
    for doc_id,path in documents.items():
        s = process(path) # pre-process doc
        s = hashingFunction(s, 4) # create finger print hashes
        s = winnow(4, s) # perform winnowing algo
        s = inverted_index_create(s) # created the inverted index
        corpus = corpus_add_index(corpus,doc_id,s) # add index to corpus
    pp.pprint(corpus) # pretty print corpus
main()
