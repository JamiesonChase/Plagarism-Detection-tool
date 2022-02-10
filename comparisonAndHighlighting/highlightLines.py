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
    MIN_MATCH_SIZE = 3 # A match must be at least this long 
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
    
def getHighlightedLines(file1, file2):
    """
    Finds matching sections of text between both file inputs, returning their corresponding line locations.

    Returns a tuple of the format:
    (file1LineBlocks=[(minLine0, maxLine0),(minLine1, maxLine1), ...], file2LineBlocks=[(minLine0, maxLine0),(minLine1, maxLine1), ...])
    """
    file1String = ""
    file2String = ""

    # store each file in a string
    with open(file1, mode = "r") as f1:
        file1String = f1.read()
    with open(file2, mode = "r") as f2:
        file2String = f2.read()

    # get the matching sections of each file
    matches = findMatches(file1String, file2String)
    
    # get the corresponding line numbers of each matching section in both files
    file1LineBlocks = []
    file2LineBlocks = []
    for match in matches:
        file1LineBlocks.append(getLines(file1String, match.a, match.a + match.size))
        file2LineBlocks.append(getLines(file2String, match.b, match.b + match.size))      

    return (file1LineBlocks, file2LineBlocks)