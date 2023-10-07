from typing import Tuple
import numpy as np
import json, codecs
from checkers.logic.BBManager import BBManager
import os

def generate_masks_whites() -> Tuple[int, int, int, int, int]:
    s = [0]*32
    s[0] = 1
    for i in range(1, 32):
        s[i] = 1 << i
        
    mask_l3 = s[ 1] | s[ 2] | s[ 3] | s[ 9] | s[10] | s[11] | s[17] | s[18] | s[19] | s[25] | s[26] | s[27]
    mask_l5 = s[ 4] | s[ 5] | s[ 6] | s[12] | s[13] | s[14] | s[20] | s[21] | s[22]
    mask_r3 = s[28] | s[29] | s[30] | s[20] | s[21] | s[22] | s[12] | s[13] | s[14] | s[ 4] | s[ 5] | s[ 6]
    mask_r5 = s[25] | s[26] | s[27] | s[17] | s[18] | s[19] | s[ 9] | s[10] | s[11]

    start = 0
    for i in range(20, 32):
        start |= s[i]  

    return mask_l3, mask_l5, mask_r3, mask_r5, start

def print_bb(bb:int, title: str = ""):
    tmp = bb
    str = ""
    mask = 0xf0000000
    mask_p = 0x00000000f
    if title!="":
        print(f"bitboard for {title}")
    else:
        print(f"bitboard for {bb} - {hex(bb)}")
    for i in range(0, 8):
        cur = tmp&mask
        cur = cur >> 28
        str = ""
        if i %2 == 0:
            str = " "
        #print(f"{cur:b}")
        for i in range(0,4):
            str += f"{(cur&mask_p)>>3} "
            cur=cur<<1
        #print(f"{cur:b}")
        
        print(str)
    
        tmp = tmp<<4
    print("")

def generate_bbs(folder: str) -> None:
    generate_normal_moves(folder)
    generate_jump_moves(folder)

def generate_jump_moves(folder: str) -> None:
    bb_m = BBManager()

    b = 0x0F000000
    w = 0
    k = 0

    white_jumps_dict = {}
    piece = 0x80000000
    
    while piece & 0xFFFFFFFF != 0:
        w = piece
        b = 1
        moves_list = []
        apply_mask = []
        while b & 0xFFFFFFFF != 0:
            _, moves, __,___ = bb_m.white_jumps(w,b,k)
            if moves != 0 and w != b:
                moves_list.append(moves)
                apply_mask.append(~b)
            b = b<<1
        white_jumps_dict[piece] = (moves_list, apply_mask)
        piece = piece >> 1
    
    filename = os.path.join(folder, "white_jumps.json")
    json.dump(obj=white_jumps_dict, fp=codecs.open(filename, "w"))

    w = 0x000000F0
    b = 0
    k = 0

    black_jumps_dict = {}
    piece = 0x00000001
    
    while piece & 0xFFFFFFFF != 0:
        b = piece
        w = 1
        moves_list = []
        apply_mask = []
        while w & 0xFFFFFFFF != 0:
            _, moves, __,___ = bb_m.black_jumps(w,b,k)
            if moves != 0 and w != b:
                moves_list.append(moves)
                apply_mask.append(~w)
            w=w<<1
        black_jumps_dict[piece] = (moves_list, apply_mask)
        piece = piece << 1
    
    filename = os.path.join(folder, "black_jumps.json")
    json.dump(obj=black_jumps_dict, fp=codecs.open(filename, "w"))

def generate_normal_moves(folder: str) -> None:
    bb_m = BBManager()
    
    b = 0
    w = 0
    k = 0

    white_moves_dict = {}
    piece = 1

    while piece & 0xFFFFFFFF != 0:
        w = piece
        _, moves, __,___ = bb_m.white_moves(w,b,k)
        moves_list = []
        i = 1
        while i & 0xFFFFFFFF != 0:
            if moves & i != 0 and w != b:
                moves_list.append(moves&i)
            i = i << 1
        
        white_moves_dict[piece] = moves_list
        piece = piece << 1

    filename = os.path.join(folder, "white_moves.json")
    json.dump(obj=white_moves_dict, fp=codecs.open(filename, "w"))

    w = 0
    b=0
    k=0

    black_moves_dict = {}
    piece = 1

    while piece & 0xFFFFFFFF != 0:
        b = piece
        _, moves, __,___ = bb_m.black_moves(w,b,k)
        moves_list = []
        i = 1
        while i & 0xFFFFFFFF != 0:
            if moves & i != 0 and w!=b:
                moves_list.append(moves&i)
            i = i << 1
        
        black_moves_dict[piece] = moves_list
        piece = piece << 1

    filename = os.path.join(folder, "black_moves.json")
    json.dump(obj=black_moves_dict, fp=codecs.open(filename, "w"))

def set_bit_to_coords(bb: int) -> Tuple[int, int]:
    bl = 0x80000000.bit_length()-bb.bit_length()
    ret_y = (bl//4)
    ret_x = (bl%4)*2 if ret_y%2==1 else (bl%4)*2 +1
    return ret_y, ret_x

def coords_to_set_bit(y: int, x: int) -> int:
    return 0x80000000 >> ((4*y) + x//2)

def bb_to_np(W:int, B:int, K:int) -> np.ndarray:
        ret = np.zeros((8, 8), dtype=int)
        wk = W & K
        bk = B & K 


        pos = 0x80000000
        i=0
        j=1
        while pos != 0:
            if j >= 8:
                j= 0 if i%2 == 0 else 1
                i+=1
            if W & pos != 0:
                ret[i,j] = 2 if wk & pos else 1
            elif B & pos != 0:
                ret[i,j] = -2 if bk & pos else -1
            j+=2
            pos= pos >> 1
        
        return ret

