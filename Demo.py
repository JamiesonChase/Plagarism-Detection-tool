from preprocessing.process import process
from hashingFingerprinting.hashFingerprint import hashingFunction
from winnowing.winnowing import winnow
import pprint as pp
from colorama import Fore, Back, Style

def inverted_index_create(s): # create inverted index for particular document
    inverted = {}
    for index, hash in s:
        locations = inverted.setdefault(hash, [])
        for i in index:
            if i not in locations:
                locations.append(i)
    return inverted

def corpus_add_index(corpus,doc_id, s): # add an inverted index to corpus
    for word, locations in s.items():
        indices = corpus.setdefault(word, {})
        indices[doc_id] = locations
    return corpus

def main():

    corpus = {}
    documents = {'doc1':'testfiles/test.py', 'doc2':'testfiles/test2.py', 'doc3':'testfiles/databaseFile1.py', 'doc4':'testfiles/databaseFile2.py', 'doc5':'testfiles/databaseFile3.py', 'doc6':'testfiles/databaseFile4.py', 'doc7':'testfiles/databaseFile5.py'} # add test files
    for doc_id,path in documents.items():
        s = process(path) # pre-process doc
        s = hashingFunction(s, 10) # create finger print hashes
        s = winnow(10, s) # perform winnowing algo
        s = inverted_index_create(s) # created the inverted index
        corpus = corpus_add_index(corpus,doc_id,s) # add index to corpus
    pp.pprint(corpus) # pretty print corpus


    a = process('testfiles/inputFile.py') #The input file that is going to be compared against the corpus
    a = hashingFunction(a, 10) #Get the hases of the input document.
    a = winnow(10, a) #Get the fingerprints of the input document.
    amountMatched = {'doc1': 0, 'doc2': 0, 'doc3': 0, 'doc4': 0, 'doc5': 0, 'doc6': 0, 'doc7': 0} #The amount of fingerprints matched.
    listOfLinesMatched = {'doc1': [], 'doc2': [], 'doc3': [], 'doc4': [], 'doc5': [], 'doc6': [], 'doc7': []} # What lines in the input document is matched.
    for index,hash in a: #For every hash and index from the input file 
        if hash in corpus: #If the hash is in the corpus
            for key in corpus[hash]: #Get the keys from the corpus which is DocID
                amountMatched[key] += 1 #Increment amount of fingerprints match for that document.
                listOfLinesMatched[key] += index  #Add the line numbers that match the input document for that DocID

    for key in listOfLinesMatched: #For each DocID
        listOfLinesMatched[key] = list(set(listOfLinesMatched[key])) #Turn the lines number into a set to get the each unique line number and it should order them.
        

    sizeOfInputFile = len(a) #Get the number of fingerprints from the input file to be used to calculate the percentage.
    for key in listOfLinesMatched: #For each DocID
        percentage = (amountMatched[key] / sizeOfInputFile) * 100 #Calculate the percentage.

        print("input file compared to " + key " is: \n\n\n") #Say what the document the input file is being compared o.
        f = open('testfiles/inputFile.py') #Open the input file.
        lines = f.readlines() #Get all the lines.
        i = 1 # Line counter.
        for line in lines: #For each line in th input document.
            if (i in listOfLinesMatched[key]): #If it is one of the line number frrom listOFLinesMatched[key]
                print(Fore.BLUE + line) #Print the line in blue.
                print(Style.RESET_ALL) #Reset the style so other lines won't be printed in blue.
            else:
                print(line) # else print the line regularly.

            i = i + 1 #Increment line number count.
        

        print(Style.RESET_ALL) # to print out other things normally.
        f.close # Close the file.
        print("Percentage matched is: " + str(percentage) + "\n\n") #Print out what the percentage is.
        print("- - - - - - - - - - - - - - - - - -") # Print a divider.

    
    
main()
