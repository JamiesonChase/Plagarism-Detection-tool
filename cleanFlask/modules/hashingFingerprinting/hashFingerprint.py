#Resources
#
# To read a file in python https://www.pythontutorial.net/python-basics/python-read-text-file/
# Loop in python3: https://www.tutorialspoint.com/python3/python_for_loop.htm
# Command line argument in python3: https://www.geeksforgeeks.org/command-line-arguments-in-python/
# Python3 get length of string: https://www.tutorialspoint.com/python3/string_len.htm
# https://careerkarma.com/blog/python-string-to-int/
# https://stackoverflow.com/questions/227459/how-to-get-the-ascii-value-of-a-character
# https://www.digitalocean.com/community/tutorials/how-to-do-math-in-python-3-with-operators
# https://careerkarma.com/blog/python-string-to-int/
# https://www.delftstack.com/howto/python/python-overwrite-file/
# Information about hashing: http://www.cs.cmu.edu/afs/cs/academic/class/15451-f14/www/lectures/lec6/karp-rabin-09-15-14.pdf
# Information about hashing: https://en.m.wikipedia.org/wiki/Rabin%E2%80%93Karp_algorithm
# Information on how to end a python program: https://www.edureka.co/community/21051/how-to-exit-a-python-script-in-an-if-statement#:~:text=To%20stop%20code%20execution%20in,stop%20the%20program%20from%20running.
# https://www.kite.com/python/answers/how-to-remove-the-first-element-from-a-list-in-python#:~:text=%5B2%2C%203%5D-,Use%20list.,and%20return%20the%20first%20element.
# https://stackoverflow.com/questions/4945548/remove-the-first-character-of-a-string
# https://stackoverflow.com/questions/2612802/list-changes-unexpectedly-after-assignment-why-is-this-and-how-can-i-prevent-it

def index_to_lines(s, index):
    """Returns (line_number, col) of `index` in `s`."""
    s = str(s)
    if not len(s):
        return 1
    a = len(s[:min(index)+1].splitlines())
    return a

def hashingFunction(inputString, ngram):

    ArrayOfTuples = [] # List to be returned
    if (len(inputString) < ngram): #End the program if the file size is less than the ngrams.
        print("Size of file is less than ngram")
        exit()


    currentIndex = 0 #Current index
    beginningString = "" # beginning String
    ArrayOfIndex = [] #Arrays of the index for the ngrams.
    while (len(beginningString) != ngram): #Build the beginning string excluding new lines
        if (inputString[currentIndex] != '\n'):
            beginningString = beginningString + inputString[currentIndex]
            ArrayOfIndex.append(currentIndex)

        currentIndex = currentIndex + 1



    firstHashValue = 0 #Hash values will be stored here.
    i = 1
    for var in beginningString: #Initial part of the Karp Rabin algorithm
        firstHashValue = firstHashValue + ord(var)*(2**(ngram - i))
        i = i + 1

    firstArrayOfIndex = index_to_lines(inputString, ArrayOfIndex) #Add the first tupele
    tupleVariable = (firstArrayOfIndex, firstHashValue)
    ArrayOfTuples.append(tupleVariable)

    while (currentIndex <= (len(inputString) - 1) ): #To get all the other tuples.
        if (inputString[currentIndex] !=  '\n'): #Exlude new line

            #Another version of getting the next hash
            #firstHashValue = ( (firstHashValue - ord(beginningString[0]) *2**ngram) + ord(inputString[currentIndex]) ) * 2
            firstHashValue = ( firstHashValue - ord(beginningString[0]) *2**(ngram - 1) )*2 +  ord(inputString[currentIndex]) # Get the next hash
            del ArrayOfIndex[0] #Remove the index no longer in use
            ArrayOfIndex.append(currentIndex) #Append the new index
            localArrayOfIndex = index_to_lines(inputString, ArrayOfIndex)

            beginningString = beginningString[1:] #Adjust the next ngrams
            beginningString += inputString[currentIndex]
            tupleVariable = (localArrayOfIndex, firstHashValue) #Add the next tuple.
            ArrayOfTuples.append(tupleVariable)



        currentIndex = currentIndex + 1 #Increment the index.

    return ArrayOfTuples


#FileVaraible = open("test.py_Processed")
#fileString = FileVaraible.read()
#returnArray = hashingFunction(fileString, 4)
#print(returnArray)




