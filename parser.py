import itertools
import re
import sys
import yaml

class Parser(object):
    TYPES = ("int", "float", "str")
    TYPE_FUNC = {"int": int, "float": float, "str": str}
    TYPE_PATTERN = {
        r"%d": r"([+-]?\d+)",
        r"%f": r"([+-]?\d+"
               r"|[+-]?\d+\.\d+"
               r"|[+-]?\d+\.\d+[eE][+-]?\d+"
               r"|[+-]?\d+\.\d+[eE][+-]?\d+\.\d+)",}

    def __init__(self):
        self.handlers = {t: [] for t in Parser.TYPES}

    def register(self, t, pattern, handler):
        if t not in Parser.TYPES:
            raise Exception(t + " is unknown type")
        for before, after in Parser.TYPE_PATTERN.iteritems():
            pattern = pattern.replace(before, after)
        if not pattern.startswith("^"):
            pattern = r"^" + pattern
        if not pattern.endswith("$"):
            pattern = pattern + r"$"
        self.handlers[t].append((re.compile(pattern), handler))

    def parse(self, t, v):
        for pattern in self.handlers[t]:
            m = pattern[0].match(v)
            if m:
                arg = [Parser.TYPE_FUNC[t](s) for s in m.groups()]
                return pattern[1](*arg)
        raise Exception("No matching pattern for {}".format(v))

    def generate(self, filename):
        with open(filename) as f:
            # TODO load json
            for conf in self.generate_impl(yaml.load(f)):
                yield conf

    def generate_impl(self, dic):
        param = {}

        keys = []
        values = []
        for k, v in dic.iteritems():
            keys.append(k)
            try:
                values.append(self.parse(v["t"], v["v"]))
            except Exception as e:
                print "Error at '{}':".format(k), str(e)
                sys.exit(1)

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
