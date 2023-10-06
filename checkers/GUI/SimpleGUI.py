from argparse import Namespace
from checkers.GUI.CheckersGUI import CheckersGUI
from checkers.logic.CheckersBoard import CheckersBoard
from checkers.logic.bb_utils import bb_to_np
from argparse import Namespace
import PySimpleGUI as sg
from queue import Queue
import base64
import os

class SimpleGUI(CheckersGUI):
    def __init__(self, args: Namespace, read_q: Queue, write_q: Queue) -> None:
        super().__init__(args, read_q, write_q)
        self.str_to_cmd = {
            "Player vs Player": "player_vs_player", 
            "Player vs CPU": "player_vs_cpu",
            "CPU vs CPU": "cpu_vs_cpu",
            "Exit": "exit",
            sg.WIN_CLOSED: "exit"
        }
        self.code_to_png = {
            0: ["white_tile.png", "black_tile.png"],
            1: ["white_tile_white_piece.png", "black_tile_white_piece.png"],
            2: ["white_tile_white_king.png", "black_tile_white_king.png"],
            -1: ["white_tile_black_piece.png", "black_tile_black_piece.png"],
            -2: ["white_tile_black_king.png", "black_tile_black_king.png"],
        }
        root = os.path.join(".", "checkers", "GUI", "imgs")
        for c in self.code_to_png:
            self.code_to_png[c][0]= os.path.join(root, self.code_to_png[c][0])
            self.code_to_png[c][1]= os.path.join(root, self.code_to_png[c][1])
    
    def _coords_color(self, j: int, i: int) -> int:
        return (((j+1)%2)+i)%2

    def menu_screen(self) -> str:
        layout = [[sg.Text("Welcome!")], [sg.Text("Select the Game Mode:")], [sg.Button("Player vs Player")], [sg.Button("Player vs CPU")], [sg.Button("CPU vs CPU")], [sg.Button("Exit")]]
        window = sg.Window("BE_Checkers - Main Menu", layout, margins=[100, 50])
        
        event, values = window.read()
        window.close()

        return [self.str_to_cmd[event]]

    def selection_screen(self) -> str:
        return super().selection_screen()
    
    def board_piece(self, key: str, color: int, highlighted: bool, is_occupied: bool, piece_color: int = 0, piece_is_king: bool = False)-> sg.Button:
        img_name = "black" if color == 1 else "white"
        img_name = img_name + "_tile.png"
        img_path = os.path.join(".", "checkers", "GUI", "imgs", img_name)
        return sg.Button(image_filename=img_path, size = 20, key=key, pad=(0,0))


    def game_screen(self) -> str:
        
        header = [[sg.Button("<---", key="-EXIT-")], sg.Text("Game Start", key="-TURN-")]
        board = [
            [self.board_piece(str(j)+ "-"+str(i), (((j+1)%2)+i)%2, False, False) for i in range(1,9)] for j in range(1,9)
        ]

        layout = [
            header, board
        ]

        window = sg.Window("BE_Checkers - Main Menu", layout, finalize=True)

        while True:
            b, movers, moves = self.read_q.get()
            np_b = bb_to_np(b.W, b.B, b.K)
            for j in range(0, 8):
                for i in range(0, 8):
                    window[str(j+1) + "-" + str(i+1)].update(image_filename=self.code_to_png[np_b[j,i]][self._coords_color(j,i)])

            event, values = window.read()
            if event == "-EXIT-" or event == sg.WIN_CLOSED:
                break
        
        window.close()

        return ["quit"]