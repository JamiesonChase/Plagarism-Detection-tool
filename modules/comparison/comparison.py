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
            # condition to control the size of the blocks
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
    # check if first line matches the last line
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
    # takes the stripped file, highlighted list, and original file as input
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
    # put the flagged lines for highlighting into blocks for the HTML module
    # a list of all the matched lines are created
    sLineMatched = list(s.values())
    aLineMatched = list(a.values())
    sHashMatched = []
    sL = []
    aHashMatched = []
    aL = []
    match = 0
    # loop through both sets of keys append to list and track count of matches
    for i in s.keys():
        for j in a.keys():
            if i == j:
                sHashMatched.append(i)
                aHashMatched.append(j)
                sL.append(sLineMatched[match])
                aL.append(aLineMatched[match])
                match += 1
    #flatten list of keys
    flatsL = list(flatten(sL))
    flataL = list(flatten(aL))
    # creates a dictionary of keys being line numbers and items being the amount of matches to that key
    sCount = createDict(flatsL)
    aCount = createDict(flataL)
    sortedLineMatchess = sorted(sCount)
    sortedLineMatchesa = sorted(aCount)
    if len(sCount) != 0:
        sCount = fillInDict(sortedLineMatchess, sCount) # line dictionary with empty lines added
        aCount = fillInDict(sortedLineMatchesa, aCount)
        sortedLineMatchess = sorted(sCount) # sort matches by line number
        sortedLineMatchesa = sorted(aCount)
        HLs = determineHBlocks(sortedLineMatchess, sCount) # highlighted Lines
        HLa = determineHBlocks(sortedLineMatchesa, aCount)
        # translate processed line matches to original
        transBlockss = getTransHighLightLines(StrippedFile1, HLs, file1)
        transBlocksa = getTransHighLightLines(StrippedFile2, HLa, file2)

        print("inputFile original code blocks: ", transBlockss)
        print("compared document original code blocks: ", transBlocksa)

        print("similarity percentage: ", calculateSim(len(s), match), "\n")
        return transBlockss, transBlocksa
    else:
        pass
