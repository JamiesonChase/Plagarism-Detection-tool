# Enter your code here. Read input from STDIN. Print output to STDOUT

N, M = [int(x) for x in raw_input().split()]  # rows, cols

cols = [""]*M


for _ in range(N):
    row = raw_input()
    for col in range(M):
        cols[col] += row[col]

s = "".join(cols)
import re

def repl(m):
    return " ".join(m.groups())
#print(s)
print(re.sub(r"([A-Za-z0-9])[^A-Za-z0-9]+([A-Za-z0-9])", repl, s))