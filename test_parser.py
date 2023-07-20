import argparse
from argparse import Namespace
from typing import List
import os

def parse_test_arguments(args_list: List[str]) -> Namespace:
    parser = argparse.ArgumentParser(description="",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    #general arguments
    parser.add_argument("--app", choices=["all", "checkers"], default="all", help="specify which RL application to run")

    #checkers arguments
    parser.add_argument("--c_data_folder", default=os.path.join(".", "checkers", "data"), help="checkers: folder where pre-computed data is stored")

    args = parser.parse_args(args_list)

    return args
