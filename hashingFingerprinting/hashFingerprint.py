# To read a file in python https://www.pythontutorial.net/python-basics/python-read-text-file/
# Loop in python3: https://www.tutorialspoint.com/python3/python_for_loop.htm
# Command line argument in python3: https://www.geeksforgeeks.org/command-line-arguments-in-python/
# Python3 get length of string: https://www.tutorialspoint.com/python3/string_len.htm
# https://careerkarma.com/blog/python-string-to-int/
# https://stackoverflow.com/questions/227459/how-to-get-the-ascii-value-of-a-character
# https://www.digitalocean.com/community/tutorials/how-to-do-math-in-python-3-with-operators
# https://careerkarma.com/blog/python-string-to-int/
# https://www.delftstack.com/howto/python/python-overwrite-file/
import sys

f = open('testing.txt')
preProcessedText = f.read()

ngram = int(sys.argv[1]) # Get the first command line argument
firstNGram = preProcessedText[0:ngram]

firstHashValue = 0
i = 1
for var in firstNGram:
    firstHashValue = ord(var)*(256**(ngram - i))
    i = i + 1

firstFingerPrint = firstHashValue % 101
fingerPrintFile = open("fingerPrint.txt", 'w')
fingerPrintFile.write(str(firstFingerPrint))
fingerPrintFile.write("\n")
j = 1
k = ngram - 1


for var in list(range(len(preProcessedText) - ngram)):
    firstHashValue = ( (firstHashValue - ord(preProcessedText[j-1]) *256**ngram) + ord(preProcessedText[k + 1]) ) * 256
    
    fingerPrint = firstHashValue % 101
    fingerPrintFile.write(str(fingerPrint))
    fingerPrintFile.write("\n")
    j = j + 1
    k = k + 1



