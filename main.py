import gflags
import sys

import parser
import handler

gflags.DEFINE_string("input", None, "input yaml file")
gflags.DEFINE_string("output", None, "output yaml file")
gflags.DEFINE_string("format", "%d.yml", "format of parameter's filename")

FLAGS = gflags.FLAGS


def main(argv):
    argv = FLAGS(argv)

    p = parser.CreateParser([
        ("int", r"(\d+)\.\.(\d+)", handler.IntRangeNoStep),
        ])
    for i, conf in enumerate(p.generate(FLAGS.input)):
        print i, conf


if __name__ == '__main__':
    main(sys.argv)
