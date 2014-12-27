import parser
import pgenerator

import tempfile
import re
import unittest

YAML_TEMPLATE="""
{0}:
    t: {1}
    v: {2}
"""

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

    def Parse(self, t, v):
        return [d["key"]
                for d in self.parser.generate_impl({"key": {"t": t, "v": v}})]

    def assertAlmostEqualList(self, first, second,
                              places=7, msg=None, delta=None):
        for x, y in zip(first, second):
            self.assertAlmostEqual(x, y, places, msg, delta)

    def testIntRange(self):
        self.assertEqual([1, 2, 3, 4, 5], self.Parse("int", "1..5"))

    def testFloatRange(self):
        self.assertAlmostEqualList([0, 0.2, 0.4, 0.6, 0.8, 1],
                                   self.Parse("float", "0.0..0.2..1.0"))

    def testLinspace(self):
        self.assertAlmostEqualList([1, 1.25, 1.5, 1.75, 2.0],
                                   self.Parse("float", "1..2/5"))
        self.assertAlmostEqual([-1.5, 0, 1.5],
                               self.Parse("float", "-1.5..1.5/3"))

    def testStr(self):
        self.assertEqual(["aiueo"],
                         self.Parse("str", "aiueo"))


if __name__ == '__main__':
    unittest.main()
