from itertools import groupby, count, chain
from preprocessing.process import process
from hashingFingerprinting.hashFingerprint import hashingFunction

MIN_HASH_THRESHOLD = 0.5 # TODO: test this number more
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
    s = hashingFunction(s, 7)
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
    
    for s2 in index2:
        score = findLongestSequence(s1, s2, index1, index2)
        if score > maxScore:
            maxScore = score
            bestLines = [s2]
        elif score == maxScore and score > 0:
            bestLines.append(s2)
        
    return (maxScore, bestLines)

def highlightedBlocks(file1, file2):
    index1 = file_setup(file1)
    index2 = file_setup(file2)

    # swap the index from {hash: [lines]} to {line: [hashes]}
    index1 = invertDict(index1)
    index2 = invertDict(index2)

    scores1 = {}
    for s1 in index1:
        scores1[s1] = getLineScore(s1, index1, index2)

    scores2 = {}
    for s2 in index2:
        scores2[s2] = getLineScore(s2, index2, index1)

    print("scores1:")
    for key, value in sorted(scores1.items()):
        print("{} : {}".format(key, value))
    print("-----------------")
    print("scores2:")
    for key, value in sorted(scores2.items()):
        print("{} : {}".format(key, value))


file1 = "C:/Users/trvrh/Documents/GitHub/Winnowing-/secondComparisonAlgorithm/database/testFile.py"
file2 = "C:/Users/trvrh/Documents/GitHub/Winnowing-/secondComparisonAlgorithm/database/testFile_reordered.py"
highlightedBlocks(file1, file2)
