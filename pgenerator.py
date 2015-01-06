import parser
from handler import *

import gflags
import os
import json
import sys
import yaml


gflags.DEFINE_bool("verbose", False, "more information")
gflags.DEFINE_enum("filetype", "yaml", ["yaml", "json"], "filetype of output")

FLAGS = gflags.FLAGS


def Output(path, data):
    dirname = os.path.dirname(path)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    with open(path, "w") as f:
        if FLAGS.filetype == "yaml":
            res = yaml.dump(data, default_flow_style=False)
        elif FLAGS.filetype == "json":
            res = json.dumps(data, indent=4)
        if FLAGS.verbose:
            print res
        f.write(res)


def CreateParser():
    return parser.CreateParser([
        ("int", r"%d\.\.%d", ArangeNoStep),
        ("int", r"%d\.\.%d\.\.%d", Arange),
        ("float", r"%f\.\.%f\.\.%f", Arange),
        ("float", r"%f\.\.%f/%d", Linspace),
        ])


def PGenerator(input_file, output_path):
    p = CreateParser()

    for i, conf in enumerate(p.generate(input_file)):
        path = output_path.format(i)
        print path
        Output(path, conf)
