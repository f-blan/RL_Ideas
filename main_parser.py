import argparse
from argparse import Namespace
from typing import List
import os

def parse_main_arguments(args_list: List[str]) -> Namespace:
    parser = argparse.ArgumentParser(description="",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    #general arguments
    parser.add_argument("--app", choices=["checkers"], default="checkers", help="specify which RL application to run")

    #checkers arguments
    parser.add_argument("--c_mode", choices=["bb_generate"], default="bb_generate", help="checkers: select which task to run with")
    parser.add_argument("--c_data_folder", default=os.path.join(".", "checkers", "data"), help="checkers: folder where pre-computed data is stored")

    args = parser.parse_args(args_list)

    return args
    