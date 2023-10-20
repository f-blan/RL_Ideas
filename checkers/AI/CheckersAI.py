from checkers.logic.MoverBoard import MoverBoard
from checkers.logic.CheckersBoard import CheckersBoard

class CheckersAI:
    def __init__(self, color: int, model_path: str = None):
        self.color = color
        self.board = MoverBoard()
    
    def copy_state(self, state: MoverBoard) -> None:
        self.board.W, self.board.B, self.board.K = state.W, state.B, state.K

    def get_next_state(self) -> CheckersBoard:
        pass