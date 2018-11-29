# ======================================================================================================================
#   Execucao do projeto 4
# ----------------------------------------------------------------------------------------------------------------------
#   Autor: Rafael Hideo Toyomoto
#   28/11/2018
# ======================================================================================================================


import numpy as np

from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from fuzzychan.base import FuzzyUniverse
from fuzzychan.function import MembershipFunc
from fuzzychan.classifier.wangmendel import WangMendelClassifier

# ======================================================================================================================


def func1():
    pass


def func2():
    pass


def main():
    sample = 1000

    x1 = FuzzyUniverse("Attr1", 0, 100, sample)
    x1["A1"] = MembershipFunc(0, 0, 40)
    x1["A2"] = MembershipFunc(20, 50, 80)
    x1["A3"] = MembershipFunc(60, 100, 100)

    x2 = FuzzyUniverse("Attr2", 0, 100, sample)
    x2["B1"] = MembershipFunc(0, 0, 40)
    x2["B2"] = MembershipFunc(20, 50, 80)
    x2["B3"] = MembershipFunc(60, 100, 100)

    dataframe = [
        {'x1': 17, 'x2': 24, 'c': 'C1'},
        {'x1': 21, 'x2': 42, 'c': 'C1'},
        {'x1': 69, 'x2': 74, 'c': 'C2'},
        {'x1': 10, 'x2': 86, 'c': 'C1'},
        {'x1': 12, 'x2': 84, 'c': 'C2'}
    ]

    wmcls = WangMendelClassifier(x1=x1, x2=x2)
    wmcls.train(dataframe, out_label='c')
    print(wmcls(x1=8, x2=15))

# ======================================================================================================================
