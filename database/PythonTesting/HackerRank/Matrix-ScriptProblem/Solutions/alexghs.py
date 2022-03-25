import sys
import re
p = re.compile(r'(?<=\w)([\$\#\%\s]+)(?=\w)')
dem = sys.stdin.readline().split();
r = int(dem[0])
c = int(dem[1])
rows = [l for l in sys.stdin]
text = "";
for i in range(c):
    for j in range(r):
        text = text+rows[j][i]
print(p.sub(' ',text))