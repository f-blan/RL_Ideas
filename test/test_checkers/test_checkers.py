from checkers.CheckersBoard import CheckersBoard
from checkers.bb_utils import *
from checkers.consts import *


from test.test_checkers.white_moves import *
from test.test_checkers.king_moves import *
from test.test_checkers.king_jumps import *
from argparse import Namespace

class TestCheckers:
    def __init__(self, args: Namespace):
        self.bb = BB_Tester(args)

    def run(self):
        #self.initialization()
        self.bb.run()

        
class BB_Tester:
    def __init__(self, args: Namespace):
        self.args = args

    def run(self):
        #self.test_masks()
        #self.test_print_bb()
        t = WhiteMovesTester(self.args.c_data_folder)
        t.run()

        t = KingMovesTester(self.args.c_data_folder)
        t.run()

        t = KingJumpsTester(self.args.c_data_folder)
        t.run()
    
    def initialization(self):
        board = CheckersBoard()
        print(board.np_board)

        masks = generate_masks_whites()
        for m in masks:
            print(f"{m:032b}")
            print(f"{m:08X}")