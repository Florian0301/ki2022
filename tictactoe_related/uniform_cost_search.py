from secrets import choice
from typing import Dict
from queue import Queue
from ttt_helper import actions, is_board_full, is_winner, result, show_board


class QueueItem(object):
    def __init__(self, state: Dict[str, str], cost: int) -> None:
        self.state = state
        self.cost = cost

    def __eq__(self, __o: object) -> bool:
        return self.state == __o.state

    def __hash__(self) -> int:
        """ Absolut illegal, keine Ahnung warum ucs funktioniert """
        return hash(self.cost)


def is_goal(state: Dict[str, str]) -> bool:
    """ Unentschieden -> Volles Board ohne Gewinner"""
    return is_board_full(state) and not True in [is_winner(state, s) for s in ["X", "O"]]


def uniform_cost_search(state: Dict[str, str]) -> QueueItem:
    node = QueueItem(state, 0)
    if(is_goal(node.state)):
        return node

    frontier = Queue()
    frontier.put(node)
    explored = set()

    while True:
        if frontier.empty():
            return None

        node = frontier.get()
        explored.add(node)

        for action in actions(node.state):
            child = QueueItem(result(node.state, action), node.cost+1)
            if child not in explored or child not in frontier.queue:
                if(is_goal(child.state)):
                    return child
                frontier.put(child)


if __name__ == "__main__":
    init_board = {'1': ' ', '2': ' ', '3': ' ',
                  '4': ' ', '5': ' ', '6': ' ',
                  '7': ' ', '8': ' ', '9': ' '}
    init_board[choice(list(init_board.keys()))] = "X"
    show_board(init_board)
    show_board(uniform_cost_search(init_board).state)
