import numpy as np


def ArangeNoStep(start, stop):
    return np.arange(start, stop+1).tolist()


def Arange(start, step, stop):
    return np.arange(start, stop, step).tolist()


def Linspace(start, stop, num):
    return np.linspace(start, stop, num).tolist()
