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


def setup_logging(output_folder, console="info",
                  info_filename="info.log", debug_filename="debug.log"):
    """Set up logging files and console output.
    Creates one file for INFO logs and one for DEBUG logs.
    Args:
        output_folder (str): creates the folder where to save the files.
        debug (str):
            if == "debug" prints on console debug messages and higher
            if == "info"  prints on console info messages and higher
            if == None does not use console (useful when a logger has already been set)
        info_filename (str): the name of the info file. if None, don't create info file
        debug_filename (str): the name of the debug file. if None, don't create debug file
    """
    if os.path.exists(output_folder):
        print("log folder already exists")#raise FileExistsError(f"{output_folder} already exists!")
    else: 
        os.makedirs(output_folder, exist_ok=True)
    if os.path.exists(os.path.join(output_folder, "info.log")):
        os.remove(os.path.join(output_folder, "info.log"))
    if os.path.exists(os.path.join(output_folder, "debug.log")):
        os.remove(os.path.join(output_folder, "debug.log"))

    # logging.Logger.manager.loggerDict.keys() to check which loggers are in use
    base_formatter = logging.Formatter('%(asctime)s   %(message)s', "%Y-%m-%d %H:%M:%S")
    logger = logging.getLogger('')
    logger.setLevel(logging.DEBUG)
    
    if info_filename != None:
        info_file_handler = logging.FileHandler(join(output_folder, info_filename))
        info_file_handler.setLevel(logging.INFO)
        info_file_handler.setFormatter(base_formatter)
        logger.addHandler(info_file_handler)
    
    if debug_filename != None:
        debug_file_handler = logging.FileHandler(join(output_folder, debug_filename))
        debug_file_handler.setLevel(logging.DEBUG)
        debug_file_handler.setFormatter(base_formatter)
        logger.addHandler(debug_file_handler)
    
    if console != None:
        console_handler = logging.StreamHandler()
        if console == "debug": console_handler.setLevel(logging.DEBUG)
        if console == "info":  console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(base_formatter)
        logger.addHandler(console_handler)
    
    def exception_handler(type_, value, tb):
        logger.info("\n" + "".join(traceback.format_exception(type, value, tb)))
    sys.excepthook = exception_handler

    logger = logging.getLogger('my-logger')
    logger.propagate = False

class GameLogger():
    def __init__(self, log_root: str, folder_name: str, game_name: str = None):
        self.root = os.path.join(log_root, folder_name)
        if os.path.exists(self.root) == False:
            os.mkdir(self.root)
        if game_name == None:
            now = datetime.now()
            game_name = now.strftime("%m_%d_%Y_%H_%M_%S")
            
        game_path = os.path.join(self.root, game_name+".npy")
        if os.path.exists(game_path):
            os.remove(game_path)
        self.path = game_path
    
    def save_game(self, boards: list[MoverBoard], turns_list: list[int] = None):
        turn = ccs.WHITE_TURN
        struct = [[0,0,0] for i in range(0, len(boards))]
        to_save = np.array(struct, dtype=np.longlong)
        i = 0
        for i in range(0, len(boards)):
            if turns_list is None:
                canon_b = boards[i].get_canonical_perspective(turn)
            else:
                canon_b = boards[i].get_canonical_perspective(turns_list[i])
            to_save[i, 0], to_save[i, 1], to_save[i, 2] = canon_b.W, canon_b.B, canon_b.K 
            i+=1
            turn = ccs.WHITE_TURN if turn == ccs.BLACK_TURN else ccs.BLACK_TURN
        print("logged at", self.path)
        np.save(self.path, to_save)




