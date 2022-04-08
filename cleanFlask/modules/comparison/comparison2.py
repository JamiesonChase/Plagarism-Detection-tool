
from itertools import groupby, count
from ..preprocessing.process import process
from ..hashingFingerprinting.hashFingerprint import hashingFunction

MIN_HASH_THRESHOLD = 0.8

def inverted_index_create(s):
    inverted = {}
    for index, hash in s:
        locations = inverted.setdefault(hash, [])
        for i in index:
            if i not in locations:
                locations.append(i)
    return inverted

def file_setup(document):

    # function to do the initial setup of the file
    s = process(document)
    s = hashingFunction(s, 7)
    s = inverted_index_create(s)
    return s

def getStripped(fileName):
    strippedFileName = fileName + "_Stripped"
    return strippedFileName

def getMatches(index1, index2):
    """
    returns a list containing the intersection of hashes from index1 and index2
    """
    return set.intersection(set(index1.keys()), set(index2.keys()))

def getMatchedHashes(matches, index):
    matchedIndex = {}
    for match in matches:
        matchedIndex[match] = index[match]
    return matchedIndex

def invertDict(matchedIndex):
    newIndex = {}
    for match in matchedIndex:
        lines = matchedIndex[match]
        for line in lines:
            if line in newIndex:
                newIndex[line].append(match)
            else:
                newIndex[line] = [match]
    return newIndex

def getLinesOfInterest(matchedIndex, originalIndex):
    """
    Returns a sorted list containing any line
    """
    linesOfInterest = []
    for line in matchedIndex:
        mHashes = matchedIndex[line]
        oHashes = originalIndex[line]
        if (len(mHashes) / len(oHashes)) >= MIN_HASH_THRESHOLD:
            linesOfInterest.append(line)
    return sorted(linesOfInterest)

def computeSimilarity(matches, index):
    matchSum = 0
    indexSum = 0
    for match in matches:
        matchSum += len(index[match])
    for lis in index.values():
        indexSum += len(lis)

    return matchSum / indexSum


# this part taken from https://stackoverflow.com/a/10420670
def as_range(g):
    l = list(g)
    return [l[0], l[-1]]

def blockifyLines(list):
    uniqueLines = []
    for num in list:
        if not num in uniqueLines:
            uniqueLines.append(num)
    uniqueLines.sort()
    # black magic taken from https://stackoverflow.com/a/10420670
    return [as_range(g) for _, g in groupby(uniqueLines, key=lambda n, c=count(): n-next(c))]

def translateLines(OldLines, SourceFile, StrippedFile):
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

def highlightedBlocks(file1, file2):
    """
    Takes the 'ws' from the following code segment:
    > s = process(document)
    > s = hashingFunction(s, 7)
    > ws = inverted_index_create(s)
    as input for index1 and index2

    more arguments: , strippedFile1, strippedFile2, file1, file2
    """

    index1 = file_setup(file1)
    index2 = file_setup(file2)
    file1Stripped = getStripped(file1)
    file2Stripped = getStripped(file2)

    # reduce the hashes in each index to just the ones that are matching
    matches = getMatches(index1, index2)
    file1MatchedHashes = getMatchedHashes(matches, index1)
    file2MatchedHashes = getMatchedHashes(matches, index2)

    # compute similarity score
    score = min(computeSimilarity(matches, index1), computeSimilarity(matches, index2))

    # swap the index from {hash: [lines]} to {line: [hashes]}
    ii1 = invertDict(file1MatchedHashes)
    ii2 = invertDict(file2MatchedHashes)    

    # do the same for original indices
    oi1 = invertDict(index1)
    oi2 = invertDict(index2)   

    # lines of interest are any line containing enough hashes to meet the condition of
    # len(matchedHashes) / len(originalHashes) > 'MIN_HASH_THRESHOLD'
    loi1 = getLinesOfInterest(ii1, oi1)
    loi2 = getLinesOfInterest(ii2, oi2)

    # organize the lines of interest into blocks (i.e. [1, 2, 3, 4, 6, 7, 8, 10] becomes [[1, 4], [6, 8], [10, 10]])
    lineBlocks1 = blockifyLines(loi1)
    lineBlocks2 = blockifyLines(loi2)

    # figure out which lines each line from file1 corresponds to in file2 and visa-versa
    # so if line 5 in file1 contains the hashes [2, 5, 6]
    # and lines 2 and 3 in file2 contain the hashes [2, 5] and [5, 6] respectively
    # then we know that file1 line 5 corresponds to file2 lines 2 and 3
    corLines1to2 = {}
    for line in loi1:
        hashes = ii1[line]
        corLines1to2[line] = []
        for hash in hashes:
            corLines1to2[line].append(file2MatchedHashes[hash])
        corLines1to2[line] = list(set.intersection(*map(set, corLines1to2[line])))

    corLines2to1 = {}
    for line in loi2:
        hashes = ii2[line]
        corLines2to1[line] = []
        for hash in hashes:
            corLines2to1[line].append(file1MatchedHashes[hash])
        corLines2to1[line] = list(set.intersection(*map(set, corLines2to1[line])))       

    # now try to match the line blocks, this is for colored block highlighting
    # use the corresponding line values to figure what block a line from file1 belongs to in file2
    # and visa-versa
    uniqueBlocks1to2 = {}
    for i in range(len(lineBlocks2)):
        uniqueBlocks1to2[i] = []
        for line in corLines1to2:
            if not corLines1to2[line]: continue
            corLine = corLines1to2[line][0]
            if corLine >= lineBlocks2[i][0] and corLine <= lineBlocks2[i][1]:
                uniqueBlocks1to2[i].append(line)

    uniqueBlocks2to1 = {}
    for i in range(len(lineBlocks1)):
        uniqueBlocks2to1[i] = []
        for line in corLines2to1:
            if not corLines2to1[line]: continue
            corLine = corLines2to1[line][0]
            if corLine >= lineBlocks1[i][0] and corLine <= lineBlocks1[i][1]:
                uniqueBlocks2to1[i].append(line)
            
    # finally, map the lines of interest to the lines of the original file,
    # keeping track of which matched block they belong to.
    # This is what we will output to the html generation/highlighting.
    for block in uniqueBlocks1to2:
        lines = uniqueBlocks1to2[block]
        if len(lines) > 0:
            uniqueBlocks1to2[block] = blockifyLines(translateLines(lines, file1, file1Stripped))

    for block in uniqueBlocks2to1:
        lines = uniqueBlocks2to1[block]
        if len(lines) > 0: uniqueBlocks2to1[block] = blockifyLines(translateLines(lines, file2, file2Stripped))


    sortedBlocks1 = []
    for key in uniqueBlocks1to2:
        blocks = uniqueBlocks1to2[key]
        for block in blocks:
            sortedBlocks1.append([key, block])
    sortedBlocks1.sort(key = lambda x: x[1][0])

    sortedBlocks2 = []
    for key in uniqueBlocks2to1:
        blocks = uniqueBlocks2to1[key]
        for block in blocks:
            sortedBlocks2.append([key, block])
    sortedBlocks2.sort(key = lambda x: x[1][0])

    print("similarity score: " + str(score))

    return (sortedBlocks1, sortedBlocks2)