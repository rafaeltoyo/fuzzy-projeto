# ======================================================================================================================
#   Classe de uma Funcao de Pertinencia
# ----------------------------------------------------------------------------------------------------------------------
#   Autor: Rafael Hideo Toyomoto
#   18/08/2018
# ======================================================================================================================

import numpy as np
from base.function import Function


# ----------------------------------------------------------------------------------------------------------------------

class PlotOperation(object):
    def __init__(self, xi, xf, sample):
        self.functions = {}
        self.xi = xi
        self.xf = xf
        self.sample = sample
        self.points = np.linspace(xi, xf, sample)

    def add_func(self, label, func):
        if label == "":
            raise TypeError("PlotOperation.add_func(): parameter label cannot be null")
        if not isinstance(func, Function):
            raise TypeError("PlotOperation.add_func(): parameter func must be instance of MembershipFunction")
        self.functions[label] = func
        return self

    def remove_func(self, label):
        try:
            self.functions.pop(label)
        except IndexError as e:
            raise e
        return self

    def get_func(self, label):
        try:
            return self.functions[label]
        except IndexError as e:
            raise e

    def clear(self):
        self.functions = {}

    def plot(self, plot):
        for key in self.functions:
            f = self.functions[key].gen(self.points)
            plot.plot(self.points, f, label=key)
            plot.fill_between(self.points, f, np.zeros(self.sample), alpha=.2)

# ======================================================================================================================
