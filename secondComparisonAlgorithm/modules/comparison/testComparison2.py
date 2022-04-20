import unittest
from time import time
from comparison2 import *
from itertools import chain

class TestComparison2(unittest.TestCase):

    def setUp(self):
        self.file1 = "C:/Users/trvrh/Documents/GitHub/Winnowing-/secondComparisonAlgorithm/database/testFile.py"
        self.file2 = "C:/Users/trvrh/Documents/GitHub/Winnowing-/secondComparisonAlgorithm/database//testFile_rearranged.py"
        self.index1 = file_setup(self.file1)
        self.index2 = file_setup(self.file2)
        self.matches = getMatches(self.index1, self.index2)
        self.score1 = computeSimilarity(self.matches, self.index1)
        self.score2 = computeSimilarity(self.matches, self.index2)
        if self.score1 < self.score2: 
            temp = self.index1; self.index1 = self.index2; self.index2 = temp
            temp = self.file1; self.file1 = self.file2; self.file2 = temp
        self.file1MatchedIndex = getMatchedIndex(self.matches, self.index1)
        self.file2MatchedIndex = getMatchedIndex(self.matches, self.index2)
        self.ii1 = invertDict(self.file1MatchedIndex)
        self.ii2 = invertDict(self.file2MatchedIndex)    
        self.oi1 = invertDict(self.index1)
        self.oi2 = invertDict(self.index2)   
        self.loi1 = getLinesOfInterest(self.ii1, self.oi1)
        self.loi2 = getLinesOfInterest(self.ii2, self.oi2)
        self.lineBlocks = blockifyLines(self.loi1)
        self.corLines2to1 = {}
        
        for line in self.loi2:
            hashes = self.ii2[line]
            self.corLines2to1[line] = []
            for hash in hashes:
                self.corLines2to1[line].append(self.file1MatchedIndex[hash])
            self.corLines2to1[line] = list(chain(*self.corLines2to1[line]))
            self.corLines2to1[line] = max(set(self.corLines2to1[line]), key=self.corLines2to1[line].count)
        
        self.corBlocks2to1 = {}
        for i in range(len(self.lineBlocks)):
            self.corBlocks2to1[i] = []
            for line in self.corLines2to1:
                if not self.corLines2to1[line]: continue
                corLine = self.corLines2to1[line]
                if corLine >= self.lineBlocks[i][0] and corLine <= self.lineBlocks[i][1]:
                    self.corBlocks2to1[i].append(line)
        self.file1Stripped = self.file1 + "_Stripped"
        self.file2Stripped = self.file2 + "_Stripped"

    #### TESTS ####

    def test_invertedIndexCreate(self):
        print("\n\nIn invertedIndexCreate test: ")
        print(self.index1)
        print(self.index2)

    def test_getLinesOfInterest(self):
        print("\n\nIn getLinesOfInterest test: ")
        # line numbers mapped to ngrams
        original = {1: [1, 4, 2], 2: [5, 3], 3: [8, 9], 4: [7]}
        matches = {1: [1, 4], 2: [5, 3], 3: [8, 9]}
        self.assertEqual(getLinesOfInterest(matches, original), [1, 2, 3])


    def test_invertDict(self):
        print("\n\nIn invertDict test: ")

        dct = {"a": [1, 2, 3], "b": [4, 2, 3], "c": [1, 1, 3]}
        invdct = invertDict(dct)
        self.assertTrue(
            ("a" in invdct[1] and "c" in invdct[1]) and
            ("a" in invdct[2] and "b" in invdct[2]) and
            ("a" in invdct[3] and "b" in invdct[3] and "c" in invdct[3]), 
            "invertDict failed")


    def test_corLines(self):
        print("\n\nIn corLines test:")
        
        t0 = time()        
        corLines2to1 = {}
        for line in self.loi2:
            hashes = self.ii2[line]
            corLines2to1[line] = []
            for hash in hashes:
                corLines2to1[line].append(self.file1MatchedIndex[hash])
            corLines2to1[line] = list(chain(*corLines2to1[line]))
            corLines2to1[line] = max(set(corLines2to1[line]), key=corLines2to1[line].count)

        
        print(corLines2to1)
        print("corLines time: " + str(time() - t0))


    def test_corBlocks(self):
        print("\n\nIn corBlocks test: ")
        t0 = time()

        corBlocks2to1 = {}
        for i in range(len(self.lineBlocks)):
            corBlocks2to1[i] = []
            for line in self.corLines2to1:
                if not self.corLines2to1[line]: continue
                corLine = self.corLines2to1[line]
                if corLine >= self.lineBlocks[i][0] and corLine <= self.lineBlocks[i][1]:
                    corBlocks2to1[i].append(line)
        
        
        print(corBlocks2to1)
        print("corBlocks time: " + str(time() - t0))


    def test_sortedBlocks(self):
        t0 = time()
        sortedBlocks1 = []
        for i in range(0, len(self.lineBlocks)):
            if len(self.lineBlocks[i]) > 0:
                lines = list(range(self.lineBlocks[i][0], self.lineBlocks[i][1]+1))
                self.lineBlocks[i] = blockifyLines(translateLines(lines, self.file1, self.file1Stripped))
                for block in self.lineBlocks[i]:
                    sortedBlocks1.append([i, block])
        sortedBlocks1.sort(key = lambda x: x[1][0])

        for block in self.corBlocks2to1:
            lines = self.corBlocks2to1[block]
            if len(lines) > 0: self.corBlocks2to1[block] = blockifyLines(translateLines(lines, self.file2, self.file2Stripped))
        
        sortedBlocks2 = []
        for key in self.corBlocks2to1:
            blocks = self.corBlocks2to1[key]
            for block in blocks:
                sortedBlocks2.append([key, block])
        sortedBlocks2.sort(key = lambda x: x[1][0])
        
        print("\n\nIn sorted blocks test: ")
        print(sortedBlocks1)
        print(sortedBlocks2)
        print("sortedBlocks time: " + str(time() - t0))

        
if __name__ == "__main__":
    unittest.main()