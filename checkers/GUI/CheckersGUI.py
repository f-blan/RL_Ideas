from argparse import Namespace
from checkers.logic.CheckersBoard import CheckersBoard
from threading import Thread
from queue import Queue
from checkers.GUI.Commands import Commands as cmds

class CheckersGUI(Thread):
    def __init__(self, args: Namespace, read_q: Queue, write_q: Queue) -> None:
        super().__init__()
        self.read_q = read_q
        self.write_q = write_q

    def run(self) -> None:
        data = [cmds.EXIT_APP]
        while True:
            cmd = self.read_q.get()
            print("gui received", cmd)
            match cmd[0]:
                case cmds.MENU_SCREEN:
                    data = self.menu_screen()
                case cmds.SELECTION_SCREEN:
                    data = self.selection_screen()
                case cmds.GAME_SCREEN:
                    data = self.game_screen()
                case cmds.GUI_TERMINATE:
                    break
            print("gui sends", data)
            self.write_q.put(data)

    def menu_screen(self) -> str:
        pass

    def selection_screen(self) -> str:
        pass

    def game_screen(self, state: CheckersBoard) -> str:
        pass