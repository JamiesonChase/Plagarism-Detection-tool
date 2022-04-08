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
from modules.comparison.comparison import highlightedBlocks

app = Flask(__name__)
global items 
items = []
totalhashes = {}

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

def allowed_file(filename):
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

        for doc in documents:
            doc = 'input/' + doc
            a=process(doc)
            a=hashingFunction(a,7)
            a=winnow(4,a)
            lists.append(a) # winnow the hashes and append to lists

        r=[]
        for i in range(0,len(lists)):
            a = lists[i]
            a = [lis[1] for lis in a] # do intersection comparison
            for j in range(i+1,len(lists)):
                b = lists[j]
                b = [lis[1] for lis in b]
                s = dl.SequenceMatcher(None, a, b) # sequence match a&b
                sum = 0
                lines = 0
                for block in s.get_matching_blocks(): #get matching blocks
                    sum = sum + block[2] # calculate total matched hashes
                    if block[0] < len(a)-1 and block[1] < len(b)-1: # calculate lines matched
                        lines = lines + -lists[i][block[0]][0] + lists[i][block[0]+block[2]-1][0] + 1
                r.append([documents[i] + ' - ' + documents[j],100*sum/min(len(a),len(b)),lines]) # append to result

        r = sorted(r, key=lambda tup: tup[2], reverse=True) # sort by lines matched, tup[2] -> tup[1] to sort by %
        print(r)

        return redirect('/listCorpus') # Go to the next page to list the corpus.


@app.route('/listCorpus') # List the corpus files avaialbe.
def showComparisonFiles():
    savedFiles = []
    dir = 'corpus/' #Will be in the corpus directory.
    for file in os.scandir(dir):
        savedFiles.append(file.path) #Add the files to the list
    return render_template("listCorpus.html",newEntry=savedFiles) #Load the webpage with the list to display table of filenames.

@app.route('/loadCorpusFile') # When one of the corpus file is clicked.
def loadCorpusFile():
    print(os.listdir("input/"))
    corpusName = request.args.get('fileName') #Load the specific corpus and assign it to the dictionary table.
    dictionary = json.load(open(corpusName,"r"))
    return redirect('/mainTable')

@app.route('/mainTable')
def mainTable():
    global items
    items = [(0,'testfiles/file1.py - testfiles/file2.py', 57.2, 20), (1,'testfiles/file1 - testfiles/file2.py', 57.2, 20)]
    return render_template("mainTable.html",htmlTable = items) # Load the main compairison page.






@app.route('/Link/<int:id>')
def single_item_a(id): # renders new page when clicking on link
    global items
    print(items)
    element = items[id][1]
    filenames = element.split(" - ")

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

    lines = [[10,13,15,20],[15,20,2,7],[35,40,50,55]] # REPLACE WITH TREVORS CODE
    colors = ['blue','green','red','orange','purple','brown','violet','turquoise','cadetblue']
    random.shuffle(colors)

    for i in range(0,len(lines)): # highlight lines
        b = lines[i]
        for j in range(b[0],b[1]+1):
            res_left[j][2] = colors[i%len(colors)] # changing line #'s color
        for k in range(b[2],b[3]+1):
            res_right[k][2] = colors[i%len(colors)]

    Template(render_template('left_template.html',left=res_left)).stream().dump('templates/left_filled.html')
    Template(render_template('right_template.html',right=res_right)).stream().dump('templates/right_filled.html')
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
