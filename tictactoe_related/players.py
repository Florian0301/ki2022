from random import choice
from typing import Dict, Tuple
from numpy import argmax
from ttt_helper import *


class PlayerInterface(object):
    """ Player - Kann einen Move machen """

    def __init__(self, player_symbol: str, board: Dict[str, str]) -> None:
        self.player_symbol = player_symbol
        self.board = board
        self.syms = ["X", "O"]

    def get_move(self) -> str:
        pass


class HumanPlayer(PlayerInterface):
    """ Human Player - Spieler darf selber spielen """

    def get_move(self) -> str:
        while True:
            move = input(f"Dein Move: ")
            if is_valid_move(self.board, move):
                return move
            print("Invalid Move!")


class RandomNPC(PlayerInterface):
    """ Random NPC - Setzt einen Random Move """

    def get_move(self) -> str:
        return choice([move for move in self.board.keys() if is_valid_move(self.board, move)])


class MinimaxNPC(PlayerInterface):
    """ Minimax NPC - Spielt nach dem Minimax Algorithmus """

    def __init__(self, player_symbol: str, board: Dict[str, str]) -> None:
        super().__init__(player_symbol, board)
        self.other_player_sym = [s for s in self.syms if s != player_symbol][0]

    def terminal_test(self, state: Dict[str, str]) -> bool:
        """ Endzustand? """
        return is_board_full(state) or True in [is_winner(state, sym) for sym in self.syms]

    def utility(self, state: Dict[str, str]) -> int:
        if is_winner(state, self.player_symbol):
            return 1
        if is_winner(state, self.other_player_sym):
            return -1
        if is_board_full(state):
            return 0

        raise Exception("Something is wrong")

    def max_value(self, state: Dict[str, str]) -> int:
        if self.terminal_test(state):
            return self.utility(state)
        v = -2
        for action in actions(state):
            v = max(v, self.min_value(result(state, action)))
        return v

    def min_value(self, state: Dict[str, str]) -> int:
        if self.terminal_test(state):
            return self.utility(state)
        v = 2
        for action in actions(state):
            v = min(v, self.max_value(result(state, action)))
        return v

    def get_move(self) -> str:
        return actions(self.board)[argmax([self.min_value(result(self.board, action)) for action in actions(self.board)])]


class AlphaBetaNPC(MinimaxNPC):
    """ AlphaBeta NPC - Spielt nach dem AlphaBetaPruning Algorithmus.
    Min- und Max_value returnen Value, Move Tuple """

    def max_value(self, state: Dict[str, str], alpha: int, beta: int) -> Tuple[int, str]:
        if self.terminal_test(state):
            return self.utility(state), None
        v = -2
        for action in actions(state):
            v2, a2 = self.min_value(result(state, action), alpha, beta)
            if v2 > v:
                v, move = v2, action
                alpha = max(alpha, v)
            if v >= beta:
                return v, move
        return v, move

    def min_value(self, state: Dict[str, str], alpha: int, beta: int) -> Tuple[int, str]:
        if self.terminal_test(state):
            return self.utility(state), None
        v = 2
        for action in actions(state):
            v2, a2 = self.max_value(result(state, action), alpha, beta)
            if v2 < v:
                v, move = v2, action
                beta = min(beta, v)
            if v <= alpha:
                return v, move
        return v, move

    def get_move(self) -> str:
        value, move = self.max_value(self.board, -2, 2)
        return move
