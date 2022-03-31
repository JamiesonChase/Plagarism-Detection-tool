import random
import sys
import os, glob
import os.path
import threading
from threading import Lock
from modules.preprocessing.process import process
from modules.hashingFingerprinting.hashFingerprint import hashingFunction
from modules.winnowing.winnowing import winnow
from modules.comparison.comparison import highlightedBlocks
from modules.HTMLGeneration.HTMLGeneration import createHTMLFiles, createJumpTable, createIFramePage
from flask import Flask, render_template, request, render_template_string, redirect, url_for, flash
from prettytable import PrettyTable
import pickle
import time 
from werkzeug.utils import secure_filename 

app = Flask(__name__)
global html_template # Global variable used by the browser to display the comparison data
html_template = [] 

global irow # Global variable to give each comparison a unique ID and to be used as part of the name of HTML files
irow = 0
global checkRefresh # To check if we should stop Refreshing or not
checkRefresh = 0
global loadOrNew # Check if we should do a new run or load previous data
loadOrNew = 0

global lock # Locks to make variables in threads be thread safe.
lock = Lock()
global refreshLock
refreshLock = Lock()
global lNLock
lNLock = Lock()
global docIDNumber
docIDNumber = 1

t = PrettyTable(['doc pairs', 'Pair Similarity'])

eachCorpusFileTotalHashes = {}


app.secret_key = "secret key"
app.config['MAX_CONTENT_LENGTH'] = 16 *1024 * 1024

UPLOAD_FOLDER = "templates/Input"


if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = set(['py', 'c', 'java'])















def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

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
        lock.acquire() # Acquire the lock
        if (len(s) <= eachCorpusFileTotalHashes[doc_id]):
            t.add_row([documents[doc_id] + " - " + inputfile,"{:05.2f}".format(percentages / len(s) * 100)])

            html_template.append([irow, documents[doc_id] + " - " + inputfile,  float( "{:05.2f}".format(percentages / len(s) * 100)  ), documents[doc_id], inputfile]) # Add new entry into the variable that will be displayed by the HTML page. 
            html_template.sort(key = lambda x: x[2], reverse=True) # Sort the array of values
            irow = irow + 1 

        else:
            t.add_row([documents[doc_id] + " - " + inputfile,"{:05.2f}".format(percentages / eachCorpusFileTotalHashes[doc_id] * 100)])

            html_template.append([irow, documents[doc_id] + " - " + inputfile,float( "{:05.2f}".format(percentages / eachCorpusFileTotalHashes[doc_id] * 100) ), documents[doc_id], inputfile]) # Add new entry into the variable that will be displayed by the HTML page. 
            html_template.sort(key = lambda x: x[2], reverse=True) # Sort the array of values
            irow = irow + 1 # Increment the unique idea of each entry
        percentages = 0
        lock.release() # Release the lock.
    return t

def load_documents(d):
    global docIDNumber
    k = os.listdir(d)
    k.sort()
    docs = {}
    for file in k:
        if file.endswith(".py") or file.endswith(".c"):
            item = docs.setdefault("doc" + str(docIDNumber),""+d+file)
            docIDNumber = docIDNumber + 1
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
def upload_form():
    return render_template('upload.html')

@app.route('/',methods=['POST'])
def upload_file():
    if request.method == 'POST':
        if 'files[]' not in request.files:
            flash('No file part')
            return redirect(request.url)

        for file in os.scandir("templates/Input/"):
            os.remove(file.path)

        files = request.files.getlist('files[]')

        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        flash('Files successfully uploaded')
        return redirect('/corpus')

@app.route('/corpus')
def upload_form_corpus():
    return render_template('uploadCorpus.html')

@app.route('/corpus',methods=['POST'])
def upload_file_corpus():
    global lNLock
    global loadOrNew
    if request.method == 'POST':
        if 'files[]' not in request.files:
            flash('No file part')
            return redirect(request.url)

        for file in os.scandir("templates/corpusFiles/"):
            os.remove(file.path)

        files = request.files.getlist('files[]')

        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                
                file.save(os.path.join("templates/corpusFiles/", filename))

        flash('Files successfully uploaded')
        lNLock.acquire() 
        loadOrNew = 1
        lNLock.release()
        return redirect('/comparisonTable')



@app.route('/comparisonTable') # Main page of the comparison table.
def comparisonTable():
    global irow  # Global Variables.
    global checkRefresh
    global html_template
    lock.acquire() # Copy the arrays to prevent race condition.
    newList = html_template.copy()
    lock.release()

    refreshLock.acquire()
    if (checkRefresh == 1): # If the table is not done updating load the HTML page that will refresh every 3 seconds
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
    else: #If the array is done updating then load the HTML page that won't update.
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
    

@app.route('/HTMLFiles/baseFiles/<files>') #If the link to the file is clicked
def testing(files):
    file1 = request.args.get('file1') #Get the variables passed into the URL
    file2 = request.args.get('file2')
    rowNumber = request.args.get('rowNumber')
    print(file1)
    print(file2)


    stringFile = '/HTMLFiles/baseFiles/' + files #To get the path to the html files in baseFiles
    if ( os.path.exists("templates/" + stringFile) == True): #If they already exist just render the file already there.
        return render_template(stringFile)
    else:
        start = time.time()
        createIFramePage(rowNumber) # Create the page that will hold all the iframes

        highlightLines = highlightedBlocks(file_setup(file1), file_setup(file2), getStripped(file1), getStripped(file2), file1, file2) #To get the highlighting information between files.
        file1Lines = highlightLines[0]; file2Lines = highlightLines[1]

        createJumpTable(rowNumber, file1Lines, file2Lines) #Create the table that appears on top of the comparison files.

        mainStart = time.time()
        createHTMLFiles(file1, file1Lines, 2,rowNumber) # Create the 2 HTML files that will appear side by side
        createHTMLFiles(file2, file2Lines, 3,rowNumber) 
        mainEnd = time.time()
        end = time.time()
        print("Main Part = " + str(mainEnd - mainStart))
        print("Total Part = " + str(end - start))


        return render_template(stringFile) # Render the file.

    

@app.route('/HTMLFiles/contentFiles/<files>') #If the html files from contentFiles are called then render it
def loadingFiles(files):
    stringFile = '/HTMLFiles/contentFiles/' + files 
    return render_template(stringFile)



@app.before_first_request #This will run before the first request.
def before_first_request():
    threading.Thread(target=update_load).start() #Start a new thread

def update_load():
    with app.app_context():
        global irow  #Global variables.
        global checkRefresh
        global html_template
        global lNLock
        global loadOrNew

        while(1): #Keep looping until the user makes the choice of either loading saved file or start new comparison.
            lNLock.acquire() 
            if (loadOrNew != 0):
                lNLock.release()
                break
            lNLock.release()

        
        dir = 'templates/HTMLFiles/baseFiles/' #For the new run delete old html files.
        dir2 = 'templates/HTMLFiles/contentFiles/'
        for file in os.scandir(dir):
            os.remove(file.path)
            
        for file in os.scandir(dir2):
            os.remove(file.path)

        directoryInput = "templates/Input/" # directory for testfiles
        documentsInput = load_documents(directoryInput) # find documents inside testfiles directory
        originalInputLength = len(documentsInput) + 1
        directory = "templates/corpusFiles/" # directory for testfiles
        documents = load_documents(directory) # find documents inside testfiles directory
        documents.update(documentsInput)
        corpus = create_corpus(documents) # create a corpus of those documents


        
        for i in range(1,originalInputLength):
            file = documents["doc" + str(i)]
            documents.pop("doc" + str(i))
            table = query(corpus,documents,file)

        table.sortby = 'Pair Similarity'
        table.reversesort = True
        print(table)
        Rows = table.rows
        Rows.sort(key=lambda x: x[1], reverse=True)

        lock.acquire()
        open_file = open("last_save.pkl", "wb") #Save content of the comparison
        pickle.dump(html_template, open_file)
        open_file.close()
        lock.release()
        refreshLock.acquire()
        checkRefresh = 1 #Tell the main comparison page it can stop updating.
        refreshLock.release()
        
if __name__ == "__main__":
    
    app.run(debug=True)
