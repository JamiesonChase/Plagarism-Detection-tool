def createMainTableHTML(Rows): #Will create the HTML file with all the comparison.
    f = open('HTMLFiles/index.html', 'w') # Create the index.html file.
    # Header part of the HTML file, will write this variable to the file.
    html_template = """<!DOCTYPE html>
    <html>
    <head>
    <title>ComparisonTable</title>
    <style>
        table, th, td {
            border: 1px solid black;
            border-collapse: collapse;
        }
        table.center {
            margin-left: auto;
            margin-right: auto;
        }
    </style>
    </head>
    <body>
    <table class="center">
    <tr>
    <th>doc Pairs</th>
    <th>Pair Similarity</th>
    </tr>
    """
    i = 0
    for row in Rows: # Add each entry of the table to the file.
        currentName = row[0]
        splitNames = currentName.split(" - ") #Split the names so there are no spaces
        file1 = splitNames[0]; file2 = splitNames[1] #Assign the names of the files
        html_template = html_template + "<tr>\n<th><A HREF=\"{currentNumber}-1.html?file1={firstFile}&file2={secondFile}&rowNumber={rowNumber}\">{name}</A></th>\n".format(currentNumber=i,name=row[0], firstFile=file1, secondFile=file2,rowNumber=currentNumber)
        html_template = html_template + "<th>{percentScore}</th>\n</tr>\n".format(percentScore=row[1])   
        i = i + 1
        
    html_template = html_template + "</table></body>\n</html>" #Add the ending parts of the html file.
    f.write(html_template) # Write everything to the file and close it.
    f.close()
    return 

def createIFramePage(currentRowNumber): #Create the HTML page that will display the table and the 2 comparison files.
    htmlFileName = "templates/HTMLFiles/baseFiles/{number}-1.html".format(number=currentRowNumber) #Th file name that will be used.

    f = open(htmlFileName, 'w') # Open the file.
    # Beginning part of the HTML file.
    html_template = """<!DOCTYPE html> 
    <html>
    <head>
    <title>Side by side Comparison</title>
    
    </head>
    """
    html_template = html_template + "<iframe src=\"../contentFiles/{number}-4.html\" height=\"150\" width=\"100%\" title=\"TableFile\"></iframe>\n".format(number=currentRowNumber) # Add the correct links.
    html_template = html_template + "<iframe src=\"../contentFiles/{number}-2.html\" height=\"450\" width=\"47%\" name=\"LeftFile\"></iframe>\n".format(number=currentRowNumber)
    html_template = html_template + "<iframe src=\"../contentFiles/{number}-3.html\" height=\"450\" width=\"47%\" name=\"RightFile\"></iframe>\n".format(number=currentRowNumber)
    html_template = html_template + "</body>\n</html>" #Ending parts of the HTML file.
    f.write(html_template) # Write everything to the file and close it.
    f.close()
    return 

def createJumpTable(currentRowNumber, arrayOfNamesLeft, arrayOfNamesRight): #Create the table at the top of the 2 files being compared.
    htmlFileName = "templates/HTMLFiles/contentFiles/{number}-4.html".format(number=currentRowNumber) #File name that will be used 

    f = open(htmlFileName, 'w') #Open the file
    # header information
    html_template = """<!DOCTYPE html>
    <html>
    <head>
    <title>Side by side comparison</title>
    <style>
    table, th, td {
        border: 1px solid black;
        border-collapse: collapse;
    }
    table.center {
        margin-left: auto;
        margin-right: auto;
    }
    </style>
    </head>
    <body>
    <table class="center">
        <tr>
            <th>File1</th>
            <th>File2</th>
        </tr>
    """

    if (len(arrayOfNamesLeft) >= len(arrayOfNamesRight)): #If the length of the array on the left side is bigger than on the right side
        for var in list(range(len(arrayOfNamesLeft))): # for each entry in the left array
            html_template = html_template + "<tr>" # Start a new tale row.
            if (var < len(arrayOfNamesLeft)): #If the left side needs to be added, add the corresponding html code.
                html_template = html_template + "<th><A HREF=\"{number}-2.html#{jumpPoint}\" TARGET=\"LeftFile\">{l}-{r}</A></th>\n".format(number=currentRowNumber,jumpPoint=var,l=arrayOfNamesLeft[var][0],r=arrayOfNamesLeft[var][1])
            else:
                pass

            if (var < len(arrayOfNamesRight)): # If the right side needs to be added, add the corresponding HTML coe
                html_template = html_template + "<th><A HREF=\"{number}-3.html#{jumpPoint}\" TARGET=\"RightFile\">{l}-{r}</A></th>\n".format(number=currentRowNumber,jumpPoint=var,l=arrayOfNamesRight[var][0],r=arrayOfNamesRight[var][1])
            else:
                pass

            html_template = html_template + "</tr>\n" # End the table row.
    else: # Else if the length of the array on the right side is bigger than on the left side. 
        for var in list(range(len(arrayOfNamesRight))): # For each entry in the right array
            
            html_template = html_template + "<tr>" # Start a table row
            if (var < len(arrayOfNamesLeft)): #If we need to add an entry to the left table, add the HTML code
                html_template = html_template + "<th><A HREF=\"{number}-2.html#{jumpPoint}\" TARGET=\"LeftFile\">{l}-{r}</A></th>\n".format(number=currentRowNumber,jumpPoint=var,l=arrayOfNamesLeft[var][0],r=arrayOfNamesLeft[var][1])
            else: # Else put an empty slot for left side
                html_template = html_template + "<th></th>\n"

            if (var < len(arrayOfNamesRight)): # If the right side needs to be added, add it
                html_template = html_template + "<th><A HREF=\"{number}-3.html#{jumpPoint}\" TARGET=\"RightFile\">{l}-{r}</A></th>\n".format(number=currentRowNumber,jumpPoint=var,l=arrayOfNamesRight[var][0],r=arrayOfNamesRight[var][1])
            else:
                pass

            html_template = html_template + "</tr>\n" # End the row
    
    html_template = html_template + "</table>\n</body>\n</html>" # Add the ending information
    f.write(html_template) # Write to the file and close it.
    f.close()
    return 

def createHTMLFiles(fileName, blocks ,LeftOrRight,currentRowNumber): #Creat the HTML files that will contain the the source code.
    colorCode = ["800000", "469990", "9A6324", "3cb44b", "e6194B",  "42d4f4", "f58231", "911eb4", "f032e6", "dcbeff"  ]
    a_file = open(fileName) #Open the file
    
    lines = a_file.readlines() # Read all the lines
    htmlFileName = "templates/HTMLFiles/contentFiles/{number}-{side}.html".format(number=currentRowNumber,side=LeftOrRight) #Nam eof the html file.

    f = open(htmlFileName, 'w') # Create the html file.
    html_template = """<!DOCTYPE html><html><head><title>{nameOfFile}</title></head><body BGCOLOR=white><HR>{nameOfFile}<p><PRE>\n""".format(nameOfFile=fileName) #Header information.
    f.write(html_template) # Write to the html file.
    a_file.close() #Close the source file.

    i = 1 #Variables to determine what values are written to the HTML file
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
            if (colorNumber > 9):
                colorNumber = 0
        i = i + 1 # Increase the line number counter.
        
    f.write("</PRE></PRE></Body></HTML>") # Write the ending parts of the HTML file
    f.close() # Close the file.