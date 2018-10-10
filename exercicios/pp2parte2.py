# ======================================================================================================================
#   Execucao do projeto 2 - parte 1
# ----------------------------------------------------------------------------------------------------------------------
#   Autor: Rafael Hideo Toyomoto
#   11/09/2018
# ======================================================================================================================


import numpy as np

from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from exercicios.mymenu import Menu

from fuzzychan.base import FuzzyUniverse, MembershipFunc
from fuzzychan.relation import FuzzyRelation, EnumRelation
from fuzzychan.rule import FuzzyRule, EnumRule, fuzzy_conclusion

# ======================================================================================================================

SAMPLE = 30


def func1():
    """

    :return: FuzzyUniverse
    """

    func = FuzzyUniverse("altura", 1.0, 2.0, SAMPLE)
    func['baixo'] = MembershipFunc(1.0, 1.0, 1.5)
    func['medio'] = MembershipFunc(1.0, 1.5, 2.0)
    func['alto'] = MembershipFunc(1.5, 2.0, 2.0)
    return func


def func2():
    """

    :return: FuzzyUniverse
    """

    func = FuzzyUniverse("peso", 0.0, 100.0, SAMPLE)
    func['leve'] = MembershipFunc(0.0, 0.0, 50.0)
    func['moderado'] = MembershipFunc(0.0, 50.0, 100.0)
    func['pesado'] = MembershipFunc(50.0, 100.0, 100.0)
    return func


def func3():
    """

    :return: FuzzyUniverse
    """

    func = FuzzyUniverse("forca", 0.0, 100.0, SAMPLE)
    func['media'] = MembershipFunc(0.0, 0.0, 50.0)
    func['forte'] = MembershipFunc(0.0, 50.0, 100.0, 100.0)
    return func


# ======================================================================================================================


def main():
    """
    Funcao Main
    :return: None
    """

    main_menu = Menu("Selecione uma opcao")
    main_menu.add("Ver universos")
    main_menu.add("Ver antecedentes")
    main_menu.add("Executar tudo")
    main_menu.add("Sair")

    user_func = main_menu.show()

    """
    1) Regras
        1) Se eh alto e pesado entao eh forte
        2) Se tem altura media e tem peso moderado entao eh levemente forte
        3) Se eh baixo e leve entao tem forca media
    """

    altura, peso, forca = func1(), func2(), func3()

    if user_func == 1:
        altura.plot(figure=plt.figure())
        peso.plot(figure=plt.figure())
        forca.plot(figure=plt.figure())
        plt.show()
        return True
    if user_func == 4:
        return False

    """
    1.1) Calcular e plotar os antecedentes da regra:
        1) alto e pesado
        2) altura media e peso moderado
        3) baixo e leve
    """

    aggr_menu = Menu("Escolha um operador para agregacao do antecedente:")
    aggr_menu.add("min")
    aggr_menu.add("prod")
    user_aggr = EnumRelation.Min if aggr_menu.show() == 1 else EnumRelation.Prod

    relacao1 = FuzzyRelation(kind=user_aggr, x=altura['alto'], y=peso['pesado'])
    relacao2 = FuzzyRelation(kind=user_aggr, x=altura['medio'], y=peso['moderado'])
    relacao3 = FuzzyRelation(kind=user_aggr, x=altura['baixo'], y=peso['leve'])

    if user_func == 2:
        relacao1.plot(figure=plt.figure())
        relacao2.plot(figure=plt.figure())
        relacao3.plot(figure=plt.figure())
        plt.show()
        return True

    """
    1.2) Obter cada relacao que descreve as regras Rj (j=1,2,3).
        Operador agregacao E -> min ou prod (usuario escolhe)
    """

    # TODO: Acoplar as regras em um banco de regras
    regra1 = FuzzyRule(relacao1, FuzzyRelation(x=forca['forte']), kind=EnumRule.ConjMin)
    regra2 = FuzzyRule(relacao2, FuzzyRelation(x=forca['levemente forte']), kind=EnumRule.ConjMin)
    regra3 = FuzzyRule(relacao3, FuzzyRelation(x=forca['media']), kind=EnumRule.ConjMin)

    """
    input = levemente alto e muito pesado
    """

    input = FuzzyRelation(kind=user_aggr, x=altura['levemente alto'], y=peso['muito pesado'])
    #input.plot(figure=plt.figure())
    plt.show()

    inX, inY = np.meshgrid(altura.domain.points, peso.domain.points)

    """
    2) 
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

    # FIXME: Acoplar a projecao para sempre ser feita no dominio do consequente
    conc1 = fuzzy_conclusion(regra1, input).max(2).max(1)
    plt.plot(forca.domain.points, conc1)
    conc2 = fuzzy_conclusion(regra2, input).max(2).max(1)
    plt.plot(forca.domain.points, conc2)
    conc3 = fuzzy_conclusion(regra3, input).max(2).max(1)
    plt.plot(forca.domain.points, conc3)

    conclusion = np.array([max(c1, c2, c3) for (c1, c2, c3) in
                           zip(np.ravel(conc1), np.ravel(conc2), np.ravel(conc3))]).reshape(conc1.shape)

    fig = plt.figure()
    #ax = fig.add_subplot(111, projection='3d')
    #ax.plot_surface(inX, inY, conclusion)
    plt.plot(forca.domain.points, conclusion)

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

    result1 = regra1.matrix()
    result2 = regra2.matrix()
    result3 = regra3.matrix()
    regra = np.array(
        [max(r1, r2, r3) for (r1, r2, r3) in zip(np.ravel(result1), np.ravel(result2), np.ravel(result3))]).reshape(
        result1.shape)
    conclusion = fuzzy_conclusion(regra, input).max(2).max(1)

    fig = plt.figure()
    #ax = fig.add_subplot(111, projection='3d')
    #ax.plot_surface(inX, inY, conclusion)
    plt.plot(forca.domain.points, conclusion)

    plt.show()

    return True


if __name__ == "__main__":
    main()

# ======================================================================================================================
