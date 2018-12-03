# ======================================================================================================================
#   Gerador de arquivo para o projeto 4
# ----------------------------------------------------------------------------------------------------------------------
#   Autor: Rafael Hideo Toyomoto
#   02/12/2018
# ======================================================================================================================


class DatasetGenerator(object):
    from fuzzychan.base import FuzzyUniverse
    from typing import Dict, Any

    def __init__(self, cls_label, **kwargs):
        """
        Classe para geracao de arquivos para teste
        :param cls_label: Label do dicionario que armazena a classe em cada amostra
        :param kwargs: Universos (Dominio)
        """
        from fuzzychan.base import FuzzyUniverse

        # --------------------------------------------------------------------------------------------------------------
        # Label para acessar a classe da amostra
        self.cls_label = cls_label

        # --------------------------------------------------------------------------------------------------------------
        # Salvar os universos
        self.__axes = {}
        for label in kwargs.keys():
            if isinstance(kwargs[label], FuzzyUniverse):
                self.__axes[label] = kwargs[label]
            else:
                raise TypeError

        # --------------------------------------------------------------------------------------------------------------
        # Grupos
        self.__groups = []

    # ==================================================================================================================

    def __get_point(self, **kwargs):
        """
        Confirmar um ponto ou gerar um randomico, baseado nos universos passados no construtor
        :param kwargs:
        :return:
        """
        import random
        from fuzzychan.base import FuzzyUniverse

        # Gerar o ponto vazio
        point = {}

        """ Tentar criar o ponto com os valores passado pelo usuario """
        rnd_init = False

        # Para cada coordenada que o ponto deve ter ...
        for label in self.__axes.keys():
            # [...] Checar se o usuario passou um valor valido para coordenada
            universe = self.__axes[label]  # type: FuzzyUniverse
            xi, xf = universe.domain.limits

            # Faltou essa coordenada OU valor nao pertence ao dominio?
            if (label not in kwargs) or (xi > float(kwargs[label]) or float(kwargs[label]) > xf):
                # Se sim, cancelamos a leitura e passamos para o modo random
                rnd_init = True
                break

            point[label] = float(kwargs[label])

        """ Modo randomico de criacao do ponto """

        if rnd_init:

            # Gerar um novo ponto (limpar possiveis leituras ja feitas)
            point = {}

            # Para cada coordenada que o ponto deve ter ...
            for label in self.__axes.keys():
                # [...] Sortear um valor baseado nos limites do universo correspondente a essa coordenada
                universe = self.__axes[label]  # type: FuzzyUniverse
                point[label] = random.uniform(*universe.domain.limits)

        """ END """
        return point

    # ==================================================================================================================

    def add_group(self, name=None, nelem=20, spread=0.2, **kwargs):
        """
        Adicionar um grupo de amostras com uma classe em comum
        :param name: Nome da classe das amostras
        :param nelem: Numero de amostras
        :param spread: Porcentagem (0 a 1) de 'spread' dos dados
        :param kwargs: Coordenadas do ponto (se faltar algo ou tiver algo invalido, sera random)
        :return: Esse mesmo objeto
        """

        # Checar nome
        if name is None:
            name = ("C%d" % (len(self.__groups) + 1))

        # Checar 'spread'
        if spread < 0 or spread > 1:
            print("Warning: 'spread' params must be a value between 0 and 1. Setting default value(0.2).")
            spread = 0.2

        # Centro do grupo
        centroid = self.__get_point(**kwargs)
        self.__groups.append({
            'centroid': centroid,
            'spread': float(spread),
            'nelem': int(nelem),
            'class': name
        })
        return self

    # ==================================================================================================================

    def generate(self, filename="train.csv", path="dataset/"):
        """
        Gerar um arquivo de treino/teste
        :param filename: Nome do arquivo
        :param path: Diretorio do arquivo
        :return: Proprio objeto
        """

        import csv

        """ Criar dados em memoria """
        header = self.__generate_header()
        dataset = self.__generate_data()

        """ Gerar o arquivo """
        with open(str(path + filename), 'w+') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(header)
            for row in dataset:
                writer.writerow(row.values())

        return self

    def __generate_header(self):
        header = [label for label in self.__axes.keys()]
        header.append(self.cls_label)
        return header

    def __generate_data(self):

        import random
        from fuzzychan.base import FuzzyUniverse

        points = []

        # Percorrer cada um dos grupos criados
        for group in self.__groups:

            # Gerar varios pontos
            for i in range(group["nelem"]):
                # Gerar um ponto novo
                point = {}

                # Percorrer cada um dos universo salvos (o ponto devera ter uma coordenada para cada um deles)
                for label in self.__axes.keys():
                    universe = self.__axes[label]  # type: FuzzyUniverse

                    # Pegar os limites desse  universo
                    xi, xf = universe.domain.limits
                    # Pegar o ponto central desse grupo
                    center = group["centroid"][label]
                    # Calcular o 'spread' do grupo
                    spread = (xf - xi) * group["spread"]
                    # Sortear a coordenada
                    point[label] = random.triangular(max(xi, center-spread), min(xf, center+spread))

                # Salvar a classe
                point[self.cls_label] = group["class"]
                # Salvar o ponto
                points.append(point)
        return points

# ======================================================================================================================
