
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

    #print("Lines of interest:")
    #print(loi1)
    #print(loi2, end="\n\n")

    # organize the lines of interest into blocks (i.e. [1, 2, 3, 4, 6, 7, 8, 10] becomes [[1, 4], [6, 8], [10, 10]])
    lineBlocks1 = blockifyLines(loi1)
    lineBlocks2 = blockifyLines(loi2)

    #print("Line blocks: ")
    #print(lineBlocks1)
    #print(lineBlocks2, end="\n\n")

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
    
    #print("Line correspondances:")
    #print(corLines1to2)
    #print(corLines2to1, end="\n\n")        

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
            
    #print("Unique blocks: ")
    #print(uniqueBlocks1to2)
    #print(uniqueBlocks2to1, end="\n\n")

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

    #print(uniqueBlocks1to2)
    #print(uniqueBlocks2to1, end="\n\n")

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

    #print(sortedBlocks1)
    #print(sortedBlocks2, end="\n\n")
    #
    #print("similarity score: " + str(score))

    return (uniqueBlocks1to2, uniqueBlocks2to1)

#index1 = {11921: [1, 11], 11100: [1, 11], 9304: [1, 11], 5584: [1, 11], 7104: [1, 11], 5280: [1, 11], 5526: [2, 7, 14], 5836: [2, 7, 14], 4309: [2, 3, 4, 7, 8, 9, 14], 4554: [2, 3, 4, 7, 8, 9, 14], 5061: [2, 14], 6058: [2, 14], 8063: [2], 5150: [2], 6254: [2], 4732: [2], 5400: [2], 4560: [2], 5056: [2], 4694: [3], 5324: [3], 5098: [3, 4, 9], 6132: [3, 4, 9], 8211: [3, 4, 9], 5446: [3, 4, 9], 6882: [3, 9], 5988: [3, 9], 7912: [3, 9], 4848: [3, 9], 5632: [3, 9], 5846: [4], 7628: [4], 6845: [4], 5914: [4], 7764: [4], 4552: [4], 5040: [4], 4690: [5], 5385: [5], 4614: [5, 10], 5249: [5, 10], 6516: [5, 10], 9046: [5, 10], 14028: [5, 10], 13550: [5, 10], 14272: [5], 13797: [5], 12720: [5], 10880: [5], 7750: [6], 11444: [6], 11966: [6, 13], 11176: [6], 9456: [6], 5942: [6], 7829: [6], 6756: [6], 8424: [6], 5872: [6], 6144: [6], 8224: [6, 13], 5095: [7, 8], 6177: [7, 8], 8341: [7, 8], 5706: [7, 8], 7348: [7, 8], 6920: [7, 8], 9776: [7, 8], 9014: [8, 9], 7436: [8, 9], 5874: [10], 7753: [10], 14204: [10], 13660: [10], 12445: [10], 10400: [10], 6752: [10], 9478: [11], 7988: [11], 5552: [12], 5970: [12], 4621: [12], 5256: [12], 6532: [12], 9008: [12], 14003: [12], 13753: [12], 12997: [12], 12637: [12], 11235: [12], 7722: [12], 10425: [12], 10328: [12], 10064: [12], 9574: [13], 8564: [13], 11173: [13], 9476: [13], 5928: [13], 7792: [13], 6656: [13], 8065: [14], 5171: [14], 6278: [14], 4834: [14], 5612: [14], 4993: [14], 5976: [14], 6232: [15], 6283: [15], 8553: [15], 6181: [16], 7325: [16], 9446: [16], 7967: [16], 10897: [16], 10229: [16], 9927: [16], 9271: [16]}
#index2 = {11921: [1, 11], 11100: [1, 11], 9304: [1, 11], 5584: [1, 11], 7104: [1, 11], 5280: [1, 11], 5526: [2, 7, 12, 16], 5836: [2, 7, 12, 16], 4309: [2, 3, 4, 7, 8, 9, 12, 13, 14, 16], 4554: [2, 3, 4, 7, 8, 9, 12, 13, 14, 16], 5061: [2, 12], 6058: [2, 12], 8063: [2], 5150: [2], 6254: [2], 4732: [2], 5400: [2], 4560: [2], 5056: [2], 4694: [3], 5324: [3], 5098: [3, 4, 9, 16], 6132: [3, 4, 9, 16], 8211: [3, 4, 9, 16], 5446: [3, 4, 9, 16], 6882: [3, 9], 5988: [3, 9], 7912: [3, 9], 4848: [3, 9], 5632: [3, 9], 5846: [4], 7628: [4], 6845: [4], 5914: [4], 7764: [4], 4552: [4], 5040: [4], 4690: [5], 5385: [5], 4614: [5, 10], 5249: [5, 10], 6516: [5, 10], 9046: [5, 10], 14028: [5, 10], 13550: [5, 10], 14272: [5], 13797: [5], 12720: [5], 10880: [5], 7750: [6], 11444: [6], 11966: [6, 15], 11176: [6], 9456: [6], 5942: [6], 7829: [6], 6756: [6], 8424: [6], 5872: [6], 6144: [6], 8224: [6, 15], 5095: [7, 8, 13], 6177: [7, 8, 13], 8341: [7, 8, 13], 5706: [7, 8, 13], 7348: [7, 8, 13], 6920: [7, 8, 13], 9776: [7, 8, 13], 9014: [8, 9, 14], 7436: [8, 9, 14], 5874: [10], 7753: [10], 14204: [10], 13660: [10], 12445: [10], 10400: [10], 6752: [10], 9478: [11], 7988: [11], 8052: [12], 5128: [12], 6192: [12], 4662: [13], 5260: [13], 5096: [14], 6210: [14], 8441: [14], 5975: [14], 7954: [14], 8201: [14], 12408: [14], 14096: [14], 13670: [15], 12404: [15], 11173: [15], 9476: [15], 5928: [15], 7792: [15], 6656: [15], 6887: [16], 6015: [16], 8027: [16], 5132: [16], 6208: [16], 6953: [16], 9896: [16], 8184: [17], 10179: [17], 8537: [17], 6149: [18], 7222: [18], 9279: [18], 7633: [18], 10229: [18], 9875: [18], 9212: [18], 7840: [18], 10089: [18], 9640: [18], 8696: [19], 6859: [19], 8522: [19], 6080: [20], 7091: [20], 8978: [20], 6998: [20], 8969: [20], 6331: [20]}

if __name__ == "__main__":
    file1 = "databaseFile2.py"
    file2 = "databaseFile3.py"

    highlightedBlocks(file1, file2)