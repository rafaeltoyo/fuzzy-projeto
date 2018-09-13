# ==================================================================================================================== #
#   Author: Rafael Hideo Toyomoto                                                                                      #
#   Created: 12/09/2018                                                                                                #
# ==================================================================================================================== #

from matplotlib import pyplot as plt
from numpy import linspace

from myfuzzy.continuous.function import Function

# ==================================================================================================================== #
#   Domain
# -------------------------------------------------------------------------------------------------------------------- #
#   Classe que representa um dominio com ponto inicial, ponto final e taxa de amostragem (discretizacao)
# ==================================================================================================================== #


class Domain(object):

    def __init__(self, label="", xi=0, xf=10, sample=100):
        self.id = label + "-" + str(xi) + "-" + str(xf) + "-" + str(sample)
        self.points = linspace(xi, xf, sample)

    def __eq__(self, other):
        if isinstance(other, Domain):
            return self.id == other.id
        return False

# ==================================================================================================================== #
#   Variable
# -------------------------------------------------------------------------------------------------------------------- #
#   Classe que representa uma variavel fuzzy
# ==================================================================================================================== #


class Variable(dict):
    __cont = 0

    def __init__(self, label, xi, xf, sample, *arg, **kw):
        super(Variable, self).__init__(*arg, **kw)

        # Verificar se o Label esta correto
        if isinstance(label, str) and label != "":
            self.label = label
        else:
            raise TypeError("Variable: label must be not empty string")

        # criar o dominio dessa variavel
        self.domain = Domain(label=label, xi=xi, xf=xf, sample=sample)

    def __setitem__(self, key, value):
        # Verificar se o value eh um termo fuzzy
        if isinstance(value, Term):
            super(Variable, self).__setitem__(key, value)
            return self
        # Compatibilidade
        if isinstance(value, Function):
            super(Variable, self).__setitem__(key, Term(self, value))
            return self

        raise TypeError("Variable.__setitem__(): value must be instance of Term")

    def plot(self, vars=None, figure=None):
        if figure is None:
            figure = plt.figure()

        axes = figure.add_subplot(111)

        for label in self.__iter__():
            if not isinstance(vars, list) or label in vars:
                axes.plot(self.domain.points, self[label].func.gen(self.domain.points), label=label)

        axes.legend()
        return axes

# ==================================================================================================================== #
#   Term
# -------------------------------------------------------------------------------------------------------------------- #
#   Classe que representa um termo de uma variavel fuzzy
# ==================================================================================================================== #


class Term(object):

    def __init__(self, variable, func):
        self.variable = variable
        if not isinstance(func, Function):
            raise TypeError("Term: values must be list")
        self.func = func

# ======================================================================================================================
