from difflib import SequenceMatcher
from itertools import groupby, count

def findMatches(s1, s2):    
    """
    Repeatedly searches for longest common substrings within both input strings
    until a substring too small is found.

    Returns a list of named tuples match(a, b, size) where
    -a = the start index of the match in string1
    -b = the start index of the match in string2
    -size = the length of the matching string
    """
    MIN_MATCH_SIZE = 5 # A match must be at least this long 

    string1 = s1
    string2 = s2

    sm = SequenceMatcher(None, string1, string2)
    blocks = sm.get_matching_blocks()
    goodBlocks = []
    for match in blocks:
        a = match.a
        b = match.b
        size = match.size
        if size >= MIN_MATCH_SIZE:
            goodBlocks.append(match)
    return goodBlocks  

def getLines(string, matchMin, matchMax):
    """
    Returns a tuple (minLine, maxLine) where
    -minLine = the line number of the min index
    -maxLine = the line number of the max index 
    """
    minLine = len(string[:matchMin+1].splitlines(keepends=True)) - 1
    maxLine = len(string[:matchMax+1].splitlines(keepends=True)) - 1
    return [minLine, maxLine]
    
def matchProcessedLines(file1String, file2String):
    """
    Finds matching sections of text between both string inputs, returning their corresponding line locations.
    String inputs should be from preprocessed files

    Returns a tuple of the format:
    (file1LineBlocks=[(minLine0, maxLine0),(minLine1, maxLine1), ...], file2LineBlocks=[(minLine0, maxLine0),(minLine1, maxLine1), ...])
    """

    # get the matching sections of each file
    matches = findMatches(file1String, file2String)
    
    # get the corresponding line numbers of each matching section in both files
    file1LineBlocks = []
    file2LineBlocks = []
    for match in matches:
        file1LineBlocks.append(getLines(file1String, match.a, match.a + match.size))
        file2LineBlocks.append(getLines(file2String, match.b, match.b + match.size))

    return [file1LineBlocks, file2LineBlocks]

def TranslateLines(StrippedFile,OldLines,SourceFile):
    file = open(StrippedFile)
    content = file.readlines()  # Get all lines from stripped file
    newlines = []
    i = 0
    lookup = content[OldLines[0]].strip()  # initialize first line
    with open(SourceFile) as myFile:  # iterate through source file
        for num, line in enumerate(myFile, 1):
            if lookup in line:  # if processed line is in source line
                newlines.append(num - 1)  # append source line value
                if i < len(OldLines)-1:
                    i = i+1  # iterate through each suspect old line
                lookup = content[OldLines[i]].strip() #
    return newlines  # return list of translated lines

# this part taken from https://stackoverflow.com/a/10420670
def as_range(g):
    l = list(g)
    return [l[0], l[-1]]

def blockifyLines(list):
    uniqueLines = []
    for numberlist in list:
        for num in numberlist:
            if not num in uniqueLines:
                uniqueLines.append(num)
    uniqueLines.sort()
    # black magic taken from https://stackoverflow.com/a/10420670
    return [as_range(g) for _, g in groupby(uniqueLines, key=lambda n, c=count(): n-next(c))]


def getHighlightLines(file1, file2, processedFile1, processedFile2, strippedFile1, strippedFile2):

    f1 = open(processedFile1, "r"); string1 = f1.read(); f1.close()
    f2 = open(processedFile2, "r"); string2 = f2.read(); f2.close()

    matchProcessedLines(string1, string2)

    matchedLines = matchProcessedLines(string1, string2)
    file1Lines = matchedLines[0]
    file2Lines = matchedLines[1]

    newLines1 = []
    newLines2 = []

    # convert the line blocks from matching to line up with the original files
    for lineBlock in file1Lines:
        lines = list(range(lineBlock[0], lineBlock[1] + 1))
        newLineBlock = TranslateLines(strippedFile1, lines, file1)
        newLines1.append(newLineBlock)

    for lineBlock in file2Lines:
        lines = list(range(lineBlock[0], lineBlock[1] + 1))
        newLineBlock = TranslateLines(strippedFile2, lines, file2)
        newLines2.append(newLineBlock)
    

    return [blockifyLines(newLines1), blockifyLines(newLines2)]

#lines = getHighlightLines("databaseFile2.py", "databaseFile3.py", "databaseFile2.py_Processed", "databaseFile3.py_Processed", "databaseFile2.py_Stripped", "databaseFile3.py_Stripped")
#print("output: " + str(lines))
