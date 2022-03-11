import unittest
from time import time
from comparison2 import *

class TestComparison2(unittest.TestCase):
    
    testFiles = [
        "testfiles/testFile.py",
        "testfiles/testFile_rearranged.py",
        "testfiles/testFile_reordered.py",
        "testfiles/testFile2.py",
        "testfiles/testFile3.py"
    ]

    t0 = time()
    testIndices = [file_setup(file) for file in testFiles]
    print("File setup time: " + str(time() - t0))

    def test_getMatches(self):
        t0 = time()

        print("getMatches time: " + str(time() - t0))

    def test_getMatchedIndex(self):
        t0 = time()

        print("getMatchedIndex time: " + str(time() - t0))

    def test_invertDict(self):
        t0 = time()

        print("invertDict time: " + str(time() - t0))
    
    def test_getLinesOfInterest(self):
        t0 = time()

        print("getLinesOfInterest time: " + str(time() - t0))

    def test_computeSimilarity(self):
        t0 = time()

        print("computeSimilarity time: " + str(time() - t0))

    def test_blockifyLines(self):
        t0 = time()

        print("blockifyLines time: " + str(time() - t0))

    def test_translateLines(self):
        t0 = time()

        print("translateLines time: " + str(time() - t0))

    def corLinesSetup(index1, index2):
        matches = getMatches(index1, index2)
        file1MatchedIndex = getMatchedIndex(matches, index1)
        file2MatchedIndex = getMatchedIndex(matches, index2)

        ii1 = invertDict(file1MatchedIndex)
        ii2 = invertDict(file2MatchedIndex)    

        oi1 = invertDict(index1)
        oi2 = invertDict(index2)   

        loi1 = getLinesOfInterest(ii1, oi1)
        loi2 = getLinesOfInterest(ii2, oi2)

        corLines1to2 = {}
        for line in loi1:
            hashes = ii1[line]
            corLines1to2[line] = []
            for hash in hashes:
                corLines1to2[line].append(file2MatchedIndex[hash])
            corLines1to2[line] = list(set.intersection(*map(set, corLines1to2[line])))

        corLines2to1 = {}
        for line in loi2:
            hashes = ii2[line]
            corLines2to1[line] = []
            for hash in hashes:
                corLines2to1[line].append(file1MatchedIndex[hash])
            corLines2to1[line] = list(set.intersection(*map(set, corLines2to1[line])))

        return (corLines1to2, corLines2to1)

    def test_corLines(self):
        index1 = self.testIndices[0]
        for i in range(1, len(self.testIndices)):
            t0 = time()
            with self.subTest(i=1):
                index2 = self.testIndices[i]
                corLines = self.corLinesSetup(index1, index2)
                print("corLines " + str(i) + " time: " + str(time() - t0))

            with self.subTest(i=2):
                index2 = self.testIndices[i]
                corLines = self.corLinesSetup(index1, index2)
                print("corLines " + str(i) + " time: " + str(time() - t0))

            with self.subTest(i=3):
                index2 = self.testIndices[i]
                corLines = self.corLinesSetup(index1, index2)
                print("corLines " + str(i) + " time: " + str(time() - t0))

            with self.subTest(i=4):
                index2 = self.testIndices[i]
                corLines = self.corLinesSetup(index1, index2)
                print("corLines " + str(i) + " time: " + str(time() - t0))

            
if __name__ == "__main__":
    unittest.main()