import parser
import handler

import gflags
import os
import json
import yaml


gflags.DEFINE_bool("verbose", False, "more information")
gflags.DEFINE_enum("filetype", "yaml", ["yaml", "json"], "filetype of output")
gflags.DEFINE_bool("show", False, "show parsed values")

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
        ("int", r"%d\.\.%d",         handler.ArangeNoStep),
        ("int", r"%d\.\.%d\.\.%d",   handler.Arange),
        ("float", r"%f\.\.%f\.\.%f", handler.Arange),
        ("float", r"%f\.\.%f/%d",    handler.Linspace),
        ])


def PGenerator(input_file, output_path):
    p = CreateParser()

    if FLAGS.show:
        keys, values = p.ParseFile(input_file)
        for key, val in zip(keys, values):
            print "{}: {}".format(key, val)
    else:
        for idx, conf in enumerate(p.Generate(input_file)):
            path = output_path.format(idx)
            print path
            Output(path, conf)
