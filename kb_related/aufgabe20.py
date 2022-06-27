from kb import LogicApplier, KnowledgeBase, trenner
from nltk.sem.logic import *
from typing import Dict, List
from copy import deepcopy
from pprint import pprint


class NewLogicApplier(LogicApplier):
    def __init__(self) -> None:
        super().__init__()
        self.models: Dict[bool, List[Dict[str, bool]]] = {True: [], False: []}

    def tt_check_all(self, kb_sentence: Expression, sentence: Expression, symbols: List[str], model: Dict[str, bool]) -> bool:
        if not symbols:
            # Einzige Aenderung
            self.models[self.pl_true(kb_sentence, model)].append(model)
            if self.pl_true(kb_sentence, model):
                return self.pl_true(sentence, model)
            return True
        p = symbols[0]
        rest = symbols[1:]
        model_with_true = deepcopy(model)
        model_with_true[p] = True
        model_with_false = deepcopy(model)
        model_with_false[p] = False
        return self.tt_check_all(kb_sentence, sentence, rest, model_with_true) and self.tt_check_all(kb_sentence, sentence, rest, model_with_false)


if __name__ == "__main__":
    kb = KnowledgeBase()
    la = LogicApplier()
    lp = LogicParser()
    nla = NewLogicApplier()
    kb.tell("(a or b or c) and (a or b or not c) and (not a or b or c) and (not a or not b or not (not c))")
    kb.tell("(a or b or c) and ((a or b or not c) and (not a or b or c)) and (not a or not b or c)")
    kb.tell("(a or b or c) and (a or not c) and (not a or b or c or d) and (not a or not b or c)")
    kb.tell("(a or b or c) and (a or not c) and (not a or b and c or d) and (not a or not b or c)")
    kb.tell("(a or b or c) and (a or not c) and ((not a or b) and (c or d)) or (not a or not b or c)")
    kb.tell("(a or b or c) and (a or not c) and (((not a or b) and c) or d) and (not a or not b or c)")

    # Tabelle mit altem Algorithmus
    la.print_truth_table(kb.kb_to_expression())

    # Mittels TT_Entails
    trenner()
    nla.tt_entails(kb.kb_to_expression(), kb.kb_to_expression())
    pprint(nla.models)

    trenner()
    a1 = lp.parse("a => b => c => d")
    a2 = lp.parse("a => (b => (c => d))")
    print(a1, la.tt_entails(kb.kb_to_expression(), a1))
    print(a2, la.tt_entails(kb.kb_to_expression(), a2))

    trenner()
    for model in nla.models[True]:
        print(a1, model, la.pl_true(a1, model))
        print(a2, model, la.pl_true(a2, model))
