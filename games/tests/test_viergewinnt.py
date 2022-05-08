"""Dieses Modul testet die Hilfsmethoden der VierGewinnt Klasse. Zum Ausführen braucht es folgenden Befehl:
python -m unittest games/tests/test_viergewinnt.py oder
python -m unittest games.tests.test_viergewinnt.TestVierGewinnt
Siehe https://docs.python.org/3/library/unittest.html für weitere Informationen.
"""
import unittest
from games.vier_gewinnt import VierGewinnt

class TestVierGewinnt(unittest.TestCase):

    def test_countSameTokensIn(self):
        """Diese Methode testet VierGewinnt.countSameTokensIn() mit verschiedenen Eingaben."""
        self.assertEqual(VierGewinnt.countSameTokensIn([1, 1, 0, -1, -1, 1, 1]),   2)
        self.assertEqual(VierGewinnt.countSameTokensIn([0, 1, 1, -1, 1, 1, 1]),    3)
        self.assertEqual(VierGewinnt.countSameTokensIn([0, 1, 0, -1, -1, -1, 1]),  -3)
        self.assertEqual(VierGewinnt.countSameTokensIn([-1, -1, -1, 0, 1, 1, 1]),  3)
        self.assertEqual(VierGewinnt.countSameTokensIn([-1, -1, -1, -1, 1, 1, 1]), -4)
        self.assertEqual(VierGewinnt.countSameTokensIn([-1, -1, -1, 1, 1, 1, 1]),  4)
        self.assertEqual(VierGewinnt.countSameTokensIn([0, 1, 1, 1, 1, 1, -1]),    5)
        self.assertEqual(VierGewinnt.countSameTokensIn([0, 0, 0, 0, 0, 0, 0]),     0)
        self.assertEqual(VierGewinnt.countSameTokensIn([0, 1, 0, 1, 0, -1, 0]),    1)
        self.assertEqual(VierGewinnt.countSameTokensIn([1, 0, -1, -1, 1, 0, 1]),   -2)

    def test_getWinnerIn(self):
        """Diese Methode testet VierGewinnt.getWinnerIn() mit verschiedenen Eingaben."""
        self.assertEqual(VierGewinnt.getWinnerIn([1, 1, 0, -1, -1, 1, 1]),   0)
        self.assertEqual(VierGewinnt.getWinnerIn([0, 1, 1, -1, 1, 1, 1]),    0)
        self.assertEqual(VierGewinnt.getWinnerIn([0, 1, 0, -1, -1, -1, 1]),  0)
        self.assertEqual(VierGewinnt.getWinnerIn([-1, -1, -1, 0, 1, 1, 1]),  0)
        self.assertEqual(VierGewinnt.getWinnerIn([-1, -1, -1, -1, 1, 1, 1]), 2)
        self.assertEqual(VierGewinnt.getWinnerIn([-1, -1, -1, 1, 1, 1, 1]),  1)
        self.assertEqual(VierGewinnt.getWinnerIn([0, 1, 1, 1, 1, 1, -1]),    1)
        self.assertEqual(VierGewinnt.getWinnerIn([0, 0, 0, 0, 0, 0, 0]),     0)
        self.assertEqual(VierGewinnt.getWinnerIn([0, 1, 0, 1, 0, -1, 0]),    0)
        self.assertEqual(VierGewinnt.getWinnerIn([1, 0, -1, -1, 1, 0, 1]),   0)

    def test_countTokensIn(self):
        """Diese Methode testet VierGewinnt.countTokensIn() mit verschiedenen Eingaben."""
        self.assertEqual(VierGewinnt.countTokensIn([1, 1, 0, -1, -1, 1, 1]),   6)
        self.assertEqual(VierGewinnt.countTokensIn([0, 1, 1, -1, 1, 1, 1]),    6)
        self.assertEqual(VierGewinnt.countTokensIn([0, 1, 0, -1, -1, -1, 1]),  5)
        self.assertEqual(VierGewinnt.countTokensIn([-1, -1, -1, 0, 1, 1, 1]),  6)
        self.assertEqual(VierGewinnt.countTokensIn([-1, -1, -1, -1, 1, 1, 1]), 7)
        self.assertEqual(VierGewinnt.countTokensIn([-1, -1, -1, 1, 1, 1, 1]),  7)
        self.assertEqual(VierGewinnt.countTokensIn([0, 1, 1, 1, 1, 1, -1]),    6)
        self.assertEqual(VierGewinnt.countTokensIn([0, 0, 0, 0, 0, 0, 0]),     0)
        self.assertEqual(VierGewinnt.countTokensIn([0, 1, 0, 1, 0, -1, 0]),    3)
        self.assertEqual(VierGewinnt.countTokensIn([1, 0, -1, -1, 1, 0, 1]),   5)

    def test_getSameCountList(self):
        """Diese Methode testet VierGewinnt.getSameCountList() mit verschiedenen Eingaben."""
        self.assertListAlmostEqual(VierGewinnt.getSameCountList([1, 1, 0, -1, -1, 1, 1]),   [2.4, 0, -2.4, 2])
        self.assertListAlmostEqual(VierGewinnt.getSameCountList([0, 1, 1, -1, 1, 1, 1]),    [0, 2.4, -1, 3])
        self.assertListAlmostEqual(VierGewinnt.getSameCountList([0, 1, 0, -1, -1, -1, 1]),  [0, 1.8, 0, -3.4, 1])
        self.assertListAlmostEqual(VierGewinnt.getSameCountList([-1, -1, -1, 0, 1, 1, 1]),  [-3.4, 0, 3.4])
        self.assertListAlmostEqual(VierGewinnt.getSameCountList([-1, -1, -1, -1, 1, 1, 1]), [-4, 3])
        self.assertListAlmostEqual(VierGewinnt.getSameCountList([-1, -1, -1, 1, 1, 1, 1]),  [-3, 4])
        self.assertListAlmostEqual(VierGewinnt.getSameCountList([0, 1, 1, 1, 1, 1, -1]),    [0, 5.4, -1])
        self.assertListAlmostEqual(VierGewinnt.getSameCountList([0, 0, 0, 0, 0, 0, 0]),     [0])
        self.assertListAlmostEqual(VierGewinnt.getSameCountList([0, 1, 0, 1, 0, -1, 0]),    [0, 1.8, 0, 1.8, 0, -1.8, 0])
        self.assertListAlmostEqual(VierGewinnt.getSameCountList([1, 0, -1, -1, 1, 0, 1]),   [1.4, 0, -2.4, 1.4, 0, 1.4])

    def assertListAlmostEqual(self, list1, list2):
        """Diese Methode vergleicht zwei Listen, die Zahlen beinhalten, ob die jeweiligen Zahlen weniger als 10**-7 voneinander abweichen."""
        self.assertEqual(len(list1), len(list2))
        for i in range(len(list1)):
            self.assertAlmostEqual(list1[i], list2[i])

    def test_getPlaceValue(self):
        """Diese Methode testet VierGewinnt.getPlaceValue() mit verschiedenen Eingaben."""
        self.assertEqual(VierGewinnt.getPlaceValue(1, 1), 3)
        self.assertEqual(VierGewinnt.getPlaceValue(1, 2), 4)
        self.assertEqual(VierGewinnt.getPlaceValue(1, 3), 5)
        self.assertEqual(VierGewinnt.getPlaceValue(1, 4), 7)
        self.assertEqual(VierGewinnt.getPlaceValue(1, 5), 5)
        self.assertEqual(VierGewinnt.getPlaceValue(1, 6), 4)
        self.assertEqual(VierGewinnt.getPlaceValue(1, 7), 3)
        self.assertEqual(VierGewinnt.getPlaceValue(6, 1), 3)
        self.assertEqual(VierGewinnt.getPlaceValue(6, 2), 4)
        self.assertEqual(VierGewinnt.getPlaceValue(6, 3), 5)
        self.assertEqual(VierGewinnt.getPlaceValue(6, 4), 7)
        self.assertEqual(VierGewinnt.getPlaceValue(6, 5), 5)
        self.assertEqual(VierGewinnt.getPlaceValue(6, 6), 4)
        self.assertEqual(VierGewinnt.getPlaceValue(6, 7), 3)
        self.assertEqual(VierGewinnt.getPlaceValue(2, 1), 4)
        self.assertEqual(VierGewinnt.getPlaceValue(2, 2), 6)
        self.assertEqual(VierGewinnt.getPlaceValue(2, 3), 8)
        self.assertEqual(VierGewinnt.getPlaceValue(2, 4), 10)
        self.assertEqual(VierGewinnt.getPlaceValue(3, 4), 13)
        self.assertEqual(VierGewinnt.getPlaceValue(4, 4), 13)
        self.assertEqual(VierGewinnt.getPlaceValue(4, 5), 11)
        self.assertEqual(VierGewinnt.getPlaceValue(4, 6), 8)
        self.assertEqual(VierGewinnt.getPlaceValue(4, 7), 5)