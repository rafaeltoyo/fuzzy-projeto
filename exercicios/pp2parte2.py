# ======================================================================================================================
#   Execucao do projeto 2 - parte 1
# ----------------------------------------------------------------------------------------------------------------------
#   Autor: Rafael Hideo Toyomoto
#   11/09/2018
# ======================================================================================================================

from matplotlib import pyplot as plt
from myfuzzy.base import FuzzyUniverse, MembershipFunc


# ======================================================================================================================


def func1():
    func = FuzzyUniverse("altura", 1.0, 2.0, 1000)
    func['baixo'] = MembershipFunc(1.0, 1.0, 1.5)
    func['medio'] = MembershipFunc(1.0, 1.5, 2.0)
    func['alto'] = MembershipFunc(1.5, 2.0, 2.0)
    return func


def func2():
    func = FuzzyUniverse("peso", 0.0, 100.0, 1000)
    func['leve'] = MembershipFunc(0.0, 0.0, 50.0)
    func['moderado'] = MembershipFunc(0.0, 50.0, 100.0)
    func['pesado'] = MembershipFunc(50.0, 100.0, 100.0)
    return func


def func3():
    func = FuzzyUniverse("forca", 0.0, 100.0, 1000)
    func['media'] = MembershipFunc(0.0, 0.0, 50.0)
    func['forte'] = MembershipFunc(0.0, 50.0, 100.0, 100.0)
    return func

# ======================================================================================================================


def main():
    altura = func1()
    altura.plot()
    plt.show()

    peso = func2()
    peso.plot()
    plt.show()

    forca = func3()
    forca.plot()
    plt.show()


if __name__ == "__main__":
    main()

# ======================================================================================================================
