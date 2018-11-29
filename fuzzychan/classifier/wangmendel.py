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
            txt += '(' + str(self.__operation(oper, rule)) + ')'
            rules.append({
                'antecedent': rule,
                'consequent': row[out_label],
                'txt': txt
            })

        print('\n'.join(str(rule['txt']) for rule in rules))

        import copy as cp
        c_rules = cp.deepcopy(rules)

        for i in range(len(rules)):

            if rules[i] not in c_rules:
                continue

            for j in range(i+1, len(rules)):

                if rules[j] not in c_rules:
                    continue

                #print(str(rules[i]["txt"]) + " -> " + str(rules[j]["txt"]))

                if min([(1 if rules[i]['antecedent'][k]['label'] == rules[j]['antecedent'][k]['label'] else 0) for k in range(len(rules[i]['antecedent']))]) == 1:

                    mship_i = self.__operation(oper, rules[i]['antecedent'])
                    mship_j = self.__operation(oper, rules[j]['antecedent'])

                    # Remover redundancias e contradicoes -> sempre que o antecedente for igual, havera um dos casos
                    if mship_i > mship_j:
                        c_rules.remove(rules[j])
                        continue
                    else:
                        c_rules.remove(rules[i])
                        break

        print('-' * 80)
        print('\n'.join(str(rule['txt']) for rule in c_rules))

        return rules

    def __operation(self, oper, rule):

        import numpy as np
        from fuzzychan.relation import EnumRelation

        elems = [elem['mship'] for elem in rule]

        if oper == EnumRelation.Min:
            return min(elems)
        elif oper == EnumRelation.Prod:
            return np.prod(elems)
        return 0


# ======================================================================================================================
