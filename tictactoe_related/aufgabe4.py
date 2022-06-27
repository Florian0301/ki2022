from time import sleep
from aufgabe3 import TicTacToe
from random import choice


class TicTacToeKI(TicTacToe):
    def __init__(self) -> None:
        super().__init__()
        self.is_player_ki = {}
        for sym in self.player_symbols:
            while self.is_player_ki.get(sym) == None:
                is_ki = input(f"Ist Player {sym} eine KI? [y/n]: ")
                if(is_ki == "y"):
                    self.is_player_ki[sym] = True
                elif(is_ki == "n"):
                    self.is_player_ki[sym] = False
                else:
                    print("y/n! :)")

    def get_and_set_move(self, player_symbol) -> None:
        # get a move until valid and then set it
        if player_symbol not in self.player_symbols:
            exit("Invalid Symbol!")
        if(self.is_player_ki.get(player_symbol)):
            # "KI" ;)
            print(f"{player_symbol} is thinking...")
            sleep(1)
            move = choice(
                [x for x in "123456789" if self.is_valid_move(x)]
            )
            print(f"{player_symbol} Move: {move}")
            self.board[move] = player_symbol
        else:
            # Player
            super().get_and_set_move(player_symbol)


if __name__ == "__main__":
    tttki = TicTacToeKI()
    tttki.start()
