# Defining functions: https://www.tutorialspoint.com/python3/python_functions.htm
# https://www.kite.com/python/answers/how-to-print-every-line-of-a-text-file-in-python
# https://www.geeksforgeeks.org/print-colors-python-terminal/
# https://attacomsian.com/blog/javascript-array-search
# https://www.kite.com/python/answers/how-to-remove-an-element-from-an-array-in-python

from colorama import Fore, Back, Style


def printFiles(file1, file2, list1, list2):
    print("File1 source code:\n\n\n")
    f1 = open(file1)
    lines = f1.readlines()
    i = 1
    for line in lines:
        if i in list1:
            print(Fore.BLUE + line)
            print(Style.RESET_ALL)
        else:
            print(line)

        i = i + 1

    print(Style.RESET_ALL)

    f1.close()

    print("File2 source code:\n\n\n")
    f2 = open(file2)
    lines = f2.readlines()
    i = 1
    for line in lines:
        if i in list2:
            print(Fore.BLUE + line)
            print(Style.RESET_ALL)
        else:
            print(line)

        i = i + 1

    print(Style.RESET_ALL)

    f2.close()
    return
