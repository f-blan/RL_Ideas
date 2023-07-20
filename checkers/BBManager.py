from checkers.consts import *
from typing import Tuple, Dict
import numpy as np
import os
import json, codecs

class BBManager:
    def black_jumps(self, W: int, B: int, K: int) -> Tuple[int, int, int, int]:
        not_occ = ~(W | B)&0xFFFFFFFF
        b_k = B & K
        movers = 0
        moves = 0
        b = B ^ K

        tmp = (not_occ>>4) & W
        movers |= (W_R3L&b)&(tmp>>3)
        movers |= (W_L3R&b)&(tmp>>5)

        tmp = ((W_R5R&not_occ)>>3)&W
        movers|= (W_L3&b)&(tmp>>4)

        tmp = ((W_R3L&not_occ)>>5)&W
        movers|= (W_R3&b)&(tmp>>4)

        tmp = (W << 4)&not_occ
        moves |= ((W_L3R&b)<<9)&tmp
        moves |= ((W_R3L&b)<<7)&tmp

        tmp = ((W_R3L&W)<<3) & not_occ
        moves |= ((b&W_L3)<<7) &tmp

        tmp = ((W_L3R&W)<<5) &not_occ
        moves |= ((b&W_R3)<<9) & tmp

        moves &= 0xFFFFFFFF 

        k_movers = 0
        k_moves = 0
        if b_k:
            #backward
            tmp = (not_occ<<4) & W
            k_movers |= (W_L3R&b_k)&(tmp<<3)
            k_movers |= (W_R3L&b_k)&(tmp<<5)

            tmp = ((W_L5L&not_occ)<<3)&W
            k_movers|= (W_R3&b_k)&(tmp<<4)

            tmp = ((W_L3R&not_occ)<<5)&W
            k_movers|= (W_L3&b_k)&(tmp<<4)

            #forward
            tmp = (not_occ>>4) & W
            k_movers |= (W_R3L&b_k)&(tmp>>3)
            k_movers |= (W_L3R&b_k)&(tmp>>5)

            tmp = ((W_R5R&not_occ)>>3)&W
            k_movers |= (W_L3&b_k)&(tmp>>4)

            tmp = ((W_R3L&not_occ)>>5)&W
            k_movers |= (W_R3&b_k)&(tmp>>4)

            #moves backward
            tmp = (W >> 4)&not_occ
            k_moves |= ((W_R3L&b_k)>>9)&tmp
            k_moves |= ((W_L3R&b_k)>>7)&tmp

            tmp = ((W_L3R&W)>>3) & not_occ
            k_moves |= ((b_k&W_R3)>>7) &tmp

            tmp = ((W_R3L&W)>>5) &not_occ
            k_moves |= ((b_k&W_L3)>>9) & tmp

            #moves forward
            tmp = (W << 4)&not_occ
            k_moves |= ((W_L3R&b_k)<<9)&tmp
            k_moves |= ((W_R3L&b_k)<<7)&tmp

            tmp = ((W_R3L&W)<<3) & not_occ
            k_moves |= ((b_k&W_L3)<<7) &tmp

            tmp = ((W_L3R&W)<<5) &not_occ
            k_moves |= ((b_k&W_R3)<<9) & tmp

            k_moves &= 0xFFFFFFFF 

            
        return movers, moves, k_movers, k_moves

    def white_jumps(self, W: int, B: int, K: int) -> Tuple[int,int,int,int]:
        not_occ = ~(W | B)&0xFFFFFFFF
        w_k = W & K
        movers = 0
        moves = 0
        w = W ^ K

        tmp = (not_occ<<4) & B
        movers |= (W_L3R&w)&(tmp<<3)
        movers |= (W_R3L&w)&(tmp<<5)

        tmp = ((W_L5L&not_occ)<<3)&B
        movers|= (W_R3&w)&(tmp<<4)

        tmp = ((W_L3R&not_occ)<<5)&B
        movers|= (W_L3&w)&(tmp<<4)

        tmp = (B >> 4)&not_occ
        moves |= ((W_R3L&w)>>9)&tmp
        moves |= ((W_L3R&w)>>7)&tmp

        tmp = ((W_L3R&B)>>3) & not_occ
        moves |= ((w&W_R3)>>7) &tmp

        tmp = ((W_R3L&B)>>5) &not_occ
        moves |= ((w&W_L3)>>9) & tmp

        moves&= 0xFFFFFFFF

        k_movers = 0
        k_moves = 0
        if w_k:
            #forward
            tmp = (not_occ<<4) & B
            k_movers |= (W_L3R&w_k)&(tmp<<3)
            k_movers |= (W_R3L&w_k)&(tmp<<5)

            tmp = ((W_L5L&not_occ)<<3)&B
            k_movers|= (W_R3&w_k)&(tmp<<4)

            tmp = ((W_L3R&not_occ)<<5)&B
            k_movers|= (W_L3&w_k)&(tmp<<4)

            #backward
            tmp = (not_occ>>4) & B
            k_movers |= (W_R3L&w_k)&(tmp>>3)
            k_movers |= (W_L3R&w_k)&(tmp>>5)

            tmp = ((W_R5R&not_occ)>>3)&B
            k_movers |= (W_L3&w_k)&(tmp>>4)

            tmp = ((W_R3L&not_occ)>>5)&B
            k_movers |= (W_R3&w_k)&(tmp>>4)

            #moves forward
            tmp = (B >> 4)&not_occ
            k_moves |= ((W_R3L&w_k)>>9)&tmp
            k_moves |= ((W_L3R&w_k)>>7)&tmp

            tmp = ((W_L3R&B)>>3) & not_occ
            k_moves |= ((w_k&W_R3)>>7) &tmp

            tmp = ((W_R3L&B)>>5) &not_occ
            k_moves |= ((w_k&W_L3)>>9) & tmp

            #moves bakward
            tmp = (B << 4)&not_occ
            k_moves |= ((W_L3R&w_k)<<9)&tmp
            k_moves |= ((W_R3L&w_k)<<7)&tmp

            tmp = ((W_R3L&B)<<3) & not_occ
            k_moves |= ((w_k&W_L3)<<7) &tmp

            tmp = ((W_L3R&B)<<5) &not_occ
            k_moves |= ((w_k&W_R3)<<9) & tmp

            k_moves&= 0xFFFFFFFF
            
        return movers, moves, k_movers, k_moves
    
    def black_moves(self, W: int, B: int, K: int) -> Tuple[int, int, int, int]:
        not_occ = ~(W | B)&0xFFFFFFFF
        b_k = B&K
        b = B ^ K

        movers = (not_occ >> 4) & b
        movers |= ((not_occ&W_R3L) >> 5) & b
        movers |= ((not_occ&W_R5R) >> 3) & b

        moves = (b << 4) & not_occ
        moves |= ((b & W_L3R)<<5) & not_occ
        moves |= ((b & W_L5L)<<3) & not_occ 

        moves &= 0xFFFFFFFF 

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
            
            k_moves &= 0xFFFFFFFF 

        return movers, moves, k_movers, k_moves
    
    def white_moves(self, W: int, B: int, K: int) -> Tuple[int, int, int, int]:
        not_occ = ~(W | B)&0xFFFFFFFF
        w_k = W&K
        w = W ^ K

        movers = (not_occ << 4) & w
        movers |= ((not_occ&W_L3R) << 5) & w
        movers |= ((not_occ&W_L5L) << 3) & w

        moves = (w >> 4) & not_occ
        moves |= ((w & W_R3L)>>5) & not_occ
        moves |= ((w & W_R5R)>>3) & not_occ

        moves &= 0xFFFFFFFF 

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

            k_moves&= 0xFFFFFFFF  
        return movers, moves, k_movers, k_moves

    def load_dicts(self, data_folder: str) -> Tuple[Dict, Dict, Dict, Dict]:
        ret_wm = {}
        ret_bm = {}
        ret_wj = {}
        ret_bj = {}

        filename = os.path.join(data_folder, "white_moves.json")
        d = codecs.open(filename, 'r').read()
        d = json.loads(d)

        for k in d:
            ret_wm[k] = np.array(d[k])
        
        filename = os.path.join(data_folder, "black_moves.json")
        d = codecs.open(filename, 'r').read()
        d = json.loads(d)

        for k in d:
            ret_bm[k] = np.array(d[k])

        return ret_wm, ret_bm, ret_wj, ret_bj

    def bb_to_np(w:int, b:int, k:int) -> np.ndarray:
        pass