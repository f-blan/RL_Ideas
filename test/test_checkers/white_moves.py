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
        

    def jump_moves(self):
        board = CheckersBoard()

        board.W = 0x10000000
        board.B = 0x01000000
        movers, moves, _, __ = board._white_jumps()

        assert movers == 0x10000000
        assert moves == 0x00200000

        board.W = 0x80000000
        board.B = 0x04000000
        movers, moves, _, __ = board._white_jumps()

        assert movers == 0x80000000
        assert moves == 0x00400000

        board.W = 0x01000000
        board.B = 0x00200000
        movers, moves, _, __ = board._white_jumps()

        assert movers == 0x01000000
        assert moves == 0x00020000

        board.W = 0x08000000
        board.B = 0x00800000
        movers, moves, _, __ = board._white_jumps()

        assert movers == 0x08000000
        assert moves == 0x00040000

        board.W = 0x06000000
        board.B = 0x00400000
        movers, moves, _, __ = board._white_jumps()

        assert movers == 0x06000000
        assert moves == 0x00060000

        board.W = 0x00600000
        board.B = 0x00020000
        movers, moves, _, __ = board._white_jumps()

        assert movers == 0x00600000
        assert moves == 0x00006000

        board.W = 0x0C000000
        board.B = 0x00C00000
        movers, moves, _, __ = board._white_jumps()
        
        assert movers == 0x0C000000
        assert moves == 0x000E0000

        board.W = 0x0E000000
        board.B = 0x00C00000
        movers, moves, _, __ = board._white_jumps()
        
        assert movers == 0x0E000000
        assert moves == 0x000E0000

        board.W = 0x03000000
        board.B = 0x00300000
        movers, moves, _, __ = board._white_jumps()
        
        assert movers == 0x03000000
        assert moves == 0x00030000

        board.W = 0x03000000
        board.B = 0x00700000
        movers, moves, _, __ = board._white_jumps()
        
        assert movers == 0x03000000
        assert moves == 0x00070000

        #................
        board.W = 0x00C00000
        board.B = 0x000C0000
        movers, moves, _, __ = board._white_jumps()
        
        assert movers == 0x00C00000
        assert moves == 0x0000C000

        board.W = 0x00E00000
        board.B = 0x000E0000
        movers, moves, _, __ = board._white_jumps()
        
        assert movers == 0x00E00000
        assert moves == 0x0000E000

        board.W = 0x00300000
        board.B = 0x00030000
        movers, moves, _, __ = board._white_jumps()
        
        assert movers == 0x00300000
        assert moves == 0x00007000

        board.W = 0x00300000
        board.B = 0x00070000
        movers, moves, _, __ = board._white_jumps()
        
        assert movers == 0x00300000
        assert moves == 0x00007000

        

        
        


    """
        print_bb(board.W)
        print_bb(board.B)
        print_bb(movers)
        print_bb(moves)
    """