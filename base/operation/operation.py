# ======================================================================================================================
#   Classes de Funcoes de Pertinencia
# ----------------------------------------------------------------------------------------------------------------------
#   Autor: Rafael Hideo Toyomoto
#   18/08/2018
# ======================================================================================================================

import abc
from base.function import Function

# ----------------------------------------------------------------------------------------------------------------------


class Operator(Function):
    def __init__(self, color=None):
        Function.__init__(self, color=color)


# ----------------------------------------------------------------------------------------------------------------------


class StandardOperator(Operator):
    def __init__(self, color=None):
        Operator.__init__(self, color=color)


# ----------------------------------------------------------------------------------------------------------------------


class NormOperator(Operator):
    def __init__(self, func_x, func_y, color=None):
        Operator.__init__(self, color=color)
        self.func_x = func_x
        self.func_y = func_y

    def calc(self, x):
        return self.calc_z(x, x)

    @abc.abstractmethod
    def calc_z(self, x, y):
        pass

# ======================================================================================================================
