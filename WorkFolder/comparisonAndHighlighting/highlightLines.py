from difflib import SequenceMatcher

def findMatches(string1, string2):    
    """
    Repeatedly searches for longest common substrings within both input strings
    until a substring too small is found.

    Returns a list of named tuples match(a, b, size) where
    -a = the start index of the match in string1
    -b = the start index of the match in string2
    -size = the length of the matching string
    """
    MIN_MATCH_SIZE = 5 # A match must be at least this long 
    matches = []

    # return empty list if either string is empty
    if len(string1) < 1 or len(string2) < 1:
        return matches
    
    # loop until no large enough matches
    while True:
        # find the longest substring ignoring null characters
        s = SequenceMatcher(lambda x: x == "\0", string1, string2)
        match = s.find_longest_match(0, len(string1), 0, len(string2))
        a = match.a
        b = match.b
        size = match.size
        # make sure the substring is long enough
        if size >= MIN_MATCH_SIZE:
            matches.append(match)
            # replace the matching sections with null characters
            string1 = string1[:a] + "\0" * size + string1[a+size:]
            string2 = string2[:b] + "\0" * size + string2[b+size:]
        else:
            break

    return matches    

def getLines(string, matchMin, matchMax):
    """
    Returns a tuple (minLine, maxLine) where
    -minLine = the line number of the min index
    -maxLine = the line number of the max index 
    """
    minLine = len(string[:matchMin+1].splitlines(keepends=True)) - 1
    maxLine = len(string[:matchMax+1].splitlines(keepends=True)) - 1
    return(minLine, maxLine)
    
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

    return (file1LineBlocks, file2LineBlocks)

def TranslateLines(StrippedFile,OldLines,SourceFile):
    file = open(StrippedFile)
    content = file.readlines()  # Get all lines from stripped file
    newlines = []
    i = 0
    lookup = content[OldLines[0]-1].strip()  # initialize first line
    with open(SourceFile) as myFile:  # iterate through source file
        for num, line in enumerate(myFile, 1):
            if lookup in line:  # if processed line is in source line
                newlines.append(num)  # append source line value
                if i < len(OldLines)-1:
                    i = i+1  # iterate through each suspect old line
                lookup = content[OldLines[i]-1].strip() #
    return newlines  # return list of translated lines

def getHighlightLines(file1, file2, processedFile1, processedFile2, strippedFile1, strippedFile2):

    lines = matchProcessedLines(processedFile1, processedFile2)
    file1Lines = lines[0]
    file2Lines = lines[1]

    newLines1 = []
    newLines2 = []

    # convert the line blocks from matching to line up with the original files
    for lineBlock in file1Lines:
        lines = list(range(lineBlock[0], lineBlock[1] + 1))
        newLineBlock = TranslateLines(strippedFile1, lines, file1)
        newLineBlock = (min(newLineBlock), max(newLineBlock)) 
        newLines1.append(newLineBlock)

    for lineBlock in file2Lines:
        lines = list(range(lineBlock[0], lineBlock[1] + 1))
        newLineBlock = TranslateLines(strippedFile2, lines, file2)
        newLineBlock = (min(newLineBlock), max(newLineBlock)) 
        newLines2.append(newLineBlock)

    newLines1.sort(key=lambda a : a[0])
    newLines2.sort(key=lambda a : a[0])

    return (newLines1, newLines2)