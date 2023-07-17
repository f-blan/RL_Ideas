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
        movers |= ((not_occ&W_L3R) << 5) & w
        movers |= ((not_occ&W_L5L) << 3) & w

        moves = (w >> 4) & not_occ
        moves |= ((w & W_R3L)>>5) & not_occ
        moves |= ((w & W_R5R)>>3) & not_occ 

        k_movers = 0
        k_moves = 0

        if w_k:
            #forward
            k_movers |= (not_occ << 4) & w_k
            k_movers |= ((not_occ&W_L3R) << 5) & w_k
            k_movers |= ((not_occ&W_L5L) << 3) & w_k
            
            #backward
            k_movers |= (not_occ >> 4) & w_k
            k_movers |= ((not_occ&W_R3L) >> 5) & w_k
            k_movers |= ((not_occ&W_R5R) >> 3) & w_k

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
        movers |= ((not_occ&W_R3L) >> 5) & b
        movers |= ((not_occ&W_R5R) >> 3) & b

        moves = (b << 4) & not_occ
        moves |= ((b & W_L3R)<<5) & not_occ
        moves |= ((b & W_L5L)<<3) & not_occ 

        k_movers = 0
        k_moves = 0

        if b_k:
            #forward
            k_movers |= (not_occ >> 4) & b_k
            k_movers |= ((not_occ&W_R3L) >> 5) & b_k
            k_movers |= ((not_occ&W_R5R) >> 3) & b_k

            #backward
            k_movers |= (not_occ << 4) & b_k
            k_movers |= ((not_occ&W_L3R) << 5) & b_k
            k_movers |= ((not_occ&W_L5L) << 3) & b_k

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
        moves = 0
        w = self.W ^ self.K

        tmp = (not_occ<<4) & self.B
        movers |= (W_L3R&w)&(tmp<<3)
        movers |= (W_R3L&w)&(tmp<<5)

        tmp = ((W_L5L&not_occ)<<3)&self.B
        movers|= (W_R3&w)&(tmp<<4)

        tmp = ((W_L3R&not_occ)<<5)&self.B
        movers|= (W_L3&w)&(tmp<<4)

        tmp = (self.B >> 4)&not_occ
        moves |= ((W_R3L&w)>>9)&tmp
        moves |= ((W_L3R&w)>>7)&tmp

        tmp = ((W_L3R&self.B)>>3) & not_occ
        moves |= ((w&W_R3)>>7) &tmp

        tmp = ((W_R3L&self.B)>>5) &not_occ
        moves |= ((w&W_L3)>>9) & tmp

        k_movers = 0
        k_moves = 0
        if w_k:
            #forward
            tmp = (not_occ<<4) & self.B
            k_movers |= (W_L3R&w_k)&(tmp<<3)
            k_movers |= (W_R3L&w_k)&(tmp<<5)

            tmp = ((W_L5L&not_occ)<<3)&self.B
            k_movers|= (W_R3&w_k)&(tmp<<4)

            tmp = ((W_L3R&not_occ)<<5)&self.B
            k_movers|= (W_L3&w_k)&(tmp<<4)

            #backward
            tmp = (not_occ>>4) & self.B
            k_movers |= (W_R3L&w_k)&(tmp>>3)
            k_movers != (W_L3R&w_k)&(tmp>>5)

            tmp = ((W_R5R&not_occ)>>3)&self.B
            k_movers |= (W_L3&w_k)&(tmp>>4)

            tmp = ((W_R3L&not_occ)>>5)&self.B
            k_movers |= (W_R3&w_k)&(tmp>>4)

            #moves forward
            tmp = (self.B >> 4)&not_occ
            k_moves |= ((W_R3L&w_k)>>9)&tmp
            k_moves |= ((W_L3R&w_k)>>7)&tmp

            tmp = ((W_L3R&self.B)>>3) & not_occ
            k_moves |= ((w&W_R3)>>7) &tmp

            tmp = ((W_R3L&self.B)>>5) &not_occ
            k_moves |= ((w&W_L3)>>9) & tmp

            #moves bakward
            tmp = (self.B << 4)&not_occ
            k_moves |= ((W_L3R&w_k)<<9)&tmp
            k_moves |= ((W_R3L&w_k)<<7)&tmp

            tmp = ((W_R3L&self.B)<<3) & not_occ
            k_moves |= ((w&W_L3)<<7) &tmp

            tmp = ((W_L3R&self.B)<<5) &not_occ
            k_moves |= ((w&W_R3)<<9) & tmp

            
        return movers, moves, k_movers, k_moves
    
    def get_metrics(self, board: np.ndarray)->np.ndarray:
        pass

    def as_np(self) -> np.ndarray:
        pass

