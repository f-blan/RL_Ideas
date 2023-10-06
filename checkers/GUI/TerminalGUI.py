from checkers.GUI.CheckersGUI import CheckersGUI
from checkers.logic.CheckersBoard import CheckersBoard
from argparse import Namespace
from queue import Queue

class TerminalGUI(CheckersGUI):
    def __init__(self, args: Namespace, read_q: Queue, write_q: Queue) -> None:
        super().__init__(args, read_q, write_q)
    
    def menu_screen(self) -> str:
        print("Welcome!")
        return ""

    def selection_screen(self) -> str:
        return super().selection_screen()
    
    def game_screen(self, state: CheckersBoard) -> str:
        return super().game_screen(state)