# Defining functions: https://www.tutorialspoint.com/python3/python_functions.htm
# https://www.kite.com/python/answers/how-to-print-every-line-of-a-text-file-in-python
# https://www.geeksforgeeks.org/print-colors-python-terminal/
# https://attacomsian.com/blog/javascript-array-search
# https://www.kite.com/python/answers/how-to-remove-an-element-from-an-array-in-python

from colorama import Fore, Back, Style


def printFiles(source, list1):
    print("possible plagiarized matches found in source code:\n")
    f = open(source)
    lines = f.readlines()
    i = 1
    for line in lines:
        if i in list1:
            print(Fore.BLUE + line)
            print(Style.RESET_ALL)
        else:
            print(line)

        i = i + 1

    print(Style.RESET_ALL)

    f.close()

    return
