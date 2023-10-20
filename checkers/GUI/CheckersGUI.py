from argparse import Namespace
from checkers.logic.CheckersBoard import CheckersBoard
from threading import Thread
from queue import Queue
from checkers.GUI.Commands import Commands as cmds
from typing import List, Any

class CheckersGUI(Thread):
    def __init__(self, args: Namespace, read_q: Queue, write_q: Queue, cpu_delay: float = 0.5) -> None:
        super().__init__()
        self.read_q = read_q
        self.write_q = write_q
        self.cpu_delay = cpu_delay
        self.show_engine_eval = args.c_GUI_engine

    def run(self) -> None:
        data = [cmds.EXIT_APP]
        while True:
            cmd = self.read_q.get()
            print("gui received", cmd[0])
            match cmd[0]:
                case cmds.MENU_SCREEN:
                    data = self.menu_screen()
                case cmds.SELECTION_SCREEN:
                    data = self.selection_screen()
                case cmds.GAME_SCREEN:
                    data = self.game_screen()
                case cmds.BROWSE_SCREEN:
                    data = self.browse_screen()
                case cmds.VIEW_SCREEN:
                    data = self.view_screen()
                case cmds.GUI_TERMINATE:
                    break
            print("gui sends", data)
            self.write_q.put(data)

    def menu_screen(self) -> List[Any]:
        pass

    def selection_screen(self) -> List[Any]:
        pass

    def game_screen(self, state: CheckersBoard) -> List[Any]:
        pass

    def browse_screen(self) -> List[Any]:
        pass

    def view_screen(self) -> List[Any]:
        pass