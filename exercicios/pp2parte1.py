# ======================================================================================================================
#   Execucao do projeto 2 - parte 1
# ----------------------------------------------------------------------------------------------------------------------
#   Autor: Rafael Hideo Toyomoto
#   11/09/2018
# ======================================================================================================================

import numpy as np
from matplotlib import pyplot as plt

from fuzzychan.v1.variable import Variable
from fuzzychan.v1.rule import Rule
from fuzzychan.continuous.function import TriagularMFunction


# ----------------------------------------------------------------------------------------------------------------------

def var_altura(sample=1000):
    fig = plt.figure(num="altura", figsize=(5, 5), dpi=100)

    altura = Variable("Altura", 1, 2, sample)
    altura["alto"] = TriagularMFunction(1.5, 2, 2)
    altura["medio"] = TriagularMFunction(1, 1.5, 2)
    altura["baixo"] = TriagularMFunction(1, 1, 1.5)

    altura.plot(figure=fig)
    plt.show()


def var_peso(sample=1000):
    fig = plt.figure(num="peso", figsize=(5, 5), dpi=100)

    peso = Variable("Peso", 0, 100, sample)
    peso["pesado"] = TriagularMFunction(50, 100, 100)
    peso["moderado"] = TriagularMFunction(0, 50, 100)
    peso["leve"] = TriagularMFunction(0, 0, 50)

    peso.plot(figure=fig)
    plt.show()


def main():
    while True:

        # Escolher opcao principal
        print("-----------------------------------------------------------------------------")
        print("")
        print("Escolha uma opcao:")
        print("[1] Regra 1: Se eh alto, entao eh pesado")
        print("[2] Regra 2: Se tem altura media entao tem peso moderado")
        print("[3] Regra 3: Se eh baixo entao eh leve")
        print("[4] Ver universo 'altura'")
        print("[5] Ver universo 'peso'")
        print("[6] Sair")
        # Leitura da opcao
        while True:
            num_regra = int(raw_input("R: "))
            if 1 <= num_regra <= 6:
                break
            print("Opcao invalida!")

        term_x = ""
        term_y = ""

        if num_regra == 1:
            term_x = "alto"
            term_y = "pesado"

        if num_regra == 2:
            term_x = "medio"
            term_y = "moderado"

        if num_regra == 3:
            term_x = "baixo"
            term_y = "leve"

        # Plotar Altura
        if num_regra == 4:
            var_altura()
            continue
        # Plotar Peso
        if num_regra == 5:
            var_peso()
            continue
        # Quit
        if num_regra == 6:
            break

        # Escolheu alguma regra
        # Escolher uma operacao
        print("-----------------------------------------------------------------------------")
        print("")
        print("Escolha um operador:")
        print("[1] Conjuncao (minimo)")
        print("[2] Conjuncao (produto)")
        print("[3] Disjuncao")
        print("[4] Implicacao (Lucasiewicz minimo)")
        print("[5] Implicacao (Lucasiewicz produto)")
        print("[6] Implicacao (Godel)")
        print("[7] Implicacao (Kleene)")
        print("[8] Implicacao (Zadeh)")
        print("[9] Cancelar")
        # Leitura da operacao
        while True:
            num_oper = int(raw_input("R: "))
            if 1 <= num_oper <= 9:
                break
            print("Opcao invalida!")

        # Cancelar
        if num_oper == 9:
            continue

        # Pegar a operacao escolhida
        kind = ""
        if num_oper == 1:
            kind = "conj-min"
        elif num_oper == 2:
            kind = "conj-pro"
        elif num_oper == 3:
            kind = "disj"
        elif num_oper == 4:
            kind = "impl-lucasiewicz-min"
        elif num_oper == 5:
            kind = "impl-lucasiewicz-pro"
        elif num_oper == 6:
            kind = "impl-godel"
        elif num_oper == 7:
            kind = "impl-kleene"
        elif num_oper == 8:
            kind = "impl-zadeh"

        # Escolheu alguma operacao
        # Escolher uma acao
        print("-----------------------------------------------------------------------------")
        print("")
        print("Deseja qual acao?")
        print("[1] Plotagem simples")
        print("[2] Plotagem por reconstrucao com alfa cortes")
        # Leitura da acao
        while True:
            num_acao = int(raw_input("R: "))
            if 1 <= num_acao <= 2:
                break
            print("Opcao invalida!")

        # Leitura do nivel de discretizacao
        while True:
            sample = int(raw_input("Nivel de Discretizacao: "))
            if sample > 0:
                break
            print("Opcao invalida!")

        # Variavel Altura
        altura = Variable("Altura", 1, 2, sample)
        altura["alto"] = TriagularMFunction(1.5, 2, 2)
        altura["medio"] = TriagularMFunction(1, 1.5, 2)
        altura["baixo"] = TriagularMFunction(1, 1, 1.5)

        # Variavel Peso
        peso = Variable("Peso", 0, 100, sample)
        peso["pesado"] = TriagularMFunction(50, 100, 100)
        peso["moderado"] = TriagularMFunction(0, 50, 100)
        peso["leve"] = TriagularMFunction(0, 0, 50)

        # Criar regra
        regra = Rule(antecedent=altura, consequent=peso, kind=kind)

        alpha = None
        axes = None

        # Reconstrucao por alfa corte
        if num_acao == 1:
            regra.plot(term_x=term_x, term_y=term_y)
        if num_acao == 2:
            # Leitura do step para o alpha corte
            while True:
                alpha = float(raw_input("Step: "))
                if 0 < alpha <= 1:
                    break
                print("Opcao invalida (valor entre 0 e 1)!")

            alpha_iter = 1

            # Primeiro alfa-corte = 1
            x, y, z = regra.get_alpha_cut(alpha=1, term_x=term_x, term_y=term_y)

            # Matriz 3D -> Array unidimensional
            z = np.ravel(z)

            # Criar os demais alfa corte com o step passado
            while alpha_iter >= 0:
                alpha_iter -= alpha

                # Criar o n-esimo alfa-corte
                xs, ys, zs = regra.get_alpha_cut(alpha=alpha_iter, term_x=term_x, term_y=term_y)
                # Juntar o alfa-corte aos demais
                z = np.array([max(z_iter, z_current) for (z_iter, z_current) in zip(np.ravel(zs), z)])

            axes = plt.figure().gca(projection='3d')
            axes.plot_surface(x, y, z.reshape(x.shape))
            axes.legend()
        plt.show()


if __name__ == "__main__":
    main()

# ======================================================================================================================
