# ======================================================================================================================
#   Classes de Funcoes de Pertinencia
# ----------------------------------------------------------------------------------------------------------------------
#   Autor: Rafael Hideo Toyomoto
#   10/08/2018
# ======================================================================================================================

import abc

# ----------------------------------------------------------------------------------------------------------------------


class Relation(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, color=None):
        self.color = color

# ----------------------------------------------------------------------------------------------------------------------


class Relation2D(Relation):
    def __init__(self):
        Relation.__init__(self)

    @abc.abstractmethod
    def calc(self, x, y):
        pass

# ----------------------------------------------------------------------------------------------------------------------


class Relation2DOperation(Relation2D):
    def __init__(self):
        Relation2D.__init__(self)
        self.funcs = []

    def add_func(self, func):
        self.funcs.append(func)
        return self

# ----------------------------------------------------------------------------------------------------------------------


class RelationUnion(Relation2DOperation):
    def __init__(self, func1, func2):
        Relation2DOperation.__init__(self)
        self.add_func(func1)
        self.add_func(func2)

    def calc(self, x, y):
        return max([func.calc(x, y) for func in self.funcs])

# ----------------------------------------------------------------------------------------------------------------------


class RelationIntersection(Relation2DOperation):
    def __init__(self, func1, func2):
        Relation2DOperation.__init__(self)
        self.add_func(func1)
        self.add_func(func2)

    def calc(self, x, y):
        return min([func.calc(x, y) for func in self.funcs])

# ======================================================================================================================
