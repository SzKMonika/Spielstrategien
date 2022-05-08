"""Dieses Modul testet die Hilfsmethoden der Mastermind Klasse. Zum Ausführen braucht es folgenden Befehl:
python -m unittest games/tests/test_mastermind.py oder
python -m unittest games.tests.test_mastermind.TestMastermind
Siehe https://docs.python.org/3/library/unittest.html für weitere Informationen.
"""
import unittest
from games.mastermind import Mastermind

class TestMastermind(unittest.TestCase):

    def assertCompare(self, guess, secret, result):
        self.assertEqual(Mastermind.compareNumbers(guess, secret), result, "Falsch: " + str(guess) + " / " + str(secret))

    def test_compareNumbers_zero(self):
        for guess in (1234, 1212, 4554, 0, 1, 12, 123, 3210, 210, 10, 4455):
            for secret in (9876, 9898, 9988, 9998, 9999, 6776, 6777):
                self.assertCompare(guess, secret, (0,0))
                self.assertCompare(secret, guess, (0,0))

    def test_compareNumbers_halbgut(self):
        for guess in (1234, 5212, 3412, 5152):
            for secret in (4500, 4567, 6745, 45):
                self.assertCompare(guess, secret, (0,1))
                self.assertCompare(secret, guess, (0,1))
        for guess in (102, 101, 201):
            for secret in (6070, 6060):
                self.assertCompare(guess, secret, (0,2))
                self.assertCompare(secret, guess, (0,2))

    def test_compareNumbers_gut(self):
        for guess in (1234, 1212, 1221, 1211, 1222):
            for secret in (1200, 1299):
                self.assertCompare(guess, secret, (2,0))
                self.assertCompare(secret, guess, (2,0))
        for guess in (1011, 110, 1034, 4310):
            for secret in (1220, 1290):
                self.assertCompare(guess, secret, (1,1))
                self.assertCompare(secret, guess, (1,1))

    def test_compareNumbers_perfekt(self):
        for n in (1234, 1212, 1221, 1211, 1222, 3210, 0, 1, 110, 9988, 9999):
            self.assertCompare(n, n, (4,0))
