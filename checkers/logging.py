import os
import sys
import logging
import traceback
import numpy as np
from os.path import join
from datetime import datetime
import numpy as np
from checkers.logic.MoverBoard import MoverBoard
from checkers.CheckersConstants import CheckersConstants as ccs


class GameLogger():
    def __init__(self, log_root: str, folder_path: str, game_name: str = None):
        self.root = os.path.join(log_root, folder_path)
        if os.path.exists(self.root) == False:
            os.mkdir(self.root)
        if game_name == None:
            now = datetime.now()
            game_name = now.strftime("%m_%d_%Y_%H_%M_%S")
            
        game_path = os.path.join(self.root, game_name+".npy")
        if os.path.exists(game_path):
            os.remove(game_path)
        self.path = game_path
    
    def save_game(self, boards: list[MoverBoard]):
        turn = ccs.WHITE_TURN
        struct = [[0,0,0] for i in range(0, len(boards))]
        to_save = np.array(struct, dtype=np.longlong)
        i = 0
        for b in boards:
            canon_b = b.get_canonical_perspective(turn)
            to_save[i, 0], to_save[i, 1], to_save[i, 2] = canon_b.W, canon_b.B, canon_b.K 
            i+=1
            turn = ccs.WHITE_TURN if turn == ccs.BLACK_TURN else ccs.BLACK_TURN
        print("logged at", self.path)
        np.save(self.path, to_save)

        



