from argparse import Namespace
from checkers.logic.CheckersBoard import CheckersBoard
from threading import Thread
from queue import Queue 

class CheckersGUI(Thread):
    def __init__(self, args: Namespace, read_q: Queue, write_q: Queue) -> None:
        super().__init__()
        self.read_q = read_q
        self.write_q = write_q

    def run(self) -> None:
        data = "exit"
        while True:
            cmd = self.read_q.get()
            print("gui received", cmd)
            match cmd[0]:
                case "menu_screen":
                    data = self.menu_screen()
                case "selection_screen":
                    data = self.selection_screen()
                case "game_screen":
                    data = self.game_screen()
                case "terminate":
                    break
            print("gui sends", data)
            self.write_q.put(data)

    def menu_screen(self) -> str:
        pass

    def selection_screen(self) -> str:
        pass

    def game_screen(self, state: CheckersBoard) -> str:
        pass