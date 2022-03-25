# Enter your code here. Read input from STDIN. Print output to STDOUT
import re
import sys

n, m = map(int, raw_input().split())
matrix = ''.join(sys.stdin.readline()[:m] for _ in xrange(n))
line = ''.join(matrix[i::m] for i in xrange(m))
print re.sub(r"([a-zA-Z0-9])([^a-zA-Z0-9]+)([a-zA-Z0-9])", r"\1 \3", line)