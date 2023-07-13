from checkers.CheckersBoard import CheckersBoard
from checkers.bb_utils import *

class WhiteMovesTester:
    def run(self):
        print("---- White Moves Tester ----")
        for name in dir(self):
            obj = getattr(self, name)
            if callable(obj) and name != 'run' and name[:2] != '__':
                obj()
        print("---- END ----")

    def normal_moves(self):
        board = CheckersBoard()
        movers, moves, _, __ = board._white_moves()
        
        assert movers == 0x00F00000
        assert moves == 0x000F0000
        
    def king_moves(self):
        board = CheckersBoard()
        #kings
        board.K = 0x0000F000
        board.W = 0x0000F000
        board.B = 0

        _, __, k_movers, k_moves = board._white_moves()

        assert k_movers == 0x0000F000
        assert k_moves == 0x000F0F00
    
    def normal_moves_edges(self):
        board = CheckersBoard()
        board.B = 0

        board.W = 0x10000000
        movers, moves, _, __ = board._white_moves()

        assert movers == 0x10000000
        assert moves == 0x01000000

        board.W = 0x80000000
        movers, moves, _, __ = board._white_moves()
    
        assert movers == 0x80000000
        assert moves == 0x0C000000

        board.W = 0x08000000
        movers, moves, _, __ = board._white_moves()

        assert movers == 0x08000000
        assert moves == 0x00800000

        board.W = 0x00000010
        movers, moves, _, __ = board._white_moves()

        assert movers == 0x00000010
        assert moves == 0x00000001

        board.W = 0x00000080
        movers, moves, _, __ = board._white_moves()

        assert movers == 0x00000080
        assert moves == 0x0000000C

        board.W = 0x00004000
        movers, moves, _, __ = board._white_moves()

        assert movers == 0x00004000
        assert moves == 0x00000600

        board.W = 0x00000400
        movers, moves, _, __ = board._white_moves()

        assert movers == 0x00000400
        assert moves == 0x000000C0
        
    def normal_moves_edges_blocked(self):
        board = CheckersBoard()
        board.B = 0

        board.W = 0x11000000
        movers, moves, _, __ = board._white_moves()

        assert movers == 0x01000000
        assert moves == 0x00300000

        board.W = 0x8C000000
        movers, moves, _, __ = board._white_moves()

        assert movers == 0x0C000000
        assert moves == 0x00C00000

        board.W = 0x08800000
        movers, moves, _, __ = board._white_moves()

        assert movers == 0x00800000
        assert moves == 0x000C0000

        board.W = 0x00000011
        movers, moves, _, __ = board._white_moves()

        assert movers == 0
        assert moves == 0

        board.W = 0x0000008C
        movers, moves, _, __ = board._white_moves()

        assert movers == 0
        assert moves == 0

        board.W = 0x00004600
        movers, moves, _, __ = board._white_moves()

        assert movers == 0x00000600
        assert moves == 0x000000E0

        board.W = 0x000004C0
        movers, moves, _, __ = board._white_moves()

        assert movers == 0x000000C0
        assert moves == 0x0000000E
        

    def test_white_jumps(self):
        board = CheckersBoard()

        
        board.W = 0x00000800
        board.B = 0x00000088

        print_bb(board.W)
        print_bb(board.B)
        print_bb(board.W | board.B)

        jumpers, _,__,___=board._white_jumps()

        print_bb(jumpers)