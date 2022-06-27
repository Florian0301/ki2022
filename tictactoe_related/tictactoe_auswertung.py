from aufgabe3 import TicTacToe
from random import choice


class TicTacToeKI(TicTacToe):
    def __init__(self) -> None:
        super().__init__()
        self.n = 100000
        self.is_player_ki = {sym: True for sym in self.player_symbols}
        self.auswertung = {sym: 0 for sym in self.player_symbols}
        self.auswertung["tie"] = 0

    def get_and_set_move(self, player_symbol) -> None:
        # get a move until valid and then set it
        move = choice(
            [x for x in "123456789" if self.is_valid_move(x)]
        )
        self.board[move] = player_symbol

    def reset_board(self) -> None:
        self.board = {c: " " for c in "123456789"}

    def start(self) -> None:
        # begin the game
        try:
            for x in range(self.n):
                self.reset_board()
                i = 0
                while True:
                    curr_symbol = self.player_symbols[i]
                    self.get_and_set_move(curr_symbol)
                    i = (i + 1) % 2
                    if self.is_winner(curr_symbol):
                        print(f"{curr_symbol} won!")
                        self.auswertung[curr_symbol] += 1
                        break
                    if self.is_board_full():
                        self.auswertung["tie"] += 1
                        print("Tie!")
                        break
            print(f"n  : {self.n}")
            print(f"X  : {self.auswertung.get('X')/self.n}")
            print(f"O  : {self.auswertung.get('O')/self.n}")
            print(f"Tie: {self.auswertung.get('tie')/self.n}")
        except KeyboardInterrupt:
            print("Bye!")


if __name__ == "__main__":
    tttki = TicTacToeKI()
    tttki.start()
