# ======================================================================================================================
#   Exercicio 2
# ----------------------------------------------------------------------------------------------------------------------
#   Autor: Rafael Hideo Toyomoto
#   29/08/2018
# ======================================================================================================================

import numpy as np

from math import exp

import matplotlib.pyplot as plt
from base.relation import Relation2D, RelationUnion, RelationIntersection

# ----------------------------------------------------------------------------------------------------------------------


class R1Function(Relation2D):
    # R1: x e y sao similares
    def __init__(self, k=6):
        Relation2D.__init__(self)
        self.k = k if k > 0 else 1

    def calc(self, x, y):
        if abs(x - y) <= 5:
            return exp((-((x-y)**2))/self.k)
        else:
            return 0


class R2Function(Relation2D):
    # R2: x e y sao aproximadamente iguais
    def __init__(self, k=2):
        Relation2D.__init__(self)
        self.k = k if k > 0 else 1

    def calc(self, x, y):
        return exp(abs(x-y)/self.k)


class R3Function(Relation2D):
    # R3: y eh muito maior que x
    def __init__(self, beta=1):
        Relation2D.__init__(self)
        self.beta = beta if beta > 0 else 1

    def calc(self, x, y):
        if y > x:
            return (y-x)/(x+y+2)
        else:
            return 0


class Ex2Script(object):
    def __init__(self):
        self.sample = 50

    def run_func(self, func):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        ax.clear()

        x = np.linspace(0, 100, self.sample)
        y = np.linspace(0, 100, self.sample)
        X, Y = np.meshgrid(x, y)
        zs = np.array([func.calc(x, y) for x, y in zip(np.ravel(X), np.ravel(Y))])
        Z = zs.reshape(X.shape)

        ax.plot_surface(X, Y, Z)
        ax.set_xlabel('X Label')
        ax.set_ylabel('Y Label')
        ax.set_zlabel('Z Label')

        plt.show()

    def run_func_1(self):
        self.run_func(R1Function())

    def run_func_2(self):
        self.run_func(R2Function())

    def run_func_3(self):
        self.run_func(R3Function())

    def run_func_ex2(self):
        self.run_func(RelationUnion(R1Function(), R3Function()))
        self.run_func(RelationIntersection(R1Function(), R3Function()))

# ======================================================================================================================
