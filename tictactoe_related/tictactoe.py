from typing import Dict
from aufgabe3 import TicTacToe as ttt_base
from players import AlphaBetaNPC, HumanPlayer, MinimaxNPC, RandomNPC, PlayerInterface


class TicTacToe(ttt_base):
    def __init__(self) -> None:
        super().__init__()
        self.moves = []
        self.sym_to_type: Dict[str, PlayerInterface] = {}
        for sym in self.player_symbols:
            while self.sym_to_type.get(sym) == None:
                choice = input(
                    f"Welche Art ist {sym} [h -> Human, z -> Zufalls NPC, m -> Minimax, a -> AlphaBeta]: ")
                if(choice == "h"):
                    self.sym_to_type[sym] = HumanPlayer(sym, self.board)
                elif(choice == "z"):
                    self.sym_to_type[sym] = RandomNPC(sym, self.board)
                elif(choice == "m"):
                    self.sym_to_type[sym] = MinimaxNPC(sym, self.board)
                elif(choice == "a"):
                    self.sym_to_type[sym] = AlphaBetaNPC(sym, self.board)
                else:
                    print("Try again you silly goose!")

    def get_and_set_move(self, player_symbol: str) -> None:
        move = self.sym_to_type.get(player_symbol).get_move()
        print(f"{player_symbol} Move: {move}")
        self.board[move] = player_symbol
        self.moves.append({player_symbol: move})


if __name__ == "__main__":
    ttt = TicTacToe()
    ttt.start()
    print(f"Moves: {ttt.moves}")
