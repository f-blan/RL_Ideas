
#masks for the white pieces
W_START = 0xfff00000
W_L3 = 0x0e0e0e0e
W_L5 = 0x00707070
W_L3R = W_L3 >> 1
W_L5L = W_L5 << 1

W_R3 = 0x70707070
W_R5 = 0x0e0e0e00
W_R3L = W_R3<<1
W_R5R = W_R5>>1  

#masks for the black pieces
B_START = 0x00000fff