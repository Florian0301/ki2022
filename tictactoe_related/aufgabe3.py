class TicTacToe(object):
    def __init__(self) -> None:
        self.board = {c: " " for c in "123456789"}
        self.player_symbols = ["X", "O"]

    def show_board(self) -> None:
        # print the current status of the board
        print()
        for i, val in enumerate(self.board.values()):
            print(f"{val}", end="")
            if(i % 3 != 2):
                print("|", end="")
            if(i % 3 == 2 and i != 8):
                print("\n-+-+-")
        print("\n")

    def get_and_set_move(self, player_symbol) -> None:
        # get a move until valid and then set it
        if player_symbol not in self.player_symbols:
            exit("Invalid Symbol!")
        while True:
            move = input(f"{player_symbol} Move: ")
            if self.is_valid_move(move):
                self.board[move] = player_symbol
                break
            print("Invalid Move!")

    def is_valid_move(self, move) -> bool:
        # check if a move is valid
        return move in "123456789" and self.board.get(move) == " "

    def is_board_full(self) -> bool:
        # check if all spots are filled with symbols
        return " " not in self.board.values()

    def is_winner(self, player_symbol) -> bool:
        # check if player with symbol has three in a row
        board_copy = [
            [self.board.get("1"), self.board.get("2"), self.board.get("3")],
            [self.board.get("4"), self.board.get("5"), self.board.get("6")],
            [self.board.get("7"), self.board.get("8"), self.board.get("9")]
        ]

        # horizontal
        for zeile in range(len(board_copy)):
            if(board_copy[zeile][0] == board_copy[zeile][1] == board_copy[zeile][2] == player_symbol):
                return True

        # vertikal
        for spalte in range(len(board_copy[zeile])):
            if(board_copy[0][spalte] == board_copy[1][spalte] == board_copy[2][spalte] == player_symbol):
                return True

        # diagonal
        if(board_copy[0][0] == board_copy[1][1] == board_copy[2][2] == player_symbol):
            return True
        if(board_copy[0][2] == board_copy[1][1] == board_copy[2][0] == player_symbol):
            return True

        return False

    def start(self) -> None:
        # begin the game
        try:
            self.show_board()
            i = 0
            while True:
                curr_symbol = self.player_symbols[i]
                self.get_and_set_move(curr_symbol)
                self.show_board()
                i = (i + 1) % 2
                if self.is_winner(curr_symbol):
                    print(f"{curr_symbol} won!")
                    break
                if self.is_board_full():
                    print("Board full!")
                    break
            print("GG")
        except KeyboardInterrupt:
            print("Bye!")


if __name__ == "__main__":
    ttt = TicTacToe()
    ttt.start()
