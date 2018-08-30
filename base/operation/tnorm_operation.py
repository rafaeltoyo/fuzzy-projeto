# ======================================================================================================================
#   Operadores para variaveis de mesmo dominio
# ----------------------------------------------------------------------------------------------------------------------
#   Autor: Rafael Hideo Toyomoto
#   22/08/2018
# ======================================================================================================================

from base.operation.operation import NormOperator

# ----------------------------------------------------------------------------------------------------------------------


class TNormOperator(NormOperator):
    def __init__(self, func_x, func_y, color=None):
        NormOperator.__init__(self, func_x, func_y, color=color)

# ----------------------------------------------------------------------------------------------------------------------


class TNorm1(TNormOperator):
    def __init__(self, func_x, func_y, pt):
        TNormOperator.__init__(self, func_x, func_y)
        self.pt = pt

    def calc_z(self, x, y):
        a = self.func_x.calc(x)
        b = self.func_y.calc(y)
        return a * b / (self.pt + (1-self.pt)*(a+b-a*b))

# ----------------------------------------------------------------------------------------------------------------------


class TNorm9(TNormOperator):
    def calc_z(self, x, y):
        a = self.func_x.calc(x)
        b = self.func_y.calc(y)
        return min(a, b)

# ======================================================================================================================
