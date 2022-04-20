from ..preprocessing.process import process
from ..hashingFingerprinting.hashFingerprint import hashingFunction

MIN_HASH_THRESHOLD = 0.6 # TODO: test this number more
DEBUG = False

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

def invertDict(matchedIndex):
    """
    Inverts the input dictionary 'matchedIndex' {ngram : [line numbers]}
    to the format {line number : [ngrams]}
    
    Complexity: O(m*l)
        - m is the number of matching ngrams
        - l is the average number of lines mapped to each ngram
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
    """
    Computes the ratio of the number of shared hashes in hashes1 and hashes2
    to the total number of hashes in the larger of the two lists.

    Compexity: O(min(len(s), len(t))) on average, O(len(s) * len(t)) worst case
        - s is hashes1
        - t is hashes2
    """
    matches = set.intersection(set(hashes1), set(hashes2))
    return len(matches) / max(len(hashes1), len(hashes2))

def findLongestSequence(s1, s2, index1, index2):
    """
    Returns the length of the longest sequence of similar lines in index1 and index2
    starting on lines s1 and s2 respectively.

    TODO: time complexity
    """

    # base cases for recursion
    if s1 > len(index1) or s2 > len(index2):
        # don't go past index bounds
        return 0
    if compareLine(index1[s1], index2[s2]) < MIN_HASH_THRESHOLD:
        # once the two lines aren't similar enough, return
        return 0
    
    # add 1
    return 1 + findLongestSequence(s1 + 1, s2 + 1, index1, index2)

def getLineScore(line1, index1, index2):
    """
    Compares line1 from index1 to every line in index2, finding the longest sequence
    at each one. Returns the maximum of longest sequences found, along with the line
    number(s) that longest sequence was found at.

    TODO: time complexity
    """
    score = 0
    maxScore = 0
    bestLines = []
    
    # iterate over the lines in index2
    line2 = 1
    while line2 < len(index2):
        # calculate the score for line1 on line2
        score = findLongestSequence(line1, line2, index1, index2)
        if score > maxScore:
            maxScore = score
            bestLines = [line2]
        # when score is the same as max, add line2 to list of best lines
        elif score == maxScore and score > 0:
            bestLines.append(line2)
        # increment line2
        line2 += max(score, 1)
        
    return [maxScore, bestLines]

def adjustScores(startLine, scores):
    """
    Adjusts any improper line scores that appear from overlapping blocks.
    For example, if a sequence of lines in the scores dictionary looks like this:
    [5, 4, 3, 2, 5, ...] it will be adjusted to this: [4, 3, 2, 1, 5, ...].
    This is to help with constructing blocks later.

    TODO: time complexity
    """
    # base cases for recursion
    if scores[startLine][0] < 2 or startLine >= len(scores):
        # score is too small or startLine is out of bounds
        return 0
    if scores[startLine + 1][0] >= scores[startLine][0]:
        # the next score is greater than the current one, decrement the current score
        return scores[startLine][0] - 1
    # go to next line
    return adjustScores(startLine + 1, scores)

def getBlocks(scores):
    """
    Returns a list of blocks constructed from the scores dictionary.
    For example, if line 3 in scores has a score of 4, then the longest sequence
    that line 3 matched with was 4 lines long, so the block constructed is (3, 6).

    TODO: time complexity
    """
    blocks = []
    block = 1
    while block < len(scores):
        score = scores[block][0]
        # don't include blocks that are only 1 line long
        # these blocks tend to match to ~many~ lines in the opposite file and are a pain
        if score > 1:
            blocks.append((block, block + score - 1))
            block += score
        else:
            block += 1
    return blocks

def translateLines(SourceFile, StrippedFile):
    """
    Returns a list of lines from SourceFile that the lines in StrippedFile
    were translated from.

    TODO: time complexity
    """
    file = open(StrippedFile)
    content = file.readlines()  # Get all lines from stripped file
    newlines = []
    i = 0
    lookup = content[i].strip()
    with open(SourceFile) as myFile:  # iterate through source file
        for num, line in enumerate(myFile, 1):
            if lookup in line:  # if processed line is in source line
                newlines.append(num)  # append source line value
                i += 1  # iterate through each suspect old line
                if i == len(content):
                    break
                else:
                    lookup = content[i].strip() #
    return newlines  # return list of translated lines

def getBlockFromLine(line, blocks):
    """
    Returns the block from 'blocks' that the given line number belongs to,
    so long as that block exists.

    TODO: time complexity
    """
    for block in blocks: 
        # line is within the blocks start and end lines.
        if line >= block[0] and line <= block[1]:
            return block

def getBlockMappings(scores, oppBlocks):
    """
    Returns a dictionary of blocks from one file mapped to a
    set of corresponding blocks in the opposite file.
    
    TODO: time complexity
    """
    mappings = {}
    i = 1
    while i < len(scores):
        score = scores[i][0]
        # ignore blocks less than length 2
        if score < 2:
            i += 1
            continue
        # get all blocks that the current line number maps to
        lineMaps = scores[i][1]
        blockMaps = set()
        for line in lineMaps:
            # set addition ignores duplicates
            blockMaps.add(getBlockFromLine(line, oppBlocks))
        # add this mapping to the dictionary and increment the line number
        mappings[(i, i + score - 1)] = list(blockMaps)
        i += score
    return mappings

def getFullPath(block, oppBlockMappings):
    """
    Builds a set, 'blocksThere', of all the blocks in the opposite file that map back to 'block'.
    Builds another set, 'blocksHere', of the all the blocks in the same file that are also mapped back to
    by blocks in the opposite file.
    This feels like an inelegant way to do this, but I was unable to come up with anything better.
    I apologize if this method is confusing.

    TODO: time complexity
    """
    blocksHere = set()
    blocksThere = set()
    queue = [block]
    blocksHere.add(block)

    # loop until no new blocks are found
    while(len(queue) > 0):
        b = queue.pop()
        # find any blocks from the opposite file that map back to the block 'b'
        for k in oppBlockMappings:
            if b in oppBlockMappings[k]:
                # store (without duplicates) the block from opposite file
                blocksThere.add(k)
                for i in oppBlockMappings[k]:
                    # if the block 'i' hasn't been seen yet, add it to the queue
                    if i not in blocksHere:
                        queue.append(i)
                    # store (without duplicates) any blocks that the blocks from the opposite file map back to
                    blocksHere.add(i)
    # return both sets
    return (blocksHere, blocksThere)

def highlightedBlocks(file1, file2):
    """
    Returns two lists of the format [[colorNum, (startLine, endLine)], ...]
    - colorNum is a number to uniquely identify which color to assign the following block
    - startLine is the beginning line of a block of code to highlight, endLine is the end of that same block
    - the first list corresponds to file1, and the second to file2
    """
    # set up the indices
    index1 = file_setup(file1)
    index2 = file_setup(file2)

    # swap the index from {hash: [lines]} to {line: [hashes]}
    index1 = invertDict(index1)
    index2 = invertDict(index2)

    # build two dictionaries of the format {lineNumber: [score, [bestLines]]}
    # where score represents the longest matching sequence that line corresponds to
    # and bestLines is the list of lines that longest matching sequence begin on
    scores1 = {}
    for s1 in index1:
        scores1[s1] = getLineScore(s1, index1, index2)
    scores2 = {}
    for s2 in index2:
        scores2[s2] = getLineScore(s2, index2, index1)

    # adjust for overlaps (see adjustScores for more info)
    for i in range(1, len(scores1)):
        scores1[i][0] -= adjustScores(i, scores1)
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

    # build two lists of blocks from the respective scores dictionaries (see getBlocks for more info)
    blocks1 = getBlocks(scores1)
    blocks2 = getBlocks(scores2)

    if DEBUG:
        print("blocks1 = " + str(blocks1))
        print("blocks2 = " + str(blocks2))

    # build two dictionaries of the format {block1: [blocks2]} (sett getBlockMappings for more info)
    blockMappings1 = getBlockMappings(scores1, blocks2)
    blockMappings2 = getBlockMappings(scores2, blocks1)

    if DEBUG:
        print("blockMappings1 = " + str(blockMappings1))
        print("blockMappings2 = " + str(blockMappings2))

    # match corresponding blocks
    matchedBlocks1 = []
    matchedBlocks2 = []
    i = 0

    # for each block, find all similar blocks and assign them all the same number (for coloring).
    # remove each of these blocks from their respective lists along the way until no blocks remain
    while len(blocks1) > 0:
        block = blocks1.pop()
        res = getFullPath(block, blockMappings2)
        for b in res[0]:
            matchedBlocks1.append([i, b])
            if b in blocks1: blocks1.remove(b)
        for b in res[1]:
            matchedBlocks2.append([i, b])
            if b in blocks2: blocks2.remove(b)
        i += 1

    while len(blocks2) > 0:
        block = blocks2.pop()
        res = getFullPath(block, blockMappings1)
        for b in res[1]:
            matchedBlocks1.append([i, b])
            if b in blocks1: blocks1.remove(b)
        for b in res[0]:
            matchedBlocks2.append([i, b])
            if b in blocks2: blocks2.remove(b)
        i += 1

    # sort the blocks by order of start line (assuming no blocks should overlap, this is sufficient)
    matchedBlocks1.sort(key = lambda x: x[1][0])
    matchedBlocks2.sort(key = lambda x: x[1][0])

    if DEBUG:
        print("matchedBlocks1 = " + str(matchedBlocks1))
        print("matchedBlocks2 = " + str(matchedBlocks2))

    # get the line translations (see translateLines for more info)
    file1Lines = translateLines(file1, file1 + "_Stripped")
    file2Lines = translateLines(file2, file2 + "_Stripped")

    # finally, translate the lines of each block to line up with the original files
    for block in matchedBlocks1:
        block[1] = (file1Lines[block[1][0] - 1], file1Lines[block[1][1] - 1])
    for block in matchedBlocks2:
        block[1] = (file2Lines[block[1][0] - 1], file2Lines[block[1][1] - 1])

    if DEBUG:
        print("matchedBlocks1 after translating = " + str(matchedBlocks1))
        print("matchedBlocks2 after translating = " + str(matchedBlocks2))

    return(matchedBlocks1, matchedBlocks2)

    