import itertools
from preprocessing.process import process
from preprocessing.translate import TranslateLines
from hashingFingerprinting.hashFingerprint import hashingFunction
from winnowing.winnowing import winnow
import os
from prettytable import PrettyTable

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
        else:
            t.add_row([documents[doc_id] + " - " + inputfile,"{:05.2f}".format(percentages / eachCorpusFileTotalHashes[doc_id] * 100)])
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
        eachCorpusFileTotalHashes[doc_id] = len(s)
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

    
    i = 0

# how to get strings from table rows
    Rows = table.rows
    Rows.sort(key=lambda x: x[1], reverse=True)
    createMainTableHTML(Rows)


    for row in Rows:
        currentName = row[0]
        #print(currentName)

        splitNames = currentName.split(" - ")
        createIFramePage(i)
        # Here is where you call your functions
        createJumpTable(i, [[0, 5]], [[0, 5]])
        createHTMLFiles(splitNames[0], [[0, 5]], 2,i)
        createHTMLFiles(splitNames[1], [[0, 5]], 3,i)
        i = i + 1
        
        #print(row.get_string(fields=["doc pairs"]).strip())  # Column 1
        #print(row.get_string(fields=["Pair Similarity"]).strip())  # Column 1
   
    

    


def createMainTableHTML(Rows):
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
    <th>doc Pairs</th>
    <th>Pair Similarity</th>
    </tr>
    """
    i = 0
    for row in Rows:
        html_template = html_template + "<tr>\n<th><A HREF=\"{currentNumber}-1.html\">{name}</A></th>\n".format(currentNumber=i,name=row[0])
        html_template = html_template + "<th>{percentScore}</th>\n</tr>\n".format(percentScore=row[1])   
        i = i + 1
        

        

    html_template = html_template + "</table></body>\n</html>"
    f.write(html_template)
    f.close()
    return 

def createIFramePage(currentRowNumber):
    htmlFileName = "{number}-1.html".format(number=currentRowNumber)

    f = open(htmlFileName, 'w')
    html_template = """<!DOCTYPE html>
    <html>
    <head>
    <title>Side by side Comparison</title>
    
    </head>
    """
    html_template = html_template + "<iframe src=\"{number}-4.html\" height=\"150\" width=\"100%\" title=\"TableFile\"></iframe>\n".format(number=currentRowNumber)
    html_template = html_template + "<iframe src=\"{number}-2.html\" height=\"450\" width=\"47%\" name=\"LeftFile\"></iframe>\n".format(number=currentRowNumber)
    html_template = html_template + "<iframe src=\"{number}-3.html\" height=\"450\" width=\"47%\" name=\"RightFile\"></iframe>\n".format(number=currentRowNumber)
    html_template = html_template + "</body>\n</html>"
    f.write(html_template)
    f.close()
    return 

def createJumpTable(currentRowNumber, arrayOfNamesLeft, arrayOfNamesRight):
    htmlFileName = "{number}-4.html".format(number=currentRowNumber)

    f = open(htmlFileName, 'w')
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
    if (len(arrayOfNamesLeft) >= len(arrayOfNamesRight)):
        for var in list(range(len(arrayOfNamesLeft))):
            html_template = html_template + "<tr>"
            if (var < len(arrayOfNamesLeft)):
                html_template = html_template + "<th><A HREF=\"{number}-2.html#{jumpPoint}\" TARGET=\"LeftFile\">{l}-{r}</A></th>\n".format(number=currentRowNumber,jumpPoint=var,l=arrayOfNamesLeft[var][0],r=arrayOfNamesLeft[var][1])
            else:
                pass

            if (var < len(arrayOfNamesRight)):
                html_template = html_template + "<th><A HREF=\"{number}-3.html#{jumpPoint}\" TARGET=\"RightFile\">{l}-{r}</A></th>\n".format(number=currentRowNumber,jumpPoint=var,l=arrayOfNamesRight[var][0],r=arrayOfNamesRight[var][1])
            else:
                pass

            html_template = html_template + "</tr>\n"
    else:
        
        for var in list(range(len(arrayOfNamesRight))):
            
            html_template = html_template + "<tr>"
            if (var < len(arrayOfNamesLeft)):
                html_template = html_template + "<th><A HREF=\"{number}-2.html#{jumpPoint}\" TARGET=\"LeftFile\">{l}-{r}</A></th>\n".format(number=currentRowNumber,jumpPoint=var,l=arrayOfNamesLeft[var][0],r=arrayOfNamesLeft[var][1])
            else:
                html_template = html_template + "<th></th>\n"

            if (var < len(arrayOfNamesRight)):
                
                
                html_template = html_template + "<th><A HREF=\"{number}-3.html#{jumpPoint}\" TARGET=\"RightFile\">{l}-{r}</A></th>\n".format(number=currentRowNumber,jumpPoint=var,l=arrayOfNamesRight[var][0],r=arrayOfNamesRight[var][1])
            else:
                pass

            html_template = html_template + "</tr>\n"
    
    html_template = html_template + "</table>\n</body>\n</html>"
    f.write(html_template)
    f.close()
    return 

def createHTMLFiles(fileName, blocks ,LeftOrRight,currentRowNumber):
    a_file = open(fileName)
    
    lines = a_file.readlines()






    htmlFileName = "{number}-{side}.html".format(number=currentRowNumber,side=LeftOrRight)

    f = open(htmlFileName, 'w')
    html_template = """<!DOCTYPE html><html><head><title>{nameOfFile}</title></head><body BGCOLOR=white><HR>{nameOfFile}<p><PRE>\n""".format(nameOfFile=fileName)
    f.write(html_template)
    a_file.close()
    i = 0
    blockNumber = 0
    jumpPoint = 0
    for line in lines:
        
        

        if (blockNumber < len(blocks) and i == blocks[blockNumber][0]):
            f.write("<A NAME=\"{j}\"></A><FONT color = #FF0000>".format(j=jumpPoint))
            jumpPoint = jumpPoint + 1
        
        f.write(line)
        if (blockNumber < len(blocks) and i == blocks[blockNumber][1]):
            f.write("</FONT>")
            blockNumber = blockNumber + 1

        i = i + 1
        
    
    f.write("</PRE></PRE></Body></HTML>")
    f.close()

    

    



main()
