from checkers.AI.CheckersAI import CheckersAI
from checkers.logic.CheckersBoard import CheckersBoard
from checkers.logic.MoverBoard import MoverBoard
import numpy as np

class SimpleAI(CheckersAI):
    def __init__(self, color: int):
        super().__init__(color)
    
    def get_next_state(self) -> MoverBoard:
        boards = self.board.generate_next()
        return MoverBoard(board=boards[np.random.randint(0, len(boards))])