# Method for translating lines from processed to original
# Input variables:
# <StrippedFile> stripped version of source file i.e. test.py_Stripped
# <OldLines> Lines of Processed file which were flagged
# <SourceFile> Original source file
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

#TranslateLines("test.py_Stripped",[2,3,6],"test.py")
# Test Case return value should be [4, 5, 11]