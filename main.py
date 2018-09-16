# ======================================================================================================================
#   Inicio
#   Rodar o programa a partir desse arquivo
# ----------------------------------------------------------------------------------------------------------------------
#   Autor: Rafael Hideo Toyomoto
#   11/08/2018
# ======================================================================================================================

from matplotlib import pyplot as plt
from myfuzzy.base import FuzzyUniverse, MembershipFunc


def main():
    altura = FuzzyUniverse("altura", 1.0, 2.0, 1000)
    altura['alto'] = MembershipFunc(1.5, 2.0, 2.0)
    altura['medio'] = MembershipFunc(1.0, 1.5, 2.0)
    altura['baixo'] = MembershipFunc(1.0, 1.0, 1.5)
    altura['a-baixo'] = MembershipFunc(1.0, 1.0, 1.5).alpha_cut(0.4)
    altura['teste1'] = MembershipFunc(1.2, 1.3)
    altura['teste2'] = MembershipFunc(1.4, 1.6, 1.8, 1.9)
    altura['teste3'] = MembershipFunc(lambda x: x+2, lambda mi: mi-2)

    altura.plot()
    plt.show()


if __name__ == "__main__":
    main()

# ======================================================================================================================
