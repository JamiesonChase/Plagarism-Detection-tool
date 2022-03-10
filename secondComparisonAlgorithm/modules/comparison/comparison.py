from collections.abc import Iterable

def flatten(l):
    # function to flatten a list
    for item in l:
        if isinstance(item, Iterable) and not isinstance(item, str):
            for x in flatten(item):
                yield x
        else:
            yield item

def createDict(countList):
    # creates a dictionary of keys being line numbers and items being the amount of matches to that key
    countDict = {}
    for i in countList:
        countDict[i] = countList.count(i)
    return countDict

def fillInDict(sortedLines, dict):
    # fill in matching line gaps with line number key and 0 value
    count = sortedLines[0]
    for line in sortedLines:
        if line == count:
            count +=1
            pass  # do nothing
        else:
            gap = line - count
            for i in range(1, gap+1):
                dict[count] = 0
                count +=1

            count += 1
    #print("filled dict: ", dict)

    return dict

def determineHBlocks(sortedLineMatches, dict):
    # Get blocks of text to be highlighted from the sorted list of line matches
    tempBlock = []
    hBlocks = []
    count = 0
    blocks = []

    # values and keys are for testing to watch dict_values and keys
    values = dict.values()
    keys = dict.keys()
    # since values is not subscriptable create a list of the sorted lines number of matches
    res = [dict[i] for i in sortedLineMatches]
    # res takes the amount of all the matches and puts them in a list relevent to the values location in the sortedLineMatches
    for i in range(0, len(sortedLineMatches)):
        if res[i] != 0:   # if i is not a gap line
            tempBlock.append(sortedLineMatches[i])   # append ith element of sortedLineMatches to tempBlock
            if (count != 4):       # high number will shorten the blocks
                # count sets the blocksize to count + 1
                    # ie. count = 3 will produce blocks like [1,4],[5,8]
                count += 1
                continue
            else:
                # when block size is reached clear the count and append the block to tempBlock
                count = 0
                hBlocks.append(tempBlock) # end the block, append tempBlock to highlightBlocks variable: hBlocks
                tempBlock = [] # clear tempBlock
        else:  # if there is a gap
            if len(tempBlock) != 0:  # if tempBlock is not already empty
                hBlocks.append(tempBlock)   # ends the block by appending tempBlock to hBlocks
                count = 0
                tempBlock = []
    # out of lines, end the block
    hBlocks.append(tempBlock) # completes list of blocks ie. ([1,2,3,4],[5,6,7,8],[11,12,13,14],[16,17])
    for i in hBlocks:
        if len(i) == 0: continue        # if hBlocks is empty continue to return
        blocks.append([i[0], i[-1]])    # append first and last element of each ith hBlock

    return blocks
    # blocks is a list of flagged blocks of lines to highlight ie. [1,4],[5,8],[9,12],[14,17],[18,19]


def TranslateLineBlocks(StrippedFile,SourceFile,first, last, currentSourceLine):
    # takes blocks of flagged lines from processed document and translates them to the original source file lines
    # returns the first and last line of the original source file
    file = open(StrippedFile)
    content = file.readlines()  # Get all lines from stripped file
    lookupFirstLine = content[first - 1].strip()  # string of first line
    lookupLastLine = content[last - 1].strip()  # string of last line

    sourceLineFirst = 0
    sourceLineLast = 0

    with open(SourceFile) as myFile:  # iterate through source file
        for num, line in enumerate(myFile, 1):
            if num < currentSourceLine:
                pass
            else:
                # should not be updating num if the line number is less than the currentSourceLine
                if lookupFirstLine in line:
                    sourceLineFirst = num
                    currentSourceLine = num + 1
                    break

    if first == last:  # if they are the same, ie [5,5], we can return here
        return [sourceLineFirst, sourceLineFirst, currentSourceLine]

    with open(SourceFile) as myFile:  # iterate through source file
        for num, line in enumerate(myFile, 1):
            if num < currentSourceLine:
                pass
            else:
                # should not be updating num if the line number is less than the currentSourceLine
                if lookupLastLine in line:
                    sourceLineLast = num
                    currentSourceLine = num + 1
                    break


    return [sourceLineFirst, sourceLineLast, currentSourceLine]

def getTransHighLightLines(StrippedFile, highlightedList, origFile):
    # function to create a list of blocks from the original code to highlight
    appHLs = []
    currentSourceLine = 0       # variable to keep track of original source line
    for i in range(len(highlightedList)):   # iterate through blocks returned from determineHBlocks
        first = highlightedList[i][0] # take the first element of ith block
        last = highlightedList[i][1]    # take the second element of ith block
        returnValue = TranslateLineBlocks(StrippedFile, origFile, first, last, currentSourceLine)  # gets first and last lines of block and currentSourceLine value
        line = [returnValue[0], returnValue[1]] # take first and second elements of returnValue for line block to be highlighted
        currentSourceLine = returnValue[2]      # take 3rd element as current source line
        appHLs.append(line)

    return appHLs

def calculateSim(inputFileLen, matches):  # Needs fixed? Not sure this is correct
    # calculate the similarity score between input document and compared document
    # matches is the sum of number of matches found on each line
    # inputFileLen is the number of lines in the document
    res = (matches / inputFileLen) * 100
    return res

def highlightedBlocks(s, a, StrippedFile1, StrippedFile2, file1, file2):
    sLineMatched = list(s.values())
    aLineMatched = list(a.values())
    sHashMatched = []
    sL = []
    aHashMatched = []
    aL = []
    match = 0
    for i in s.keys():
        for j in a.keys():
            if i == j:
                sHashMatched.append(i)
                aHashMatched.append(j)
                sL.append(sLineMatched[match])
                aL.append(aLineMatched[match])
                match += 1
    flatsL = list(flatten(sL))
    #print("flatsl: ", flatsL)
    flataL = list(flatten(aL))
    # creates a dictionary of keys being line numbers and items being the amount of matches to that key
    sCount = createDict(flatsL)
    #print("sCount: ", sCount)

    # sCount:  {1: 6, 15: 1, 11: 5, 2: 8, 12: 5, 16: 6, 3: 11, 13: 6, 4: 9, 14: 1, 5: 7, 10: 6, 6: 8, 7: 7, 8: 7, 9: 10, 18: 1}
    # here is an opportunity to sort this data into blocks based on higher density of matches

    aCount = createDict(flataL)
    #print("aCount: ", aCount)
    sortedLineMatchess = sorted(sCount)
    #print("s sorted line numbers: ", sortedLineMatchess)
    sortedLineMatchesa = sorted(aCount)
    #print("a sorted line numbers: ", sortedLineMatchesa)
    if len(sCount) != 0:
        sCount = fillInDict(sortedLineMatchess, sCount) # line dictionary with empty lines added
        aCount = fillInDict(sortedLineMatchesa, aCount)
        sortedLineMatchess = sorted(sCount)
        sortedLineMatchesa = sorted(aCount)
        HLs = determineHBlocks(sortedLineMatchess, sCount)
        HLa = determineHBlocks(sortedLineMatchesa, aCount)
        print("inputFile processed blocks: ", HLs)
        print("compared document processed blocks: ", HLa)
        transBlockss = getTransHighLightLines(StrippedFile1, HLs, file1)
        if len(transBlockss[-1]) == 1:
            temp = transBlockss[-1]
            for i in temp:
                pass
            transBlockss[-1].append(i)
            # need to add the same element

        transBlocksa = getTransHighLightLines(StrippedFile2, HLa, file2)
        # found an edge case where if there is more than one instance of the lookup string, it will add the additional line/lines to the highlighted blocks
        # for instance, the loop finds the first line 5, then the new lookup value changes to "string2="cda"\n". line 9 contains the lookup string. It finds the line and places it in newlines.
        # the function then continues looking for lines until it finishes looping or finding additional matching lines. In this case, line number 21 contained the same lookup value
        # this returns the highlighted block of lines [5, 9, 21]
        # propose a change to translate so when lookup is found, it recognizes and moves to the next lookup values and then stops when it has found 1 of each the start and the end value
        # found another edge case, where the lookup line matches a previous line as well as the actual translated line
        # for instance, processed line 19 shows a lookup value of 'return string2'
        # it finds a matching string at line 11 when the actual translated line should be line 23
        # it then continues and adds line 23 also. the only line added should be 23.
        # need a first and last reference to check the current i val with
        # added edge case for documents with 0 matches

        # created a new translate method for when a translation is needed specifically for the highlighted blocks of text only


        print("inputFile original code blocks: ", transBlockss)
        print("compared document original code blocks: ", transBlocksa)

        print("similarity percentage: ", calculateSim(len(s), match), "\n")
        return transBlockss, transBlocksa
    else:
        pass





# need to add edge cases for spaces in the lines with matches

# processBlockss:  [[1, 3], [4, 6], [7, 9], [10, 12], [13, 15]]
# processBlocksa:  [[1, 3], [4, 6], [7, 9], [10, 12]]
# transBlockss:  [[1, 3], [4, 7], [8, 10], [11, 14], [15, 18]]
# transBlocksa:  [[1, 3], [4, 7], [8, 10], [11, 14]]