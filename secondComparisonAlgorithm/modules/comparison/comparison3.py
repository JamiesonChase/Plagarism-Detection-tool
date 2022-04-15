from ..preprocessing.process import process
from ..hashingFingerprinting.hashFingerprint import hashingFunction

MIN_HASH_THRESHOLD = 0.6 # TODO: test this number more
DEBUG = True

# some time complexity calculations taken from https://wiki.python.org/moin/TimeComplexity

def invertedIndexCreate(s):
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
    s = hashingFunction(s, 4)
    s = invertedIndexCreate(s)
    return s

def compareLine(hashes1, hashes2):
    matches = set.intersection(set(hashes1), set(hashes2))
    return min(len(matches) / len(hashes1), len(matches) / len(hashes2))

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

def compareLine(hashes1, hashes2):
    matches = set.intersection(set(hashes1), set(hashes2))
    return min(len(matches) / len(hashes1), len(matches) / len(hashes2))

def findLongestSequence(s1, s2, index1, index2):
    if s1 > len(index1) or s2 > len(index2):
        return 0
    if compareLine(index1[s1], index2[s2]) < MIN_HASH_THRESHOLD:
        return 0
    
    return 1 + findLongestSequence(s1 + 1, s2 + 1, index1, index2)

def getLineScore(s1, index1, index2):
    score = 0
    maxScore = 0
    bestLines = []
    
    s2 = 1
    while s2 < len(index2):
        score = findLongestSequence(s1, s2, index1, index2)
        if score > maxScore:
            maxScore = score
            bestLines = [s2]
        elif score == maxScore and score > 0:
            bestLines.append(s2)
        s2 += max(score, 1)
        
    return [maxScore, bestLines]

def adjustScores(startLine, scores):
    if scores[startLine][0] < 2 or startLine + 1 > len(scores):
        return 0
    if scores[startLine + 1][0] >= scores[startLine][0]:
        return scores[startLine][0] - 1
    return adjustScores(startLine + 1, scores)

def getBlocks(scores):
    blocks = []
    block = 1
    while block < len(scores):
        score = scores[block][0]
        if score > 1:
            # don't forget about the tuple
            blocks.append((block, block + score - 1))
            block += score
        else:
            block += 1
    return blocks

def translateLines(OldLines, SourceFile, StrippedFile):
    file = open(StrippedFile)
    content = file.readlines()  # Get all lines from stripped file
    newlines = []
    i = 0
    lookup = content[OldLines[0]-1].strip()  # initialize first line
    with open(SourceFile) as myFile:  # iterate through source file
        for num, line in enumerate(myFile, 1):
            if lookup in line and num >= OldLines[i]:  # if processed line is in source line
                newlines.append(num)  # append source line value
                if i < len(OldLines)-1:
                    i = i+1  # iterate through each suspect old line
                lookup = content[OldLines[i]-1].strip() #
    file.close()
    return newlines  # return list of translated lines

def isInBlock(line, block):
    return line >= block[0] and line <= block[1]

def getBlockFromLine(line, blocks):
    for block in blocks: 
        if isInBlock(line, block):
            return block

def findMatchingBlocks(block, scores1, scores2, blocks1, blocks2):
    # store blocks in sets so no duplicates
    mBlocks1 = set()
    mBlocks2 = set()
    # block matches itself
    mBlocks1.add(block)

    mLines = scores1[block[0]][1]
    for line in mLines:
        g = getBlockFromLine(line, blocks2)
        if g != None:
            mBlocks2.add(g)

    # find which blocks from the other set map back to 'block'
    for b in blocks2:
        start = b[0]
        mLines = scores2[start][1]
        doesMatch = False
        # check if block2 maps at all to block
        for line in mLines:
            if isInBlock(line, block):
                doesMatch = True
        if doesMatch:
            mBlocks2.add(b)
            # get all the blocks that b maps to in blocks1
            for line in mLines:
                g = getBlockFromLine(line, blocks1)
                if g != None:
                    mBlocks1.add(g)

    return (mBlocks1, mBlocks2)

def highlightedBlocks(file1, file2):
    index1 = file_setup(file1)
    index2 = file_setup(file2)

    # swap the index from {hash: [lines]} to {line: [hashes]}
    index1 = invertDict(index1)
    index2 = invertDict(index2)

    
    scores1 = {}
    for s1 in index1:
        scores1[s1] = getLineScore(s1, index1, index2)
    for i in range(1, len(scores1)):
        scores1[i][0] -= adjustScores(i, scores1)
    
    scores2 = {}
    for s2 in index2:
        scores2[s2] = getLineScore(s2, index2, index1)
    for i in range(1, len(scores2)):
        scores2[i][0] -= adjustScores(i, scores2)

    if DEBUG:
        print("scores1:")
        for key, value in sorted(scores1.items()):
            print("{} : {}".format(key, value))
        print("-----------------")
        print("scores2:")
        for key, value in sorted(scores2.items()):
            print("{} : {}".format(key, value))

    blocks1 = getBlocks(scores1)
    blocks2 = getBlocks(scores2)

    if DEBUG:
        print("blocks1 = " + str(blocks1))
        print("blocks2 = " + str(blocks2))

    matchedBlocks1 = []
    matchedBlocks2 = []
    i = 0

    # match corresponding blocks
    matchedBlocks1 = []
    matchedBlocks2 = []
    i = 0

    while len(blocks1) > 0:
        block = blocks1.pop()
        res = findMatchingBlocks(block, scores1, scores2, blocks1, blocks2)
        for b in res[0]:
            matchedBlocks1.append([i, b])
            if b in blocks1: blocks1.remove(b)
        for b in res[1]:
            matchedBlocks2.append([i, b])
            if b in blocks2: blocks2.remove(b)
        i += 1

    while len(blocks2) > 0:
        block = blocks2.pop()
        res = findMatchingBlocks(block, scores2, scores1, blocks2, blocks1)
        for b in res[1]:
            matchedBlocks1.append([i, b])
            if b in blocks1: blocks1.remove(b)
        for b in res[0]:
            matchedBlocks2.append([i, b])
            if b in blocks2: blocks2.remove(b)
        i += 1

    #for block in blocks1:
    #    matchedBlocks1.append([block[0], block])
    #    for line in scores1[block[0]][1]:
    #        matchedBlocks2.append([block[0], [line, line + scores2[line][0] - 1]])

    matchedBlocks1.sort(key = lambda x: x[1][0])
    matchedBlocks2.sort(key = lambda x: x[1][0])

    if DEBUG:
        print("matchedBlocks1 = " + str(matchedBlocks1))
        print("matchedBlocks2 = " + str(matchedBlocks2))

    for block in matchedBlocks1:
        
        #print("translating block " + str(block[1]))
        block[1] = translateLines(block[1], file1, file1 + "_Stripped")
        if len(block[1]) == 1:
            block[1].append(block[1][0])
        #print("after translation: " + str(block[1]))
    for block in matchedBlocks2:
        #print("translating block " + str(block[1]))
        block[1] = translateLines(block[1], file2, file2 + "_Stripped")
        if len(block[1]) == 1:
            block[1].append(block[1][0])
        #print("after translation: " + str(block[1]))
        

    if DEBUG:
        print("matchedBlocks1 after translating = " + str(matchedBlocks1))
        print("matchedBlocks2 after translating = " + str(matchedBlocks2))

    return(matchedBlocks1, matchedBlocks2)