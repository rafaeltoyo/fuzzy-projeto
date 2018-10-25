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
from fuzzychan.inference.sugeno import SugenoModel, EnumSugenoDfzz, EnumSugenoAggr, EnumSugenoOper, EnumSugenoImpl, SugenoRule


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


def main1():
    x1 = func_x1(SAMPLE)
    x2 = func_x2(SAMPLE)
    y = func_y(SAMPLE)

    mamdani = MamdaniModel(
        oper=EnumMamdaniOper.Prod,
        impl=EnumMamdaniImpl.ConjPro,
        aggr=EnumMamdaniAggr.Max,
        dfzz=EnumMamdaniDfzz.MoM,
        x1=x1,
        x2=x2,
        out=y)
    mamdani.create_rule(x1='PS', x2='SM', out='MC')
    mamdani.create_rule(x1='PS', x2='MM', out='M')
    mamdani.create_rule(x1='PS', x2='GM', out='L')
    mamdani.create_rule(x1='MS', x2='SM', out='C')
    mamdani.create_rule(x1='MS', x2='MM', out='M')
    mamdani.create_rule(x1='MS', x2='GM', out='L')
    mamdani.create_rule(x1='GS', x2='SM', out='M')
    mamdani.create_rule(x1='GS', x2='MM', out='L')
    mamdani.create_rule(x1='GS', x2='GM', out='ML')

    out = np.array([[int(i), int(j), mamdani(x1=i, x2=j)] for i in range(0, 110, 10) for j in range(0, 110, 10)])
    np.savetxt("mamdani-mom.csv", out, fmt=['%d', '%d', '%.5f'], delimiter=";")


def main2():
    x1 = func_x1(SAMPLE)
    x2 = func_x2(SAMPLE)
    y = func_y(SAMPLE)

    sugeno = SugenoModel(
        oper=EnumSugenoOper.Prod,
        dfzz=EnumSugenoDfzz.Avg,
        x1=x1,
        x2=x2,
        out=y)
    sugeno.create_rule(x1='PS', x2='SM', out=0.5)
    sugeno.create_rule(x1='PS', x2='MM', out=23)
    sugeno.create_rule(x1='PS', x2='GM', out=42)
    sugeno.create_rule(x1='MS', x2='SM', out=10)
    sugeno.create_rule(x1='MS', x2='MM', out=26)
    sugeno.create_rule(x1='MS', x2='GM', out=42)
    sugeno.create_rule(x1='GS', x2='SM', out=27)
    sugeno.create_rule(x1='GS', x2='MM', out=41)
    sugeno.create_rule(x1='GS', x2='GM', out=60)

    out = np.array([[int(i), int(j), sugeno(x1=i, x2=j)] for i in range(0, 110, 10) for j in range(0, 110, 10)])
    np.savetxt("sugeno-pro.csv", out, fmt=['%d', '%d', '%.5f'], delimiter=";")


if __name__ == "__main__":
    main2()

# ======================================================================================================================
