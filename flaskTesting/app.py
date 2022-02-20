import random
import re
import sys
from flask import Flask, render_template, request
from turbo_flask import Turbo
import threading
import time 
import itertools
from mailcap import findmatch
from preprocessing.process import process
from preprocessing.translate import TranslateLines
from hashingFingerprinting.hashFingerprint import hashingFunction
from winnowing.winnowing import winnow
import comparisonAndHighlighting.highlightLines
import os
from prettytable import PrettyTable

app = Flask(__name__)
turbo = Turbo(app)
global html_template
html_template = []
global irow
irow = 0







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



            html_template.append([irow, documents[doc_id] + " - " + inputfile,"{:05.2f}".format(percentages / len(s) * 100), documents[doc_id], inputfile])
            html_template.sort(key = lambda x: x[2], reverse=True)
            irow = irow + 1
            turbo.push(turbo.replace(render_template('loadavg.html'), 'load'))

        else:
            t.add_row([documents[doc_id] + " - " + inputfile,"{:05.2f}".format(percentages / eachCorpusFileTotalHashes[doc_id] * 100)])
            html_template.append([irow, documents[doc_id] + " - " + inputfile,"{:05.2f}".format(percentages / eachCorpusFileTotalHashes[doc_id] * 100), documents[doc_id], inputfile])
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








































def createMainTableHTML(Rows): #Will create the HTML file with all the comparison.
    f = open('HTMLFiles/index.html', 'w') # Create the index.html file.
    # Header part of the HTML file, will write this variable to the file.
    html_template = """<!DOCTYPE html>
    <html>
    <head>
    <title>ComparisonTable</title>
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
    """
    i = 0
    for row in Rows: # Add each entry of the table to the file.
        currentName = row[0]
        splitNames = currentName.split(" - ") #Split the names so there are no spaces
        file1 = splitNames[0]; file2 = splitNames[1] #Assign the names of the files
        html_template = html_template + "<tr>\n<th><A HREF=\"{currentNumber}-1.html?file1={firstFile}&file2={secondFile}&rowNumber={rowNumber}\">{name}</A></th>\n".format(currentNumber=i,name=row[0], firstFile=file1, secondFile=file2,rowNumber=currentNumber)
        html_template = html_template + "<th>{percentScore}</th>\n</tr>\n".format(percentScore=row[1])   
        i = i + 1
        
    html_template = html_template + "</table></body>\n</html>" #Add the ending parts of the html file.
    f.write(html_template) # Write everything to the file and close it.
    f.close()
    return 

def createIFramePage(currentRowNumber): #Create the HTML page that will display the table and the 2 comparison files.
    htmlFileName = "templates/HTMLFiles/baseFiles/{number}-1.html".format(number=currentRowNumber) #Th file name that will be used.

    f = open(htmlFileName, 'w') # Open the file.
    # Beginning part of the HTML file.
    html_template = """<!DOCTYPE html> 
    <html>
    <head>
    <title>Side by side Comparison</title>
    
    </head>
    """
    html_template = html_template + "<iframe src=\"../contentFiles/{number}-4.html\" height=\"150\" width=\"100%\" title=\"TableFile\"></iframe>\n".format(number=currentRowNumber) # Add the correct links.
    html_template = html_template + "<iframe src=\"../contentFiles/{number}-2.html\" height=\"450\" width=\"47%\" name=\"LeftFile\"></iframe>\n".format(number=currentRowNumber)
    html_template = html_template + "<iframe src=\"../contentFiles/{number}-3.html\" height=\"450\" width=\"47%\" name=\"RightFile\"></iframe>\n".format(number=currentRowNumber)
    html_template = html_template + "</body>\n</html>" #Ending parts of the HTML file.
    f.write(html_template) # Write everything to the file and close it.
    f.close()
    return 

def createJumpTable(currentRowNumber, arrayOfNamesLeft, arrayOfNamesRight): #Create the table at the top of the 2 files being compared.
    htmlFileName = "templates/HTMLFiles/contentFiles/{number}-4.html".format(number=currentRowNumber) #File name that will be used 

    f = open(htmlFileName, 'w') #Open the file
    # header information
    html_template = """<!DOCTYPE html>
    <html>
    <head>
    <title>Side by side comparison</title>
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
            <th>File1</th>
            <th>File2</th>
        </tr>
    """

    if (len(arrayOfNamesLeft) >= len(arrayOfNamesRight)): #If the length of the array on the left side is bigger than on the right side
        for var in list(range(len(arrayOfNamesLeft))): # for each entry in the left array
            html_template = html_template + "<tr>" # Start a new tale row.
            if (var < len(arrayOfNamesLeft)): #If the left side needs to be added, add the corresponding html code.
                html_template = html_template + "<th><A HREF=\"{number}-2.html#{jumpPoint}\" TARGET=\"LeftFile\">{l}-{r}</A></th>\n".format(number=currentRowNumber,jumpPoint=var,l=arrayOfNamesLeft[var][0],r=arrayOfNamesLeft[var][1])
            else:
                pass

            if (var < len(arrayOfNamesRight)): # If the right side needs to be added, add the corresponding HTML coe
                html_template = html_template + "<th><A HREF=\"{number}-3.html#{jumpPoint}\" TARGET=\"RightFile\">{l}-{r}</A></th>\n".format(number=currentRowNumber,jumpPoint=var,l=arrayOfNamesRight[var][0],r=arrayOfNamesRight[var][1])
            else:
                pass

            html_template = html_template + "</tr>\n" # End the table row.
    else: # Else if the length of the array on the right side is bigger than on the left side. 
        for var in list(range(len(arrayOfNamesRight))): # For each entry in the right array
            
            html_template = html_template + "<tr>" # Start a table row
            if (var < len(arrayOfNamesLeft)): #If we need to add an entry to the left table, add the HTML code
                html_template = html_template + "<th><A HREF=\"{number}-2.html#{jumpPoint}\" TARGET=\"LeftFile\">{l}-{r}</A></th>\n".format(number=currentRowNumber,jumpPoint=var,l=arrayOfNamesLeft[var][0],r=arrayOfNamesLeft[var][1])
            else: # Else put an empty slot for left side
                html_template = html_template + "<th></th>\n"

            if (var < len(arrayOfNamesRight)): # If the right side needs to be added, add it
                html_template = html_template + "<th><A HREF=\"{number}-3.html#{jumpPoint}\" TARGET=\"RightFile\">{l}-{r}</A></th>\n".format(number=currentRowNumber,jumpPoint=var,l=arrayOfNamesRight[var][0],r=arrayOfNamesRight[var][1])
            else:
                pass

            html_template = html_template + "</tr>\n" # End the row
    
    html_template = html_template + "</table>\n</body>\n</html>" # Add the ending information
    f.write(html_template) # Write to the file and close it.
    f.close()
    return 

def createHTMLFiles(fileName, blocks ,LeftOrRight,currentRowNumber): #Creat the HTML files that will contain the the source code.
    a_file = open(fileName) #Open the file
    
    lines = a_file.readlines() # Read all the lines
    htmlFileName = "templates/HTMLFiles/contentFiles/{number}-{side}.html".format(number=currentRowNumber,side=LeftOrRight) #Nam eof the html file.

    f = open(htmlFileName, 'w') # Create the html file.
    html_template = """<!DOCTYPE html><html><head><title>{nameOfFile}</title></head><body BGCOLOR=white><HR>{nameOfFile}<p><PRE>\n""".format(nameOfFile=fileName) #Header information.
    f.write(html_template) # Write to the html file.
    a_file.close() #Close the source file.

    i = 0 #Variables to determine what values are written to the HTML file
    blockNumber = 0
    jumpPoint = 0

    for line in lines: #For each line in the source document.
        if (blockNumber < len(blocks) and i == blocks[blockNumber][0]): #If the block number is still inside the number of blocks and i equal to the start of the block
            f.write("<A NAME=\"{j}\"></A><FONT color = #FF0000>".format(j=jumpPoint)) #Start of the text that will be highlighted in and jump point can be referenced to go to this specific line
            jumpPoint = jumpPoint + 1 # Increase the jum point
        
        f.write(line) # Write the text to the html file.
        if (blockNumber < len(blocks) and i == blocks[blockNumber][1]): #If it is the end of the block
            f.write("</FONT>") # End the text that will be highlighted in red
            blockNumber = blockNumber + 1 # Increase the block number counter
        i = i + 1 # Increase the line number counter.
        
    f.write("</PRE></PRE></Body></HTML>") # Write the ending parts of the HTML file
    f.close() # Close the file.




























@app.route('/')
def index():
    return render_template('index.html')

@app.route('/page2')
def page2():

    return render_template('page2.html')

@app.route('/HTMLFiles/baseFiles/<files>')
def testing(files):
    print("Working")
    file1 = request.args.get('file1')
    file2 = request.args.get('file2')
    rowNumber = request.args.get('rowNumber')
    stringFile = '/HTMLFiles/baseFiles/' + files 

    createIFramePage(rowNumber) # Create the page that will hold all the iframes

    highlightLines = comparisonAndHighlighting.highlightLines.getHighlightLines(file1, file2, file1 + "_Processed", file2 + "_Processed", file1 + "_Stripped", file2 + "_Stripped")
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
        table.reversesort = True
        print(table)
        Rows = table.rows
        Rows.sort(key=lambda x: x[1], reverse=True)
        while(1):
            turbo.push(turbo.replace(render_template('loadavg.html'), 'load'))


        
            