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
import sys

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

def printFiles(file1, list1, htmlFileName):
    f = open(htmlFileName, 'w')
    html_template = """<html>
    <head>
    <title>Title</title>
    </head>
    <body>
    <h2>Table</h2>
    <p>
    \n
    """
    html_template = html_template + file1 + " source code: <br>"
    #print("File1 source code:")
    f1 = open(file1)
    lines = f1.readlines()
    i = 1
    for line in lines:
        if i in list1:
            #print(Fore.BLUE + line,end="")
            html_template = html_template + '<p style="color:blue;">' + line + "</p><br>"
            #print(Style.RESET_ALL,end="")
        else:
            #print(line,end="")
            html_template = html_template + '<p style="color:black;">' + line + "</p><br>"
        i = i + 1
    print(Style.RESET_ALL,end="")
    f1.close()
    f.write(html_template)
    f.close()
    return html_template

def query(corpus,documents, s):
    percentages = 0
    originalFileName = s
    if len(s) > 15:
        filename = s[15:]
    else:
        filename = s[15:]
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
        f = open('index.html', 'a')
        if(len(s) <= eachCorpusFileTotalHashes[doc_id]):
            #if(percentages / len(s) * 100 != 100):
            t.add_row([doc_id + " - " +filename,float("{:.2f}".format(percentages / len(s) * 100))])
            f.write("<br>" + "<a href=\"" + doc_id + " - " +filename + ".html" + "\" target=\"_blank\">" + doc_id + " - " + filename + "</a>"  + " |    " + "{:.2f}".format(percentages / len(s) * 100) + "\n")
            
        else:
            t.add_row([doc_id + " - " +filename,float("{:.2f}".format(percentages / eachCorpusFileTotalHashes[doc_id] * 100))])
            f.write("<br>" + "<a href=\"" + doc_id + " - " +filename + ".html" + "\" target=\"_blank\">" + doc_id + " - " + filename + "</a>"  + " |    " + "{:.2f}".format(percentages / eachCorpusFileTotalHashes[doc_id] * 100) + "\n")
        f.close()
        tempString = doc_id + " - " +filename + ".html"
        translate_print(doc_id,masterlist,originalFileName,tempString)
        masterlist = {}
        
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

def load_input_directory(d):
    k = os.listdir(d)
    k.sort()
    i=1
    docs = {}
    for file in k:
        if file.endswith(".py"):
            item = docs.setdefault("userInput" + str(i),""+d+file)
            i = i + 1
    return docs



def create_corpus(documents,corpus):
    for doc_id,path in documents.items():
        s = process(path)
        s = hashingFunction(s, 7)
        s = winnow(4, s)
        s = inverted_index_create(s)
        eachCorpusFileTotalHashes[doc_id] = len(s)
        corpus = corpus_add_index(corpus,doc_id,s)
    return corpus

def translate_print(doc_id,masterlist,inputFile,htmlFileName):
    endlist = []
    for i,j in masterlist[doc_id].items():
        if masterlist[doc_id][i] >= 3:
            endlist.append(i)
    endlist.sort()
    if(len(endlist) == 0):
        L = None 
    else:
        L = TranslateLines(inputFile+"_Stripped", endlist, inputFile)
    if L == None:
        L = [0]
    return printFiles(inputFile, L,htmlFileName)

def main():
    
    directory = "testfiles/" # directory for testfiles
    documents = load_documents(directory) # find documents inside testfiles directory
    documents2 = load_input_directory("inputDirectory/")
    corpus = {}
    corpus = create_corpus(documents,corpus) # create a corpus of those documents
    corpus = create_corpus(documents2,corpus)

    
    f = open('index.html', 'w')
    html_template = """<html>
    <head>
    <title>Title</title>
    </head>
    <body>
    <h2>Table</h2>
    <p>
    \n
    """
    f.write(html_template)
    f.close()
    k = os.listdir("inputDirectory/")
    k.sort()
    for file in k:
        if file.endswith(".py"):
            fileNamePath = "inputDirectory/"+ file 
            
            masterlist, t = query(corpus, documents, fileNamePath)
            new_dict = {key:val for key, val in documents2.items() if val != fileNamePath}
            masterlist, t = query(corpus, new_dict, fileNamePath)
    
    t.sortby = 'File Similarity'
    t.reversesort = True
    t.align["doc_id Pair"] = "l"
    print(t)
    f = open('index.html', 'a')
    f.write("</p>\n</body>\n</html>")
    f.close()


    


    

                

    


main()
