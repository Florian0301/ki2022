from nltk.sem.logic import *
from kb import KnowledgeBase, LogicApplier


class WumpusKB(KnowledgeBase):
    def __init__(self) -> None:
        super().__init__()
        self.tell("not P11")
        self.tell("P12 => B11 and B22 and B13")
        self.tell("P21 => B11 and B22 and B31")
        self.tell("P22 => B12 and B21 and B23 and B32")
        self.tell("P31 => B21 and B32 and B41")
        self.tell("P13 => B12 and B23 and B14")
        self.tell("B12 => P13 or P22 or P11")


if __name__ == "__main__":
    wumpus = WumpusKB()
    la = LogicApplier()
    lp = LogicParser()

    wumpus.tell("not B11")
    wumpus.tell("not B21")
    wumpus.tell("B12")

    wumpus.parsed_to_tree(wumpus.kb_to_expression()).pretty_print(unicodelines=True)

    # Erwartet: True False alternierend
    print(la.tt_entails(wumpus.kb_to_expression(), lp.parse("not P22")))
    print(la.tt_entails(wumpus.kb_to_expression(), lp.parse("P22")))
    
    print(la.tt_entails(wumpus.kb_to_expression(), lp.parse("P13")))
    print(la.tt_entails(wumpus.kb_to_expression(), lp.parse("not P13")))
    
    print(la.tt_entails(wumpus.kb_to_expression(), lp.parse("not P31")))
    print(la.tt_entails(wumpus.kb_to_expression(), lp.parse("P31")))
