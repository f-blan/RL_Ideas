from checkers.CheckersBoard import CheckersBoard
from checkers.bb_utils import *
from checkers.consts import *


import unittest
from test.test_checkers.white_moves import *

class TfDeepQ_Tester:
    def __init__(self):
        self.bb = BB_Tester(True)

    def run(self):
        #self.initialization()
        self.bb.run()

        
class BB_Tester:
    def __init__(self, print_bbs = True):
        self.print_bbs = print_bbs

    def run(self):
        #self.test_masks()
        #self.test_print_bb()
        #self.test_white_moves()
        #self.test_black_moves()
        t = WhiteMovesTester()
        t.run()
    def test_masks(self):
        print_bb(W_L3, "l3")
        print_bb(W_L5, "l5")
        print_bb(W_R3, "r3")
        print_bb(W_R5, "r5")

    def test_print_bb(self):
        if self.print_bbs:
            print_bb(1)
            print_bb(0xffffffff)
            print_bb(0x01010101)

    def test_black_moves(self):
        board = CheckersBoard()
        movers, moves, _, __ = board._black_moves()
        
        if self.print_bbs and False:
            print_bb(movers, "movers")
            print_bb(moves, "moves")
        
        #kings
        board.K = 0x00008000
        board.W = 0x02008000
        board.B = 0

        movers, moves, k_movers, k_moves = board._white_moves()

        if self.print_bbs and True:
            print_bb(k_movers, "k_movers")
            print_bb(k_moves, "k_moves")
    
    def initialization(self):
        board = CheckersBoard()
        print(board.np_board)

        masks = generate_masks_whites()
        for m in masks:
            print(f"{m:032b}")
            print(f"{m:08X}")