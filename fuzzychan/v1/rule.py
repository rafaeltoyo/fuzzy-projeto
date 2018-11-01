# ==================================================================================================================== #
#   Author: Rafael Hideo Toyomoto                                                                                      #
#   Created: 12/09/2018                                                                                                #
# ==================================================================================================================== #

import numpy as np
import matplotlib.pyplot as plt


# ==================================================================================================================== #
#   Rule
# -------------------------------------------------------------------------------------------------------------------- #
#   Classe que representa uma regra fuzzy
# ==================================================================================================================== #


class Rule(dict):

    def __init__(self, antecedent, consequent, kind="conj-min"):
        super(Rule, self).__init__()
        self.antecedent = antecedent
        self.consequent = consequent
        self.kind = kind

    def get_matrix(self, term_x="", term_y=""):
        (X, Y) = np.meshgrid(self.antecedent.domain.points, self.consequent.domain.points)
        z = np.array(
            [self._calc(self.antecedent[term_x].func.calc(x), self.consequent[term_y].func.calc(y)) for (x, y) in
             zip(np.ravel(X), np.ravel(Y))])
        Z = z.reshape(X.shape)
        return X, Y, Z

    def get_alpha_cut(self, alpha, term_x="", term_y=""):
        x, y, z = self.get_matrix(term_x=term_x, term_y=term_y)
        z = np.array([alpha if zi > alpha else 0 for zi in np.ravel(z)])
        z = z.reshape(x.shape)
        return x, y, z

    def _calc(self, a, b):
        return {
            'conj-min': min(a, b),
            'conj-pro': a * b,
            'disj': max(a, b),
            'impl-lucasiewicz-min': min(1, min(1 - a, b)),
            'impl-lucasiewicz-pro': min(1, (1 - a) * b),
            'impl-godel': 1 if a <= b else b,
            'impl-kleene': max(1 - a, b),
            'impl-zadeh': max(1 - a, min(a, b))
        }.get(self.kind)

    def plot(self, term_x="", term_y="", fig=None):
        if self.antecedent[term_x] is None or self.consequent[term_y] is None:
            return None

        if fig is None:
            fig = plt.figure()
        axes = fig.gca(projection='3d')

        x, y, z = self.get_matrix(term_x=term_x, term_y=term_y)
        axes.plot_surface(x, y, z)
        axes.legend()
        return axes

# ==================================================================================================================== #
