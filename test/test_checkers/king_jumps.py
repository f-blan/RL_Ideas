from checkers.CheckersBoard import CheckersBoard
from checkers.bb_utils import *

class KingJumpsTester:
    def __init__(self, data_folder: str):
        self.data_folder = data_folder
        
    def run(self):
        print("---- King Jumps Tester ----")
        for name in dir(self):
            obj = getattr(self, name)
            if callable(obj) and name != 'run' and name[:2] != '__':
                obj()
        print("---- END ----")
    
    def single_ton(self):
        b1 = CheckersBoard(self.data_folder)
        b2 = CheckersBoard(self.data_folder)

        assert b1.dict_wj is b2.dict_wj

    def white_jumps(self):
        b = CheckersBoard(self.data_folder)

        b.W = 0x10000000
        b.B = 0x01000000
        b.K = b.B | b.W
        _, __, movers, moves = b._white_jumps()

        assert movers == 0x10000000
        assert moves  == 0x00200000

        b.W = 0x30000000
        b.B = 0x01000000
        b.K = b.B | b.W
        _, __, movers, moves = b._white_jumps()

        assert movers == 0x30000000
        assert moves  == 0x00300000

        b.W = 0x80000000
        b.B = 0x08000000
        b.K = b.B | b.W
        _, __, movers, moves = b._white_jumps()

        assert movers == 0
        assert moves  == 0

        b.W = 0x80000000
        b.B = 0x0C000000
        b.K = b.B | b.W
        _, __, movers, moves = b._white_jumps()

        assert movers == 0x80000000
        assert moves  == 0x00400000

        b.W = 0xC0000000
        b.B = 0x0C000000
        b.K = b.B | b.W
        _, __, movers, moves = b._white_jumps()

        assert movers == 0xC0000000
        assert moves  == 0x00C00000

        b.W = 0x40000000
        b.B = 0x06000000
        b.K = b.B | b.W
        _, __, movers, moves = b._white_jumps()

        assert movers == 0x40000000
        assert moves  == 0x00A00000
        
        b.W = 0x20000000
        b.B = 0x03000000
        b.K = b.B | b.W
        _, __, movers, moves = b._white_jumps()

        assert movers == 0x20000000
        assert moves  == 0x00500000
        
        b.W = 0x01000000
        b.B = 0x10000000
        b.K = b.B | b.W
        _, __, movers, moves = b._white_jumps()

        assert movers == 0
        assert moves  == 0

        b.W = 0x01000000
        b.B = 0x00100000
        b.K = b.B | b.W
        _, __, movers, moves = b._white_jumps()

        assert movers == 0
        assert moves  == 0

        b.W = 0x01000000
        b.B = 0x00200000
        b.K = b.B | b.W
        _, __, movers, moves = b._white_jumps()

        assert movers == 0x01000000
        assert moves  == 0x00020000

        b.W = 0x08000000
        b.B = 0x00800000
        b.K = b.B | b.W
        _, __, movers, moves = b._white_jumps()

        assert movers == 0x08000000
        assert moves  == 0x00040000

        b.W = 0x0C000000
        b.B = 0x00800000
        b.K = b.B | b.W
        _, __, movers, moves = b._white_jumps()

        assert movers == 0x0C000000
        assert moves  == 0x000C0000
    
        b.W = 0x06000000
        b.B = 0x00400000
        b.K = b.B | b.W
        _, __, movers, moves = b._white_jumps()

        assert movers == 0x06000000
        assert moves  == 0x00060000

        b.W = 0x00100000
        b.B = 0x01010000
        b.K = b.B | b.W
        _, __, movers, moves = b._white_jumps()

        assert movers == 0x00100000
        assert moves  == 0x20002000

        b.W = 0x00300000
        b.B = 0x01010000
        b.K = b.B | b.W
        _, __, movers, moves = b._white_jumps()

        assert movers == 0x00300000
        assert moves  == 0x30003000
        
        b.W = 0x00800000
        b.B = 0x0C0C0000
        b.K = b.B | b.W
        _, __, movers, moves = b._white_jumps()

        assert movers == 0x00800000
        assert moves  == 0x40004000

        b.W = 0x00600000
        b.B = 0x07070000
        b.K = b.B | b.W
        _, __, movers, moves = b._white_jumps()
        
        assert movers == 0x00600000
        assert moves  == 0xF000F000

        #--------------------------
        b.W = 0x00010000
        b.B = 0x00101000
        b.K = b.B | b.W
        _, __, movers, moves = b._white_jumps()

        assert movers == 0
        assert moves  == 0

        b.W = 0x00010000
        b.B = 0x00303000
        b.K = b.B | b.W
        _, __, movers, moves = b._white_jumps()

        assert movers == 0x00010000
        assert moves  == 0x02000200
        
        b.W = 0x00080000
        b.B = 0x00808000
        b.K = b.B | b.W
        _, __, movers, moves = b._white_jumps()

        assert movers == 0x00080000
        assert moves  == 0x04000400

        b.W = 0x00060000
        b.B = 0x00404000
        b.K = b.B | b.W
        _, __, movers, moves = b._white_jumps()
        
        assert movers == 0x00060000
        assert moves  == 0x06000600

        b.W = 0x00060000
        b.B = 0x00E0E000
        b.K = b.B | b.W
        _, __, movers, moves = b._white_jumps()
        
        assert movers == 0x00060000
        assert moves  == 0x0F000F00

        b.W = 0x00000001
        b.B = 0x00000010
        b.K = b.B | b.W
        _, __, movers, moves = b._white_jumps()

        assert movers == 0x00000000
        assert moves  == 0x00000000

        b.W = 0x00000001
        b.B = 0x00000030
        b.K = b.B | b.W
        _, __, movers, moves = b._white_jumps()

        assert movers == 0x00000001
        assert moves  == 0x00000200

        b.W = 0x00000003
        b.B = 0x00000030
        b.K = b.B | b.W
        _, __, movers, moves = b._white_jumps()

        assert movers == 0x00000003
        assert moves  == 0x00000300

        b.W = 0x00000008
        b.B = 0x00000080
        b.K = b.B | b.W
        _, __, movers, moves = b._white_jumps()

        assert movers == 0x00000008
        assert moves  == 0x00000400

        b.W = 0x0000000C
        b.B = 0x00000080
        b.K = b.B | b.W
        _, __, movers, moves = b._white_jumps()

        assert movers == 0x0000000C
        assert moves  == 0x00000C00
        
        b.W = 0x00000006
        b.B = 0x00000040
        b.K = b.B | b.W
        _, __, movers, moves = b._white_jumps()

        assert movers == 0x00000006
        assert moves  == 0x00000600

        b.W = 0x00000010
        b.B = 0x00000101
        b.K = b.B | b.W
        _, __, movers, moves = b._white_jumps()

        assert movers == 0x00000010
        assert moves  == 0x00002000

    def white_jumps_blocked(self):
        b = CheckersBoard(self.data_folder)

        b.W = 0x10000000
        b.B = 0x01200000
        b.K = b.B | b.W
        _, __, movers, moves = b._white_jumps()

        assert movers == 0
        assert moves  == 0

        b.W = 0x30000000
        b.B = 0x01300000
        b.K = b.B | b.W
        _, __, movers, moves = b._white_jumps()

        assert movers == 0
        assert moves  == 0

        b.W = 0x80000000
        b.B = 0x08000000
        b.K = b.B | b.W
        _, __, movers, moves = b._white_jumps()

        assert movers == 0
        assert moves  == 0

        b.W = 0x80000000
        b.B = 0x0C400000
        b.K = b.B | b.W
        _, __, movers, moves = b._white_jumps()

        assert movers == 0
        assert moves  == 0

        b.W = 0xC0000000
        b.B = 0x0CC00000
        b.K = b.B | b.W
        _, __, movers, moves = b._white_jumps()

        assert movers == 0
        assert moves  == 0

        b.W = 0x40000000
        b.B = 0x06E00000
        b.K = b.B | b.W
        _, __, movers, moves = b._white_jumps()

        assert movers == 0
        assert moves  == 0
        
        b.W = 0x20000000
        b.B = 0x03700000
        b.K = b.B | b.W
        _, __, movers, moves = b._white_jumps()

        assert movers == 0
        assert moves  == 0
        
        b.W = 0x01000000
        b.B = 0x10000000
        b.K = b.B | b.W
        _, __, movers, moves = b._white_jumps()

        assert movers == 0
        assert moves  == 0

        b.W = 0x01000000
        b.B = 0x00100000
        b.K = b.B | b.W
        _, __, movers, moves = b._white_jumps()

        assert movers == 0
        assert moves  == 0

        b.W = 0x01000000
        b.B = 0x00220000
        b.K = b.B | b.W
        _, __, movers, moves = b._white_jumps()

        assert movers == 0
        assert moves  == 0

        b.W = 0x08000000
        b.B = 0x00840000
        b.K = b.B | b.W
        _, __, movers, moves = b._white_jumps()

        assert movers == 0
        assert moves  == 0

        b.W = 0x0C000000
        b.B = 0x008C0000
        b.K = b.B | b.W
        _, __, movers, moves = b._white_jumps()

        assert movers == 0
        assert moves  == 0
    
        b.W = 0x06000000
        b.B = 0x00460000
        b.K = b.B | b.W
        _, __, movers, moves = b._white_jumps()

        assert movers == 0
        assert moves  == 0

        b.W = 0x00100000
        b.B = 0x21012000
        b.K = b.B | b.W
        _, __, movers, moves = b._white_jumps()

        assert movers == 0
        assert moves  == 0

        b.W = 0x00300000
        b.B = 0x31013000
        b.K = b.B | b.W
        _, __, movers, moves = b._white_jumps()

        assert movers == 0
        assert moves  == 0
        
        b.W = 0x00800000
        b.B = 0x4C0C4000
        b.K = b.B | b.W
        _, __, movers, moves = b._white_jumps()

        assert movers == 0
        assert moves  == 0

        b.W = 0x00600000
        b.B = 0xF707F000
        b.K = b.B | b.W
        _, __, movers, moves = b._white_jumps()
        
        assert movers == 0
        assert moves  == 0

        #--------------------------
        b.W = 0x00010000
        b.B = 0x00101000
        b.K = b.B | b.W
        _, __, movers, moves = b._white_jumps()

        assert movers == 0
        assert moves  == 0

        b.W = 0x00010000
        b.B = 0x02303200
        b.K = b.B | b.W
        _, __, movers, moves = b._white_jumps()

        assert movers == 0
        assert moves  == 0
        
        b.W = 0x00080000
        b.B = 0x04808400
        b.K = b.B | b.W
        _, __, movers, moves = b._white_jumps()

        assert movers == 0
        assert moves  == 0

        b.W = 0x00060000
        b.B = 0x06404600
        b.K = b.B | b.W
        _, __, movers, moves = b._white_jumps()
        
        assert movers == 0
        assert moves  == 0

        b.W = 0x00060000
        b.B = 0x0FE0EF00
        b.K = b.B | b.W
        _, __, movers, moves = b._white_jumps()
        
        assert movers == 0
        assert moves  == 0

        b.W = 0x00000001
        b.B = 0x00000010
        b.K = b.B | b.W
        _, __, movers, moves = b._white_jumps()

        assert movers == 0
        assert moves  == 0

        b.W = 0x00000001
        b.B = 0x00000230
        b.K = b.B | b.W
        _, __, movers, moves = b._white_jumps()

        assert movers == 0
        assert moves  == 0

        b.W = 0x00000003
        b.B = 0x00000330
        b.K = b.B | b.W
        _, __, movers, moves = b._white_jumps()

        assert movers == 0
        assert moves  == 0

        b.W = 0x00000008
        b.B = 0x00000480
        b.K = b.B | b.W
        _, __, movers, moves = b._white_jumps()

        assert movers == 0
        assert moves  == 0

        b.W = 0x0000000C
        b.B = 0x00000C80
        b.K = b.B | b.W
        _, __, movers, moves = b._white_jumps()

        assert movers == 0
        assert moves  == 0
        
        b.W = 0x00000006
        b.B = 0x00000640
        b.K = b.B | b.W
        _, __, movers, moves = b._white_jumps()

        assert movers == 0
        assert moves  == 0

        b.W = 0x00000010
        b.B = 0x00002101
        b.K = b.B | b.W
        _, __, movers, moves = b._white_jumps()

        assert movers == 0
        assert moves  == 0

        b.W = 0x00000020
        b.B = 0x00000003
        b.K = b.B | b.W
        _, __, movers, moves = b._white_jumps()

        assert movers == 0
        assert moves  == 0
    
    #----------------------------------------------------
    def black_jumps(self):
        b = CheckersBoard(self.data_folder)

        b.B = 0x10000000
        b.W = 0x01000000
        b.K = b.B | b.W
        _, __, movers, moves = b._black_jumps()

        assert movers == 0x10000000
        assert moves  == 0x00200000

        b.B = 0x30000000
        b.W = 0x01000000
        b.K = b.B | b.W
        _, __, movers, moves = b._black_jumps()

        assert movers == 0x30000000
        assert moves  == 0x00300000

        b.B = 0x80000000
        b.W = 0x08000000
        b.K = b.B | b.W
        _, __, movers, moves = b._black_jumps()

        assert movers == 0
        assert moves  == 0

        b.B = 0x80000000
        b.W = 0x0C000000
        b.K = b.B | b.W
        _, __, movers, moves = b._black_jumps()

        assert movers == 0x80000000
        assert moves  == 0x00400000

        b.B = 0xC0000000
        b.W = 0x0C000000
        b.K = b.B | b.W
        _, __, movers, moves = b._black_jumps()

        assert movers == 0xC0000000
        assert moves  == 0x00C00000

        b.B = 0x40000000
        b.W = 0x06000000
        b.K = b.B | b.W
        _, __, movers, moves = b._black_jumps()

        assert movers == 0x40000000
        assert moves  == 0x00A00000
        
        b.B = 0x20000000
        b.W = 0x03000000
        b.K = b.B | b.W
        _, __, movers, moves = b._black_jumps()

        assert movers == 0x20000000
        assert moves  == 0x00500000
        
        b.B = 0x01000000
        b.W = 0x10000000
        b.K = b.B | b.W
        _, __, movers, moves = b._black_jumps()

        assert movers == 0
        assert moves  == 0

        b.B = 0x01000000
        b.W = 0x00100000
        b.K = b.B | b.W
        _, __, movers, moves = b._black_jumps()

        assert movers == 0
        assert moves  == 0

        b.B = 0x01000000
        b.W = 0x00200000
        b.K = b.B | b.W
        _, __, movers, moves = b._black_jumps()

        assert movers == 0x01000000
        assert moves  == 0x00020000

        b.B = 0x08000000
        b.W = 0x00800000
        b.K = b.B | b.W
        _, __, movers, moves = b._black_jumps()

        assert movers == 0x08000000
        assert moves  == 0x00040000

        b.B = 0x0C000000
        b.W = 0x00800000
        b.K = b.B | b.W
        _, __, movers, moves = b._black_jumps()

        assert movers == 0x0C000000
        assert moves  == 0x000C0000
    
        b.B = 0x06000000
        b.W = 0x00400000
        b.K = b.B | b.W
        _, __, movers, moves = b._black_jumps()

        assert movers == 0x06000000
        assert moves  == 0x00060000

        b.B = 0x00100000
        b.W = 0x01010000
        b.K = b.B | b.W
        _, __, movers, moves = b._black_jumps()

        assert movers == 0x00100000
        assert moves  == 0x20002000

        b.B = 0x00300000
        b.W = 0x01010000
        b.K = b.B | b.W
        _, __, movers, moves = b._black_jumps()

        assert movers == 0x00300000
        assert moves  == 0x30003000
        
        b.B = 0x00800000
        b.W = 0x0C0C0000
        b.K = b.B | b.W
        _, __, movers, moves = b._black_jumps()

        assert movers == 0x00800000
        assert moves  == 0x40004000

        b.B = 0x00600000
        b.W = 0x07070000
        b.K = b.B | b.W
        _, __, movers, moves = b._black_jumps()
        
        assert movers == 0x00600000
        assert moves  == 0xF000F000

        #--------------------------
        b.B = 0x00010000
        b.W = 0x00101000
        b.K = b.B | b.W
        _, __, movers, moves = b._black_jumps()

        assert movers == 0
        assert moves  == 0

        b.B = 0x00010000
        b.W = 0x00303000
        b.K = b.B | b.W
        _, __, movers, moves = b._black_jumps()

        assert movers == 0x00010000
        assert moves  == 0x02000200
        
        b.B = 0x00080000
        b.W = 0x00808000
        b.K = b.B | b.W
        _, __, movers, moves = b._black_jumps()

        assert movers == 0x00080000
        assert moves  == 0x04000400

        b.B = 0x00060000
        b.W = 0x00404000
        b.K = b.B | b.W
        _, __, movers, moves = b._black_jumps()
        
        assert movers == 0x00060000
        assert moves  == 0x06000600

        b.B = 0x00060000
        b.W = 0x00E0E000
        b.K = b.B | b.W
        _, __, movers, moves = b._black_jumps()
        
        assert movers == 0x00060000
        assert moves  == 0x0F000F00

        b.B = 0x00000001
        b.W = 0x00000010
        b.K = b.B | b.W
        _, __, movers, moves = b._black_jumps()

        assert movers == 0x00000000
        assert moves  == 0x00000000

        b.B = 0x00000001
        b.W = 0x00000030
        b.K = b.B | b.W
        _, __, movers, moves = b._black_jumps()

        assert movers == 0x00000001
        assert moves  == 0x00000200

        b.B = 0x00000003
        b.W = 0x00000030
        b.K = b.B | b.W
        _, __, movers, moves = b._black_jumps()

        assert movers == 0x00000003
        assert moves  == 0x00000300

        b.B = 0x00000008
        b.W = 0x00000080
        b.K = b.B | b.W
        _, __, movers, moves = b._black_jumps()

        assert movers == 0x00000008
        assert moves  == 0x00000400

        b.B = 0x0000000C
        b.W = 0x00000080
        b.K = b.B | b.W
        _, __, movers, moves = b._black_jumps()

        assert movers == 0x0000000C
        assert moves  == 0x00000C00
        
        b.B = 0x00000006
        b.W = 0x00000040
        b.K = b.B | b.W
        _, __, movers, moves = b._black_jumps()

        assert movers == 0x00000006
        assert moves  == 0x00000600

        b.B = 0x00000010
        b.W = 0x00000101
        b.K = b.B | b.W
        _, __, movers, moves = b._black_jumps()

        assert movers == 0x00000010
        assert moves  == 0x00002000

    def black_jumps_blocked(self):
        b = CheckersBoard(self.data_folder)

        b.B = 0x10000000
        b.W = 0x01200000
        b.K = b.B | b.W
        _, __, movers, moves = b._black_jumps()

        assert movers == 0
        assert moves  == 0

        b.B = 0x30000000
        b.W = 0x01300000
        b.K = b.B | b.W
        _, __, movers, moves = b._black_jumps()

        assert movers == 0
        assert moves  == 0

        b.B = 0x80000000
        b.W = 0x08000000
        b.K = b.B | b.W
        _, __, movers, moves = b._black_jumps()

        assert movers == 0
        assert moves  == 0

        b.B = 0x80000000
        b.W = 0x0C400000
        b.K = b.B | b.W
        _, __, movers, moves = b._black_jumps()

        assert movers == 0
        assert moves  == 0

        b.B = 0xC0000000
        b.W = 0x0CC00000
        b.K = b.B | b.W
        _, __, movers, moves = b._black_jumps()

        assert movers == 0
        assert moves  == 0

        b.B = 0x40000000
        b.W = 0x06E00000
        b.K = b.B | b.W
        _, __, movers, moves = b._black_jumps()

        assert movers == 0
        assert moves  == 0
        
        b.B = 0x20000000
        b.W = 0x03700000
        b.K = b.B | b.W
        _, __, movers, moves = b._black_jumps()

        assert movers == 0
        assert moves  == 0
        
        b.B = 0x01000000
        b.W = 0x10000000
        b.K = b.B | b.W
        _, __, movers, moves = b._black_jumps()

        assert movers == 0
        assert moves  == 0

        b.B = 0x01000000
        b.W = 0x00100000
        b.K = b.B | b.W
        _, __, movers, moves = b._black_jumps()

        assert movers == 0
        assert moves  == 0

        b.B = 0x01000000
        b.W = 0x00220000
        b.K = b.B | b.W
        _, __, movers, moves = b._black_jumps()

        assert movers == 0
        assert moves  == 0

        b.B = 0x08000000
        b.W = 0x00840000
        b.K = b.B | b.W
        _, __, movers, moves = b._black_jumps()

        assert movers == 0
        assert moves  == 0

        b.B = 0x0C000000
        b.W = 0x008C0000
        b.K = b.B | b.W
        _, __, movers, moves = b._black_jumps()

        assert movers == 0
        assert moves  == 0
    
        b.B = 0x06000000
        b.W = 0x00460000
        b.K = b.B | b.W
        _, __, movers, moves = b._black_jumps()

        assert movers == 0
        assert moves  == 0

        b.B = 0x00100000
        b.W = 0x21012000
        b.K = b.B | b.W
        _, __, movers, moves = b._black_jumps()

        assert movers == 0
        assert moves  == 0

        b.B = 0x00300000
        b.W = 0x31013000
        b.K = b.B | b.W
        _, __, movers, moves = b._black_jumps()

        assert movers == 0
        assert moves  == 0
        
        b.B = 0x00800000
        b.W = 0x4C0C4000
        b.K = b.B | b.W
        _, __, movers, moves = b._black_jumps()

        assert movers == 0
        assert moves  == 0

        b.B = 0x00600000
        b.W = 0xF707F000
        b.K = b.B | b.W
        _, __, movers, moves = b._black_jumps()
        
        assert movers == 0
        assert moves  == 0

        #--------------------------
        b.B = 0x00010000
        b.W = 0x00101000
        b.K = b.B | b.W
        _, __, movers, moves = b._black_jumps()

        assert movers == 0
        assert moves  == 0

        b.B = 0x00010000
        b.W = 0x02303200
        b.K = b.B | b.W
        _, __, movers, moves = b._black_jumps()

        assert movers == 0
        assert moves  == 0
        
        b.B = 0x00080000
        b.W = 0x04808400
        b.K = b.B | b.W
        _, __, movers, moves = b._black_jumps()

        assert movers == 0
        assert moves  == 0

        b.B = 0x00060000
        b.W = 0x06404600
        b.K = b.B | b.W
        _, __, movers, moves = b._black_jumps()
        
        assert movers == 0
        assert moves  == 0

        b.B = 0x00060000
        b.W = 0x0FE0EF00
        b.K = b.B | b.W
        _, __, movers, moves = b._black_jumps()
        
        assert movers == 0
        assert moves  == 0

        b.B = 0x00000001
        b.W = 0x00000010
        b.K = b.B | b.W
        _, __, movers, moves = b._black_jumps()

        assert movers == 0
        assert moves  == 0

        b.B = 0x00000001
        b.W = 0x00000230
        b.K = b.B | b.W
        _, __, movers, moves = b._black_jumps()

        assert movers == 0
        assert moves  == 0

        b.B = 0x00000003
        b.W = 0x00000330
        b.K = b.B | b.W
        _, __, movers, moves = b._black_jumps()

        assert movers == 0
        assert moves  == 0

        b.B = 0x00000008
        b.W = 0x00000480
        b.K = b.B | b.W
        _, __, movers, moves = b._black_jumps()

        assert movers == 0
        assert moves  == 0

        b.B = 0x0000000C
        b.W = 0x00000C80
        b.K = b.B | b.W
        _, __, movers, moves = b._black_jumps()

        assert movers == 0
        assert moves  == 0
        
        b.B = 0x00000006
        b.W = 0x00000640
        b.K = b.B | b.W
        _, __, movers, moves = b._black_jumps()

        assert movers == 0
        assert moves  == 0

        b.B = 0x00000010
        b.W = 0x00002101
        b.K = b.B | b.W
        _, __, movers, moves = b._black_jumps()

        assert movers == 0
        assert moves  == 0

        b.B = 0x00000020
        b.W = 0x00000003
        b.K = b.B | b.W
        _, __, movers, moves = b._black_jumps()

        assert movers == 0
        assert moves  == 0
        """
        print_bb(b.W, "W")
        print_bb(b.B, "B")
        print_bb(movers, "movers")
        print_bb(moves, "moves")
        """