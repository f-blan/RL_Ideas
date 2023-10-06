from checkers.CheckersBoard import CheckersBoard
from typing import List
import numpy as np
import itertools as it
from checkers.bb_utils import print_bb

class MoverBoard(CheckersBoard):
    """
        Expands CheckersBoard: it is the board as seen from the moving player's perspective, regardless of color.
        More convenient for training the models.
        By convention, self.W are the moving pieces
    """

    def __init__(self, data_folder: str, board: CheckersBoard = None):
        super().__init__(data_folder)
        """
        self.np_board = np.zeros((8,4))
        self.np_board[0:3, :] = 1
        self.np_board[5:8, :] = -1
        """
    def reverse(self) -> None:
        tmp = self.W
        
        self.W = self.bb_m.bb_reverse(self.B)
        self.B = self.bb_m.bb_reverse(tmp)
        self.K = self.bb_m.bb_reverse(self.K)
    
    def generate_next(self) -> List[CheckersBoard]:
        movers, moves, k_movers, k_moves = self._white_moves()
        jumpers, jumps, k_jumpers, k_jumps = self._white_jumps()

        ret = []
        
        n=1

        if jumpers != 0 or k_jumpers != 0:
            while n & 0xFFFFFFFF !=0:
                if n & jumpers != 0 or n & k_jumpers !=0:
                    iterator_j = self.dict_wj[n][0] if n&k_jumpers ==0 else it.chain(self.dict_wj[n][0], self.dict_bj[n][0])
                    iterator_m = self.dict_wj[n][1] if n&k_jumpers ==0 else it.chain(self.dict_wj[n][1], self.dict_bj[n][1])
                    for j,m in zip(iterator_j, iterator_m):
                        if j&jumps!=0 and (self.B ^ self.K) & ~m != 0:
                            to_add = CheckersBoard()
                            to_add.W, to_add.B, to_add.K = self.bb_m.apply_jump(self.W, n, j, m, self.B, self.K, False)
                            ret.append(to_add)
                        elif j&k_jumps != 0 and self.B & ~m != 0:
                            to_add = CheckersBoard()
                            to_add.W, to_add.B, to_add.K = self.bb_m.apply_jump(self.W, n, j, m, self.B,  self.K, True)
                            ret.append(to_add)
                n=n<<1
            return ret
    
        while n & 0xFFFFFFFF != 0:
            if n & movers != 0 or n & k_movers != 0:
                iterator = self.dict_wm[n] if n & k_movers == 0 else it.chain(self.dict_wm[n], self.dict_bm[n])
                for m in iterator:
                    if m & moves != 0 or m & k_moves != 0:
                        to_add = CheckersBoard()
                        to_add.W, to_add.K = self.bb_m.apply_move(self.W, n, m, self.K, n& k_movers != 0)
                        to_add.B = self.B
                        ret.append(to_add)
            n = n<<1

        return ret




