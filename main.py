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
    altura['teste3'] = MembershipFunc(lambda x: 1 - 1/x, lambda mi: 1/(1 - mi))

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


def cupuacu():
    """
    1) Regras
        1) Se eh alto e pesado entao eh forte
        2) Se tem altura media e tem peso moderado entao eh levemente forte
        3) Se eh baixo e leve entao tem forca media
    """
    pass

    """
    1.1) Calcular e plotar os antecedentes da regra:
        1) alto e pesado
        2) altura media e peso moderado
        3) baixo e leve
    """
    pass

    """
    1.2) Obter cada relacao que descreve as regras Rj (j=1,2,3).
        Operador agregacao E -> min ou prod (usuario escolhe)
    """
    pass

    """
    2) 
    input = levemente alto e muito pesado
        Conc1: input * R1
        Conc2: input * R2
        Conc3: input * R3
        onde * -> operador de composicao sup-min
        Conc = Uniao(Conc1, Conc2, Conc3)
        
        Dicas:
        2.1) input -> matriz bidimensional
        2.2) extensao cilindrica do input -> matriz tridimensional
        2.3) Relacao Rj de cada regra -> matriz tridimensional
        2.4) Conc_j = Projecao em X1 e X2 (altura e peso)
        2.5) Conc = Uniao(Conc_j, j{1,2,3})
    """
    pass

    """
    3) parecido com o 2
    Conc: input * R
    onde R = Uniao(R1, R2, R3)
    
        Dicas:
        3.1) input -> matriz bidimensional
        3.2) extensao cilindrica do input -> matriz tridimensional
        3.3) Relacao Rj de cada regra -> matriz tridimensional
        3.4) R=Uniao(R_j, j={1,2,3})
        3.5) Conc = Projecao em X1 e X2 (altura e peso)
    """
    pass


def main():
    usage_example()


if __name__ == "__main__":
    main()

# ======================================================================================================================
