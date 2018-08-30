# ======================================================================================================================
#   Variaveis Fuzzy
# ----------------------------------------------------------------------------------------------------------------------
#   Autor: Rafael Hideo Toyomoto
#   18/08/2018
# ======================================================================================================================

from base.function import MembershipFunction as MFunc


# ----------------------------------------------------------------------------------------------------------------------

class FuzzyVariable(object):
    __cont = 0

    def __init__(self, label=""):
        if label == "":
            FuzzyVariable.__cont += 1
            self.label = "Var" + str(FuzzyVariable.__cont)
        else:
            self.label = label
        self.terms = {}

    def add_term(self, label, func):
        if label == "":
            label = "Term" + str(self.terms.__len__())
        if not isinstance(func, MFunc):
            raise TypeError("FuzzyVariable.add_term(): parameter func must be instance of MembershipFunction")
        self.terms[label] = func
        return self

    def remove_term(self, label):
        try:
            self.terms.pop(label)
        except IndexError as e:
            raise e
        return self

    def generate_terms(self):
        for key, term in self.terms:
            yield term

# ======================================================================================================================
