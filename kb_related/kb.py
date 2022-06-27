from pprint import pprint
from nltk.sem.logic import *
from nltk.sem import Model, Valuation, Assignment
from nltk.tree import Tree
from typing import Dict, List, Tuple
from copy import deepcopy
from itertools import combinations
from tabulate import tabulate


class KnowledgeBase(object):
    def __init__(self) -> None:
        self.sentences: List[Expression] = []
        self.logic_parser: LogicParser = LogicParser()

    def parsed_to_tree(self, expression) -> Tree:
        if isinstance(expression, BooleanExpression):
            baum = Tree(expression.getOp(),
                        [self.parsed_to_tree(expression.first),
                        self.parsed_to_tree(expression.second)])
            return baum
        if isinstance(expression, NegatedExpression):
            return Tree("-", [self.parsed_to_tree(expression.term)])
        return expression

    def print_sentences(self) -> None:
        pprint(self.sentences)

    def print_sentences_as_tree(self) -> None:
        for sentence in self.sentences:
            print(sentence, end="\n\n")
            self.parsed_to_tree(sentence).pretty_print(unicodelines=True)

    def kb_to_expression(self) -> Expression:
        if len(self.sentences) == 0:
            return None
        if len(self.sentences) == 1:
            return self.sentences[0]
        res = AndExpression(self.sentences[0], self.sentences[1])
        for i in range(2, len(self.sentences)):
            res = AndExpression(res, self.sentences[i])

        return res

    def tell(self, new_sentence: str) -> None:
        try:
            parsed = self.logic_parser.parse(new_sentence)
        except Exception as e:
            print("Try again!")
            print(e)
            return

        self.sentences.append(parsed)


class LogicApplier(object):
    def __init__(self) -> None:
        self.kb = KnowledgeBase()

    def pl_true(self, expression: Expression, model: Dict[str, bool]) -> bool:
        if isinstance(expression, BooleanExpression):
            a = self.pl_true(expression.first, model)
            b = self.pl_true(expression.second, model)
            if isinstance(expression, OrExpression):
                return a or b
            if isinstance(expression, AndExpression):
                return a and b
            if isinstance(expression, ImpExpression):
                return not a or b
            if isinstance(expression, IffExpression):
                return a and b or not a and not b
        if isinstance(expression, NegatedExpression):
            return not self.pl_true(expression.term, model)
        if isinstance(expression, AbstractVariableExpression):
            return model[expression.variable.name]

        raise Exception("Something went wrong!", expression, model)

    def pl_true_nltk(self, expression: Expression, model: List[Tuple[str, bool]]) -> bool:
        val = Valuation(model)
        dom = val.domain
        g = Assignment(dom)
        m = Model(dom, val)

        return m.satisfy(expression, g)

    def tt_entails(self, kb_sentence: Expression, sentence: Expression):
        symbols = set()
        if isinstance(kb_sentence, AbstractVariableExpression):
            symbols.add(kb_sentence.variable.name)
        else:
            leaves = self.kb.parsed_to_tree(kb_sentence).leaves()
            for x in leaves:
                symbols.add(x.variable.name)

        if isinstance(sentence, AbstractVariableExpression):
            symbols.add(sentence.variable.name)
        else:
            leaves = self.kb.parsed_to_tree(sentence).leaves()
            for x in leaves:
                symbols.add(x.variable.name)

        return self.tt_check_all(kb_sentence, sentence, list(symbols), {})

    def tt_check_all(self, kb_sentence: Expression, sentence: Expression, symbols: List[str], model: Dict[str, bool]) -> bool:
        if not symbols:
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

    def print_truth_table(self, expression: Expression) -> None:
        symbols = set()
        if isinstance(expression, IndividualVariableExpression):
            symbols.add(expression.variable.name)
        else:
            leaves = self.kb.parsed_to_tree(expression).leaves()
            for x in leaves:
                symbols.add(x.variable.name)
        symbols = sorted(symbols)

        combs = []
        for i in range(0, len(symbols)+1):
            combs.extend(list(combinations(symbols, i)))

        model = {x: None for x in symbols}
        table = []
        for comb in combs:
            for sym in symbols:
                if sym in comb:
                    model[sym] = True
                else:
                    model[sym] = False
            row = [int(x) for x in model.values()]
            model_as_list = [(key, value) for key, value in model.items()]
            row.append(int(self.pl_true(expression, model)))
            row.append(int(self.pl_true_nltk(expression, model_as_list)))
            table.append(row)
        header = symbols
        header.append("Self")
        header.append("NLTK")
        print(expression)
        print(tabulate(table, headers=header, tablefmt="fancy_grid"))
        return table


def trenner():
    print("\n" + "=-" * 80 + "=\n")


if __name__ == "__main__":
    kb = KnowledgeBase()
    la = LogicApplier()
    lp = LogicParser()
    kb.tell(r"(a and c) => (b or d)")
    kb.tell(r"(a and c) <=> (b or d)")
    kb.tell(r"(a => c) <=> (b => d)")
    kb.tell(r"(a and b) <=> not (not a or not b)")
    kb.tell(r"((a => b) and (b => c)) => (a => c)")
    kb.print_sentences()
    trenner()

    kb.print_sentences_as_tree()
    trenner()

    kb.parsed_to_tree(kb.kb_to_expression()).pretty_print(unicodelines=True)
    trenner()

    print(la.tt_entails(kb.kb_to_expression(), lp.parse("a")))
    trenner()

    la.print_truth_table(kb.kb_to_expression())
