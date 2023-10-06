from checkers.logic.consts import *
from typing import Tuple, Dict
import numpy as np
import os
import json, codecs

class BBManager:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(BBManager, cls).__new__(cls)
        return cls.instance
    
    def black_jumpers_only(self, W: int, B: int, K: int) -> Tuple[int, int]:
        not_occ = ~(W | B)&0xFFFFFFFF
        b_k = B & K
        movers = 0
        b = B ^ K

        tmp = (not_occ>>4) & W
        movers |= (W_R3L&b)&(tmp>>3)
        movers |= (W_L3R&b)&(tmp>>5)

        tmp = ((W_R5R&not_occ)>>3)&W
        movers|= (W_L3&b)&(tmp>>4)

        tmp = ((W_R3L&not_occ)>>5)&W
        movers|= (W_R3&b)&(tmp>>4)

        k_movers = 0

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
        return movers, k_movers

    def black_jumps_only(self, W: int, B: int, K: int) -> Tuple[int, int]:
        not_occ = ~(W | B)&0xFFFFFFFF
        b_k = B & K
        moves = 0
        b = B ^ K

        tmp = (W << 4)&not_occ
        moves |= ((W_L3R&b)<<9)&tmp
        moves |= ((W_R3L&b)<<7)&tmp

        tmp = ((W_R3L&W)<<3) & not_occ
        moves |= ((b&W_L3)<<7) &tmp

        tmp = ((W_L3R&W)<<5) &not_occ
        moves |= ((b&W_R3)<<9) & tmp

        moves &= 0xFFFFFFFF 

        k_moves = 0
        if b_k:
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

        return moves, k_moves


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

    def white_jumpers_only(self, W: int, B: int, K: int) -> Tuple[int, int]:
        not_occ = ~(W | B)&0xFFFFFFFF
        w_k = W & K
        movers = 0
        w = W ^ K

        tmp = (not_occ<<4) & B
        movers |= (W_L3R&w)&(tmp<<3)
        movers |= (W_R3L&w)&(tmp<<5)

        tmp = ((W_L5L&not_occ)<<3)&B
        movers|= (W_R3&w)&(tmp<<4)

        tmp = ((W_L3R&not_occ)<<5)&B
        movers|= (W_L3&w)&(tmp<<4)

        k_movers = 0
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

        return movers, k_movers

    def white_jumps_only(self, W: int, B: int, K: int) -> Tuple[int, int]:
        not_occ = ~(W | B)&0xFFFFFFFF
        w_k = W & K
        moves = 0
        w = W ^ K

        tmp = (B >> 4)&not_occ
        moves |= ((W_R3L&w)>>9)&tmp
        moves |= ((W_L3R&w)>>7)&tmp

        tmp = ((W_L3R&B)>>3) & not_occ
        moves |= ((w&W_R3)>>7) &tmp

        tmp = ((W_R3L&B)>>5) &not_occ
        moves |= ((w&W_L3)>>9) & tmp

        moves&= 0xFFFFFFFF

        k_moves = 0

        if w_k:
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
        
        return moves, k_moves


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

    def apply_move(self, movers_bb: int, mover:int, move: int, K:int, is_king_move: bool, mover_color: int = 0)-> Tuple[int, int]:
        ret_movers = movers_bb
        ret_kings = K

        ret_movers = (ret_movers & ~mover) | move
        
        promote_mask = 0xF0000000 if mover_color == 1 else 0x0000000F
        if is_king_move:
            ret_kings &= ~mover
        if move & promote_mask != 0 or is_king_move:
            ret_kings |= move

        return ret_movers, ret_kings

    def apply_jump(self, jumpers_bb: int, jumper: int, jump: int, apply_mask: int, non_jumpers: int, K: int, is_king_move: bool, mover_color: int = 0) -> Tuple[int, int, int]:
        ret_jumpers = jumpers_bb
        ret_non_jumpers = non_jumpers
        ret_kings = K

        ret_jumpers = (ret_jumpers & ~jumper) | jump
        ret_non_jumpers = ret_non_jumpers & apply_mask

        promote_mask = 0xF0000000 if mover_color == 1 else 0x0000000F
        if is_king_move:
            ret_kings &= ~jumper
            ret_kings &= apply_mask
        if jump & promote_mask != 0 or is_king_move:
            ret_kings |= jump
        
        return ret_jumpers, ret_non_jumpers, ret_kings

    def load_dicts(self, data_folder: str = None) -> Tuple[Dict, Dict, Dict, Dict]:
        if hasattr(self, "dict_wm"):
            return self.dict_wm, self.dict_bm, self.dict_wj, self.dict_bj
        
        assert data_folder is not None, "data folder required"
        ret_wm = {}
        ret_bm = {}
        ret_wj = {}
        ret_bj = {}

        filename = os.path.join(data_folder, "white_moves.json")
        d = codecs.open(filename, 'r').read()
        d = json.loads(d)

        for k in d:
            ret_wm[int(k)] = np.array(d[k])
        
        filename = os.path.join(data_folder, "black_moves.json")
        d = codecs.open(filename, 'r').read()
        d = json.loads(d)

        for k in d:
            ret_bm[int(k)] = np.array(d[k])

        filename = os.path.join(data_folder, "white_jumps.json")
        d = codecs.open(filename, 'r').read()
        d = json.loads(d)
        for k in d:
            ret_wj[int(k)] = (np.array(d[k][0]), np.array(d[k][1]))

        filename = os.path.join(data_folder, "black_jumps.json")
        d = codecs.open(filename, 'r').read()
        d = json.loads(d)

        for k in d:
            ret_bj[int(k)] = (np.array(d[k][0]), np.array(d[k][1]))

        self.dict_wm = ret_wm
        self.dict_wj = ret_wj
        self.dict_bm = ret_bm
        self.dict_bj = ret_bj
        return ret_wm, ret_bm, ret_wj, ret_bj

    def bb_scores(self, W: int, B: int, K: int)-> Tuple[int, int, int, int, int, int, int]:
        w_movers, w_moves, wk_movers, wk_moves = self.white_moves(W, B, K)
        b_movers, b_moves, bk_movers, bk_moves = self.black_moves(W, B, K)

        w_jumpers, wk_jumpers = self.white_jumpers_only(W,B,K)
        b_jumpers, bk_jumpers = self.black_jumpers_only(W,B,K)

        capped_score = (24-B.bit_count())-(24-W.bit_count())
        potential_score = (w_moves | wk_moves).bit_count() - (b_moves | bk_moves).bit_count()
        men_score = (W^K).bit_count()-(B^K).bit_count()
        kings_score = (W&K).bit_count()-(B&K).bit_count()
        mid_score = (W&0x000FF000).bit_count()-(B&0x000FF000)
        capturables_score = (w_jumpers | wk_jumpers).bit_count()-(b_jumpers | bk_jumpers).bit_count()

        won = 0
        if W == 0:
            won = -1
        elif B == 0:
            won = 1

        return capped_score, potential_score, men_score, kings_score, mid_score, capturables_score, won

    def bb_reverse(self, x: int):
        x = ((x & 0x55555555) << 1) | ((x & 0xAAAAAAAA) >> 1)
        x = ((x & 0x33333333) << 2) | ((x & 0xCCCCCCCC) >> 2)
        x = ((x & 0x0F0F0F0F) << 4) | ((x & 0xF0F0F0F0) >> 4)
        x = ((x & 0x00FF00FF) << 8) | ((x & 0xFF00FF00) >> 8)
        x = ((x & 0x0000FFFF) << 16) | ((x & 0xFFFF0000) >> 16)
        return x