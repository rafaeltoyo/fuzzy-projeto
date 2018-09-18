# ======================================================================================================================
#   Inicio
#   Rodar o programa a partir desse arquivo
# ----------------------------------------------------------------------------------------------------------------------
#   Autor: Rafael Hideo Toyomoto
#   11/08/2018
# ======================================================================================================================

from matplotlib import pyplot as plt
from myfuzzy.base import FuzzyUniverse, MembershipFunc


def usage_example():
    """
    Exemplo de uso da biblioteca Fuzzy
    :return:
    """

    """
    Ideia de Universo Fuzzy e seus termos (funcoes de pertinencia)
    """

    # Criacao do universo 'altura'
    altura = FuzzyUniverse("altura", 1.0, 2.0, 1000)

    # Funcoes de perticencia triangulares
    altura['alto'] = MembershipFunc(1.5, 2.0, 2.0)
    altura['medio'] = MembershipFunc(1.0, 1.5, 2.0)
    altura['baixo'] = MembershipFunc(1.0, 1.0, 1.5)

    # Alfa-corte
    altura['a-baixo'] = MembershipFunc(1.0, 1.0, 1.5).alpha_cut(0.4)

    # Funcao de pertinencia retangular/crisp
    altura['teste1'] = MembershipFunc(1.2, 1.3)

    # Funcao de pertinencia trapezoidal
    altura['teste2'] = MembershipFunc(1.4, 1.6, 1.8, 1.9)

    # Funcao de pertinencia customizada
    altura['teste3'] = MembershipFunc(lambda x: x+2, lambda mi: mi-2)

    # Plot do universo
    fig = plt.figure()
    altura.plot(figure=fig)
    plt.show()

    # Plot do universo filtrado
    altura.plot(vars=['alto', 'medio'])
    plt.show()

    """
    Ideia de criacao das relacoes
    """
    # funcN = MembershipFunc
    # union = Union(x=func1, y=func2, z=func3, a=func4, kind=kind)
    # union(x=1, y=2, z=9, a=4) -> point
    # union(x=[1, 9]) -> limit x only

    """
    Ideia de criacao de regras
    """
    # rule = Rule(antecedent=antecedent, consequent=consequent, kind=kind)
    # rule.plot()
    # plt.show()

    # TODO: Unir regras?


def main():
    usage_example()


if __name__ == "__main__":
    main()

# ======================================================================================================================
