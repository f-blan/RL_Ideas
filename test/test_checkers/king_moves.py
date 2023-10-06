from checkers.logic.CheckersBoard import CheckersBoard
from checkers.logic.bb_utils import *

class KingMovesTester:
    def __init__(self, data_folder: str):
        self.data_folder = data_folder
        
    def run(self):
        print("---- King Moves Tester ----")
        for name in dir(self):
            obj = getattr(self, name)
            if callable(obj) and name != 'run' and name[:2] != '__':
                obj()
        print("---- END ----")
    
    def _white_normal(self):
        b = CheckersBoard(self.data_folder)

        b.W = 0x10000000
        b.B = 0x00000000
        b.K = b.W | b.K

        _, __, movers, moves = b._white_moves()

        assert movers == 0x10000000
        assert moves == 0x01000000

        b.W = 0x80000000
        b.B = 0x00000000
        b.K = b.W | b.K

        _, __, movers, moves = b._white_moves()

        assert movers == 0x80000000
        assert moves == 0x0C000000

        b.W = 0x10000000
        b.B = 0x00000000
        b.K = b.W | b.K

        _, __, movers, moves = b._white_moves()

        assert movers == 0x10000000
        assert moves == 0x01000000

        b.W = 0x40000000
        b.B = 0x00000000
        b.K = b.W | b.K

        _, __, movers, moves = b._white_moves()

        assert movers == 0x40000000
        assert moves == 0x06000000
        
        b.W = 0x20000000
        b.B = 0x00000000
        b.K = b.W | b.K

        _, __, movers, moves = b._white_moves()

        assert movers == 0x20000000
        assert moves == 0x03000000

        b.W = 0x01000000
        b.B = 0x00000000
        b.K = b.W | b.K

        _, __, movers, moves = b._white_moves()

        assert movers == 0x01000000
        assert moves == 0x30300000

        b.W = 0x08000000
        b.B = 0x0000000
        b.K = b.W | b.K

        _, __, movers, moves = b._white_moves()

        assert movers == 0x08000000
        assert moves == 0x80800000

        b.W = 0x04000000
        b.B = 0x00000000
        b.K = b.W | b.K

        _, __, movers, moves = b._white_moves()

        assert movers == 0x04000000
        assert moves == 0xC0C00000

        b.W = 0x02000000
        b.B = 0x00000000
        b.K = b.W | b.K

        _, __, movers, moves = b._white_moves()

        assert movers == 0x02000000
        assert moves == 0x60600000

        b.W = 0x00400000
        b.B = 0x00000000
        b.K = b.W | b.K

        _, __, movers, moves = b._white_moves()

        assert movers == 0x00400000
        assert moves == 0x06060000

        b.W = 0x00200000
        b.B = 0x00000000
        b.K = b.W | b.K

        _, __, movers, moves = b._white_moves()

        assert movers == 0x00200000
        assert moves == 0x03030000

        b.W = 0x00000001
        b.B = 0x00000000
        b.K = b.W | b.K

        _, __, movers, moves = b._white_moves()

        assert movers == 0x00000001
        assert moves == 0x00000030

        b.W = 0x00000008
        b.B = 0x00000000
        b.K = b.W | b.K

        _, __, movers, moves = b._white_moves()

        assert movers == 0x00000008
        assert moves == 0x00000080

    def _white_normal_blocked(self):
        b = CheckersBoard(self.data_folder)

        b.W = 0x10000000
        b.B = 0x01000000
        b.K = b.W | b.K
        _, __, movers, moves = b._white_moves()

        assert movers == 0
        assert moves == 0

        b.W = 0x80000000
        b.B = 0x0C000000
        b.K = b.W | b.K

        _, __, movers, moves = b._white_moves()

        assert movers == 0
        assert moves == 0

        b.W = 0x40000000
        b.B = 0x06000000
        b.K = b.W | b.K

        _, __, movers, moves = b._white_moves()

        assert movers == 0
        assert moves == 0
        
        b.W = 0x20000000
        b.B = 0x03000000
        b.K = b.W | b.K

        _, __, movers, moves = b._white_moves()

        assert movers == 0
        assert moves == 0

        b.W = 0x01000000
        b.B = 0x30300000
        b.K = b.W | b.K

        _, __, movers, moves = b._white_moves()

        assert movers == 0
        assert moves == 0

        b.W = 0x08000000
        b.B = 0x80800000
        b.K = b.W | b.K

        _, __, movers, moves = b._white_moves()

        assert movers == 0
        assert moves == 0

        b.W = 0x04000000
        b.B = 0xC0C00000
        b.K = b.W | b.K

        _, __, movers, moves = b._white_moves()

        assert movers == 0
        assert moves == 0

        b.W = 0x02000000
        b.B = 0x60600000
        b.K = b.W | b.K

        _, __, movers, moves = b._white_moves()

        assert movers == 0
        assert moves == 0

        b.W = 0x00400000
        b.B = 0x06060000
        b.K = b.W | b.K

        _, __, movers, moves = b._white_moves()

        assert movers == 0
        assert moves == 0

        b.W = 0x00200000
        b.B = 0x03030000
        b.K = b.W | b.K

        _, __, movers, moves = b._white_moves()

        assert movers == 0
        assert moves == 0

        b.W = 0x00000001
        b.B = 0x00000030
        b.K = b.W | b.K

        _, __, movers, moves = b._white_moves()

        assert movers == 0
        assert moves == 0

        b.W = 0x00000008
        b.B = 0x00000080
        b.K = b.W | b.K

        _, __, movers, moves = b._white_moves()

        assert movers == 0
        assert moves == 0

    def _black_normal(self):
        b = CheckersBoard(self.data_folder)

        b.B = 0x10000000
        b.W = 0x00000000
        b.K = b.B | b.W

        _, __, movers, moves = b._black_moves()

        assert movers == 0x10000000
        assert moves == 0x01000000

        b.B = 0x80000000
        b.W = 0x00000000
        b.K = b.B | b.W

        _, __, movers, moves = b._black_moves()

        assert movers == 0x80000000
        assert moves == 0x0C000000

        b.B = 0x10000000
        b.W = 0x00000000
        b.K = b.B | b.W

        _, __, movers, moves = b._black_moves()

        assert movers == 0x10000000
        assert moves == 0x01000000

        b.B = 0x40000000
        b.W = 0x00000000
        b.K = b.B | b.W

        _, __, movers, moves = b._black_moves()

        assert movers == 0x40000000
        assert moves == 0x06000000
        
        b.B = 0x20000000
        b.W = 0x00000000
        b.K = b.B | b.W

        _, __, movers, moves = b._black_moves()

        assert movers == 0x20000000
        assert moves == 0x03000000

        b.B = 0x01000000
        b.W = 0x00000000
        b.K = b.B | b.W

        _, __, movers, moves = b._black_moves()

        assert movers == 0x01000000
        assert moves == 0x30300000

        b.B = 0x08000000
        b.W = 0x0000000
        b.K = b.B | b.W

        _, __, movers, moves = b._black_moves()

        assert movers == 0x08000000
        assert moves == 0x80800000

        b.B = 0x04000000
        b.W = 0x00000000
        b.K = b.B | b.W

        _, __, movers, moves = b._black_moves()

        assert movers == 0x04000000
        assert moves == 0xC0C00000

        b.B = 0x02000000
        b.W = 0x00000000
        b.K = b.B | b.W

        _, __, movers, moves = b._black_moves()

        assert movers == 0x02000000
        assert moves == 0x60600000

        b.B = 0x00400000
        b.W = 0x00000000
        b.K = b.B | b.W

        _, __, movers, moves = b._black_moves()

        assert movers == 0x00400000
        assert moves == 0x06060000

        b.B = 0x00200000
        b.W = 0x00000000
        b.K = b.B | b.W

        _, __, movers, moves = b._black_moves()

        assert movers == 0x00200000
        assert moves == 0x03030000

        b.B = 0x00000001
        b.W = 0x00000000
        b.K = b.B | b.W

        _, __, movers, moves = b._black_moves()

        assert movers == 0x00000001
        assert moves == 0x00000030

        b.B = 0x00000008
        b.W = 0x00000000
        b.K = b.B | b.W

        _, __, movers, moves = b._black_moves()

        assert movers == 0x00000008
        assert moves == 0x00000080

    def _black_normal_blocked(self):
        b = CheckersBoard(self.data_folder)

        b.B = 0x10000000
        b.W = 0x01000000
        b.K = b.B | b.W
        _, __, movers, moves = b._black_moves()

        assert movers == 0
        assert moves == 0

        b.B = 0x80000000
        b.W = 0x0C000000
        b.K = b.B | b.W

        _, __, movers, moves = b._black_moves()

        assert movers == 0
        assert moves == 0

        b.B = 0x40000000
        b.W = 0x06000000
        b.K = b.B | b.W

        _, __, movers, moves = b._black_moves()

        assert movers == 0
        assert moves == 0
        
        b.B = 0x20000000
        b.W = 0x03000000
        b.K = b.B | b.W

        _, __, movers, moves = b._black_moves()

        assert movers == 0
        assert moves == 0

        b.B = 0x01000000
        b.W = 0x30300000
        b.K = b.B | b.K

        _, __, movers, moves = b._black_moves()

        assert movers == 0
        assert moves == 0

        b.B = 0x08000000
        b.W = 0x80800000
        b.K = b.B | b.K

        _, __, movers, moves = b._black_moves()

        assert movers == 0
        assert moves == 0

        b.B = 0x04000000
        b.W = 0xC0C00000
        b.K = b.B | b.W

        _, __, movers, moves = b._black_moves()

        assert movers == 0
        assert moves == 0

        b.B = 0x02000000
        b.W = 0x60600000
        b.K = b.B | b.W

        _, __, movers, moves = b._black_moves()

        assert movers == 0
        assert moves == 0

        b.B = 0x00400000
        b.W = 0x06060000
        b.K = b.B | b.W

        _, __, movers, moves = b._black_moves()

        assert movers == 0
        assert moves == 0

        b.B = 0x00200000
        b.W = 0x03030000
        b.K = b.B | b.W

        _, __, movers, moves = b._black_moves()

        assert movers == 0
        assert moves == 0

        b.B = 0x00000001
        b.W = 0x00000030
        b.K = b.B | b.W

        _, __, movers, moves = b._black_moves()

        assert movers == 0
        assert moves == 0

        b.B = 0x00000008
        b.W = 0x00000080
        b.K = b.B | b.W

        _, __, movers, moves = b._black_moves()

        assert movers == 0
        assert moves == 0
    """
        print_bb(b.W, "W")
        print_bb(b.B, "B")
        print_bb(movers, "movers")
        print_bb(moves, "moves")
    """