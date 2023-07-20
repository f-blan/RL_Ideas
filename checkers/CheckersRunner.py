from checkers.bb_utils import *
from checkers.train import *
from argparse import Namespace

class CheckersRunner:
    def run(self, args: Namespace) -> None:
        if args.c_mode == "bb_generate":
            self._bb_generate(args)

    def _bb_generate(self, args: Namespace)-> None:
        generate_bbs(args.c_data_folder)
