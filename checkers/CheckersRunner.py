from checkers.logic.bb_utils import *
from checkers.train import *
from argparse import Namespace
from checkers.GameHandler import GameHandler
from checkers.metrics_train import make_metrics_model

class CheckersRunner:
    def run(self, args: Namespace) -> None:
        if args.c_mode == "bb_generate":
            self._bb_generate(args)
        
        if args.c_mode == "game_run":
            self._game_run(args)
        
        if args.c_mode == "metrics_train":
            self._metrics_train(args)

    def _bb_generate(self, args: Namespace) -> None:
        generate_bbs(args.c_data_folder)
    
    def _game_run(self, args: Namespace) -> None:
        GameHandler(args).run_game()
    
    def _metrics_train(self, args: Namespace) -> None:
        make_metrics_model(args)