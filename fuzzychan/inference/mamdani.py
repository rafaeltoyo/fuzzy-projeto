# ======================================================================================================================
#   Modelo Mamdani de inferencia Fuzzy
# ----------------------------------------------------------------------------------------------------------------------
#   Autor: Rafael Hideo Toyomoto
#   07/10/2018
# ======================================================================================================================


from enum import Enum

import numpy as np
import matplotlib.pyplot as plt

from fuzzychan.base import FuzzyUniverse, MembershipFunc, FuzzySet
from fuzzychan.relation import FuzzyRelation
from fuzzychan.rule import fuzzy_rule_compute
from fuzzychan.operator import FuzzyOperator

from fuzzychan.rule import EnumRule as EnumMamdaniImpl
from fuzzychan.relation import EnumRelation as EnumMamdaniOper
from fuzzychan.relation import EnumRelation as EnumMamdaniAggr
from fuzzychan.operator import EnumFuzzyOper


# ======================================================================================================================

class EnumMamdaniDfzz(Enum):
    CoS = 'CenterOfSums'
    CoG = 'CenterOfGravity'
    BoA = 'BisectorOfArea'
    FoM = 'FisrtOfMaxima'
    LoM = 'LastOfMaxima'
    MoM = 'MeanOfMaxima'


# ======================================================================================================================


class MamdaniRule(object):

    def __init__(self, antecedent, consequent, kind=EnumMamdaniImpl.ConjMin, *args, **kwargs):
        """
        Regra Fuzzy
        :param antecedent:
        :type antecedent: FuzzyRelation
        :param consequent:
        :type consequent: FuzzySet
        :param kind:
        :type kind: EnumMamdaniImpl
        :param sample: Taxa de amostagem da saida
        :type sample: int
        :param args:
        :param kwargs:
        """

        # Salvar o antecedente e o consequente
        self.__antecedent = antecedent
        self.__consequent = consequent

        # Salvar a semantica da regra
        self.__kind = kind

    def getAntecedent(self):
        return self.__antecedent

    def getConsequent(self):
        return self.__consequent

    def __call__(self, continuous=False, **kwargs):

        # Verificar se tem input suficiente
        inp_size = self.__antecedent.dimension()
        if len(kwargs) != inp_size:
            raise AttributeError

        # Computar o antecedente
        out_height = self.__antecedent(**kwargs)

        # Gerar a saida
        universe = self.__consequent._universe

        # FIXME: o codigo de continuo ate funciona, porem nao permite todas semanticas (intersection - min apenas)
        if continuous:
            f_limit = MembershipFunc(min(universe.domain.points), max(universe.domain.points), height=out_height)
            f_out = FuzzyOperator(f_limit, self.__consequent.func, kind=EnumFuzzyOper.Intersection)
            return FuzzySet(universe, func=f_out)

        # Implementacao provisoria, porem efetiva (nao permite continuo)
        return [fuzzy_rule_compute(out_height, self.__consequent.func(x=x), self.__kind) for x in universe.domain]


# ======================================================================================================================


class MamdaniModel(object):

    def __init__(self,
                 oper=EnumMamdaniOper.Min,
                 impl=EnumMamdaniImpl.ConjMin,
                 aggr=EnumMamdaniAggr.Min,
                 dfzz=EnumMamdaniDfzz.CoG,
                 out=None,
                 **kwargs):
        """
        Modelo Mamdani de inferencia Fuzzy
        :param oper: AND ou OR + semantica do operador de agregacao do antecedente. Matlab: AND or OR method
        :type oper: EnumMamdaniOper
        :param impl: Semantica da regra (Implicacao). Matlab: Implication
        :type impl: EnumMamdaniImpl
        :param aggr: Operador de agregacao das regras. Matlab: Aggregation
        :type aggr: EnumMamdaniAggr
        :param dfzz: Metodo de Defuzzificacao. Matlab: Defuzzification
        :type dfzz: EnumMamdaniDfzz
        :param out: passar o output (Y)
        :type out: FuzzyUniverse
        :param kwargs: passar os inputs (Xi)
        """

        self.__input = {}
        self.__output = out
        if out is None:
            raise AttributeError

        # Processar todos universos adicionados a esse modelo
        for var in kwargs:
            # Apenas universos fuzzy sao aceitos como um input/output
            if not isinstance(kwargs[var], FuzzyUniverse):
                raise TypeError
            # Demais serao apenas um input
            self.__input[var] = kwargs[var]

        self.__oper = oper
        self.__impl = impl
        self.__aggr = aggr
        self.__dfzz = dfzz

        # Criar um banco de regras para esse modelo
        self.__rules = []

    def create_rule(self, out='', **kwargs):
        """
        Criar uma regra para esse modelo
        :param out:
        :type out: str
        :param kwargs:
        :return:
        """

        # Precisamos de um label de  selecao para cada input + o output
        if len(kwargs) != len(self.__input):
            raise AttributeError

        funcs = {}
        for var in kwargs:
            label = str(kwargs[var])
            funcs[var] = self.__input[var][label]

        antecedent = FuzzyRelation(kind=self.__oper, **funcs)
        consequent = self.__output[str(out)]

        rule = MamdaniRule(antecedent, consequent, kind=self.__impl)
        self.__rules.append(rule)

    def __call__(self, *args, **kwargs):

        make_plot = args[0] if len(args) > 0 else False


        # Eh necessario um valor para cada input
        if len(kwargs) != len(self.__input):
            raise AttributeError

        # Dominio do universo do consequente
        domain = self.__output.domain

        # ---------------------------------------------------------- #
        # 1) Computar as regras a partir das entradas

        n_antc = len(self.__input)
        r_rules = []

        if make_plot:
            fig = plt.figure(figsize=(8, 8))
            axarr = fig.subplots(len(self.__rules) + 1, 2 + n_antc)

        iter = 0
        for rule in self.__rules:
            # Computar a regra
            r_rule = rule(**kwargs)
            r_rules.append(r_rule)

            if make_plot:
                # Antecedente
                iter_antc = 0
                for key in rule.getAntecedent()._funcs:
                    func = rule.getAntecedent()._funcs[key]
                    f_height = func.func(x=kwargs[key])

                    f_domain = func._universe.domain.points
                    axarr[iter, iter_antc].plot(f_domain, func.gen())
                    axarr[iter, iter_antc].plot([kwargs[key], kwargs[key]], [0, 1])
                    axarr[iter, iter_antc].plot([min(f_domain), max(f_domain)], [f_height, f_height])

                    iter_antc += 1

                # Consequente
                axarr[iter, n_antc].plot(domain.points, self.__rules[iter - 1].getConsequent().gen())
                # Resultado
                axarr[iter, n_antc + 1].plot(domain.points, r_rule)
                axarr[iter, n_antc + 1].set_ylim(0, 1)

            iter += 1

        result_index = iter

        # ---------------------------------------------------------- #
        # 2) Unir as regras

        union = []
        for iter in range(len(r_rules[0])):
            values = []
            for rule in r_rules:
                values.append(rule[iter])

            # escolher operador de uniao
            if self.__aggr == EnumMamdaniAggr.Max:
                union.append(max(values))
            elif self.__aggr == EnumMamdaniAggr.Sum:
                union.append(sum(values) - np.multiply(*values))
            else:
                union.append(max(values))

        if make_plot:
            axarr[result_index, n_antc + 1].plot(domain.points, union)
            axarr[result_index, n_antc + 1].set_ylim(0, 1)
            plt.show()

        # ---------------------------------------------------------- #
        # 3) Defuzzificar

        if self.__dfzz == EnumMamdaniDfzz.CoS:
            # Center of Sums
            pass

        if self.__dfzz == EnumMamdaniDfzz.CoG:
            # Center of Gravity
            sum1 = sum2 = 0
            iter = 0
            for x in domain.points:
                sum1 += x * union[iter]
                sum2 += union[iter]
                iter += 1
            return sum1/sum2 if sum2 != 0 else 0

        if self.__dfzz == EnumMamdaniDfzz.BoA:
            # Bisector of Area
            pass

        if self.__dfzz == EnumMamdaniDfzz.FoM:
            # First of Maxima
            maxima = max(union)
            iter = 0
            for x in domain.points:
                if union[iter] >= maxima:
                    return x
                iter += 1

        if self.__dfzz == EnumMamdaniDfzz.LoM:
            # Last of Maxima
            maxima = max(union)
            iter = 0
            last = domain.points[0]
            for x in domain.points:
                if union[iter] >= maxima:
                    last = x
                iter += 1
            return last

        if self.__dfzz == EnumMamdaniDfzz.MoM:
            # Mean of Maxima
            maxima = max(union)
            iter = 0
            points = []
            for x in domain.points:
                if union[iter] >= maxima:
                    points.append(x)
                iter += 1
            return sum(points)/len(points) if len(points) > 0 else 0

        return 0

# ======================================================================================================================
