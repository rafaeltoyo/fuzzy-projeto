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
import time

from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from fuzzychan.base import FuzzyUniverse
from fuzzychan.function import MembershipFunc
from fuzzychan.classifier.wangmendel import WangMendelClassifier

from exercicios.pp4_dataset_gen import DatasetGenerator

from genetic.base.algorithm import Algorithm as GaAlgorithm
from genetic.base.population import Population as GaPopulation
from genetic.base.chromosome import Chromosome
from genetic.base.gene import Gene


# ======================================================================================================================


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
    Teste AG + Fuzzy
    :return:
    """

    exectime = {
        'all': {},
        'file': {},
        'ga': {},
        'wm': {}
    }
    sample = 1000
    exectime["all"]["start"] = time.time()

    """ Opening train data file """
    exectime["file"]["start"] = time.time()
    df = pd.read_csv("dataset/train1.csv")
    exectime["file"]["end"] = time.time()
    print df['x1'].size
    return
    """ Implemetation of fitness function to GA """
    def fitness_function(chromosome):
        """
        ::param chromosome:
        :type chromosome: Chromosome
        """

        gs = chromosome.genes

        if len(gs) != 14:
            return 0

        if not (0 <= gs[0].value() < gs[1].value()) or not (gs[1].value() > gs[2].value()):
            return 0
        if not (gs[2].value() < gs[3].value() < gs[4].value()) or not (gs[4].value() > gs[5].value()):
            return 0
        if not (gs[5].value() < gs[6].value() <= 100):
            return 0
        if not (gs[0].value() < gs[3].value() < gs[6].value()):
            return 0

        if not (0 < gs[7].value() < gs[8].value()) or not (gs[8].value() > gs[9].value()):
            return 0
        if not (gs[9].value() < gs[10].value() < gs[11].value()) or not (gs[11].value() > gs[12].value()):
            return 0
        if not (gs[12].value() < gs[13].value() <= 100):
            return 0
        if not (gs[7].value() < gs[10].value() < gs[13].value()):
            return 0

        x1, x2 = generate_universes(gs, sample)

        wmcls = WangMendelClassifier(x1=x1, x2=x2)
        wmcls.train(df.to_dict('records'), out_label='cls', debug=False)
        return wmcls.get_fitness() * 100

    """ Creating first universe """
    n_genes1 = [random.uniform(0, 100) for i in range(0, 7)]
    n_genes1.sort()
    genes1 = [Gene(0, 100, n) for n in n_genes1]
    genes1[1], genes1[2] = genes1[2], genes1[1]
    genes1[4], genes1[5] = genes1[5], genes1[4]

    """ Creating second universe """
    n_genes2 = [random.uniform(0, 100) for i in range(0, 7)]
    n_genes2.sort()
    genes2 = [Gene(0, 100, n) for n in n_genes2]
    genes2[1], genes2[2] = genes2[2], genes2[1]
    genes2[4], genes2[5] = genes2[5], genes2[4]

    """ Genetic Algorithm Tuning """
    exectime["ga"]["start"] = time.time()
    pop = GaPopulation(Chromosome(fitness_function, *(genes1 + genes2)), 50)
    ga = GaAlgorithm(pop, maxgen=100, mutation=0.15)
    ga.run(debug=True)
    exectime["ga"]["end"] = time.time()

    best = pop.best()
    gs = best.genes
    print('-' * 80)
    print(str(best))

    """ WangMendel Classifier to show results """
    exectime["wm"]["start"] = time.time()
    x1, x2 = generate_universes(gs, sample)
    wmcls = WangMendelClassifier(x1=x1, x2=x2)
    wmcls.train(df.to_dict('records'), out_label='cls', debug=False)
    wmcls.print_status()
    exectime["wm"]["end"] = time.time()

    """ Ploting results """
    fig = plt.figure()
    axes = fig.add_subplot(111)

    axes.set_xbound(x1.domain.limits)
    axes.set_ybound(x2.domain.limits)
    seaborn.scatterplot('x1', 'x2', hue='cls', data=df, ax=axes)

    gs0 = [gs[0].value(), gs[0].value()]
    gs1 = [gs[1].value(), gs[1].value()]
    gs2 = [gs[2].value(), gs[2].value()]
    gs3 = [gs[3].value(), gs[3].value()]
    gs4 = [gs[4].value(), gs[4].value()]
    gs5 = [gs[5].value(), gs[5].value()]
    gs6 = [gs[6].value(), gs[6].value()]
    gs7 = [gs[7].value(), gs[7].value()]
    gs8 = [gs[8].value(), gs[8].value()]
    gs9 = [gs[9].value(), gs[9].value()]
    gs10 = [gs[10].value(), gs[10].value()]
    gs11 = [gs[11].value(), gs[11].value()]
    gs12 = [gs[12].value(), gs[12].value()]
    gs13 = [gs[13].value(), gs[13].value()]
    interval = [0, 100]

    # X1/A1
    plt.plot([0, 0], interval, gs1, interval, color="blue")
    axes.fill_between([0, gs[1].value()], [0, 0], [100, 100], facecolor='blue', alpha=0.2, interpolate=True)
    # X1/A2
    plt.plot(gs2, interval, gs4, interval, color="red")
    axes.fill_between([gs[2].value(), gs[4].value()], [0, 0], [100, 100], facecolor='red', alpha=0.2, interpolate=True)
    # X1/A3
    plt.plot(gs5, interval, [100, 100], interval, color="green")
    axes.fill_between([gs[5].value(), 100], [0, 0], [100, 100], facecolor='green', alpha=0.2, interpolate=True)

    # X1/A1
    plt.plot(interval, [0, 0], interval, gs8, color="blue")
    axes.fill_between(interval, [0, 0], gs8, where=gs8 >= [0, 0], facecolor='blue', alpha=0.2, interpolate=True)
    # X1/A2
    plt.plot(interval, gs9, interval, gs11, color="red")
    axes.fill_between(interval, gs9, gs11, where=gs11 >= gs9, facecolor='red', alpha=0.2, interpolate=True)
    # X1/A3
    plt.plot(interval, gs12, interval, [100, 100], color="green")
    axes.fill_between(interval, gs12, [100, 100], where=[100, 100] >= gs12, facecolor='green', alpha=0.2, interpolate=True)

    x1.plot()

    x2.plot()

    plt.show()

    exectime["all"]["end"] = time.time()

    """ Printing timers """
    print('=' * 80)
    for label in exectime:
        print("%s time: \t%.3fs" % (label, float(exectime[label]["end"] - exectime[label]["start"])))
    print('=' * 80)



def generate_universes(gs, sample):
    x1 = FuzzyUniverse("Attr1", 0, 100, sample)
    x1["A1"] = MembershipFunc(0, gs[0].value(), gs[1].value())
    x1["A2"] = MembershipFunc(gs[2].value(), gs[3].value(), gs[4].value())
    x1["A3"] = MembershipFunc(gs[5].value(), gs[6].value(), 100)

    x2 = FuzzyUniverse("Attr2", 0, 100, sample)
    x2["B1"] = MembershipFunc(0, gs[7].value(), gs[8].value())
    x2["B2"] = MembershipFunc(gs[9].value(), gs[10].value(), gs[11].value())
    x2["B3"] = MembershipFunc(gs[12].value(), gs[13].value(), 100)

    return x1, x2


def main2():
    """
    Teste WangMendel
    :return:
    """

    """ Taxa de amostragem (Discretizacao) para as funcoes de pertinencia """
    sample = 1000

    """ Universos dos dados """
    x1 = func1(sample)
    x2 = func2(sample)

    """ Gerar/Abrir arquivo input de treino """
    filename = "train6.csv"

    # dg = DatasetGenerator("cls", x1=x1, x2=x2)
    # dg.add_group(name="C1", nelem=70, spread=0.47)
    # dg.add_group(name="C2", nelem=40, spread=0.35)
    # dg.add_group(name="C3", nelem=100, spread=0.6)
    # dg.generate(filename)

    # test_dataframe(filename='dataset/train1.csv', ncls=5, spreadv=40)
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

    plt.show()

# ======================================================================================================================
