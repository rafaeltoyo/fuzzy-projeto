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
    #test_dataframe(filename='exercicios/train1.csv', ncls=5, spreadv=40)
    df = pd.read_csv('exercicios/train.csv')
    seaborn.scatterplot(df['x1'], df['x2'], hue='cls', data=df)
    plt.show()

    sample = 1000

    x1 = func1(sample)
    x2 = func2(sample)

    wmcls = WangMendelClassifier(x1=x1, x2=x2)
    wmcls.train(df.to_dict('records'), out_label='cls')
    print(wmcls(x1=8, x2=15))

# ======================================================================================================================
