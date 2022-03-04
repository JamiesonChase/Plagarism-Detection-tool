import random
import sys
import os, glob
import os.path
import threading
from threading import Lock
from modules.preprocessing.process import process
from modules.hashingFingerprinting.hashFingerprint import hashingFunction
from modules.winnowing.winnowing import winnow
from modules.comparison.comparison2 import highlightedBlocks
from modules.HTMLGeneration.HTMLGeneration import createHTMLFiles, createJumpTable, createIFramePage
from flask import Flask, render_template, request, render_template_string, redirect, url_for
from prettytable import PrettyTable
import pickle

app = Flask(__name__)
global html_template
html_template = []
global irow
irow = 0
global lock
lock = Lock()
global refreshLock
refreshLock = Lock()
global checkRefresh
checkRefresh = 0
global loadOrNew
loadOrNew = 0
global lNLock
lNLock = Lock()

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
    global lock
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
        lock.acquire()
        if (len(s) <= eachCorpusFileTotalHashes[doc_id]):
            t.add_row([documents[doc_id] + " - " + inputfile,"{:05.2f}".format(percentages / len(s) * 100)])



            html_template.append([irow, documents[doc_id] + " - " + inputfile,  float( "{:05.2f}".format(percentages / len(s) * 100)  ), documents[doc_id], inputfile])
            html_template.sort(key = lambda x: x[2], reverse=True)
            irow = irow + 1

        else:
            t.add_row([documents[doc_id] + " - " + inputfile,"{:05.2f}".format(percentages / eachCorpusFileTotalHashes[doc_id] * 100)])
            html_template.append([irow, documents[doc_id] + " - " + inputfile,float( "{:05.2f}".format(percentages / eachCorpusFileTotalHashes[doc_id] * 100) ), documents[doc_id], inputfile])
            html_template.sort(key = lambda x: x[2], reverse=True)
            irow = irow + 1
        percentages = 0
        lock.release()
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
    return render_template("index.html")

@app.route('/loadFile')
def loadFile():
    global lNLock
    global loadOrNew
    lNLock.acquire()
    loadOrNew = 1
    lNLock.release()
    return redirect(url_for('comparisonTable'))

@app.route('/newStart')
def newStart():
    global lNLock
    global loadOrNew
    lNLock.acquire()
    loadOrNew = 2
    lNLock.release()
    return redirect(url_for('comparisonTable'))


@app.route('/comparisonTable')
def comparisonTable():
    global irow 
    global checkRefresh
    global html_template
    lock.acquire()
    newList = html_template.copy()
    lock.release()

    refreshLock.acquire()
    if (checkRefresh == 1):
        refreshLock.release()
        return render_template_string("""<!DOC html>
    <html>
    <head>

    
    <meta charset="utf-8" />
    <title>Test</title>
    
    <style>
      table, th, td {
          border: 1px solid black;
          border-collapse: collapse;
      }
      table.center {
          margin-left: auto;
          margin-right: auto;
      }
    </style>
    </head>
    <body>
    <table class="center">
      <tr>
        <th>doc Pairs</th>
        <th>Pair Similarity</th>
      </tr>
      {% for i in newEntry %}
        <tr><th><A HREF="HTMLFiles/baseFiles/{{i[0]}}-1.html?file1={{i[3]}}&file2={{i[4]}}&rowNumber={{i[0]}}">{{i[1]}}</A></th><th>{{i[2]}}</th></tr>
    {% endfor %}
    </table>
    </body>
        </html>""", newEntry=newList)
    else:
        refreshLock.release()
        return render_template_string("""<!DOC html>
    <html>
    <head>
     <meta http-equiv="refresh" content="3">
    
    <meta charset="utf-8" />
    <title>Test</title>
    
    <style>
      table, th, td {
          border: 1px solid black;
          border-collapse: collapse;
      }
      table.center {
          margin-left: auto;
          margin-right: auto;
      }
    </style>
    </head>
    <body>
    <table class="center">
      <tr>
        <th>doc Pairs</th>
        <th>Pair Similarity</th>
      </tr>
      {% for i in newEntry %}
        <tr><th><A HREF="HTMLFiles/baseFiles/{{i[0]}}-1.html?file1={{i[3]}}&file2={{i[4]}}&rowNumber={{i[0]}}">{{i[1]}}</A></th><th>{{i[2]}}</th></tr>
    {% endfor %}
    </table>
    </body>
        </html>""", newEntry=newList)
    
    


@app.route('/HTMLFiles/baseFiles/<files>')
def testing(files):
    print("Working")
    file1 = request.args.get('file1')
    file2 = request.args.get('file2')
    rowNumber = request.args.get('rowNumber')
    stringFile = '/HTMLFiles/baseFiles/' + files 
    if ( os.path.exists(stringFile) == True):
        return render_template(stringFile)
    else:
        createIFramePage(rowNumber) # Create the page that will hold all the iframes

        highlightLines = highlightedBlocks(file1, file2)
        file1Lines = highlightLines[0]; file2Lines = highlightLines[1]
        print("-----------------")
        print(file1Lines)
        print(file2Lines)
        print("-------------------")

        createJumpTable(rowNumber, file1Lines, file2Lines) #Create the table that appears on top of the comparison files.
        createHTMLFiles(file1, file1Lines, 2,rowNumber) # Create the 2 HTML files that will appear side by side
        createHTMLFiles(file2, file2Lines, 3,rowNumber) 

        return render_template(stringFile)

    

@app.route('/HTMLFiles/contentFiles/<files>')
def loadingFiles(files):
    stringFile = '/HTMLFiles/contentFiles/' + files 
    return render_template(stringFile)



@app.before_first_request
def before_first_request():
    threading.Thread(target=update_load).start()

def update_load():
    with app.app_context():
        global irow 
        global checkRefresh
        global html_template
        global lNLock
        global loadOrNew
        while(1):
            lNLock.acquire()
            if (loadOrNew != 0):
                lNLock.release()
                break
            lNLock.release()

        if loadOrNew == 1:
            open_file = open("last_save.pkl", "rb")
            html_template = pickle.load(open_file)
            open_file.close()
            refreshLock.acquire()
            checkRefresh = 1
            refreshLock.release()
        else:
            dir = 'templates/HTMLFiles/baseFiles/'
            dir2 = 'templates/HTMLFiles/contentFiles/'
            for file in os.scandir(dir):
                os.remove(file.path)
            
            for file in os.scandir(dir2):
                os.remove(file.path)
            


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
            lock.acquire()
            open_file = open("last_save.pkl", "wb")
            pickle.dump(html_template, open_file)
            open_file.close()
            lock.release()
            #print(html_template)
            refreshLock.acquire()
            checkRefresh = 1
            refreshLock.release()
        
        
        """
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
        print(html_template)
        refreshLock.acquire()
        checkRefresh = 1
        refreshLock.release()
        """
        
        
if __name__ == "__main__":
    
    app.run(debug=True)
