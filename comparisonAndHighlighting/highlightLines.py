from difflib import SequenceMatcher
from xmlrpc.client import MAXINT

MIN_MATCH_SIZE = 3 # A match must be at least this long 

def findMatches(string1, string2):

    matches = []

    if len(string1) < 1 or len(string2) < 1:
        return matches
    
    size = MAXINT
    while True:
        s = SequenceMatcher(lambda x: x == "\0", string1, string2)
        match = s.find_longest_match(0, len(string1), 0, len(string2))
        a = match.a
        b = match.b
        size = match.size
        if size >= MIN_MATCH_SIZE:
            matches.append(match)
            string1 = string1[:a] + "\0" * size + string1[a+size:]
            string2 = string2[:b] + "\0" * size + string2[b+size:]
        else:
            break

    return matches    

def getHighlightedLines(file1, file2):
    file1String = ""
    file2String = ""

    with open(file1, mode = "r") as f1:
        file1String = f1.read()

    with open(file2, mode = "r") as f2:
        file2String = f2.read()

    matches = findMatches(file1String, file2String)
    
    for match in matches:
        print("`" + file1String[match.a : match.a + match.size] + "`\n")


getHighlightedLines("databaseFile1.py_Stripped", "databaseFile2.py_Stripped")