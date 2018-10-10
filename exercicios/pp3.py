# ======================================================================================================================
#   Execucao do projeto 3 - Maquina de Lavar
# ----------------------------------------------------------------------------------------------------------------------
#   Autor: Rafael Hideo Toyomoto
#   07/10/2018
# ======================================================================================================================


import numpy as np

from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from exercicios.mymenu import Menu

from fuzzychan.base import FuzzyUniverse, MembershipFunc
from fuzzychan.inference.mamdani import MamdaniModel, EnumMamdaniDfzz, EnumMamdaniAggr, EnumMamdaniOper, EnumMamdaniImpl


# ======================================================================================================================


SAMPLE = 200


def func_x1(sample):

    f = FuzzyUniverse("Sujeira", 0, 100, sample)
    f["PS"] = MembershipFunc(0, 0, 50)
    f["MS"] = MembershipFunc(0, 50, 100)
    f["GS"] = MembershipFunc(50, 100, 100)
    return f


def func_x2(sample):

    f = FuzzyUniverse("Mancha", 0, 100, sample)
    f["SM"] = MembershipFunc(0, 0, 50)
    f["MM"] = MembershipFunc(0, 50, 100)
    f["GM"] = MembershipFunc(50, 100, 100)
    return f


def func_y(sample):

    f = FuzzyUniverse("TempoLavagem", 0, 60, sample)
    f["MC"] = MembershipFunc(0, 0, 10)
    f["C"] = MembershipFunc(0, 10, 25)
    f["M"] = MembershipFunc(10, 25, 40)
    f["L"] = MembershipFunc(25, 40, 60)
    f["ML"] = MembershipFunc(40, 60, 60)
    return f


# ======================================================================================================================


def main():
    x1 = func_x1(SAMPLE)
    x2 = func_x2(SAMPLE)
    y = func_y(SAMPLE)

    model = MamdaniModel(
        oper=EnumMamdaniOper.Prod,
        impl=EnumMamdaniImpl.ConjPro,
        aggr=EnumMamdaniAggr.Max,
        dfzz=EnumMamdaniDfzz.MoM,
        x1=x1,
        x2=x2,
        out=y)
    model.create_rule(x1='PS', x2='SM', out='MC')
    model.create_rule(x1='PS', x2='MM', out='M')
    model.create_rule(x1='PS', x2='GM', out='L')
    model.create_rule(x1='MS', x2='SM', out='C')
    model.create_rule(x1='MS', x2='MM', out='M')
    model.create_rule(x1='MS', x2='GM', out='L')
    model.create_rule(x1='GS', x2='SM', out='M')
    model.create_rule(x1='GS', x2='MM', out='L')
    model.create_rule(x1='GS', x2='GM', out='ML')

    out = np.array([[int(i), int(j), model(x1=i, x2=j)] for i in range(0, 110, 10) for j in range(0, 110, 10)])
    np.savetxt("mamdani-mom.csv", out, fmt=['%d', '%d', '%.5f'], delimiter=";")

if __name__ == "__main__":
    main()

# ======================================================================================================================
