import numpy as np
from checkers.consts import *
from checkers.bb_utils import *

class CheckersBoard:

    def __init__(self):
        self.np_board = np.zeros((8,4))
        self.np_board[0:3, :] = 1
        self.np_board[5:8, :] = -1
        self.W = W_START
        self.B = B_START
        self.K = 0
    
    def _white_moves(self) -> int:
        not_occ = ~(self.W | self.B)
        w_k = self.W&self.K
        w = self.W ^ self.K

        movers = (not_occ << 4) & w
        movers |= ((not_occ&W_L3) << 3) & w
        movers |= ((not_occ&W_L5) << 5) & w

        moves = (w >> 4) & not_occ
        moves |= ((w & W_R3L)>>5) & not_occ
        moves |= ((w & W_R5R)>>3) & not_occ 

        k_movers = 0
        k_moves = 0

        if w_k:
            k_movers |= (not_occ >> 4) & w_k
            k_movers |= ((not_occ&W_R3) >> 3) & w_k
            k_movers |= ((not_occ&W_R5) >> 5) & w_k

            #forward
            k_moves = (w_k >> 4) & not_occ
            k_moves |= ((w_k & W_R3L)>>5) & not_occ
            k_moves |= ((w_k & W_R5R)>>3) & not_occ

            #backward
            k_moves |= (w_k << 4) & not_occ
            k_moves |= ((w_k & W_L3R)<<5) & not_occ
            k_moves |= ((w_k & W_L5L)<<3) & not_occ        
        return movers, moves, k_movers, k_moves

    def _black_moves(self) -> int:
        not_occ = ~(self.W | self.B)
        b_k = self.B&self.K
        b = self.B ^ self.K

        movers = (not_occ >> 4) & b
        movers |= ((not_occ&W_R3) >> 3) & b
        movers |= ((not_occ&W_R5) >> 5) & b

        moves = (b << 4) & not_occ
        moves |= ((b & W_L3R)<<5) & not_occ
        moves |= ((b & W_L5L)<<3) & not_occ 

        k_movers = 0
        k_moves = 0

        if b_k:
            k_movers |= (not_occ >> 4) & b_k
            k_movers |= ((not_occ&W_R3) >> 3) & b_k
            k_movers |= ((not_occ&W_R5) >> 5) & b_k

            #backward
            k_moves = (b_k >> 4) & not_occ
            k_moves |= ((b_k & W_R3L)>>5) & not_occ
            k_moves |= ((b_k & W_R5R)>>3) & not_occ

            #forward
            k_moves |= (b_k << 4) & not_occ
            k_moves |= ((b_k & W_L3R)<<5) & not_occ
            k_moves |= ((b_k & W_L5L)<<3) & not_occ        
        return movers, moves, k_movers, k_moves

    def _white_jumps(self) -> int:
        not_occ = ~(self.W | self.B)
        w_k = self.W & self.K
        movers = 0

        tmp = (not_occ << 4) & self.W
        if tmp:
            movers |= (((tmp&W_L3) << 3) | ((tmp&W_L5) << 5)) & self.W

        tmp = ( ((not_occ&W_L3) << 3) | ((not_occ&W_L5) << 5) ) & self.B
        
        movers |= (tmp << 4) & self.W

        if w_k:
            tmp = (not_occ>> 4) & self.B
            if (tmp): 
                movers |= (((tmp&W_R3) >> 3) | ((tmp&W_R5) >> 5)) & w_k
            tmp = ( ((not_occ&W_R3) >> 3) | ((not_occ&W_R5) >> 5) ) & self.B
            if tmp: 
                movers |= (tmp >> 4) & w_k
        return movers
    
    def get_metrics(self, board: np.ndarray)->np.ndarray:
        pass

    def as_np(self) -> np.ndarray:
        pass

