from kb import *


if __name__ == "__main__":
    kb = KnowledgeBase()
    la = LogicApplier()
    lp = LogicParser()

    la.print_truth_table(lp.parse("a => b"))
    la.print_truth_table(lp.parse("not a or b"))
    la.print_truth_table(lp.parse("not b => not a"))
    la.print_truth_table(lp.parse("a => b <=> not a or b"))
    la.print_truth_table(lp.parse("not a or b <=> not b => not a"))
    trenner()

    la.print_truth_table(lp.parse("(a or b or c) and (d or not a or e)"))
    la.print_truth_table(lp.parse("b or c or d or e"))
    la.print_truth_table(lp.parse("(a or b or c) and (d or not a or e) <=> (b or c or d or e)"))
    trenner()
    la.print_truth_table(lp.parse("(a or b) and (not a or c)"))
    la.print_truth_table(lp.parse("b or c"))

    trenner()
    kb.tell("a or b")
    kb.tell("not a or c")
    print(la.tt_entails(kb.kb_to_expression(), lp.parse("b or c")))

    a = lp.parse("(a or b or c) and (d or not a or e)")
    b = lp.parse("b or c or d or e")
    print(la.tt_entails(a, b))

    a = lp.parse("(a => b) and a")
    b = lp.parse("b")
    print(la.tt_entails(a, b))

    a = lp.parse("a or not b or not c")
    b = lp.parse("(b and c) => a")
    print(la.tt_entails(a, b))
    la.print_truth_table(a)
    la.print_truth_table(b)