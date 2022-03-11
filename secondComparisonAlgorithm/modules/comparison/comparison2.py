
from itertools import groupby, count, chain
from ..preprocessing.process import process
from ..hashingFingerprinting.hashFingerprint import hashingFunction

MIN_HASH_THRESHOLD = 0.45 # TODO: test this number more
DEBUG = True

# some time complexity calculations taken from https://wiki.python.org/moin/TimeComplexity

def inverted_index_create(s):
    """
    Takes the output of hashingFunction as input [(ngram, [line numbers]), ...]
    The input list can have the same ngram appear multiple times in the list on different
    line numbers.
    Returns a dictionary {ngram : [line numbers], ...} 
        - each ngram is unique and the list it maps to contains every line that ngram appeared on
        in preprocessing.

    TODO: time complexity
    """
    inverted = {}
    for index, hash in s:
        locations = inverted.setdefault(hash, [])
        for i in index:
            if i not in locations:
                locations.append(i)
    return inverted

def file_setup(document):
    """
    This function performs the same preprocessing and hashing done for the main comparison
    table in app.py, without performing winnowing.
    Returns the output of 'inverted_index_create'
    """
    s = process(document)
    s = hashingFunction(s, 7)
    s = inverted_index_create(s)
    return s

def getMatches(index1, index2):
    """
    Returns a list containing the intersection of ngrams from index1 and index2

    Complexity: O(min(n, m)) on average, O(n * m) worst case
        - n is len(index1)
        - m is len(index2)

    TODO: this function is unnecessary, only used once and doing this manually is faster
    """
    return set.intersection(set(index1.keys()), set(index2.keys()))

def getMatchedIndex(matches, index):
    """
    Condenses the input 'index' to only contain ngrams that were matched in
    both input files.
    Returns this condensed index.

    Complexity: O(m) on average, O(m*n) worst case
        - m is the number of ngrams that appeared in both files
        - the retrieval time of each ngram is O(1) on average, O(n) worst case
    """
    matchedIndex = {}
    for match in matches:
        matchedIndex[match] = index[match]
    return matchedIndex

def invertDict(matchedIndex):
    """
    Inverts the input dictionary 'matchedIndex' {ngram : [line numbers]}
    to the format {line number : [ngrams]}
    
    Complexity: O(m*l)
        - m is the number of matching ngrams
        - l is the average number of lines mapped to each ngram

    TODO: make this more efficient with something like this:
        my_inverted_dict = dict(map(reversed, my_dict.items()))
    """
    newIndex = {}
    for match in matchedIndex:
        lines = matchedIndex[match]
        for line in lines:
            if line in newIndex:
                # line is already in dict, append the ngram to its list
                newIndex[line].append(match)
            else:
                # line isn't in dict, add a new {line : [matches]} mapping 
                newIndex[line] = [match]
    return newIndex

def getLinesOfInterest(matchedIndex, originalIndex):
    """
    Returns a sorted list containing any line with a ratio of
    (matched ngram count) / (original ngram count) greater than 'MIN_HASH_THRESHOLD"

    Complexity: O(l)
        - l is the number of lines that contained matching hashes
    """
    linesOfInterest = []
    for line in matchedIndex:
        mHashes = matchedIndex[line]
        oHashes = originalIndex[line]
        if (len(mHashes) / len(oHashes)) >= MIN_HASH_THRESHOLD:
            linesOfInterest.append(line)
    return sorted(linesOfInterest)

def computeSimilarity(matches, index):
    """
    Computes the similarity score of a file by dividing the number
    of matched ngrams by the original number of ngrams.

    Complexity: O(m + l)
        - m is the number of matched ngrams
        - l is the number of total ngrams
    """
    matchSum = 0
    indexSum = 0
    for match in matches:
        matchSum += len(index[match])
    for lis in index.values():
        # len(lis) is the number of lines an ngram appeared on
        # aka (approximately) the total number of times an ngram appeared
        indexSum += len(lis)

    return matchSum / indexSum

def as_range(g):
    """
    Helper function for blockifyLines.
    """
    l = list(g)
    return [l[0], l[-1]]

def blockifyLines(list):
    """
    Returns a sorted list of line blocks
    i.e. [1, 2, 3, 4, 5, 9, 10, 11, 12] becomes [[1,5], [9,12]]

    Complexity: idk
    """
    list.sort()
    # black magic taken from https://stackoverflow.com/a/10420670
    return [as_range(g) for _, g in groupby(list, key=lambda n, c=count(): n-next(c))]

def translateLines(OldLines, SourceFile, StrippedFile):
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

def highlightedBlocks(file1, file2):
    """
    1.  Processes the input files into an inverted index of ngram hashes mapped to line numbers.

    2.  Takes the set intersection of ngram hashes to determine which sections appear in both files.

    3.  Inverts the inverted index to map line numbers to matched ngrams.

    4.  Calculate the similarity score of each file, use this to determine which file is smaller
    (larger similarity = smallr file). The smaller file will be mapped back to by the larger one.

    5.  Indentify interesting lines by comparing the ratio of matched ngrams on that line to the original
        number of ngrams on that line to a constant ratio, 'MIN_HASH_THRESHOLD'

    6.  Organizes those interesting lines into blocks.

    7.  Maps each interesting line in file1 to its corresponding line in file2 by looking at all of the
        ngrams on that line in file1, then finding which line each of those ngrams maps to in file2, and
        then taking the intersection of that set of lines. Repeat for file2 to file1.

    8.  Maps these corresponding lines to the block number they appear in.

    9.  Translates the line numbers to the line numbers from the original, unprocessed file and
        organizes those into blocks.
    """

    index1 = file_setup(file1)
    index2 = file_setup(file2)
    

    # reduce the hashes in each index to just the ones that are matching
    matches = getMatches(index1, index2)

    # compute similarity score, use this to swap file1 and file2 if necessary
    # because mapping only goes one-way, the larger file should be mapped to the smaller one
    # we will always be mapping file2 to file1, so file1 should be the smaller one
    swapped = False
    score1 = computeSimilarity(matches, index1)
    score2 = computeSimilarity(matches, index2)
    score = min(score1, score2)
    if score1 < score2: #file1 is bigger, it should be the smaller one
        temp = index1; index1 = index2; index2 = temp
        temp = file1; file1 = file2; file2 = temp
        swapped = True

    file1MatchedIndex = getMatchedIndex(matches, index1)
    file2MatchedIndex = getMatchedIndex(matches, index2)

    # swap the index from {hash: [lines]} to {line: [hashes]}
    ii1 = invertDict(file1MatchedIndex)
    ii2 = invertDict(file2MatchedIndex)    

    # do the same for original indices
    oi1 = invertDict(index1)
    oi2 = invertDict(index2)   

    # lines of interest are any line containing enough hashes to meet the condition of
    # len(matchedHashes) / len(originalHashes) > 'MIN_HASH_THRESHOLD'
    loi1 = getLinesOfInterest(ii1, oi1)
    loi2 = getLinesOfInterest(ii2, oi2)

    # organize the lines of interest into blocks (i.e. [1, 2, 3, 4, 6, 7, 8, 10] becomes [[1, 4], [6, 8], [10, 10]])
    lineBlocks = blockifyLines(loi1)
    if DEBUG: print("lineBlocks1 = " + str(lineBlocks))

    # figure out which lines each line from file1 corresponds to in file2 and visa-versa
    # so if line 5 in file1 contains the hashes [2, 5, 6]
    # and lines 2 and 3 in file2 contain the hashes [2, 5] and [5, 6] respectively
    # then we know that file1 line 5 corresponds to file2 lines 2 and 3
    # TODO: compute time complexity of this and make one-way
    if DEBUG: print("finding corresponding lines...", end="\n\n")

    corLines2to1 = {}
    # iterate over lines of interest
    for line in loi2:
        # iterate over ngrams on each line, store which line that ngram is on in file1 in a list
        hashes = ii2[line]
        corLines2to1[line] = []
        for hash in hashes:
            corLines2to1[line].append(file1MatchedIndex[hash])
        # flatten the list
        corLines2to1[line] = list(chain(*corLines2to1[line]))
        # get the line that was mapped to most by the ngrams on this line
        corLines2to1[line] = max(set(corLines2to1[line]), key=corLines2to1[line].count)

    if DEBUG: print("corLines2to1 = " + str(corLines2to1), end="\n\n")

    # now try to match the line blocks, this is for colored block highlighting
    # use the corresponding line values to figure what block a line from file2 belongs to in file1
    # TODO: compute time complexity of this and make one-way

    corBlocks2to1 = {}
    # iterate over lineBlocks1 to see which block in file1 the block in file2 corresponds to
    for i in range(len(lineBlocks)):
        # if the corresponding line maps to a block from file1, store that line in a list
        # mapped to by the index of that block 
        corBlocks2to1[i] = []
        for line in corLines2to1:
            # don't do anything if the line is empty
            if not corLines2to1[line]: continue
            corLine = corLines2to1[line]
            if corLine >= lineBlocks[i][0] and corLine <= lineBlocks[i][1]:
                corBlocks2to1[i].append(line)

    if DEBUG: print("corBlocks2to1 = " + str(corBlocks2to1), end="\n\n")
    
    # finally, map the lines of interest to the lines of the original file,
    # keeping track of which matched block they belong to.
    # This is what we will output to the html generation/highlighting.
    # TODO: compute time complexity of this
    file1Stripped = file1 + "_Stripped"
    file2Stripped = file2 + "_Stripped"

    if DEBUG: print("generating sortedBlocks1...")

    sortedBlocks1 = []
    for i in range(0, len(lineBlocks)):
        if len(lineBlocks[i]) > 0:
            if DEBUG: print("examining lineBlock[" + str(i) + "] = " + str(lineBlocks[i]))
            lines = list(range(lineBlocks[i][0], lineBlocks[i][1]+1))
            lineBlocks[i] = blockifyLines(translateLines(lines, file1, file1Stripped))
            if DEBUG: print("translated lineBlock = " + str(lineBlocks[i]))
            for block in lineBlocks[i]:
                sortedBlocks1.append([i, block])
                if DEBUG: print("added to sortedBlocks1: " + str([i, block]))
    sortedBlocks1.sort(key = lambda x: x[1][0])

    if DEBUG: print("sortedBlocks1 = " + str(sortedBlocks1), end="\n\n")

    for block in corBlocks2to1:
        lines = corBlocks2to1[block]
        if len(lines) > 0: corBlocks2to1[block] = blockifyLines(translateLines(lines, file2, file2Stripped))

    # Sort the blocks and put them in a list [blockid, [block]]
    # TODO: compute time complexity of this
    #sortedBlocks1 = []
    #for i in range(0, len(lineBlocks1)):
    #    sortedBlocks1.append([i, lineBlocks1[i]])
    
    sortedBlocks2 = []
    for key in corBlocks2to1:
        blocks = corBlocks2to1[key]
        for block in blocks:
            sortedBlocks2.append([key, block])
    sortedBlocks2.sort(key = lambda x: x[1][0])

    print("similarity score: " + str(score))
    if DEBUG: print("Swapped = " + str(swapped))

    if swapped:
        if DEBUG: print("Output = " + str((sortedBlocks2, sortedBlocks1)), end="\n\n")
        return (sortedBlocks2, sortedBlocks1)
    if DEBUG: print("Output = " + str((sortedBlocks1, sortedBlocks2)), end="\n\n")
    return ((sortedBlocks1, sortedBlocks2))