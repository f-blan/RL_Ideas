from checkers.CheckersBoard import CheckersBoard
from checkers.bb_utils import *


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
        print("change")