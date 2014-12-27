import gflags
import sys

import parser
from handler import *

gflags.DEFINE_string("input", None, "input yaml file")
gflags.DEFINE_string("output", None, "output yaml file")
gflags.DEFINE_string("format", "%d.yml", "format of parameter's filename")

FLAGS = gflags.FLAGS


def main(argv):
    argv = FLAGS(argv)

    p = parser.CreateParser([
        ("int", r"(int)\.\.(int)", IntRangeNoStep),
        ("float", r"(float)\.\.(float)\.\.(float)", FloatRange),
        ])
    for i, conf in enumerate(p.generate(FLAGS.input)):
        print i, conf


if __name__ == '__main__':
    main(sys.argv)
