from nltk.sem.logic import LogicParser
from kb import KnowledgeBase


if __name__ == "__main__":
    lp = LogicParser()
    kb = KnowledgeBase()
    # Zum Erstellen des Baumes
    aussage = r"(a or (b or c)) and (a or b or not c) and ( not a or b or c) and ( not a or not b or c)"
    print(f"{aussage = }")
    print(lp.parse(aussage))
    kb.parsed_to_tree(lp.parse(aussage)).pretty_print(unicodelines=True)

    # Zum Testen der Hierarchie
    aussage = r"a or b and c <=> d => not e"
    print(f"{aussage = }")
    kb.parsed_to_tree(lp.parse(aussage)).pretty_print(unicodelines=True)
    aussage = r"a or b and c => d <=> not e"
    print(f"{aussage = }")
    kb.parsed_to_tree(lp.parse(aussage)).pretty_print(unicodelines=True)
    aussage = r"a <=> b => c or d and not e"
    print(f"{aussage = }")
    kb.parsed_to_tree(lp.parse(aussage)).pretty_print(unicodelines=True)
