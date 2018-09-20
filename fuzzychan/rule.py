# ==================================================================================================================== #
#   Author: Rafael Hideo Toyomoto                                                                                      #
#   Created: 19/09/2018                                                                                                #
# ==================================================================================================================== #

import math
from enum import Enum

import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from fuzzychan.base import FuzzySet
from fuzzychan.relation import FuzzyRelation


# ==================================================================================================================== #
#   EnumRelation
# -------------------------------------------------------------------------------------------------------------------- #
#   Enum de Normas implementadas
# ==================================================================================================================== #


class EnumRule(Enum):
    ConjMin = 'conj-min'
    ConjPro = 'conj-pro'
    DisjMax = 'disj'
    ImplLSWMin = 'impl-lucasiewicz-min'
    ImplLSWPro = 'impl-lucasiewicz-pro'
    ImplGodel = 'impl-godel'
    ImplKleene = 'impl-kleene'
    ImplZadeh = 'impl-zadeh'


# ==================================================================================================================== #
#   Relation
# -------------------------------------------------------------------------------------------------------------------- #
#   Classe que representa relacoes fuzzy
# ==================================================================================================================== #


class FuzzyRule(object):

    def __init__(self, antecedent, consequent, kind=EnumRule.ConjMin, *args, **kwargs):
        """
        Regra Fuzzy
        :param antecedent:
        :type antecedent: FuzzyRelation
        :param consequent:
        :type consequent: FuzzyRelation
        :param kind:
        :type kind: str|EnumRule
        :param args:
        :param kwargs:
        """

        # Tipo que sera utilizado para relacionar os conjuntos
        self._kind = str(kind)
        # Lista dos conjuntos fuzzy da relacao
        self._antecedent = antecedent
        self._consequent = consequent

    def __call__(self, *args, **kwargs):

        # Get 'kind'
        kind = self._kind

        # Get values of antecedent and consequent
        a = args[0] if len(args) > 1 else self._antecedent(*args, **kwargs)
        b = args[1] if len(args) > 1 else self._consequent(*args, **kwargs)

        # Computar a regra para a coordenada passada
        if kind == EnumRule.ConjMin:
            return min(a, b)
        if kind == EnumRule.ConjPro:
            return a * b
        if kind == EnumRule.DisjMax:
            return max(a, b)
        if kind == EnumRule.ImplLSWMin:
            return min(1, min(1 - a, b))
        if kind == EnumRule.ImplLSWPro:
            return min(1, (1 - a) * b)
        if kind == EnumRule.ImplGodel:
            return 1 if a <= b else b
        if kind == EnumRule.ImplKleene:
            return max(1 - a, b)
        if kind == EnumRule.ImplZadeh:
            return max(1 - a, min(a, b))
        return 0

    def matrix(self, complete=False):

        # Gerar as matrizes para regra
        r_a = self._antecedent.matrix(complete=True)
        r_b = self._consequent.matrix(complete=True)

        # Pegar apenas o resultado
        a = r_a[len(r_a) - 1]
        b = r_b[len(r_b) - 1]

        dim_a = self._antecedent.dimension() + 1
        dim_b = self._consequent.dimension() + 1

        # Diferenca de dimensoes ???
        diff = abs(dim_a - dim_b)
        targ = max(dim_a, dim_b)
        dim = len(a)

        if diff > 0:
            # Parametros para o numpy.tile()
            fix = [dim if diff > iter else 1 for iter in range(0, targ)]

            # Expansao cilindrica
            if dim_a > dim_b:
                prod_cart = np.array(a).copy()
                b = np.tile(b, fix)
            else:
                prod_cart = np.array(b).copy()
                a = np.tile(a, fix)
        else:
            prod_cart = np.array(a).copy()

        A, B = np.meshgrid(a, b)

        results = []
        results = np.array([self(val_a, val_b) for (val_a, val_b) in zip(np.ravel(A), np.ravel(B))]).reshape(
            [dim for iter in range(0, targ + 1)])

        if complete:
            prod_cart[len(prod_cart) - 1] = results
            return prod_cart
        return results

    def plot(self, vars=None, figure=None):
        """
        Plotar o universo pela biblioteca 'matplotlib'
        :param vars: Filtro do plot
        :type vars: str|list
        :param figure:
        :type figure: Figure
        :return:
        """
        if figure is None:
            figure = plt.figure()

        # Plot 2D?
        if len(self._funcs) == 1:
            x, y = self.matrix(complete=True)
            axes = figure.add_subplot(111)
            axes.plot(x, y)

        # Plot 3D?
        elif len(self._funcs) >= 2:
            coord = self.matrix(complete=True)
            axes = figure.add_subplot(111, projection='3d')
            axes.plot_surface(coord[0], coord[1], coord[len(coord) - 1])

        # Invalid
        else:
            return False

        axes.legend()
        return axes

    def alpha_cut(self, alpha, height=1):

        def explore_array(param):
            if isinstance(param, list):
                if isinstance(param[0], list):
                    return [explore_array(param)]
                else:
                    return [explore_array(item) for item in param]
            else:
                return param

        # TODO: tirar alfa corte da relacao (discreto)
        pass

    def support(self):
        # TODO: tirar o conjunto suporte (discreto/continuo)
        pass

# ==================================================================================================================== #
