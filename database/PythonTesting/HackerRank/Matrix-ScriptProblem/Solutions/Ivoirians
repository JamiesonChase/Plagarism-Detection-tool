import re
# Enter your code here. Read input from STDIN. Print output to STDOUT

def as_link(match):
    link = match.group(1)
    return 'XXX'

n, m = map(int, raw_input().split(" "))


x = []
for k in range(n):
    x += [list(raw_input())]
s = ""
for i in range(m):
    for j in range(n):
        s += x[j][i]
s = re.sub(r'([A-Za-z])([^A-Za-z]+)([A-Za-z])', r'\1 \3', s)
print s