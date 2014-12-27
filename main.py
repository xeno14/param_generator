import gflags
import os
import sys
import yaml

import parser
from handler import *

gflags.DEFINE_string("input", None, "input yaml file")
gflags.DEFINE_string("output", "run{}/param.yml",
                     "output with format of parameter's filename")
gflags.DEFINE_bool("verbose", False, "more information")

FLAGS = gflags.FLAGS


def Output(path, data, verbose=False):
    dirname = os.path.dirname(path)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    with open(path, "w") as f:
        yml = yaml.dump(data, default_flow_style=False)
        if verbose:
            print yml
        f.write(yml)
    

def main(argv):
    argv = FLAGS(argv)

    p = parser.CreateParser([
        ("int", r"(int)\.\.(int)", ArangeNoStep),
        ("float", r"(float)\.\.(float)\.\.(float)", Arange),
        ("float", r"(float)\.\.(float)/(int)", Linspace),
        ])

    for i, conf in enumerate(p.generate(FLAGS.input)):
        path = FLAGS.output.format(i)
        print path
        Output(path, conf, FLAGS.verbose)


if __name__ == '__main__':
    main(sys.argv)
