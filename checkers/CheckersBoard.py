import numpy as np
from checkers.consts import *
from checkers.bb_utils import *
from checkers.BBManager import BBManager

class CheckersBoard:

    def __init__(self, data_folder: str):
        self.np_board = np.zeros((8,4))
        self.np_board[0:3, :] = 1
        self.np_board[5:8, :] = -1
        self.W = W_START
        self.B = B_START
        self.K = 0
        self.bb_m = BBManager()

        self.dict_wm, self.dict_bm, self.dict_wj, self.dict_bj = self.bb_m.load_dicts(data_folder)
        
    
    def _white_moves(self) -> Tuple[int, int, int, int]:
        return self.bb_m.white_moves(self.W, self.B, self.K)

    def _black_moves(self) -> Tuple[int, int, int, int]:
        return self.bb_m.black_moves(self.W, self.B, self.K)

    def _white_jumps(self) -> Tuple[int, int, int, int]:
        return self.bb_m.white_jumps(self.W, self.B, self.K)
    
    def _black_jumps(self) -> Tuple[int, int, int, int]:
        return self.bb_m.black_jumps(self.W, self.B, self.K)

    def get_metrics(self)-> np.ndarray:

        capped, potential, men, kings, mid, capturables, won = self.bb_m.bb_scores(self.W, self.B, self.K)
        score = 4*capped + potential + men + 3*kings + capturables + 2*mid + 100*won

        if score < 0:
            return np.array([-1, capped, potential, men, kings,  mid, won])
        else:
            return np.array([1, capped, potential, men, kings,  mid, won])

    def as_np(self) -> np.ndarray:
        pass

