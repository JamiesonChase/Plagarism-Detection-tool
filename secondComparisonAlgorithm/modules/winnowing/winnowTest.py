import winnowing

hashes = []
i = 0
with open("fingerPrint.txt", "r") as file:
    for line in file:
        hashes.append((i, int(line[0:len(line)-1]))) # add the line without newline as an int
        i += 1
    file.close()

fingerPrints = winnowing.winnow(4, hashes)
for key in fingerPrints:
    print(key)