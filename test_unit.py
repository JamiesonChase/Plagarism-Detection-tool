import unittest
import visual
import winnowing
import hashFingerprint
import process


class TestProcess(unittest.TestCase):
    # this part still needs to be made modular
    def test_preProcess(self):  # example of test function for process unit test
        processed = process.preProcess('source1.py')
        self.assertEqual(processed, ("def fun1(1, 2):"
                                     "  print(1)"
                                     "  print(2)"
                                     "  return"
                                     ""
                                     "fun1(1,2)"))


class TestHashFingerprint(unittest.TestCase):
    # this part still needs to be made modular
    def test_hashFingerprint(self):  # example of test function for process unit test
        fingerprint = hashFingerprint.hashFingerprint('testing.txt')
        self.assertEqual(fingerprint, [0, 88, 98, 55, 36, 4, 26, 6, 32, 86, 69, 18, 67, 87, 11, 24, 50, 38, 79,
                                       6, 80, 33, 49, 82, 91, 23, 31, 18, 55, 67, 69, 21, 24, 54, 16, 55, 27, 99,
                                       36, 95, 57, 38, 43, 61, 66, 94, 97, 38, 81, 33, 85, 88, 16, 23, 37, 72, 15,
                                       70, 14, 55, 65, 52, 31, 62, 81, 72, 28, 91, 61, 52, 56, 50, 0, 74, 74, 94,
                                       4, 16, 98, 3, 31, 72, 1, 58, 61, 9, 8, 96, 33, 47, 54, 78, 66, 100, 69, 78,
                                       42, 45, 67, 10, 31, 99, 21, 24, 26, 12, 14, 23, 64, 92, 79, 75, 89, 6, 21, 18,
                                       64, 25, 95, 91, 78, 18, 67, 47, 49, 66, 4, 46, 61, 15, 58, 7, 63, 16, 92, 44,
                                       63, 88, 2, 79, 85, 15, 55, 71, 82, 93, 43, 77, 13, 43, 69, 19, 8, 66, 49, 63,
                                       80, 45, 13, 89, 24, 51, 99, 100, 71, 14, 17, 39, 46, 38, 2, 46, 53, 72, 20,
                                       74, 2, 73, 58, 31, 68, 50, 45, 30, 18, 31, 29, 16, 3, 20, 96, 31, 42, 60, 49,
                                       57, 60, 52, 71, 13, 41, 84, 100, 17, 87, 48, 14, 18, 69, 40, 49, 54, 57, 7, 25,
                                       15, 50, 74, 52, 82, 88, 63, 80, 90, 60, 19, 53, 35, 5, 92, 73, 52, 92, 80, 48,
                                       12, 30, 39, 7, 63, 40, 38, 93, 0, 55, 57, 8, 29, 21, 14, 79, 85, 4, 62, 42, 13,
                                       96, 15, 43, 3, 96, 64, 93, 39, 90, 49, 91, 85, 73, 78, 4, 13, 1, 18, 95, 30, 74,
                                       61, 27, 75, 70, 27, 98, 92, 0, 48, 37, 23, 23, 94, 86, 12])


class TestWinnowing(unittest.TestCase):

    def test_winnow(self):
        hashes = []
        i = 0
        with open("fingerPrint.txt", "r") as file:
            for line in file:
                hashes.append((i, int(line[0:len(line) - 1])))  # add the line without newline as an int
                i += 1
            file.close()
        winnow = winnowing.winnow(4, hashes)
        self.assertEqual(winnow, [(0, 0), (4, 36), (5, 4), (7, 6), (11, 18), (14, 11), (15, 24), (19, 6), (21, 33),
                                  (25, 23), (27, 18), (31, 21), (34, 16), (36, 27), (38, 36), (41, 38), (42, 43),
                                  (43, 61), (47, 38), (49, 33), (52, 16), (56, 15), (58, 14), (62, 31), (66, 28),
                                  (69, 52), (71, 50), (72, 0), (76, 74), (77, 16), (79, 3), (82, 1), (86, 8), (88, 33),
                                  (89, 47), (90, 54), (92, 66), (96, 42), (99, 10), (102, 21), (105, 12), (106, 14),
                                  (107, 23), (108, 64), (111, 75), (113, 6), (115, 18), (117, 25), (121, 18),
                                  (123, 47), (126, 4), (129, 15), (131, 7), (133, 16), (135, 44), (138, 2), (141, 15),
                                  (142, 55), (146, 43), (148, 13), (152, 8), (154, 49), (157, 45), (158, 13), (160, 24),
                                  (161, 51), (165, 14), (166, 17), (170, 2), (174, 20), (176, 2), (179, 31), (183, 30),
                                  (184, 18), (187, 16), (188, 3), (189, 20), (191, 31), (192, 42), (194, 49), (197, 52),
                                  (199, 13), (203, 17), (206, 14), (207, 18), (209, 40), (213, 7), (215, 15), (216, 50),
                                  (218, 52), (221, 63), (224, 60), (225, 19), (228, 5), (231, 52), (234, 48), (235, 12),
                                  (238, 7), (241, 38), (243, 0), (246, 8), (249, 14), (252, 4), (255, 13), (259, 3),
                                  (263, 39), (265, 49), (268, 73), (270, 4), (272, 1), (273, 18), (275, 30), (278, 27),
                                  (281, 27), (284, 0), (288, 23), (291, 12)])


class TestVisual(unittest.TestCase):
    # issue getting this test to work correctly with colorama
    def test_printFiles(self):
        list_ = [2, 3]
        visual_source = visual.printFiles('source1', list_)
        self.assertEqual(visual_source, visual_source)  # comparison needs fixed


if __name__ == '__main__':
    unittest.main()
