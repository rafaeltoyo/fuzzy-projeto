# ==================================================================================================================== #
#   Author: Rafael Hideo Toyomoto                                                                                      #
#   Created: 15/09/2018                                                                                                #
# ==================================================================================================================== #

from numpy import linspace
from matplotlib import pyplot as plt

from myfuzzy.function import MembershipFunc


# ==================================================================================================================== #
#   Domain
# -------------------------------------------------------------------------------------------------------------------- #
#   Classe que representa um dominio com ponto inicial, ponto final e taxa de amostragem (discretizacao)
# ==================================================================================================================== #


class Domain(object):

    def __init__(self, label="", xi=0.0, xf=10.0, sample=100):
        """
        Dominio de um universo Fuzzy
        :param label: Nome do universo
        :type label: str
        :param xi: ponto inicial
        :type xi: int|float
        :param xf: ponto final
        :type xf: int|float
        :param sample: taxa de discretizacao
        :type sample: int
        """
        self.id = label + "-" + str(xi) + "-" + str(xf) + "-" + str(sample)
        self.points = linspace(float(xi), float(xf), int(sample))

    def __eq__(self, other):
        if isinstance(other, Domain):
            return self.id == other.id
        return False

    def __iter__(self):
        for x in self.points:
            yield x

# ==================================================================================================================== #
#   FuzzyUniverse
# -------------------------------------------------------------------------------------------------------------------- #
#   Classe que representa um universo fuzzy
# ==================================================================================================================== #


class FuzzyUniverse(dict):

    def __init__(self, label, xi, xf, sample, **kwargs):
        """
        Universo Fuzzy (discretizado)
        :param label: Nome do universo
        :type label: str
        :param xi: ponto inicial
        :type xi: int|float
        :param xf: ponto final
        :type xf: int|float
        :param sample: taxa de discretizacao
        :type sample: int
        :param kwargs: Criar conjuntos fuzzy no universo
        """
        super(FuzzyUniverse, self).__init__(**kwargs)

        # salvar o nome
        self.name = str(label)

        # criar o dominio dessa variavel
        self.domain = Domain(label=label, xi=xi, xf=xf, sample=sample)

    def __setitem__(self, key, value):
        """
        Criar um termo nesse universo
        :param key:
        :type key: str
        :param value:
        :type value: MembershipFunc|FuzzySet
        :return:
        """
        if isinstance(value, MembershipFunc):
            value = FuzzySet(self, func=value)
        if not isinstance(value, FuzzySet):
            raise TypeError("FuzzyUniverse dict only accept instance of 'FuzzySet'")
        super(FuzzyUniverse, self).__setitem__(key, value)

    def plot(self, vars=None, figure=None):
        """
        Plotar o universo pela biblioteca 'matplotlib'
        :param vars:
        :param figure:
        :return:
        """
        if figure is None:
            figure = plt.figure()

        axes = figure.add_subplot(111)

        for label in self.__iter__():
            if not isinstance(vars, list) or label in vars:
                axes.plot(self.domain.points, self[label].gen(), label=label)

        axes.legend()
        return axes


# ==================================================================================================================== #
#   FuzzySet
# -------------------------------------------------------------------------------------------------------------------- #
#   Classe que representa um conjunto fuzzy
# ==================================================================================================================== #


class FuzzySet(object):

    def __init__(self, universe, *args, **kwargs):
        """
        Conjunto Fuzzy
        :param universe: Universo desse conjunto
        :type universe: FuzzyUniverse
        :param args:
        :param kwargs:
        """
        if not isinstance(universe, FuzzyUniverse):
            raise TypeError("FuzzySet: parameter 'universe' must be instance of 'FuzzyUniverse'")
        self._universe = universe

        if 'func' in kwargs.keys():
            self.func = kwargs['func']
        else:
            self.func = MembershipFunc(*args, **kwargs)

    def gen(self):
        return [self.func(x=x) for x in self._universe.domain]

# ==================================================================================================================== #
