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
import sys 
import line_profiler
import atexit
profile = line_profiler.LineProfiler()
prof = line_profiler.LineProfiler()
atexit.register(profile.print_stats)
import sys 



global r 
r = []
global lists 
lists = [] #How initial information about the input

@profile
def createNgrams(dir):
    global lists
    global r
    documents = os.listdir(dir)  # find documents inside testfiles directory
    lists = []
    for doc in documents: # Go through the process of getting the winnowed information for the inputs
        originalName = doc 
        doc = dir + doc
        a=process(doc)
        a=hashingFunction(a,7)
        a=winnow(4,a)
        lists.append([a,doc,originalName]) # winnow the hashes and append to lists

def comparisons():
    global lists
    global r
    idNumber = 0

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
            #items[idNumber] = lists[i][1] + ' - ' + corpusLists[j][1]
            r.append([idNumber, lists[i][1] + ' - ' + lists[j][1],100*sum/min(len(a),len(b)),lines]) # append to result
            idNUmber = idNumber + 1

    r = sorted(r, key=lambda tup: tup[2], reverse=True) # sort by lines matched, tup[2] -> tup[1] to sort by %

    total = 0
    num = 0
    for x in r:
        print(x)
        
        total = total + x[2]
        num = num + 1

    average = total / num 
    print("Average is: " + str(average))


@profile
def comparisonsFilter():
    global lists
    global r
    idNumber = 0

    r=[] # Just calculate similairty based off of the inputs
    for i in range(0,len(lists)):
        a = lists[i][0]
        a = [lis[1] for lis in a] # do intersection comparison
        leftFileNameKey = lists[i][1].split("_")
        leftFileNameKey = leftFileNameKey[0]
        for j in range(i+1,len(lists)):
            rightFileNameKey = lists[j][1].split("_")
            rightFileNameKey = rightFileNameKey[0]
            if (rightFileNameKey == leftFileNameKey):
                continue

            b = lists[j][0]
            b = [lis[1] for lis in b]
            s = dl.SequenceMatcher(None, a, b) # sequence match a&b
            sum = 0
            lines = 0
            for block in s.get_matching_blocks(): #get matching blocks
                sum = sum + block[2] # calculate total matched hashes
                if block[0] < len(a)-1 and block[1] < len(b)-1: # calculate lines matched
                    lines = lines + -lists[i][0][block[0]][0] + lists[i][0][block[0]+block[2]-1][0] + 1
            #items[idNumber] = lists[i][1] + ' - ' + corpusLists[j][1]
            r.append([idNumber, lists[i][1] + ' - ' + lists[j][1],100*sum/min(len(a),len(b)),lines]) # append to result
            idNUmber = idNumber + 1

    r = sorted(r, key=lambda tup: tup[2], reverse=True) # sort by lines matched, tup[2] -> tup[1] to sort by %

    total = 0
    num = 0
    for x in r:
        print(x)
        
        total = total + x[2]
        num = num + 1

    average = total / num 
    print("Average is: " + str(average))

    
def cleanDirectory(dir):
    directory = dir
    files_in_directory = os.listdir(directory)
    filtered_files = [file for file in files_in_directory if file.endswith("_Stripped")]
    for file in filtered_files:
        path_to_file = os.path.join(directory, file)
        os.remove(path_to_file)

if (len(sys.argv) == 2):
    createNgrams(sys.argv[1])
    comparisons()
    cleanDirectory(sys.argv[1])

elif (len(sys.argv) == 3): # Command line argument to use the filter.
    if (sys.argv[1] != "-f"):
        print("Format: python3 timeTesting.py [input directory] or python3 timeTesting.py -f [input directory]")
        exit()

    createNgrams(sys.argv[2])
    comparisonsFilter()
    cleanDirectory(sys.argv[2])

else: # Error in the format.
    print("Format: python3 timeTesting.py [input directory] or python3 timeTesting.py -f [input directory]")
    exit()



#cleanDirectory()


    