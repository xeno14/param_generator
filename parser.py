import itertools
import re
import yaml

class Parser(object):
    TYPES = ("int", "float", "str")
    TYPE_FUNCS = {"int": int, "float": float, "str": str}

    def __init__(self):
        self.handlers = {t: [] for t in Parser.TYPES}

    def register(self, t, pattern, handler):
        if t not in Parser.TYPES:
            raise Exception(t + " is unknown type")
        if not pattern.startswith("^"):
            pattern = r"^" + pattern
        if not pattern.endswith("$"):
            pattern = pattern + r"$"
        self.handlers[t].append((re.compile(pattern), handler))

    def parse(self, t, v):
        for pattern in self.handlers[t]:
            m = pattern[0].match(v)
            if m:
                arg = [Parser.TYPE_FUNCS[t](s) for s in m.groups()]
                return pattern[1](*arg)
        return []

    def generate(self, filename):
        with open(filename) as f:
            conf = yaml.load(f)
            param = {}

            keys = []
            values = []
            for k, v in conf.iteritems():
                keys.append(k)
                values.append(self.parse(v["t"], v["v"]))

            for product in itertools.product(*values):
                conf = {}
                for i, k in enumerate(keys):
                    conf[k] = product[i]
                yield conf


def CreateParser(handlers):
    parser = Parser()
    for tup in handlers:
        parser.register(*tup)
    return parser
