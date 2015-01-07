import parser
import pgenerator

import re
import unittest


class ParserTest(unittest.TestCase):

    def testTypePatternInt(self):
        PATTERN = parser.Parser.TYPE_PATTERN[r"%d"]
        p = re.compile(r"^" + PATTERN + r"$")   # full match
        self.assertTrue(p.match("1"))
        self.assertTrue(p.match("+1"))
        self.assertTrue(p.match("-123"))
        self.assertFalse(p.match("aiueo"))
        self.assertFalse(p.match("1.2"))

    def testTypePatternFloat(self):
        PATTERN = parser.Parser.TYPE_PATTERN[r"%f"]
        p = re.compile(r"^" + PATTERN + r"$")   # full match
        self.assertTrue(p.match("1"))
        self.assertTrue(p.match("-1"))
        self.assertTrue(p.match("1.0"))
        self.assertTrue(p.match("-1.0"))
        self.assertFalse(p.match("1."))
        self.assertFalse(p.match(".1"))
        self.assertTrue(p.match("1.0e-100"))
        self.assertTrue(p.match("1.0E3.14"))
        self.assertTrue(p.match("-1.0E1000"))


class GeneratorTest(unittest.TestCase):

    def setUp(self):
        self.parser = pgenerator.CreateParser()

    def Parse(self, val):
        """Parses dictionary {"key": val}."""
        _, values = self.parser.ParseDict({"key": val})
        return values[0]

    def assertAlmostEqualList(self, first, second,
                              places=7, msg=None, delta=None):
        for x, y in zip(first, second):
            self.assertAlmostEqual(x, y, places, msg, delta)

    def testIntRange(self):
        self.assertEqual([1, 2, 3, 4, 5], self.Parse("1..5"))

    def testFloatRange(self):
        self.assertAlmostEqualList([0, 0.2, 0.4, 0.6, 0.8, 1],
                                   self.Parse("0.0..0.2..1.0"))

    def testLinspace(self):
        self.assertAlmostEqualList([1, 1.25, 1.5, 1.75, 2.0],
                                   self.Parse("1..2/5"))
        self.assertAlmostEqual([-1.5, 0, 1.5],
                               self.Parse("-1.5..1.5/3"))

    def testStr(self):
        self.assertEqual(["aiueo"],
                         self.Parse("aiueo"))

    def testList(self):
        self.assertEqual(["I", "love", "you"],
                         self.Parse(["I", "love", "you"]))

    def testListInt(self):
        self.assertEqual([0, 1, 2, 10, 11, 12],
                         self.Parse(["0..2", "10..12"]))


if __name__ == '__main__':
    unittest.main()
