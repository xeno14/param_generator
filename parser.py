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

    def Generate(self, filename):
        """Yields one of parameter sets from filename."""
        with open(filename) as f:
            # TODO load json?
            for param in self.GenerateImpl(yaml.load(f)):
                yield param

    def GenerateImpl(self, dic):
        """Yields one of parameter sets from dictionary."""
        keys = []
        values = []     # variable name -> list of values

        for key, val in dic.iteritems():
            keys.append(key)
            if isinstance(val, str):
                values.append(self.ParseByGuess(val))
            else:
                values.append([val])

        # Loop for all the possible combinations among values
        for product in itertools.product(*values):
            yield {k: product[i] for i, k in enumerate(keys)}


def CreateParser(args_list):
    """Registers handlers and returns parser.

    Args:
        args_list: list of (pattern, handler)
    """
    parser = Parser()
    for args in args_list:
        parser.Register(*args)
    return parser
