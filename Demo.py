from process import process
from hashFingerprint import hashingFunction
from winnowing import winnow
import pprint as pp

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

def main():

    corpus = {}
    documents = {'doc1':'test.py', 'doc2':'test2.py'}
    for doc_id,path in documents.items():
        s = process(path)
        s = hashingFunction(s, 4)
        s = winnow(4, s)
        s = inverted_index_create(s)
        corpus = corpus_add_index(corpus,doc_id,s)
    pp.pprint(corpus)
main()