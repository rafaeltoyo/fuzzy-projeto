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
    """
    Funcao Main
    :return: None
    """
    
    """
    1) Regras
        1) Se eh alto e pesado entao eh forte
        2) Se tem altura media e tem peso moderado entao eh levemente forte
        3) Se eh baixo e leve entao tem forca media
    """

    altura = func1()
    altura.plot()
    plt.show()

    peso = func2()
    peso.plot()
    plt.show()

    forca = func3()
    forca.plot()
    plt.show()

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

if __name__ == "__main__":
    main()

# ======================================================================================================================
