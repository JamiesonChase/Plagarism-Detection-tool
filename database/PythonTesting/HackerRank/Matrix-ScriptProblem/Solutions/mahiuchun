from collections import *
import sys
import re
alphanum = re.compile(r'[a-zA-Z0-9]')
N, M = map(int, raw_input().split())
matrix = []
dic = defaultdict(lambda: ' ')
dic2 = defaultdict(lambda: 'a')
for ch in map(chr, range(ord('a'), ord('z') + 1)):
    dic[ch] = ch
    dic[ch.upper()] = ch.upper()
for ch in map(chr, range(ord('0'), ord('9') + 1)):
    dic[ch] = ch
for ch in '!@#$%& ':
    dic2[ch] = ch
for _ in xrange(N):
    matrix.append(raw_input())
result = []
result2 = []
for j in xrange(M):
    for i in xrange(N):
        result.append(dic[matrix[i][j]])
        result2.append(dic2[matrix[i][j]])
res = ' '.join(''.join(result).split())
res2 = ''.join(result2).split('a')
alphanum.match(matrix[0][0]) and alphanum.match(matrix[N-1][M-1]) and (sys.stdout.write(res+'\n') or sys.exit(0))
alphanum.match(matrix[0][0]) and (sys.stdout.write(res+res2[-1]+'\n') or sys.exit(0))
alphanum.match(matrix[N-1][M-1]) and (sys.stdout.write(res2[0]+res+'\n') or sys.exit(0))
len(res2) >= 2 and (sys.stdout.write(res2[0]+res+res2[-1]+'\n') or sys.exit(0))
sys.stdout.write(res2[0]+'\n')