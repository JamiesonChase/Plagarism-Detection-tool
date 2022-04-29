from flask import Flask, url_for, render_template, request, flash, redirect
from jinja2 import Template
from flask_table import Table, Col, LinkCol
import random
import os, glob
import os.path
from werkzeug.utils import secure_filename 
import json
import difflib as dl
from modules.preprocessing.process import process
from modules.hashingFingerprinting.hashFingerprint import hashingFunction
from modules.winnowing.winnowing import winnow
from modules.comparison.comparison3 import highlightedBlocks
import shutil 
import time
import pickle

app = Flask(__name__)
global items 
items = []
totalhashes = {}
global r 
r = []
global idNumber 
idNumber = 1
global lists 
lists = [] #How initial information about the input
global justCorpusInformation # Hold just the corpus winnowed information 
justCorpusInformation = [] 
global justInputInformation # Hold just the input winnowed information.
justInputInformation = []

ALLOWED_EXTENSIONS = set(['py', 'c', 'java']) #Only these extensions will be allowed to be uploaded
app.secret_key = "secret key" #Secret key to make the seure_filename upload work.


class LinkDeciderCol(LinkCol): # will be deleted

    def url(self, item): # will be deleted
        endpoint = self.endpoint['a']
        return url_for(endpoint, **self.url_kwargs(item))


class ItemTable(Table): # will be deleted
    classes = ['myclass']
    name = Col('File Pairs')
    score = Col("Scores")
    link_decider = LinkDeciderCol(
        'Link',
        {'a': 'single_item_a'},
        url_kwargs=dict(id='id'))

class CompareTable(Table): # will be deleted
    classes = ['myclass']
    left = Col('Left File')
    right = Col('Right File')

def allowed_file(filename): # Check if the extension is allowed.
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/Link/left_filled.html') # left code file
def left():
    return render_template("left_filled.html")

@app.route('/Link/right_filled.html') # right code file
def right():
    return render_template("right_filled.html")

@app.route('/') #Initial Page where you can upload
def upload_form():
    return render_template('upload.html')

@app.route('/',methods=['POST']) #If call the root with POST request for the files.
def upload_file():
    global lists
    global justInputInformation
    
    if request.method == 'POST': # If it is the POST request.
        if 'files[]' not in request.files: # If no files were selected display a message on the page.
            flash('No file part')
            return redirect(request.url)

        if not os.path.isdir("input/"): # If the input directory does not exist then then make it.
            os.mkdir("input/")

        for file in os.scandir("input/"): #Remove all the files already in the input directory.
            os.remove(file.path)

        files = request.files.getlist('files[]') # Get the list of the files uploaded

        for file in files: #Add the appropiate path to the filename to save it
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join("input/", filename))

        flash('Files successfully uploaded')
        documents = os.listdir('input/')  # find documents inside testfiles directory

        lists = []

        for doc in documents: # Go through the process of getting the winnowed information for the inputs
            originalName = doc 
            doc = 'input/' + doc
            a=process(doc)
            a=hashingFunction(a,7)
            a=winnow(4,a)
            lists.append([a,doc,originalName]) # winnow the hashes and append to lists
            justInputInformation.append([a,doc,originalName])


        return redirect('/listCorpus') # Go to the next page to list the corpus.


@app.route('/listCorpus') # List the corpus files avaialbe.
def showComparisonFiles():
    savedFiles = []
    dir = 'corpus/' #Will be in the corpus directory.
    for file in os.scandir(dir):
        if (file.path != "corpus/OG_Files" and file.path != "corpus/filesWithProcessed"): # List the files if it is not the directories.
            savedFiles.append(file.path) #Add the files to the list
    return render_template("listCorpus.html",newEntry=savedFiles) #Load the webpage with the list to display table of filenames.

@app.route('/listCorpus',methods=['POST']) #If call the root with POST request for the files.
def upload_corpus():
    global lists 
    global r 
    global idNumber
    global justCorpusInformation

    if request.method == 'POST': # If it is the POST request.
        if 'files[]' not in request.files: # If no files were selected display a message on the page.
            flash('No file part')
            return redirect(request.url)

        if not os.path.isdir("corpus/OG_Files/"): # If the input directory does not exist then then make it.
            os.mkdir("corpus/OG_Files/")

        if not os.path.isdir("corpus/filesWithProcessed/"): # If the input directory does not exist then then make it.
            os.mkdir("corpus/filesWithProcessed/")

        for file in os.scandir("corpus/filesWithProcessed/"): #Remove all the files already in the corpus processed.
            os.remove(file.path)

        files = request.files.getlist('files[]') # Get the list of the files uploaded

        for file in files: #Add the appropiate path to the filename to save it
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join("corpus/OG_Files/", filename)) # Save the og files to the correct directory
                shutil.copy("corpus/OG_Files/" + filename, "corpus/filesWithProcessed/" + filename) # Copy the file to the processed directory.

        flash('Files successfully uploaded')

        saveFileName = request.form.to_dict()
        fullPath = "corpus/" + saveFileName['a'] + ".json"
        #pickleFullPath = "corpus/" + saveFileName['a'] + ".pkl"



        documents = os.listdir('corpus/filesWithProcessed/')  # find documents inside processed directory
        corpusLists = lists.copy()
        jsonDictionary = { }

        for doc in documents: # Add the winnowed information of the corpus to variables.
            originalName = doc 
            doc = 'corpus/filesWithProcessed/' + doc
            a=process(doc)
            a=hashingFunction(a,7)
            a=winnow(4,a)
            corpusLists.append([a,doc,originalName]) # winnow the hashes and append to lists
            justCorpusInformation.append([a,doc,originalName])
            jsonDictionary[doc] = [a,originalName] 

        #jsonTimeStart = time.time()

        json.dump(jsonDictionary, open(fullPath,"w"))
        #jsonTimeEnd = time.time()
        #jsonTotalTime = jsonTimeEnd - jsonTimeStart 

        #pickleTimeStart = time.time()
        #pickle.dump(jsonDictionary, open(pickleFullPath, 'wb'))
        #pickleTimeEnd = time.time()
        #pickleTotalTime = pickleTimeEnd - pickleTimeStart 

        #print("Json total time for saving is: " + str(jsonTotalTime) + " pickle total time is: " + str(pickleTotalTime))

        r=[] # Go through the intersection to get the similarity scores.
        for i in range(0,len(lists)):
            a = lists[i][0]
            a = [lis[1] for lis in a] # do intersection comparison
            for j in range(i + 1,len(corpusLists)):
                if (lists[i][1] == corpusLists[j][1]):
                    continue

                b = corpusLists[j][0]
                b = [lis[1] for lis in b]
                s = dl.SequenceMatcher(None, a, b) # sequence match a&b
                sum = 0
                lines = 0
                for block in s.get_matching_blocks(): #get matching blocks
                    sum = sum + block[2] # calculate total matched hashes
                    if block[0] < len(a)-1 and block[1] < len(b)-1: # calculate lines matched
                        lines = lines + -lists[i][0][block[0]][0] + lists[i][0][block[0]+block[2]-1][0] + 1
                r.append([idNumber, lists[i][1] + ' - ' + corpusLists[j][1],100*sum/min(len(a),len(b)),lines]) # append to result
                idNUmber = idNumber + 1

        r = sorted(r, key=lambda tup: tup[2], reverse=True) # sort by lines matched, tup[2] -> tup[1] to sort by %

    return redirect('/mainTable')


@app.route('/loadCorpusFile') # When one of the corpus file is clicked.
def loadCorpusFile():
    global lists 
    global r 
    global idNumber
    global justCorpusInformation

    corpusName = request.args.get('fileName') #Load the specific corpus and assign it to the dictionary table.
    #pickleName = corpusName[:-5] + ".pkl"

    #jsonTimeStart = time.time()

    dictionary = json.load(open(corpusName,"r"))
    #jsonTimeEnd = time.time()
    #jsonTotalTime = jsonTimeEnd - jsonTimeStart 

    #pickleTimeStart = time.time()
    #pickleDictionary = pickle.load(open(pickleName, 'rb'))
    #pickleTimeEnd = time.time()
    #pickleTotalTime = pickleTimeEnd - pickleTimeStart 

    #print("Json total time for loading is: " + str(jsonTotalTime) + " pickle total time is: " + str(pickleTotalTime))

    corpusLists = lists.copy() # Copy to a new list everything that was in lists from the input files.
    for x in dictionary: # Add the saved corpus information.
        corpusLists.append([dictionary[x][0],x,dictionary[x][1]])
        justCorpusInformation.append([dictionary[x][0],x,dictionary[x][1]])

    r=[] # Get the information for the similarity score.
    for i in range(0,len(lists)):
        a = lists[i][0]
        a = [lis[1] for lis in a] # do intersection comparison
        for j in range(i + 1,len(corpusLists)):
            if (lists[i][1] == corpusLists[j][1]):
                continue

            b = corpusLists[j][0]
            b = [lis[1] for lis in b]
            s = dl.SequenceMatcher(None, a, b) # sequence match a&b
            sum = 0
            lines = 0
            for block in s.get_matching_blocks(): #get matching blocks
                sum = sum + block[2] # calculate total matched hashes
                if block[0] < len(a)-1 and block[1] < len(b)-1: # calculate lines matched
                    lines = lines + -lists[i][0][block[0]][0] + lists[i][0][block[0]+block[2]-1][0] + 1
            r.append([idNumber, lists[i][1] + ' - ' + corpusLists[j][1],100*sum/min(len(a),len(b)),lines]) # append to result
            idNUmber = idNumber + 1

    r = sorted(r, key=lambda tup: tup[2], reverse=True) # sort by lines matched, tup[2] -> tup[1] to sort by %

    return redirect('/mainTable')

@app.route('/mainTable') # To show everything in the main table.
def mainTable():
    global items
    global r 

    i = 0
    total = 0
    for x in r:
        total = total + x[2]
        i = i + 1

    print(total/i)


    items = [(0,'testfiles/file1.py - testfiles/file2.py', 57.2, 20), (1,'testfiles/file1.py - testfiles/file2.py', 57.2, 20)]
    
    return render_template("mainTable.html",htmlTable = r) # Load the main compairison page.

@app.route('/noCorpus') # If select not to use corpus.
def noCorpus():
    global r
    global idNumber 
    global lists 

    r=[] # Just calculate similairty based off of the inputs
    for i in range(0,len(lists)):
        a = lists[i][0]
        a = [lis[1] for lis in a] # do intersection comparison
        for j in range(i+1,len(lists)):
            b = lists[j][0]
            b = [lis[1] for lis in b]
            s = dl.SequenceMatcher(None, a, b) # sequence match a&b
            sum = 0
            lines = 0
            for block in s.get_matching_blocks(): #get matching blocks
                sum = sum + block[2] # calculate total matched hashes
                if block[0] < len(a)-1 and block[1] < len(b)-1: # calculate lines matched
                    lines = lines + -lists[i][0][block[0]][0] + lists[i][0][block[0]+block[2]-1][0] + 1
            r.append([idNumber, lists[i][1] + ' - ' + lists[j][1],100*sum/min(len(a),len(b)),lines]) # append to result
            idNUmber = idNumber + 1

    r = sorted(r, key=lambda tup: tup[2], reverse=True) # sort by lines matched, tup[2] -> tup[1] to sort by %

    return redirect('/mainTable')

@app.route('/addToCorpus',methods=['POST']) # If decide to add to corpus.
def addToCorpus():
    global justCorpusInformation
    global justInputInformation

    if request.method == 'POST': # If it is the POST request.
        saveFileName = request.form.to_dict()
        fullPath = "corpus/" + saveFileName['a'] + ".json"
        jsonDictionary = {}

        for x in justInputInformation: # Copy the input files to the OG_Files directory
            shutil.copy(x[1], "corpus/OG_Files/" + x[2])
            jsonDictionary["corpus/OG_Files/" + x[2]] = [ x[0], x[2] ] # Add to dictionary to be saved.

        if (len(justCorpusInformation) != 0): # Add the corpus used
            for x in justCorpusInformation:
                jsonDictionary[x[1]] = [x[0], x[2]]
   
        json.dump(jsonDictionary, open(fullPath,"w")) # Save the corpus.

        #jsonDictionary[doc] = [a,originalName] 
    
    return redirect('/mainTable')



@app.route('/Link/<int:id>')
def single_item_a(id): # renders new page when clicking on link
    global items
    print(items)
    element = items[id][1]
    filenames = ("C:/Users/trvrh/Desktop/Winnowing data/database/testFile.py", "C:/Users/trvrh/Desktop/Winnowing data/database/testFile_rearranged.py")
    # filenames = element.split(" - ")


    left_file=open(filenames[0]) # open left and right files
    right_file=open(filenames[1])

    left_text=left_file.readlines() # read lines of left
    left_file.close()

    right_text = right_file.readlines() # read lines of right
    right_file.close()

    for i in range(0,len(left_text)): #append space to newline
        if left_text[i] == '\n':
            left_text[i] = ' ' + '\n'

    for i in range(0,len(right_text)): # append space to newline
        if right_text[i] == '\n':
            right_text[i] = ' ' + '\n'

    res_left = []
    i = 0
    for line in left_text: # all text black
        res_left.append([i,line,'black'])
        i += 1

    res_right = []
    i = 0
    for line in right_text: #all text black
        res_right.append([i,line,'black'])
        i += 1

    linesLeft, linesRight = highlightedBlocks(filenames[0], filenames[1]) #[[colorNum, (startLine, endLine)], ...]
    colors = ['blue','green','red','orange','purple','brown','violet','turquoise','cadetblue']
    for line in linesLeft: line[0] = line[0] % len(colors)
    for line in linesRight: line[0] = line[0] % len(colors)
    random.shuffle(colors)

    for i in range(0,len(linesLeft)): # highlight lines
        color = linesLeft[i][0]
        startLine = linesLeft[i][1][0]-1
        endLine = linesLeft[i][1][1]-1
        for j in range(startLine, endLine+1):
            res_left[j][2] = colors[color] # changing line #'s color

    for i in range(0,len(linesRight)): # highlight lines
        color = linesRight[i][0]
        startLine = linesRight[i][1][0]-1
        endLine = linesRight[i][1][1]-1
        for j in range(startLine, endLine+1):
            res_right[j][2] = colors[color] # changing line #'s color

    Template(render_template('left_template.html',left=res_left)).stream().dump('templates/left_filled.html')
    Template(render_template('right_template.html',right=res_right)).stream().dump('templates/right_filled.html')
    lines = []
    maxLen = max(len(linesLeft), len(linesRight))
    for i in range(maxLen):
        if i >= len(linesLeft):
            linesLeft.append(None)
        if i >= len(linesRight):
            linesRight.append(None)
        lines.append((linesLeft[i], linesRight[i]))

    return render_template("left-right.html",filenames = filenames,lines=lines,colors=colors)




if __name__ == '__main__':
    # html table
    # Table_row = [(0,'testfiles/file1 - testfiles/file2.py', 57.2, 20),
    #              (1,'testfiles/file1 - testfiles/file2.py', 57.2, 20)]

    # CHANGE HOMEPAGE TO UPLOAD INPUT FILES
    # NEXT PAGE TO SELECTING CORPUS
    # INTERSECTION COMPARISONS FOR INPUT FILES
    # LOAD JSON CORPUS
    # query the corpus
    # lambda functions to sort by % similarity

    app.run(debug=True)
