from argparse import Namespace
from checkers.GUI.CheckersGUI import CheckersGUI
from checkers.logic.BBManager import BBManager
from checkers.logic.CheckersBoard import CheckersBoard
from checkers.logic.MoverBoard import MoverBoard
from checkers.logic.bb_utils import bb_to_np, coords_to_set_bit, set_bit_to_coords, print_bb
from checkers.AI.DeepQAI import DeepQAI
from argparse import Namespace
import PySimpleGUI as sg
from queue import Queue
import numpy as np
import base64
import os
from checkers.GUI.Commands import Commands as cmds
from checkers.CheckersConstants import CheckersConstants as ccs
import time
from typing import List, Any
import threading
import os

class SimpleGUI(CheckersGUI):
    def __init__(self, args: Namespace, read_q: Queue, write_q: Queue) -> None:
        super().__init__(args, read_q, write_q)
        self.data_folder = args.c_data_folder

        if self.show_engine_eval:
            self.engine = DeepQAI(ccs.WHITE_TURN, args.c_model_folder)

        self.str_to_cmd = {
            "Player vs Player": cmds.START_PVP_MODE, 
            "Player vs CPU": cmds.START_PVC_MODE,
            "CPU vs CPU": cmds.START_CVC_MODE,
            "View logged game": cmds.START_VIEW_MODE,
            "Exit": cmds.EXIT_APP,
            sg.WIN_CLOSED: cmds.EXIT_APP,
            "White": ccs.WHITE_TURN,
            "Black": ccs.BLACK_TURN
        }
        self.header_msg = {
            ccs.WHITE_TURN: "White's turn to move",
            ccs.BLACK_TURN: "Black's turn to move",
            cmds.WHITE_WINS: "White wins!",
            cmds.BLACK_WINS: "Black wins!",
            cmds.DRAW_GAME:  "Game is a draw!"

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
        return p_i+np.argmax(moves[p_i:] == move_bb)

    def menu_screen(self) -> List[Any]:
        layout = [[sg.Text("Welcome!"), sg.Input("checkers_logs", key="-LOG-"), sg.Button("ok", key="-OKLOG-")], 
                  [sg.Text("Select the Game Mode:")], [sg.Button("Player vs Player")], 
                  [sg.Button("Player vs CPU")], 
                  [sg.Button("CPU vs CPU")],
                  [sg.Button("View logged game")], 
                  [sg.Button("Exit")]]
        window = sg.Window("BE_Checkers - Main Menu", layout, margins=[100, 50])
        response = [self.str_to_cmd["Player vs Player"]]
        while True:
            event, values = window.read()
            if event == "-OKLOG-":
                    if len(response) > 1:
                        response.pop()
                    response.append(window["-LOG-"].get())
            else:
                response[0] = self.str_to_cmd[event]
                break
        window.close()
        return response

    def browse_screen(self) -> List[Any]:
        layout = [[sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),sg.FolderBrowse(initial_folder=".")], 
                  [sg.Listbox(values=[], enable_events=True, size=(40, 20), key="-FILE LIST-")],
                  [sg.Button("OK", key="-OK-")]]
        window = sg.Window("BE_Checkers - Main Menu", layout, margins=[100, 50])
        response = [cmds.ACTION_PERFORMED]
        filename = ""
        while True:
            event, values = window.read()
            if event == "Exit" or event == sg.WIN_CLOSED:
                response[0] = cmds.QUIT_GAME
                response.append("")
                break
            if event == "-FOLDER-":
                folder = values["-FOLDER-"]
                try:
                    # Get list of files in folder
                    file_list = os.listdir(folder)
                except:
                    print("bad!")
                    file_list = []

                fnames = [f for f in file_list if os.path.isfile(os.path.join(folder, f)) and f.lower().endswith((".npy"))]
                window["-FILE LIST-"].update(fnames)
            elif event == "-FILE LIST-":  # A file was chosen from the listbox
                try:
                    filename = os.path.join(values["-FOLDER-"], values["-FILE LIST-"][0])
                except:
                    pass
            if event == "-OK-":
                if filename != "":
                    response.append(filename)
                    break
                
        window.close()
        return response

    def view_screen(self) -> List[Any]:
        header = [[sg.Button("Exit", key="-EXIT-")], 
                  [sg.Button("<--", key="-BACK-"),sg.Button("-->", key="-NEXT-")],
                  [sg.Text("State: ", key= "-STATE-")], 
                  [sg.Text("Move 1, White's turn", key="-HEAD-")]]
        board = [
            [self.board_piece(str(j)+ "-"+str(i), (((j+1)%2)+i)%2, False, False) for i in range(1,9)] for j in range(1,9)
        ]

        layout = [
            header, board
        ]

        window = sg.Window("BE_Checkers - Main Menu", layout, finalize=True)
        cmd, boards = self.read_q.get()
        cur_i = 0

        while True:
            b = boards[cur_i]
            c_b = MoverBoard(self.data_folder)
            c_b.W, c_b.B, c_b.K = b

            state_str = "State: " + str(c_b.get_metrics())
            if self.show_engine_eval:
                self.engine.copy_state(c_b)
                state_str += str(self.engine.evaluate_state())
            window["-STATE-"].update(state_str)

            np_b = bb_to_np(int(b[0]), int(b[1]), int(b[2]))
            for j in range(0, 8):
                for i in range(0, 8):
                    window[str(j+1) + "-" + str(i+1)].update(image_filename=self.code_to_png[np_b[j,i]][self._coords_color(j,i, False)])

            if cur_i % 2 == 0:
                window["-HEAD-"].update("Move "+ str(cur_i+1) + ", White's turn")
            else:
                window["-HEAD-"].update("Move "+ str(cur_i+1) + ", Black's turn")

            event, values = window.read()
            if event == "-EXIT-" or event == sg.WIN_CLOSED:
                break
            
            if event == "-BACK-":
                cur_i = max(0, cur_i-1)
            if event == "-NEXT-":
                cur_i = min(len(boards)-1, cur_i+1)
        window.close()
        return [cmds.ACTION_PERFORMED]


    def selection_screen(self) -> List[Any]:
        layout = [[sg.Text("Select the color for the human: ")], [sg.Button("White")], [sg.Button("Black")]]
        window = sg.Window("BE_Checkers - Selection", layout, margins=[100, 50])
        
        event, values = window.read()
        window.close()

        return [self.str_to_cmd[event]]
    
    def board_piece(self, key: str, color: int, highlighted: bool, is_occupied: bool, piece_color: int = 0, piece_is_king: bool = False)-> sg.Button:
        img_name = "black" if color == 1 else "white"
        img_name = img_name + "_tile.png"
        img_path = os.path.join(".", "checkers", "GUI", "imgs", img_name)
        return sg.Button(image_filename=img_path, size = 20, key=key, pad=(0,0))

    def _acquire_human_input(self, b: CheckersBoard, window: sg.Window, turn:int , movers: np.ndarray, moves: np.ndarray, np_b: np.ndarray) -> List[int]:
            response = [cmds.NULL_COMMAND]
            move_selected = False
            piece_selected= False
            highlighted = []
            piece = -1

            if turn == ccs.BLACK_TURN:
                movers = np.array(list(map(BBManager().bb_reverse, movers)))
                moves = np.array(list(map(BBManager().bb_reverse, moves)))
            
           
            submit_response = True
            while move_selected == False:

                event, values = window.read()
                
                if event == "-UNDO-":
                    self.write_q.put([cmds.UNDO_MOVE])
                    submit_response = False
                    break
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
                        h_bb = coords_to_set_bit(h[0], h[1])
                        if h[0] == j and h[1] == i and h_bb != piece:
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
            
            if submit_response:
                self.write_q.put(response)
            
            return response

    def _process_CPU_input(self, window: sg.Window, next_state:np.ndarray) -> List[int]:
        def timer_callback():
            if window.is_closed() == False:
                window["1-1"].click() 
        
        timer = threading.Timer(self.cpu_delay, timer_callback)
        timer.start()
        
        event, val = window.read()
    
        if event == "-EXIT-":
            window.close()
            return [cmds.QUIT_GAME]
        if event == "-UNDO-":
            return [cmds.UNDO_MOVE]

        self.write_q.put([cmds.ACTION_PERFORMED])
        return [cmds.NULL_COMMAND]

    def game_screen(self) -> str:
        
        header = [[sg.Button("<---", key="-EXIT-"), sg.Button("Undo", key="-UNDO-")], sg.Text("Game Start", key="-TURN-"), [sg.Text("State: ", key= "-STATE-")]]
        board = [
            [self.board_piece(str(j)+ "-"+str(i), (((j+1)%2)+i)%2, False, False) for i in range(1,9)] for j in range(1,9)
        ]

        layout = [
            header, board
        ]

        window = sg.Window("BE_Checkers - Main Menu", layout, finalize=True)

        while True:
            data = self.read_q.get()
            cmd = data[0]
            turn = data[1]
            b = data[2]

            state_str = "State: " + str(b.get_metrics())
            if self.show_engine_eval:
                self.engine.copy_state(b)
                state_str += str(self.engine.evaluate_state())
            window["-STATE-"].update(state_str)
            
            np_b = bb_to_np(b.W, b.B, b.K)
            for j in range(0, 8):
                for i in range(0, 8):
                    window[str(j+1) + "-" + str(i+1)].update(image_filename=self.code_to_png[np_b[j,i]][self._coords_color(j,i, False)])

            if cmd == cmds.WHITE_WINS or cmd == cmds.BLACK_WINS or cmd == cmds.DRAW_GAME:
                window["-TURN-"].update(self.header_msg[cmd])
                window["-UNDO-"].update(disabled = True)
                break
            else:
                window["-TURN-"].update(self.header_msg[turn])

            if cmd == cmds.ACQUIRE_HUMAN_INPUT:
                response = self._acquire_human_input(b, window, turn, data[3], data[4], np_b)
            else:
                response = self._process_CPU_input(window, data[3])
            
            if response[0] == cmds.QUIT_GAME:
                    return response
        
        while True:
            event, _ = window.read()
            if event == sg.WINDOW_CLOSED or event == "-EXIT-":
                break 
        
        window.close()

        