def appendFunction():
    a = "x"
	b = [1, 2, 3]
	b.append(a)
	return b

def stringFunction(input1, input2):
    string1 = "abcd"
    string2 = "cda"
    string3 = string1 + string2
    return string2 

def listSum(lis):
	sum = 0
	for item in lis:
		sum += len(item)
	return sum
    
def getMatches(index1, index2):
    # get intersection of indices
    return set.intersection(set(index1.keys()), set(index2.keys()))


aList = appendFunction()
stringFunction("a","b")
lsum = listSum(["lol", [1, 2], "funny"])
matches = getMatches({1:"a", 4:"a"}, {2:"yes", 1:"x"})