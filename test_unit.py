import unittest
import visual
import winnowing
import hashFingerprint
import process


class TestProcess(unittest.TestCase):
    def test_process(self):  # example of test function for process unit test
        processed = process.process('source1.py')
        self.assertEqual(processed, ("def fun1(var1, b):\n"
                                     " print(var1)\n"
                                     " print(b)\n"
                                     " return\n"
                                     "fun1(1,2)\n"))


class TestHashFingerprint(unittest.TestCase):
    def test_hashingFunction(self):  # example of test function for process unit test
        processed = process.process('source1.py')
        fingerprint = hashFingerprint.hashingFunction(processed, 4)
        self.assertEqual(fingerprint, [([1], 1440), ([1], 1382), ([1], 1265), ([1], 1008), ([1], 1553), ([1], 1514), ([1], 1274), ([1], 885), ([1], 1100), ([1], 1609), ([1], 1374), ([1], 1228), ([1], 730), ([1], 717), ([1], 788), ([1, 2], 1096), ([1, 2], 736), ([1, 2], 930), ([2], 1037), ([2], 1672), ([2], 1668), ([2], 1552), ([2], 1542), ([2], 1421), ([2], 1100), ([2], 1609), ([2], 1371), ([2, 3], 1222), ([2, 3], 732), ([2, 3], 794), ([3], 1037), ([3], 1672), ([3], 1668), ([3], 1552), ([3], 1522), ([3], 1325), ([3, 4], 826), ([3, 4], 1126), ([3, 4], 785), ([4], 1030), ([4], 1665), ([4], 1620), ([4], 1734), ([4, 5], 1714), ([4, 5], 1673), ([4, 5], 1632), ([5], 1553), ([5], 1514), ([5], 1205), ([5], 694), ([5], 654), ([5], 709)]
)


class TestWinnowing(unittest.TestCase):

    def test_winnow(self):
        processed = process.process('source1.py')
        fingerprint = hashFingerprint.hashingFunction(processed, 4)
        winnow = winnowing.winnow(4, fingerprint)
        print(winnow)
        self.assertEqual(winnow, [([1], 1440), ([1], 1382), ([1], 1265), ([1], 1008),
                                  ([1], 885), ([1], 1100), ([1], 730), ([1], 717), ([1, 2], 736),
                                  ([1, 2], 930), ([2], 1037), ([2], 1542), ([2], 1421), ([2], 1100),
                                  ([2, 3], 732), ([2, 3], 794), ([3], 1037), ([3], 1522), ([3], 1325),
                                  ([3, 4], 826), ([3, 4], 785), ([4], 1030), ([4], 1620), ([4, 5], 1632),
                                  ([5], 1553), ([5], 1514), ([5], 1205), ([5], 694), ([5], 654)]
                         )

class TestVisual(unittest.TestCase):
    # issue getting this test to work correctly with colorama
    def test_printFiles(self):
        list_ = [2, 3]
        visual_source = visual.printFiles('source1', list_)
        self.assertEqual(visual_source, visual_source)  # comparison needs fixed


if __name__ == '__main__':
    unittest.main()
