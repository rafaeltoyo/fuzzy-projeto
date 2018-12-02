# ======================================================================================================================
#   Execucao do projeto 4
# ----------------------------------------------------------------------------------------------------------------------
#   Autor: Rafael Hideo Toyomoto
#   28/11/2018
# ======================================================================================================================


import numpy as np
import csv
import random
import pandas as pd
import seaborn

from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from fuzzychan.base import FuzzyUniverse
from fuzzychan.function import MembershipFunc
from fuzzychan.classifier.wangmendel import WangMendelClassifier

from exercicios.pp4_dataset_gen import DatasetGenerator

# ======================================================================================================================


def test_dataframe(filename='train.csv',ndim=2, ncls=3, minelem=10, maxelem=50, spreadv=30, minv=0, maxv=100):
    # Gerar o arquivo
    with open(str(filename), 'w+') as csvfile:

        dim = []

        writer = csv.writer(csvfile)

        for i in range(ndim):
            dim.append("x{}".format(i+1))

        dim.append('cls')
        writer.writerow(dim)
        dim.remove('cls')

        # Para cada classe ...
        for i in range(ncls):
            # Centroide da classe
            centroid = {}
            for label in dim:
                centroid[label] = random.uniform(minv, maxv)


            # Para cada elemento novo ...
            for j in range(random.randrange(minelem, maxelem)):

                data = {}
                for label in dim:
                    data[label] = (centroid[label] + spreadv * random.random())
                    while data[label] < minv or data[label] > maxv:
                        if data[label] < minv:
                            data[label] = minv + (minv - data[label])
                        if data[label] > maxv:
                            data[label] = maxv - (data[label] - maxv)

                v = [data[label] for label in data]
                v.append('C' + str(i+1))
                writer.writerow(v)


def func1(sample):
    x1 = FuzzyUniverse("Attr1", 0, 100, sample)
    x1["A1"] = MembershipFunc(0, 0, 40)
    x1["A2"] = MembershipFunc(20, 50, 80)
    x1["A3"] = MembershipFunc(60, 100, 100)
    return x1


def func2(sample):
    x2 = FuzzyUniverse("Attr2", 0, 100, sample)
    x2["B1"] = MembershipFunc(0, 0, 40)
    x2["B2"] = MembershipFunc(20, 50, 80)
    x2["B3"] = MembershipFunc(60, 100, 100)
    return x2


def main():
    """
    Main
    :return:
    """

    """ Taxa de amostragem (Discretizacao) para as funcoes de pertinencia """
    sample = 1000

    """ Universos dos dados """
    x1 = func1(sample)
    x2 = func2(sample)

    """ Gerar/Abrir arquivo input de treino """
    filename = "train6.csv"

    #dg = DatasetGenerator("cls", x1=x1, x2=x2)
    #dg.add_group(name="C1", nelem=70, spread=0.47)
    #dg.add_group(name="C2", nelem=40, spread=0.35)
    #dg.add_group(name="C3", nelem=100, spread=0.6)
    #dg.generate(filename)

    #test_dataframe(filename='dataset/train1.csv', ncls=5, spreadv=40)
    df = pd.read_csv("dataset/" + filename)

    """ Gerar figura para visualizar os dados """
    fig = plt.figure()
    axes = fig.add_subplot(111)

    # Scatterplot dos dados de treino
    seaborn.scatterplot('x1', 'x2', hue='cls', data=df, ax=axes)

    n1min = [0, 0]
    n1mid = [0, 0]
    n1max = [40, 40]
    n2min = [20, 20]
    n2mid = [50, 50]
    n2max = [80, 80]
    n3min = [60, 60]
    n3mid = [100, 100]
    n3max = [100, 100]
    interval = [0, 100]

    # X1/A1
    plt.plot(interval, n1min, interval, n1max, color="blue")
    axes.fill_between(interval, n1min, n1max, where=n1max >= n1min, facecolor='blue', alpha=0.2, interpolate=True)
    # X1/A2
    plt.plot(interval, n2min, interval, n2max, color="red")
    axes.fill_between(interval, n2min, n2max, where=n2max >= n2min, facecolor='red', alpha=0.2, interpolate=True)
    # X1/A3
    plt.plot(interval, n3min, interval, n3max, color="green")
    axes.fill_between(interval, n3min, n3max, where=n3max >= n3min, facecolor='green', alpha=0.2, interpolate=True)

    # X1/A1
    plt.plot(n1min, interval, n1max, interval, color="blue")
    axes.fill_between([0, 40], [0, 0], [100, 100], facecolor='blue', alpha=0.2, interpolate=True)
    # X1/A2
    plt.plot(n2min, interval, n2max, interval, color="red")
    axes.fill_between([20, 80], [0, 0], [100, 100], facecolor='red', alpha=0.2, interpolate=True)
    # X1/A3
    plt.plot(n3min, interval, n3max, interval, color="green")
    axes.fill_between([60, 100], [0, 0], [100, 100], facecolor='green', alpha=0.2, interpolate=True)

    # Gerar modelo
    wmcls = WangMendelClassifier(x1=x1, x2=x2)
    wmcls.train(df.to_dict('records'), out_label='cls', debug=True)

    wmcls.print_status()

    plt.show()

# ======================================================================================================================
