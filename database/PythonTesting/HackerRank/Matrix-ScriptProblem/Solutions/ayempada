# Enter your code here. Read input from STDIN. Print output to STDOUT

i = raw_input().split()
a= int(i[0])
b = int(i[1])

inp = [raw_input() for i in range(a)]
inp = [i.replace('\r','') for i in inp]


s = ''.join([inp[i][j] for j in range(b) for i in range(a)])

import re
print re.sub('([A-Za-z0-9])[^A-Za-z0-9]+([A-Za-z0-9])','\g<1> \g<2>',s)