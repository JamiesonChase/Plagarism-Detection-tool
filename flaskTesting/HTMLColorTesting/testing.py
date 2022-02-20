def createHTMLFiles(fileName, blocks ,LeftOrRight,currentRowNumber): #Creat the HTML files that will contain the the source code.
    # Color code chart: https://sashamaps.net/docs/resources/20-colors/
    colorCode = ["800000", "469990", "9A6324", "3cb44b", "e6194B",  "42d4f4", "f58231", "911eb4", "f032e6", "dcbeff"  ]
    a_file = open(fileName) #Open the file
    
    lines = a_file.readlines() # Read all the lines
    htmlFileName = "{number}-{side}.html".format(number=currentRowNumber,side=LeftOrRight) #Nam eof the html file.

    f = open(htmlFileName, 'w') # Create the html file.
    html_template = """<!DOCTYPE html><html><head><title>{nameOfFile}</title></head><body BGCOLOR=white><HR>{nameOfFile}<p><PRE>\n""".format(nameOfFile=fileName) #Header information.
    f.write(html_template) # Write to the html file.
    a_file.close() #Close the source file.

    i = 0 #Variables to determine what values are written to the HTML file
    blockNumber = 0
    jumpPoint = 0
    colorNumber = 0
    for line in lines: #For each line in the source document.
        
        if (blockNumber < len(blocks) and i == blocks[blockNumber][0]): #If the block number is still inside the number of blocks and i equal to the start of the block
            f.write("<A NAME=\"{j}\"></A><FONT color = #{colorValue}>".format(j=jumpPoint, colorValue=colorCode[colorNumber])) #Start of the text that will be highlighted in and jump point can be referenced to go to this specific line
            jumpPoint = jumpPoint + 1 # Increase the jum point
        
        f.write(line) # Write the text to the html file.
        if (blockNumber < len(blocks) and i == blocks[blockNumber][1]): #If it is the end of the block
            f.write("</FONT>") # End the text that will be highlighted in red
            blockNumber = blockNumber + 1 # Increase the block number counter
            colorNumber = colorNumber + 1
            if (colorNumber > 15):
                colorNumber = colorNumber + 15
        i = i + 1 # Increase the line number counter.
        
        
    f.write("</PRE></PRE></Body></HTML>") # Write the ending parts of the HTML file
    f.close() # Close the file.


file1Highlight = {0: [0,4], 1: [6,10], 2: [12, 15], 3: [17,18], 4: [21,24]}
file2Highlight = {0: [0,4], 1: [6,10], 2: [12, 13], 3: [15,16], 4: [20,21]}
createHTMLFiles("databaseFile1.py", file1Highlight, 2, 0)
createHTMLFiles("databaseFile2.py", file2Highlight, 3, 0)
































colorCode = ["800000", "469990", "9A6324", "3cb44b", "e6194B",  "42d4f4", "f58231", "911eb4", "f032e6", "dcbeff"  ]
f = open("T2.html", 'w') # Create the html file.
html_template = """<!DOCTYPE html><html><head><title>TestingThisFile</title></head><body BGCOLOR=white><HR>TestingThisFile<p><PRE>\n""" #Header information.
colorNumber = 0
f.write(html_template)
for var in list(range(32)):
    f.write("<A NAME=\"{j}\"></A><FONT color = #{colorValue}>".format(j=0, colorValue=colorCode[colorNumber])) #Start of the text that will be highlighted in and jump point can be referenced to go to this specific line
    f.write("This line is testing.")
    f.write("</FONT>\n")
    colorNumber = colorNumber + 1
    if (colorNumber > 8):
        colorNumber = 0
f.close()

