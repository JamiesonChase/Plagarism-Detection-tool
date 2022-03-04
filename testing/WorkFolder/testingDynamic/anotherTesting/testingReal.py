import random
import sys
import os
import threading
from modules.preprocessing.process import process
from modules.hashingFingerprinting.hashFingerprint import hashingFunction
from modules.winnowing.winnowing import winnow
from modules.comparison.comparison import highlightedBlocks
from modules.HTMLGeneration.HTMLGeneration import createHTMLFiles, createJumpTable, createIFramePage
from flask import Flask, render_template, request
from turbo_flask import Turbo
from prettytable import PrettyTable
import time 

app = Flask(__name__)
turbo = Turbo(app)
global html_template
html_template = []
global irow
irow = 0
global checkEnd 
checkEnd = 0

t = PrettyTable(['doc pairs', 'Pair Similarity'])

eachCorpusFileTotalHashes = {}

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

def query(corpus,documents, s):
    global irow
    global html_template
    percentages = 0
    inputfile = s

    s = process(s)
    s = hashingFunction(s,7)
    s = winnow(4,s)
    s = inverted_index_create(s)

    for doc_id,path in documents.items():
        for key,val in s.items():
            if key in corpus.keys():
                if doc_id in corpus[key]:
                    percentages = percentages+1
        if (len(s) <= eachCorpusFileTotalHashes[doc_id]):
            t.add_row([documents[doc_id] + " - " + inputfile,"{:05.2f}".format(percentages / len(s) * 100)])



            html_template.append([irow, documents[doc_id] + " - " + inputfile,  float( "{:05.2f}".format(percentages / len(s) * 100)  ), documents[doc_id], inputfile])
            html_template.sort(key = lambda x: x[2], reverse=True)
            irow = irow + 1
            turbo.push(turbo.replace(render_template('loadavg.html'), 'load'))

        else:
            t.add_row([documents[doc_id] + " - " + inputfile,"{:05.2f}".format(percentages / eachCorpusFileTotalHashes[doc_id] * 100)])
            html_template.append([irow, documents[doc_id] + " - " + inputfile,float( "{:05.2f}".format(percentages / eachCorpusFileTotalHashes[doc_id] * 100) ), documents[doc_id], inputfile])
            html_template.sort(key = lambda x: x[2], reverse=True)
            irow = irow + 1
            turbo.push(turbo.replace(render_template('loadavg.html'), 'load'))
        percentages = 0
    return t

def load_documents(d):
    k = os.listdir(d)
    k.sort()
    i=1
    docs = {}
    for file in k:
        if file.endswith(".py") or file.endswith(".c"):
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

def getStripped(fileName):
    strippedFileName = fileName + "_Stripped"
    return strippedFileName

def file_setup(document):

    # function to do the initial setup of the file
    s = process(document)
    s = hashingFunction(s, 7)
    ws = winnow(4, s)
    ws = inverted_index_create(ws)
    return ws

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/page2')
def page2():

    return render_template('page2.html')


app.run(host="0.0.0.0", port=5000, threaded=True)

@app.route('/HTMLFiles/baseFiles/<files>')
def testing(files):
    print("Working")
    file1 = request.args.get('file1')
    file2 = request.args.get('file2')
    rowNumber = request.args.get('rowNumber')
    stringFile = '/HTMLFiles/baseFiles/' + files 

    createIFramePage(rowNumber) # Create the page that will hold all the iframes

    highlightLines = highlightLines = highlightedBlocks(file_setup(file1), file_setup(file2), getStripped(file1), getStripped(file2), file1, file2)
    file1Lines = highlightLines[0]; file2Lines = highlightLines[1]

    createJumpTable(rowNumber, file1Lines, file2Lines) #Create the table that appears on top of the comparison files.
    createHTMLFiles(file1, file1Lines, 2,rowNumber) # Create the 2 HTML files that will appear side by side
    createHTMLFiles(file2, file2Lines, 3,rowNumber) 

    return render_template(stringFile)

@app.route('/HTMLFiles/contentFiles/<files>')
def loadingFiles(files):
    stringFile = '/HTMLFiles/contentFiles/' + files 
    return render_template(stringFile)


@app.context_processor
def inject_load():
    

    print("Testing")
    
    return {'newEntry': html_template }

@app.before_first_request
def before_first_request():
    threading.Thread(target=update_load).start()
    threading.Thread(target=continuous_update).start()

def update_load():
    with app.app_context():
        global irow 
        global checkEnd
        directory = "database/" # directory for testfiles
        documents = load_documents(directory) # find documents inside testfiles directory
        corpus = create_corpus(documents) # create a corpus of those documents
        for i in range(1,len(documents)):
            file = documents["doc" + str(i)]
            documents.pop("doc" + str(i))
            table = query(corpus,documents,file)

        table.sortby = 'Pair Similarity'
        table.reversesort = True
        print(table)
        Rows = table.rows
        Rows.sort(key=lambda x: x[1], reverse=True)
        checkEnd = 1
            


def continuous_update():
    with app.app_context():
        while(1):
            turbo.push(turbo.replace(render_template('loadavg.html'), 'load'))
        
