import random
import re
import sys
from flask import Flask, render_template
from turbo_flask import Turbo
import threading
import time 
import itertools
from preprocessing.process import process
from preprocessing.translate import TranslateLines
from hashingFingerprinting.hashFingerprint import hashingFunction
from winnowing.winnowing import winnow
import os
from prettytable import PrettyTable

app = Flask(__name__)
turbo = Turbo(app)
global html_template
html_template = []
global irow
irow = 0






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

def query(corpus,documents, s):
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
        t.add_row([documents[doc_id] + " - " + inputfile,"{:05.2f}".format(percentages / len(s) * 100)])
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






















@app.route('/')
def index():
    return render_template('index.html')

@app.route('/page2')
def page2():
    return render_template('page2.html')

@app.context_processor
def inject_load():
    
    
    if sys.platform.startswith('linux'): 
        with open('/proc/loadavg', 'rt') as f:
            load = f.read().split()[0:3]
    else:
        load = [int(random.random() * 100) / 100 for _ in range(3)]

    
    return {'newEntry': html_template }

@app.before_first_request
def before_first_request():
    threading.Thread(target=update_load).start()

def update_load():
    with app.app_context():
        global irow 
        directory = "testfiles/" # directory for testfiles
        documents = load_documents(directory) # find documents inside testfiles directory
        corpus = create_corpus(documents) # create a corpus of those documents
        for i in range(1,len(documents)):
            file = documents["doc" + str(i)]
            documents.pop("doc" + str(i))
            table = query(corpus,documents,file)

        table.sortby = 'Pair Similarity'
        table.add_row(["4", "40"])
        table.add_row(["5", "50"])
        table.add_row(["6", "60"])
        table.add_row(["7", "70"])
        table.add_row(["8", "80"])
        table.reversesort = True
        print(table)
        for row in table:
            row.border = False
            row.header = False
            time.sleep(1)
            html_template.append([irow, row.get_string(fields=["doc pairs"]).strip(),row.get_string(fields=["Pair Similarity"]).strip()])
            
            irow = irow + 1
            turbo.push(turbo.replace(render_template('loadavg.html'), 'load'))
        while(1):
            turbo.push(turbo.replace(render_template('loadavg.html'), 'load'))
        
            