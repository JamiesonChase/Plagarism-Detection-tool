import itertools
from preprocessing.process import process
from preprocessing.translate import TranslateLines
from hashingFingerprinting.hashFingerprint import hashingFunction
from winnowing.winnowing import winnow
import os
from prettytable import PrettyTable

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

def main():

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

# how to get strings from table rows
    for row in table:
        row.border = False
        row.header = False
        print(row.get_string(fields=["doc pairs"]).strip())  # Column 1
        print(row.get_string(fields=["Pair Similarity"]).strip())  # Column 1
    createMainTableHTML(table)

def createMainTableHTML(table):
    f = open('index.html', 'w')
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
    <th>doc pairs</th>
    <th>Pair similarity</th>
    </tr>
    """
    for row in table:
        row.border = False
        row.header = False
        html_template = html_template + "<tr>\n<th>"
        html_template = html_template + row.get_string(fields=["doc pairs"]).strip() + "</th>\n"
        html_template = html_template + "<th>" + row.get_string(fields=["Pair Similarity"]).strip() + "</th>\n</tr>" 

    html_template = html_template + "</table>\n</body>\n</html>"
    f.write(html_template)
    f.close()
    return 


main()