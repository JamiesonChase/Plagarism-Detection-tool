# Enter your code here. Read input from STDIN. Print output to STDOUT
import re
N, M = (int(x) for x in raw_input().split())

ain = []
tin = []
for i in range(N):
    ain.append(raw_input())

for i in range(M):
    for j in range(N):
        tin.append(ain[j][i])
       
print re.compile(r"([a-zA-Z0-9])[^a-zA-Z0-9]+([a-zA-Z0-9])").sub(r"\1 \2", "".join(tin))