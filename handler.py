
def IntRange(start, step, stop):
    return range(start, stop+1, step)

def IntRangeNoStep(start, stop):
    return range(start, stop+1)

def FloatRange(start, step, stop):
    N = int(abs((start - stop)/step)) + 1
    return [float(start) + step * i for i in xrange(N)]
