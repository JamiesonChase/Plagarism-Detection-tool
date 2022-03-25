import re

rows, columns = map(int, raw_input().split())
rst = ''.join(''.join(_) for _ in map(list, zip(*[list(raw_input()) for _ in xrange(rows)])))
print re.sub(r'(?<=\w)[ !@#$%&]+(?=\w)', ' ', rst)