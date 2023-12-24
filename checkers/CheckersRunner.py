from checkers.logic.bb_utils import *
from checkers.train import *
from argparse import Namespace
from checkers.GameHandler import GameHandler
from checkers.metrics_train import make_metrics_model
from checkers.model_reinforce import make_initial_q_value, reinforce_board_model
from checkers.model_test import test_reinforce

class CheckersRunner:
    def run(self, args: Namespace) -> None:
        match args.c_mode:
            case "bb_generate":
                self._bb_generate(args)
            case "game_run":
                self._game_run(args)
            case "metrics_train":
                self._metrics_train(args)
            case "q_init":
                self._init_q_value(args)
            case "reinforce_model":
                self._reinforce_model(args)
            case "test_reinforce":
                self._test_reinforce(args)

    def _bb_generate(self, args: Namespace) -> None:
        generate_bbs(args.c_data_folder)
    
    def _game_run(self, args: Namespace) -> None:
        GameHandler(args).run_game()
    
    def _metrics_train(self, args: Namespace) -> None:
        make_metrics_model(args)

    def _init_q_value(self, args: Namespace) -> None:
        make_initial_q_value(args)
    
    def _reinforce_model(self, args: Namespace) -> None:
        reinforce_board_model(args)
    
    def _test_reinforce(self, args: Namespace) -> None:
        test_reinforce(args)