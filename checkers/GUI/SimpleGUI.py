from argparse import Namespace
from checkers.GUI.CheckersGUI import CheckersGUI
from checkers.logic.CheckersBoard import CheckersBoard
from checkers.logic.bb_utils import bb_to_np, coords_to_set_bit, set_bit_to_coords
from argparse import Namespace
import PySimpleGUI as sg
from queue import Queue
import numpy as np
import base64
import os
from checkers.GUI.Commands import Commands as cmds

class SimpleGUI(CheckersGUI):
    def __init__(self, args: Namespace, read_q: Queue, write_q: Queue) -> None:
        super().__init__(args, read_q, write_q)
        self.str_to_cmd = {
            "Player vs Player": cmds.START_PVP_MODE, 
            "Player vs CPU": cmds.START_CVC_MODE,
            "CPU vs CPU": cmds.START_PVC_MODE,
            "Exit": cmds.EXIT_APP,
            sg.WIN_CLOSED: cmds.EXIT_APP
        }
        self.code_to_png = {
            0: ["white_tile.png", "black_tile.png", "white_tile_highlighted.png"],
            1: ["white_tile_white_piece.png", "black_tile_white_piece.png", "white_tile_white_piece_highlighted.png"],
            2: ["white_tile_white_king.png", "black_tile_white_king.png", "white_tile_white_king_highlighted.png"],
            -1: ["white_tile_black_piece.png", "black_tile_black_piece.png", "white_tile_black_piece_highlighted.png"],
            -2: ["white_tile_black_king.png", "black_tile_black_king.png", "white_tile_black_king_highlighted.png"],
        }
        root = os.path.join(".", "checkers", "GUI", "imgs")
        for c in self.code_to_png:
            self.code_to_png[c][0]= os.path.join(root, self.code_to_png[c][0])
            self.code_to_png[c][1]= os.path.join(root, self.code_to_png[c][1])
            self.code_to_png[c][2]= os.path.join(root, self.code_to_png[c][2])
    
    def _coords_color(self, j: int, i: int, highlighted: bool) -> int:
        return (((j+1)%2)+i)%2 if highlighted == False else 2

    def _find_choice(self, movers: np.array, moves: np.array, mover_bb: int, move_bb: int) -> int:
        p_i = np.argmax(movers == mover_bb)
        return p_i+np.argmax(movers[p_i:] == move_bb)

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
            cmd, b, movers, moves = self.read_q.get()
            response = [cmds.QUIT_GAME]
            move_selected = False
            piece_selected= False
            np_b = bb_to_np(b.W, b.B, b.K)
            for j in range(0, 8):
                for i in range(0, 8):
                    window[str(j+1) + "-" + str(i+1)].update(image_filename=self.code_to_png[np_b[j,i]][self._coords_color(j,i, False)])
           
            highlighted = []
            piece = -1

            while move_selected == False:

                event, values = window.read()
                
                if event == "-EXIT-" or event == sg.WIN_CLOSED:
                    window.close()
                    return [cmds.QUIT_GAME]
                
                j, i = event.split("-")
                j = int(j)-1
                i = int(i)-1
                if self._coords_color(j,i,False) == 1:
                    continue
                if piece_selected == True:
                    for h in highlighted:
                        window[str(h[0]+1) + "-" + str(h[1]+1)].update(image_filename=self.code_to_png[np_b[h[0],h[1]]][self._coords_color(h[0],h[1], False)])
                        if h[0] == j and h[1] == i:
                            print("building response")
                            response = [cmds.PROCESS_ACQUIRED_MOVE, self._find_choice(movers, moves, piece, coords_to_set_bit(j,i))]
                            move_selected = True
                            break
                    if move_selected == False:
                        piece_selected = False
                    highlighted = []

                if piece_selected == False:
                    window[event].update(image_filename=self.code_to_png[np_b[j,i]][self._coords_color(j,i, True)])
                    piece_selected = True
                    piece = coords_to_set_bit(j, i)
                    moves_is = (movers == coords_to_set_bit(j, i))
                    highlighted = [(j,i)]
                    for move in moves[moves_is]:
                        y, x = set_bit_to_coords(int(move))
                        highlighted.append((y,x))
                        window[str(y+1) + "-" + str(x+1)].update(image_filename=self.code_to_png[np_b[y,x]][self._coords_color(y,x, True)])
            
            print("gui sends", response)
            self.write_q.put(response)

        