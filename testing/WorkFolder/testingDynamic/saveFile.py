import os, glob
dir = 'templates/HTMLFiles/baseFiles/'
dir2 = 'templates/HTMLFiles/contentFiles/'
for file in os.scandir(dir):
    print(file.path)
    print("HERE\n")
#os.remove("/templates/HTMLFiles/baseFile/0-1.html")
print("HERE\n")