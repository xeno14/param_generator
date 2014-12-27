from pgenerator import PGenerator

import gflags
import sys

gflags.DEFINE_string("input", None, "input yaml file")
gflags.DEFINE_string("output", "run{}/param.yml",
                     "output with format of parameter's filename")

gflags.MarkFlagAsRequired("input")

FLAGS = gflags.FLAGS


def main(argv):
    argv = FLAGS(argv)
    PGenerator(FLAGS.input, FLAGS.output)


if __name__ == '__main__':
    main(sys.argv)
