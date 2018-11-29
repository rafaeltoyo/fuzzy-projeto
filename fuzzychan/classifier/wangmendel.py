# ======================================================================================================================
#   Modelo Wang Mendel de classificacoa Fuzzy
# ----------------------------------------------------------------------------------------------------------------------
#   Autor: Rafael Hideo Toyomoto
#   28/11/2018
# ======================================================================================================================


class WangMendelClassifier(object):

    from enum import Enum

    import numpy as np
    import matplotlib.pyplot as plt
    from typing import Dict, Any, List, Union

    from fuzzychan.base import FuzzyUniverse, MembershipFunc, FuzzySet, Domain
    from fuzzychan.relation import FuzzyRelation
    from fuzzychan.rule import fuzzy_rule_compute
    from fuzzychan.operator import FuzzyOperator

    from fuzzychan.rule import EnumRule as EnumMamdaniImpl
    from fuzzychan.relation import EnumRelation
    from fuzzychan.relation import EnumRelation as EnumMamdaniAggr
    from fuzzychan.operator import EnumFuzzyOper

    __input = None  # type: Dict[str, FuzzyUniverse]

    def __init__(self,
                 **kwargs):
        """
        Modelo Wang-Mendel de classificacao Fuzzy
        :param kwargs: passar os inputs (Xi)
        """
        from fuzzychan.base import FuzzyUniverse

        self.__input = {}
        self.__rule = {}

        # Processar todos universos adicionados a esse modelo
        for var in kwargs:
            # Apenas universos fuzzy sao aceitos como um input/output
            if not isinstance(kwargs[var], FuzzyUniverse):
                raise TypeError
            # Demais serao apenas um input
            self.__input[var] = kwargs[var]

    def __call__(self, *args, **kwargs):
        # TODO: classificar entrada baseado no treinamento
        pass

    def train(self, data, out_label='cls', oper=EnumRelation.Min):

        from fuzzychan.base import FuzzyUniverse, FuzzySet

        rules = []

        # Processar todos dados passados
        for row in data:
            rule = []

            # Acessar todos label de universo
            for key_universe in self.__input.keys():

                universe = self.__input[key_universe]  # type: FuzzyUniverse

                elem = {}
                elem['name'] = key_universe
                elem['value'] = row[key_universe]

                # Acessar todos conjuntos do universo
                for key_set in universe:

                    fuzzy_set = universe[key_set]  # type: FuzzySet
                    pert_val = fuzzy_set.func(x=row[key_universe])

                    if 'label' not in elem.keys() or elem['mship'] < pert_val:
                        elem['label'] = key_set
                        elem['mship'] = pert_val

                rule.append(elem)

            txt = ' E '.join((elem['name'] + ' eh ' + elem['label']) for elem in rule) + ' ENTAO ' + row[out_label]
            rules.append({
                'antecedent': rule,
                'consequent': row[out_label],
                'txt': txt
            })

        print('\n'.join(str(rule['txt']) for rule in rules))

        for i in range(len(rules)):
            for j in range(i+1, len(rules)):
                print(i, j)
                # TODO: remover redundancia
                # TODO: remover contradicao

        print('\n'.join(str(rule['txt']) for rule in rules))

        return rules



# ======================================================================================================================
