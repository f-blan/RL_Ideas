from typing import Tuple
import numpy as np

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
        print(f"bitboard for {bb}")
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

def bb_to_np(w:int, b:int, k:int) -> np.ndarray:
    pass