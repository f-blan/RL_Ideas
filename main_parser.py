import argparse
from argparse import Namespace
from typing import List
import os

def parse_main_arguments(args_list: List[str]) -> Namespace:
    parser = argparse.ArgumentParser(description="",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    #general arguments
    parser.add_argument("--app", choices=["checkers"], default="checkers", help="specify which RL application to run")
    parser.add_argument("--log_folder", default=os.path.join(".", "logs"))

    #checkers arguments
    parser.add_argument("--c_mode", choices=["bb_generate", "game_run", "metrics_train", "q_init", "reinforce_model", "test_reinforce"], default="game_run", help="checkers: select which task to run with")
    parser.add_argument("--c_data_folder", default=os.path.join(".", "checkers", "data"), help="checkers: folder where pre-computed data is stored")
    parser.add_argument("--c_GUI_type", choices=["terminal", "simple"], default="simple", help="choose the GUI to use when running a game")
    parser.add_argument("--c_GUI_engine", action= "store_true")
    parser.add_argument("--c_AI_type", choices=["simple", "rl"], default = "rl", help="the AI class used by the CPU agent")

    parser.add_argument("--c_model_folder", default=os.path.join(".", "checkers", "models"))

    args = parser.parse_args(args_list)
    
    if os.path.exists(args.log_folder) == False:
        os.mkdir(args.log_folder)
        
    if os.path.exists(args.c_model_folder) == False:
        os.mkdir(args.c_model_folder)

    return args
    