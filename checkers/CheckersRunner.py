from checkers.logic.bb_utils import *
from checkers.train import *
from argparse import Namespace
from checkers.GameHandler import GameHandler

class CheckersRunner:
    def run(self, args: Namespace) -> None:
        if args.c_mode == "bb_generate":
            self._bb_generate(args)
        
        if args.c_mode == "game_run":
            self._game_run(args)

    def _bb_generate(self, args: Namespace) -> None:
        generate_bbs(args.c_data_folder)
    
    def _game_run(self, args: Namespace) -> None:
        GameHandler(args).run_game()