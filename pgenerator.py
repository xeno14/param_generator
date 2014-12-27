import parser
from handler import *

import gflags
import os
import sys
import yaml


gflags.DEFINE_bool("verbose", False, "more information")

FLAGS = gflags.FLAGS


def Output(path, data):
    dirname = os.path.dirname(path)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    with open(path, "w") as f:
        yml = yaml.dump(data, default_flow_style=False)
        if FLAGS.verbose:
            print yml
        f.write(yml)


def PGenerator(input_file, output_path):
    p = parser.CreateParser([
        ("int", r"%d\.\.%d", ArangeNoStep),
        ("float", r"%f\.\.%f\.\.%f", Arange),
        ("float", r"%f\.\.%f/%d", Linspace),
        ])

    for i, conf in enumerate(p.generate(input_file)):
        path = output_path.format(i)
        print path
        Output(path, conf)
