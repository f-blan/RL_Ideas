from checkers.CheckersBoard import CheckersBoard
from checkers.bb_utils import *
from checkers.MoverBoard import MoverBoard
from checkers.consts import *

class BoardTester:
    def __init__(self, data_folder: str):
        self.data_folder = data_folder
        
    def run(self):
        print("---- Board Tester ----")
        for name in dir(self):
            obj = getattr(self, name)
            if callable(obj) and name != 'run' and name[:2] != '__':
                obj()
        print("---- END ----")
    
    def test_metricsS(self):
        b = CheckersBoard(self.data_folder)
        assert b.get_metrics()[0] == 1

        b.W = 1
        b.B = 0x00000FFF
        assert b.get_metrics()[0] == -1
    
    def test_reverse(self):
        b = MoverBoard(self.data_folder)

        b.W = 1
        b.B = 0
        b.reverse()
        assert b.B == 0x80000000

        b.W = 0x80000000
        b.B = 0
        b.reverse()
        assert b.B == 0x00000001

        b.W = 0x00081000
        b.B = 0
        b.reverse()
        assert b.B == 0x00081000

        b.W = W_START
        b.B = B_START
        b.reverse()
        assert b.W == W_START
        assert b.B == B_START