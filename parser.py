import itertools
import re
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
               r"|[+-]?\d+\.\d+[eE][+-]?\d+\.\d+)"}

    def __init__(self):
        self.handlers = {t: [] for t in Parser.TYPES}

    def Register(self, t, pattern, handler):
        """Add pair of pattern and handler."""
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
        """Parses with type specification."""
        for pattern, handler in self.handlers[t]:
            m = pattern.match(v)
            if m:
                arg = [Parser.TYPE_FUNC[t](s) for s in m.groups()]
                return handler(*arg)
        raise Exception("No matching pattern for {}".format(v))

    def ParseByGuess(self, val):
        """Parses without type specification."""
        for typ in self.TYPES:
            try:
                return self.Parse(typ, val)
            except:
                pass
        return [val]

    def ReadFile(self, filename):
        res = {}
        with open(filename) as f:
            res = yaml.load(f)
        return res

    def Generate(self, filename):
        """Yields one of parameter sets from filename."""
        keys, values = self.ParseFile(filename)
        # Loop for all the possible combinations among values
        for product in itertools.product(*values):
            yield {k: product[i] for i, k in enumerate(keys)}

    def ParseFile(self, filename):
        content = self.ReadFile(filename)
        return self.ParseDict(content)

    def ParseDict(self, dic):
        """Returns pair of keys and values."""
        keys = []
        values = []

        for key, val in dic.iteritems():
            keys.append(key)
            if isinstance(val, str):
                vs = self.ParseByGuess(val)
            elif isinstance(val, list):
                vs = []
                for v in val:
                    vs.extend(self.ParseByGuess(v))
            else:
                vs = [val]
            values.append(vs)
        return (keys, values)


def CreateParser(args_list):
    """Registers handlers and returns parser.

    Args:
        args_list: list of (pattern, handler)
    """
    parser = Parser()
    for args in args_list:
        parser.Register(*args)
    return parser
