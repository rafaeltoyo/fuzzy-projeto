# ======================================================================================================================
#   Operadores para variaveis de mesmo dominio
# ----------------------------------------------------------------------------------------------------------------------
#   Autor: Rafael Hideo Toyomoto
#   18/08/2018
# ======================================================================================================================

from base.operation import StandardOperator as StdOperator


# ----------------------------------------------------------------------------------------------------------------------

class StdSingleOperator(StdOperator):
    def __init__(self, func, color=None):
        StdOperator.__init__(self, color=color)
        self.function = func


# ----------------------------------------------------------------------------------------------------------------------

class StdMultipleOperator(StdOperator):
    def __init__(self, color=None):
        StdOperator.__init__(self, color=color)
        self.functions = {}

    def add_func(self, id, func):
        self.functions[id] = func

    def get_func(self, id):
        return self.functions[id]


# ----------------------------------------------------------------------------------------------------------------------

class StdConcentration(StdSingleOperator):
    def __init__(self, p, color=None):
        # if p > 1 -> Concentration
        # if 0 > p > 1 -> Dilation
        StdSingleOperator.__init__(self, color=color)
        self.p = p

    def calc(self, x):
        return self.function.calc(x) ** self.p


# ----------------------------------------------------------------------------------------------------------------------

class StdIntensification(StdSingleOperator):
    def __init__(self, p, color=None):
        StdSingleOperator.__init__(self, color=color)
        self.p = p

    def calc(self, x):
        value = self.function.calc(x)
        if value <= 0.5:
            return (2 ** (self.p - 1)) * (value ** self.p)
        else:
            return 1 - (2 ** (self.p - 1)) * ((1 - value) ** self.p)


# ----------------------------------------------------------------------------------------------------------------------

class StdFuzzification(StdSingleOperator):
    def __init__(self, color=None):
        StdSingleOperator.__init__(self, color=color)

    def calc(self, x):
        value = self.function.calc(x)
        if value <= 0.5:
            return (value / 2) ** 0.5
        else:
            return 1 - (((1 - value)/2) ** 2)


# ----------------------------------------------------------------------------------------------------------------------

class StdComplement(StdSingleOperator):
    def calc(self, x):
        return 1 - self.function.calc(x)


# ----------------------------------------------------------------------------------------------------------------------

class StdUnion(StdMultipleOperator):
    def calc(self, x):
        return max(self.functions[func].calc(x) for func in self.functions)


# ----------------------------------------------------------------------------------------------------------------------

class StdIntersection(StdMultipleOperator):
    def calc(self, x):
        return min(self.functions[func].calc(x) for func in self.functions)

# ======================================================================================================================
