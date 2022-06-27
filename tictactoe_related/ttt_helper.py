from typing import Dict, List
from copy import deepcopy


def is_board_full(state: Dict[str, str]) -> bool:
    return " " not in state.values()


def is_winner(state: Dict[str, str], player_symbol: str) -> bool:
    state_as_list = [
        [state.get("1"), state.get("2"), state.get("3")],
        [state.get("4"), state.get("5"), state.get("6")],
        [state.get("7"), state.get("8"), state.get("9")]
    ]

    for zeile in range(len(state_as_list)):
        if(state_as_list[zeile][0] == state_as_list[zeile][1] == state_as_list[zeile][2] == player_symbol):
            return True

    for spalte in range(len(state_as_list[zeile])):
        if(state_as_list[0][spalte] == state_as_list[1][spalte] == state_as_list[2][spalte] == player_symbol):
            return True

    if(state_as_list[0][0] == state_as_list[1][1] == state_as_list[2][2] == player_symbol):
        return True
    if(state_as_list[0][2] == state_as_list[1][1] == state_as_list[2][0] == player_symbol):
        return True

    return False


def is_valid_move(state: Dict[str, str], move: str) -> bool:
    return move in state.keys() and state.get(move) == " "


def players(state: Dict[str, str]) -> str:
    """ Wer ist dran? """
    return ["X", "O"][(9 - len(actions(state))) % 2]


def actions(state: Dict[str, str]) -> List[str]:
    """ Bekomme moegliche Zuege """
    return [move for move in state.keys() if state.get(move) == " "]


def result(state: Dict[str, str], action: str) -> Dict[str, str]:
    """ Bekomme naechsten State """
    next_state = deepcopy(state)
    next_state[action] = players(state)
    return next_state


def show_board(state: Dict[str, str]) -> None:
    # print the current status of the board
    print()
    for i, val in enumerate(state.values()):
        print(f"{val}", end="")
        if(i % 3 != 2):
            print("|", end="")
        if(i % 3 == 2 and i != 8):
            print("\n-+-+-")
    print("\n")
