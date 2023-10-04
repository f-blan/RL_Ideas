from checkers.CheckersBoard import CheckersBoard

class MoverBoard(CheckersBoard):
    """
        Expands CheckersBoard: it is the board as seen from the moving player's perspective, regardless of color.
        More convenient for training the models.
        By convention, self.W are the moving pieces
    """

    def __init__(self, data_folder: str):
        super().__init__(data_folder)
    
    def reverse(self):
        tmp = self.W
        
        self.W = self.bb_m.bb_reverse(self.B)
        self.B = self.bb_m.bb_reverse(tmp)
        self.K = self.bb_m.bb_reverse(self.K)



