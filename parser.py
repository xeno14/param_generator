import itertools
import re
import sys
import yaml

class Parser(object):
    TYPES = {"int", "float", "str"}
    TYPE_NUMBER = {"int", "float"}
    TYPE_FUNC = {"int": int, "float": float, "str": str}
    TYPE_PATTERN = {
        r"%d": r"([+-]?\d+)",
        r"%f": r"([+-]?\d+"
               r"|[+-]?\d+\.\d+"
               r"|[+-]?\d+\.\d+[eE][+-]?\d+"
               r"|[+-]?\d+\.\d+[eE][+-]?\d+\.\d+)",}

    def __init__(self):
        self.handlers = {t: [] for t in Parser.TYPES}

    def Register(self, t, pattern, handler):
        if t not in Parser.TYPES:
            raise Exception(t + " is unknown type")
        for before, after in Parser.TYPE_PATTERN.iteritems():
            pattern = pattern.replace(before, after)
        if not pattern.startswith("^"):
            pattern = r"^" + pattern
        if not pattern.endswith("$"):
            pattern = pattern + r"$"
        self.handlers[t].append((re.compile(pattern), handler))

    def Parse(self, t, v):
        for pattern in self.handlers[t]:
            m = pattern[0].match(v)
            if m:
                arg = [Parser.TYPE_FUNC[t](s) for s in m.groups()]
                return pattern[1](*arg)
        raise Exception("No matching pattern for {}".format(v))

    def Generate(self, filename):
        with open(filename) as f:
            # TODO load json
            for param in self.GenerateImpl(yaml.load(f)):
                yield param

    def GenerateImpl(self, dic):
        keys = []
        values = []     # variable name -> list of values

        for key, val in dic.iteritems():
            keys.append(key)
            if isinstance(val, str):
                values.append([val])
                if "@" in val:
                    i = val.find("@")
                    typ = val[i+1:].strip()
                    exp = val[:i].strip()
                    print exp, "@", typ
                    values.append(exp)
                    # values.append(self.Parse(typ, exp))
                else:
                    values.append([val])
            else:
                values.append([val])
        #
        # for k, v in dic.iteritems():
        #     if "t" in v and "v" in v:
        #         typ = v["t"]    # type
        #         val = v["v"]    # value configuration
        #
        #         keys.append(k)
        #         if isinstance(val, int) or isinstance(val, float):
        #             values.append([val])
        #         elif typ == "str":
        #             if isinstance(val, str):
        #                 values.append([str(val)])
        #             elif isinstance(val, unicode):
        #                 values.append([unicode(val)])
        #         else:
        #             try:
        #                 values.append(self.Parse(v["t"], v["v"]))
        #             except Exception as e:
        #                 print "Error at '{}':".format(k), str(e)
        #                 sys.exit(1)
        #     else:
        #         if self.IsNumber(v):
        #             values.append([v])
        #         elif isinstance(v, str):
        #             


        # Loop for all the possible combinations among values
        for product in itertools.product(*values):
            yield {k: product[i] for i, k in enumerate(keys)}


def CreateParser(args_list):
    parser = Parser()
    for args in args_list:
        parser.Register(*args)
    return parser
