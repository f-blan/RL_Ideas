from checkers.CheckersBoard import CheckersBoard
from checkers.bb_utils import *
from checkers.MoverBoard import MoverBoard
from checkers.consts import *
from typing import List

class BoardTester:
    def __init__(self, data_folder: str):
        self.data_folder = data_folder
        
    def run(self):
        print("---- Board Tester ----")
        for name in dir(self):
            obj = getattr(self, name)
            if callable(obj) and name != 'run' and name[:2] != '__' and name[:1] != "_":
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
    
    def _reduce_list(self, gens: List[CheckersBoard])->Tuple[List[int], List[int], List[int]]:
        ret_w = []
        ret_b = []
        ret_k = []
        for b in gens:
            ret_w.append(b.W)
            ret_b.append(b.B)
            ret_k.append(b.K)
        return ret_w, ret_b, ret_k
    
    def test_move_generation(self):
        b = MoverBoard(self.data_folder)
        
        b.W = 0x80000000
        b.B = 0
        ws, bs, ks = self._reduce_list(b.generate_next())
        assert len(ws) == 2 and 0x08000000 in ws and 0x04000000 in ws

        b.W = 0x08000000
        b.B = 0
        ws, bs, ks = self._reduce_list(b.generate_next())
        assert len(ws) == 1 and 0x00800000 in ws

        b.W = 0x00070000
        b.B = 0
        ws, bs, ks = self._reduce_list(b.generate_next())
        assert len(ws) == 6 and 0x00038000 in ws and 0x00052000

        b.W = 0x00000010
        b.B = 0
        ws, bs, ks = self._reduce_list(b.generate_next())
        assert len(ws) == 1 and 0x00000001 in ws and 0x00000001 in ks

        b.W = 0x00040000
        b.B = 0
        b.K = b.W
        ws, bs, ks = self._reduce_list(b.generate_next())
        assert len(ws) == 4 and len(ks) == 4 and  0x00400000 in ks and 0x00800000 in ks and 0x00004000 in ks and 0x00008000 in ks
        
    def test_jumps_generation(self):
        b = MoverBoard(self.data_folder)
        
        b.W = 0x80000000
        b.B = 0x08000000
        ws, bs, ks = self._reduce_list(b.generate_next())
        assert len(ws) == 1 and 0x04000000 in ws

        b.W = 0x80000000
        b.B = 0x04000000
        ws, bs, ks = self._reduce_list(b.generate_next())
        assert len(ws) == 1 and 0x00400000 in ws and 0 in bs

        b.W = 0x40000000
        b.B = 0x06000000
        ws, bs, ks = self._reduce_list(b.generate_next())
        assert len(ws) == 2 and (0x00200000 in ws and 0x04000000 in bs) and (0x00800000 in ws and 0x02000000 in bs)

        b.W = 0x00000200
        b.B = 0x00000060
        ws, bs, ks = self._reduce_list(b.generate_next())
        assert len(ws) == 2 and (0x00000040 in bs and 1 in ks) and (0x00000020 in bs and 0x00000004 in ks)

        b.W = 0x00000200
        b.B = 0x00000060
        b.K = b.B
        ws, bs, ks = self._reduce_list(b.generate_next())
        assert len(ws) == 0

        b.W = 0x00040000
        b.B = 0x0000C000
        b.K = 0x0004C000
        ws, bs, ks = self._reduce_list(b.generate_next())
        assert len(ws) == 2 and 0x00004800 in ks and 0x00008200 in ks

        b.W = 0x00040000
        b.B = 0x00C00000
        b.K = 0x00C40000
        ws, bs, ks = self._reduce_list(b.generate_next())
        assert len(ws) == 2 and 0x08400000 in ks and 0x02800000 in ks

        
        
        
        

