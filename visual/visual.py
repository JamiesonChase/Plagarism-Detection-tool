# Defining functions: https://www.tutorialspoint.com/python3/python_functions.htm
# https://www.kite.com/python/answers/how-to-print-every-line-of-a-text-file-in-python
# https://www.geeksforgeeks.org/print-colors-python-terminal/
# https://attacomsian.com/blog/javascript-array-search
# https://www.kite.com/python/answers/how-to-remove-an-element-from-an-array-in-python

from colorama import Fore, Back, Style

def printFiles(file1, file2, list1, list2):
    print("File1 source code:\n\n\n")
    f = open(file1)
    lines = f.readlines()
    i = 1
    for line in lines:
        if (i in list1):
            print(Fore.BLUE + line)
            print(Style.RESET_ALL)
        else:
            print(line)

        i = i + 1
        

    print(Style.RESET_ALL)

    f.close


    print("File2 source code:\n\n\n")
    f = open(file2)
    lines = f.readlines()
    i = 1
    for line in lines:
        if (i in list2):
            print(Fore.BLUE + line)
            print(Style.RESET_ALL)
        else:
            print(line)

        i = i + 1
        

    print(Style.RESET_ALL)

    f.close
    return 


def printPercentage(array1, array2):
    totalMatches = 0
    for i in array1:
        inSecondArray = False 
        secondArrayLocation = -1
        jIndex = 0
        for j in array2:
            if (inSecondArray == False):
                if (i[0] == j[0]):
                    
                    inSecondArray = True 
                    secondArrayLocation = jIndex 
                    totalMatches = totalMatches + 1
            jIndex = jIndex + 1

        if (inSecondArray == True):
            del array2[secondArrayLocation]
        
    print("Percentage value: " + str( (totalMatches / len(array1) )*100 ))
        


    return 


printFiles("source1.py","source2.py",[1,2,3,4,6],[1,2,3,4,11])
printPercentage([ [1,55], [2, 55], [3, 55], [4, 55]], [[1,55], [2, 55], [3, 55], [17, 55]])