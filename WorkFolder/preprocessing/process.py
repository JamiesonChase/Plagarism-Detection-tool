# Second draft of pre-processing
# now inside a function
# Comments are first removed, and indented lines removed.
# Variables are changed to var1,var2, etc in sequential order.
# Functions are changed to fun1, fun2, etc in sequential order.

import re, pyminifier

class Analyser:
    names = []
    names2 = []
    translations = []

    def AnalyseLines(self, lines):
        for line in lines:
            self._AnalyseLine(line)
        Analyser.names = []
        Analyser.names2 = []
    # Method to parse imports,classes,=, and function def
    def _AnalyseLine(self, line):
        parts = self._GetParts(line)
        if len(parts) > 1 and parts[0] == "import":
            self._AnalyseImport(parts)
        if len(parts) > 1 and parts[0] == "class":
            self._AnalyseClass(parts)
        if len(parts) > 1 and parts[1] == "=":
            self._AnalyseAssignment(parts)
        if len(parts) > 1 and parts[0] == "def":
            self._AnalyseDef(parts)
    # Each line will be broken into parts
    def _GetParts(self, line):
        minusTabs = line.replace("\t", " ")
        minusDoubleSpace = minusTabs.replace("  ", " ")
        if minusDoubleSpace[0:3] == 'def':
            parts = minusDoubleSpace.split(" ",1)
        else:
            parts = minusDoubleSpace.split(" ")
        while "#" in parts:
            del parts[-1]
        while len(parts) > 0 and parts[0] == "":
            del parts[0]
        return parts
    # Renaming function for variables, replace with var and append number
    def _AddName(self, name, elementType):
        if name == "":
            return
        nameToAppend = name # + " " + elementType
        if nameToAppend in Analyser.names:
            return
        Analyser.names.append(nameToAppend)
        translation = "var" + str(len(Analyser.names))
        Analyser.translations.append((name, translation))
    # Renaming function for functions, replace with fun and append num
    def _AddName2(self, name, elementType):
        if name == "":
            return
        nameToAppend = name # + " " + elementType
        if nameToAppend in Analyser.names2:
            return
        Analyser.names2.append(nameToAppend)
        translation = "fun" + str(len(Analyser.names2))
        Analyser.translations.append((name, translation))
    # Parse for 'import as x' where x would need to be renamed
    def _AnalyseImport(self, parts):
        if len(parts) == 4 and parts[0] == "import" and parts[2] == "as":
            self._AddName(parts[3], "import")
    # Split class into parts then add name
    def _AnalyseClass(self, parts):
        p1 = parts[1].split(":")
        p2 = p1[0].split("(")
        self._AddName(p2[0], "class")
    # split a variable assign into parts then add name
    def _AnalyseAssignment(self, parts):
        mutableName = parts[0].split(".")[0]
        self._AddName(mutableName, "assignment")
    # split funciton def into parts then add name
    def _AnalyseDef(self, parts):
        methodNameParts = parts[1].split("(")
        if methodNameParts[0] == "__init__":
            return
        self._AddName2(methodNameParts[0], "method")
        if len(methodNameParts) > 1:
            part=methodNameParts[1].replace("):","")
            part=part.split(",")
            for i in part:
                i=i.replace(" ","")
                self._AddName(i,"assignment")

class Translator:
    def TranslateLines(self, content):
        for (oldWord, newWord) in Analyser.translations:
            content = re.sub(r"\b%s\b" % oldWord, newWord, content)
        newLines = content.split("\n")
        Analyser.translations = []
        return "\n".join(newLines)
def process(sourceFilePath):
    #targetFilePath = "output"

    source = open(sourceFilePath, "r")  # open file path so we can strip comments
    source_str = source.read()
    source.close()
    source_str = pyminifier.minification.remove_comments_and_docstrings(source_str)
    source_str = pyminifier.minification.remove_blank_lines(source_str)
    source_str = pyminifier.minification.dedent(source_str)  # pyminifier is nice helper for comment stripping
    output = open(sourceFilePath + "_Stripped", 'w')  # rewrite stripped file
    output.write(source_str)
    output.close()

    analyser = Analyser()
    sourceFile = open(sourceFilePath + "_Stripped", 'r')
    content = sourceFile.read()
    lines = content.split("\n")
    #print(len(lines), "lines, starting with", lines[0])
    analyser.AnalyseLines(lines)

    translator = Translator()
    newContent = translator.TranslateLines(content)
    #newLines = newContent.split("\n")
    #print("writing", len(newLines), " lines to", targetFilePath, "starting with", newLines[0])
    sourceFile.close()

    return newContent

#print(process("test.py"))
#print(process("translate.py"),end="")