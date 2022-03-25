import sys

stdin = sys.stdin

n,m = map(int,stdin.readline().split())
s = [" "] * (n*m)
for i in range(n):
    line = stdin.readline().rstrip()
    for j in range(len(line)):
        s[j*n+i] = line[j]
s = "".join(s)
# print(s)
import re
print(re.sub("(?<=\w)\W+(?=\w)", " ", s))