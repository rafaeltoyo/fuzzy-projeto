# ==================================================================================================================== #
#   Author: Rafael Hideo Toyomoto                                                                                      #
#   Created: 18/08/2018                                                                                                #
# ==================================================================================================================== #

from fuzzychan.function import MembershipFunc


# ==================================================================================================================== #
#   Operacoes de um termo
# ==================================================================================================================== #


class FuzzyOperator(MembershipFunc):

    def __init__(self, *args, **kwargs):
        pass

    def calc(self, x):
        pass

    def inv(self, mi):
        pass

    def alpha_cut(self, alpha, height=1):
        # FIXME: valido apenas para alguns tipos

        # Calculo dos pontos inversos
        p1, p2 = self(mi=alpha, inv='true')

        # Criar uma funcao crisp para representar o alfa corte
        return MembershipFunc(p1, p2, kind='crisp', height=height)

    def support(self):
        # FIXME: valido apenas para alguns tipos
        return MembershipFunc(self._a, self._b, kind='crisp')

    def core(self):
        # FIXME: valido apenas para alguns tipos
        return MembershipFunc(self._m, self._n, kind='crisp')

# ==================================================================================================================== #
