scores1 = {
    1 : [1, [1]] ,2 : [0, []], 3 : [0, []], 4 : [1, [9, 19]], 5 : [0, []],

    6 : [7, [5]],
    7 : [6, [6]],
    8 : [5, [7]],
    9 : [4, [8]],
    10 : [3, [9]],
    11 : [2, [10]],
    12 : [1, [11]],

    13 : [0, []], 14 : [1, [6, 16, 21]],

    15 : [6, [5]],
    16 : [5, [6, 16]],
    17 : [4, [7, 17]],
    18 : [3, [8, 18]],
    19 : [2, [9, 19]],
    20 : [1, [5, 10, 20]]
}

scores2 = {
    1 : [1, [1]], 2 : [1, [8, 9, 17, 18]], 3 : [0, []], 4 : [0, []],

    5 : [7, [6]],
    6 : [6, [7]],
    7 : [5, [8]],
    8 : [4, [9]],
    9 : [3, [10]],
    10 : [2, [11]],
    11 : [1, [12]],
    
    12 : [0, []], 13 : [0, []], 14 : [0, []], 15 : [0, []],

    16 : [4, [7, 16]],
    17 : [3, [8, 17]],
    18 : [2, [9, 18]],
    19 : [1, [10, 19]],

    20 : [2, [6, 15]],
    21 : [1, [7, 14, 16]],

    22 : [0, []], 23 : [0, []], 24 : [0, []], 25 : [0, []], 26 : [0, []]
}

blocks1 = [(6, 12), (15, 20)]
blocks2 = [(5, 11), (16, 19), (20, 21)]

def isInBlock(line, block):
    return line >= block[0] and line <= block[1]

def getBlockFromLine(line, blocks):
    for block in blocks: 
        if isInBlock(line, block):
            return block

def findMatchingBlocks(block, scores1, scores2, blocks1, blocks2):
    # store blocks in sets so no duplicates
    mBlocks1 = set()
    mBlocks2 = set()
    # block matches itself
    mBlocks1.add(block)

    mLines = scores1[block[0]][1]
    for line in mLines:
        g = getBlockFromLine(line, blocks2)
        if g != None:
            mBlocks2.add(g)

    # find which blocks from the other set map back to 'block'
    for b in blocks2:
        start = b[0]
        mLines = scores2[start][1]
        doesMatch = False
        # check if block2 maps at all to block
        for line in mLines:
            if isInBlock(line, block):
                doesMatch = True
        if doesMatch:
            mBlocks2.add(b)
            # get all the blocks that b maps to in blocks1
            for line in mLines:
                g = getBlockFromLine(line, blocks1)
                if g != None:
                    mBlocks1.add(g)

    return (mBlocks1, mBlocks2)

mBlocks1 = []
mBlocks2 = []
i = 0

while len(blocks1) > 0:
    block = blocks1.pop()
    print("working on " + str(block) + " from blocks1")
    res = findMatchingBlocks(block, scores1, scores2, blocks1, blocks2)
    print("res = " + str(res))
    for b in res[0]:
        print("block added to 1: " + str(b))
        mBlocks1.append([i, b])
        if b in blocks1: blocks1.remove(b)
    for b in res[1]:
        print("block added to 2: " + str(b))
        mBlocks2.append([i, b])
        if b in blocks2: blocks2.remove(b)
    i += 1

while len(blocks2) > 0:
    block = blocks2.pop()
    print("working on " + str(block) + " from blocks2")
    res = findMatchingBlocks(block, scores2, scores1, blocks2, blocks1)
    print("res = " + str(res))
    for b in res[1]:
        print("block added to 1: " + str(b))
        mBlocks1.append([i, b])
        if b in blocks1: blocks1.remove(b)
    for b in res[0]:
        print("block added to 2: " + str(b))
        mBlocks2.append([i, b])
        if b in blocks2: blocks2.remove(b)
    i += 1

print(mBlocks1)
print(mBlocks2)