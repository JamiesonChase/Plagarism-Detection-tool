import itertools
from preprocessing.process import process
from preprocessing.translate import TranslateLines
from hashingFingerprinting.hashFingerprint import hashingFunction
from winnowing.winnowing import winnow
from collections import Counter
from colorama import Fore, Back, Style
import os
from prettytable import PrettyTable
import pprint as pp

eachCorpusFileTotalHashes = {}
t = PrettyTable(['doc_id Pair', 'File Similarity'])

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

def printFiles(file1, list1):
    returnString = "File1 source code:\n"
    print("File1 source code:")
    f1 = open(file1)
    lines = f1.readlines()
    i = 1
    for line in lines:
        if i in list1:
            print(Fore.BLUE + line,end="")
            returnString = returnString + line 
            print(Style.RESET_ALL,end="")
        else:
            print(line,end="")
            returnString = returnString + line 
        i = i + 1
    print(Style.RESET_ALL,end="")
    f1.close()
    return returnString

def query(corpus,documents, s):
    percentages = 0
    if len(s) > 15:
        filename = s[10:]
    else:
        filename = s
    lines = []
    masterlist = {}

    s = process(s)
    s = hashingFunction(s,7)
    s = winnow(4,s)
    s = inverted_index_create(s)

    for doc_id,path in documents.items():
        for key,val in s.items():
            if key in corpus.keys():
                if doc_id in corpus[key]:
                    percentages = percentages+1
                    lines.append(val)
        flat = itertools.chain.from_iterable(lines)
        c = Counter(list(flat))
        masterlist.setdefault(doc_id, c)
        if(len(s) <= eachCorpusFileTotalHashes[doc_id]):
            if(percentages / len(s) * 100 != 100):
                t.add_row([doc_id + " - " +filename,float("{:.2f}".format(percentages / len(s) * 100))])
        else:
            t.add_row([doc_id + " - " +filename,float("{:.2f}".format(percentages / eachCorpusFileTotalHashes[doc_id] * 100))])
        percentages = 0
        lines = []
    return masterlist,t

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
        eachCorpusFileTotalHashes[doc_id] = len(s)
        corpus = corpus_add_index(corpus,doc_id,s)
    return corpus

def translate_print(doc_id,masterlist,inputFile):
    endlist = []
    for i,j in masterlist[doc_id].items():
        if masterlist[doc_id][i] >= 3:
            endlist.append(i)
    endlist.sort()
    L = TranslateLines(inputFile+"_Stripped", endlist, inputFile)
    if L == None:
        L = [0]
    return printFiles(inputFile, L)

def main():

    directory = "testfiles/" # directory for testfiles
    inputFile = "inputFile.py" # input file
    documents = load_documents(directory) # find documents inside testfiles directory
    corpus = create_corpus(documents) # create a corpus of those documents
    masterlist, t = query(corpus, documents, inputFile) #query input file in corpus
    masterlist, t = query(corpus, documents, 'testfiles/databaseFile1.py') #query input file in corpus
    masterlist, t = query(corpus, documents, 'testfiles/databaseFile2.py') #query input file in corpus
    masterlist, t = query(corpus, documents, 'testfiles/databaseFile3.py')
    masterlist, t = query(corpus, documents, 'testfiles/databaseFile4.py')
    masterlist, t = query(corpus, documents, 'testfiles/databaseFile5.py')
    t.sortby = 'File Similarity'
    t.reversesort = True
    t.align["doc_id Pair"] = "l"
    print(t)
    print(masterlist)

    # option print LINE similarity between 2 docs after query
    firstFile = translate_print("doc1", masterlist, inputFile)
    # translate_print("doc2", masterlist, inputFile)
    # translate_print("doc3", masterlist, inputFile)
    # translate_print("doc4", masterlist, inputFile)
    # translate_print("doc5", masterlist, inputFile)

    f = open('Testing.html', 'w')
    html_template = """<html>
    <head>
    <title>Title</title>
    </head>
    <body>
    <h2>Table</h2>
    <p>
    """
    tempT = str(t)
    tempT = tempT.replace('\n', "<br>")
    firstFile = firstFile.replace('\n', "<br>")
    html_template = html_template + str(tempT) 
    html_template = html_template + "<br><br><br>"
    html_template = html_template + firstFile
    html_template = html_template + "</p>\n</body>\n</html>"
    f.write(html_template)
    f.close()

main()
