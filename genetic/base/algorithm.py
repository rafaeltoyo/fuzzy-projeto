# ======================================================================================================================
#   Algoritmo Genetico - Principal
# ----------------------------------------------------------------------------------------------------------------------
#   Autor: Rafael Hideo Toyomoto
#   02/12/2018
# ======================================================================================================================


from genetic.base.crossover import Crossover
from genetic.base.population import Population

# ======================================================================================================================


class Algorithm(object):

    def __init__(self, population, maxgen=100, mutation=0.05):
        """

        :param population:
        :type population: Population
        :param maxgen:
        :param mutation:
        """

        self.__population = population

        self.__generation = 0
        self.__maxgen = maxgen

        self.__mutation = mutation

    def run(self, debug=False):

        # Primeira avaliacao
        self.__population.eval()

        if debug:
            print('=' * 80)
            print("Initializing GA")
            print(str(self.__population))

        while not self.stop():
            if debug:
                print('-' * 80)
                print("Generation: %d" % self.__generation)
                print(str(self.__population))

            # Reproduzir
            children = self.__population.children(n=1.0)

            # Crossover + Mutacao
            Crossover(children, mutation=self.__mutation)()

            # Reavaliar
            children.eval()

            # Juntar os melhores (evoluir)
            self.__population.evolve(children)

            # Contar uma nova geracao
            self.__generation += 1

        return self.__population.best()

    def stop(self):
        return self.__generation >= self.__maxgen

# ======================================================================================================================
