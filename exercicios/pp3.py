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
from fuzzychan.inference.sugeno import SugenoModel, EnumSugenoDfzz, EnumSugenoAggr, EnumSugenoOper, EnumSugenoImpl, \
    SugenoRule

# ======================================================================================================================


SAMPLE = 50


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


def main():
    """
    Funcao Main
    :return: None
    """

    while True:
        """
        Menu principal
        """
        print("------------------------------------------")
        menu_option = Menu("Escolha uma opcao:")
        menu_option.add("Ver universo 'Sujeira'")
        menu_option.add("Ver universo 'Mancha'")
        menu_option.add("Ver universo 'Tempo de Lavagem'")
        menu_option.add("Criar um modelo")
        menu_option.add("Sair")

        # Aguardar escolha do usuario
        option = menu_option.show()

        if option == 1:
            # Plotar universo Sujeira
            x1 = func_x1(SAMPLE)
            x1.plot()
            plt.show()

        elif option == 2:
            # Plotar universo Mancha
            x2 = func_x2(SAMPLE)
            x2.plot()
            plt.show()

        elif option == 3:
            # Plotar universo Tempo de Lavagem
            y = func_y(SAMPLE)
            y.plot()
            plt.show()

        elif option == 4:
            # Criar um modelo
            menu_model = Menu("Escolha um modelo:")
            menu_model.add("Mamdani")
            menu_model.add("Takagi-Sugeno")
            menu_model.add("Cancelar")

            # Aguardar escolha do usuario
            num_model = menu_model.show()

            if num_model == 1:
                model_mamdani()
            elif num_model == 2:
                model_sugeno()

        else:
            # Sair do loop principal: fim do programa
            break


def model_mamdani():
    x1 = func_x1(SAMPLE)
    x2 = func_x2(SAMPLE)
    y = func_y(SAMPLE)

    """
    1) Escolher agregacao do antecedente
    """
    oper = EnumMamdaniOper.Prod
    menu_oper = Menu("Escolha a agregacao do antecedente")
    menu_oper.add("E (min)")
    menu_oper.add("E (prod)")
    menu_oper.add("OU (max)")
    menu_oper.add("OU (sum)")
    num_oper = menu_oper.show()
    if num_oper == 1:
        oper = EnumMamdaniOper.Min
    elif num_oper == 2:
        oper = EnumMamdaniOper.Prod
    elif num_oper == 3:
        oper = EnumMamdaniOper.Max
    elif num_oper == 4:
        oper = EnumMamdaniOper.Sum

    """
    2) Escolher a semantica das regras
    """
    impl = EnumMamdaniImpl.ConjMin
    menu_impl = Menu("Escolha a semantica das regras")
    menu_impl.add("Conjuncao Min")
    menu_impl.add("Conjuncao Prod")
    menu_impl.add("Disjuncao Max")
    menu_impl.add("Implicacao Lucasiewicz Min")
    menu_impl.add("Implicacao Lucasiewicz Prod")
    menu_impl.add("Implicacao Godel")
    menu_impl.add("Implicacao Kleene")
    menu_impl.add("Implicacao Zadeh")
    num_impl = menu_impl.show()
    if num_impl == 1:
        impl = EnumMamdaniImpl.ConjMin
    elif num_impl == 2:
        impl = EnumMamdaniImpl.ConjPro
    elif num_impl == 3:
        impl = EnumMamdaniImpl.DisjMax
    elif num_impl == 4:
        impl = EnumMamdaniImpl.ImplLSWMin
    elif num_impl == 5:
        impl = EnumMamdaniImpl.ImplLSWPro
    elif num_impl == 6:
        impl = EnumMamdaniImpl.ImplGodel
    elif num_impl == 7:
        impl = EnumMamdaniImpl.ImplKleene
    elif num_impl == 8:
        impl = EnumMamdaniImpl.ImplZadeh

    """
    3) Escolher composicao das regras
    """
    aggr = EnumMamdaniAggr.Max
    menu_aggr = Menu("Escolha o operador de composicao dos resultados das regras")
    menu_aggr.add("Max")
    menu_aggr.add("Sum")
    num_aggr = menu_aggr.show()
    if num_aggr == 1:
        aggr = EnumMamdaniAggr.Max
    elif num_aggr == 2:
        aggr = EnumMamdaniAggr.Sum

    """
    4) Escolher o metodo de defuzzificacao
    """
    dfzz = EnumMamdaniDfzz.MoM
    menu_dfzz = Menu("Escolha o metodo de defuzzificacao")
    menu_dfzz.add("CoG - Center of Gravity")
    menu_dfzz.add("FoM - First of Maximum")
    menu_dfzz.add("LoM - Last of Maximum")
    menu_dfzz.add("MoM - Medium of Maximum")
    num_dfzz = menu_dfzz.show()
    if num_dfzz == 1:
        dfzz = EnumMamdaniDfzz.CoG
    elif num_dfzz == 2:
        dfzz = EnumMamdaniDfzz.FoM
    elif num_dfzz == 3:
        dfzz = EnumMamdaniDfzz.LoM
    elif num_dfzz == 4:
        dfzz = EnumMamdaniDfzz.MoM

    model = MamdaniModel(oper=oper, impl=impl, aggr=aggr, dfzz=dfzz, x1=x1, x2=x2, out=y)
    model.create_rule(x1='PS', x2='SM', out='MC')
    model.create_rule(x1='PS', x2='MM', out='M')
    model.create_rule(x1='PS', x2='GM', out='L')
    model.create_rule(x1='MS', x2='SM', out='C')
    model.create_rule(x1='MS', x2='MM', out='M')
    model.create_rule(x1='MS', x2='GM', out='L')
    model.create_rule(x1='GS', x2='SM', out='M')
    model.create_rule(x1='GS', x2='MM', out='L')
    model.create_rule(x1='GS', x2='GM', out='ML')

    """
    5) Acao a ser tomada com o modelo
    """

    while True:
        menu_action = Menu("Escolha uma acao:")
        menu_action.add("Entrar com valores")
        menu_action.add("Plotar")
        menu_action.add("Gerar arquivo para teste")
        menu_action.add("Sair")
        num_action = menu_action.show()

        if num_action == 1:
            # Entrar com valores
            val_x1 = float(raw_input("Entra com X1:"))
            val_x2 = float(raw_input("Entra com X2:"))
            print("Saida: " + str(model(plt.figure(), x1=val_x1, x2=val_x2)))

        elif num_action == 2:
            domain_x1 = np.array(x1.domain.points)
            domain_x2 = np.array(x2.domain.points)

            prod_x1, prod_x2 = np.meshgrid(domain_x1, domain_x2)
            domain_y = np.array([model(x1=x1i, x2=x2i) for (x1i, x2i) in zip(np.ravel(prod_x1), np.ravel(prod_x2))])
            domain_y = domain_y.reshape(prod_x1.shape)

            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            ax.plot_surface(prod_x1, prod_x2, domain_y)
            plt.show()

        elif num_action == 3:
            # Gerar arquivo teste
            file_name = raw_input("Nome do arquivo:")
            out = np.array([[int(i), int(j), model(x1=i, x2=j)] for i in range(0, 110, 10) for j in range(0, 110, 10)])
            np.savetxt(str(file_name) + ".csv", out, fmt=['%d', '%d', '%.5f'], delimiter=";")

        else:
            break


def model_sugeno():
    x1 = func_x1(SAMPLE)
    x2 = func_x2(SAMPLE)
    y = func_y(SAMPLE)

    """
    1) Escolher agregacao do antecedente
    """
    oper = EnumMamdaniOper.Prod
    menu_oper = Menu("Escolha a agregacao do antecedente")
    menu_oper.add("E (min)")
    menu_oper.add("E (prod)")
    menu_oper.add("OU (max)")
    menu_oper.add("OU (sum)")
    num_oper = menu_oper.show()
    if num_oper == 1:
        oper = EnumSugenoOper.Min
    elif num_oper == 2:
        oper = EnumSugenoOper.Prod
    elif num_oper == 3:
        oper = EnumSugenoOper.Max
    elif num_oper == 4:
        oper = EnumSugenoOper.Sum

    """
    2) Escolher o metodo de defuzzificacao
    """
    dfzz = EnumMamdaniDfzz.MoM
    menu_dfzz = Menu("Escolha o metodo de defuzzificacao")
    menu_dfzz.add("Media")
    menu_dfzz.add("Soma")
    num_dfzz = menu_dfzz.show()
    if num_dfzz == 1:
        dfzz = EnumSugenoDfzz.Avg
    elif num_dfzz == 2:
        dfzz = EnumSugenoDfzz.Sum

    model = SugenoModel(oper=oper, dfzz=dfzz, x1=x1, x2=x2, out=y)
    model.create_rule(x1='PS', x2='SM', out=0.5)
    model.create_rule(x1='PS', x2='MM', out=23)
    model.create_rule(x1='PS', x2='GM', out=42)
    model.create_rule(x1='MS', x2='SM', out=10)
    model.create_rule(x1='MS', x2='MM', out=26)
    model.create_rule(x1='MS', x2='GM', out=42)
    model.create_rule(x1='GS', x2='SM', out=27)
    model.create_rule(x1='GS', x2='MM', out=41)
    model.create_rule(x1='GS', x2='GM', out=60)

    """
    3) Acao a ser tomada com o modelo
    """

    while True:
        menu_action = Menu("Escolha uma acao:")
        menu_action.add("Entrar com valores")
        menu_action.add("Plotar")
        menu_action.add("Gerar arquivo para teste")
        menu_action.add("Sair")
        num_action = menu_action.show()

        if num_action == 1:
            # Entrar com valores
            val_x1 = float(raw_input("Entra com X1:"))
            val_x2 = float(raw_input("Entra com X2:"))
            print("Saida: " + str(model(x1=val_x1, x2=val_x2)))

        elif num_action == 2:
            domain_x1 = np.array(x1.domain.points)
            domain_x2 = np.array(x2.domain.points)

            prod_x1, prod_x2 = np.meshgrid(domain_x1, domain_x2)
            domain_y = np.array([model(x1=x1i, x2=x2i) for (x1i, x2i) in zip(np.ravel(prod_x1), np.ravel(prod_x2))])
            domain_y = domain_y.reshape(prod_x1.shape)

            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            ax.plot_surface(prod_x1, prod_x2, domain_y)
            plt.show()

        elif num_action == 3:
            # Gerar arquivo teste
            file_name = raw_input("Nome do arquivo:")
            out = np.array([[int(i), int(j), model(x1=i, x2=j)] for i in range(0, 110, 10) for j in range(0, 110, 10)])
            np.savetxt(str(file_name) + ".csv", out, fmt=['%d', '%d', '%.5f'], delimiter=";")

        else:
            break


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
    main()

# ======================================================================================================================
