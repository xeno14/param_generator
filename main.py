from pgenerator import PGenerator

import gflags
import sys

gflags.DEFINE_string("input", None, "input yaml file")
gflags.DEFINE_string("output", "run{}/param.yml",
                     "output with format of parameter's filename")
gflags.DEFINE_bool("verbose", False, "more information")

gflags.MarkFlagAsRequired("input")

FLAGS = gflags.FLAGS


def main(argv):
    argv = FLAGS(argv)
    PGenerator(FLAGS.input, FLAGS.output, FLAGS.verbose)


if __name__ == '__main__':
    main(sys.argv)
