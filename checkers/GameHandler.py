from argparse import Namespace
from checkers.GUI import CheckersGUI, SimpleGUI, TerminalGUI
from checkers.logic.MoverBoard import MoverBoard
from queue import Queue
from checkers.GUI.Commands import Commands as cmds

class GameHandler:
    def __init__(self, args: Namespace) -> None:
        self.args = args
        self.read_q = Queue()
        self.write_q = Queue()
        self.gui = SimpleGUI(args, self.write_q, self.read_q) if args.c_GUI_type == "simple" else TerminalGUI(args, self.write_q, self.read_q) 

    def run_game(self) -> None:
        self.gui.start()
        while True:
            print("handler sends menu screen")
            self.write_q.put([cmds.MENU_SCREEN])
            game_mode = self.read_q.get()
            print("handler received", game_mode)
            match game_mode[0]:
                case cmds.START_PVP_MODE:
                    self._player_vs_player()
                case cmds.START_CVC_MODE:
                    self._cpu_vs_cpu()
                case cmds.START_PVC_MODE:
                    self._player_vs_cpu()
                case cmds.EXIT_APP:
                    break
        self.write_q.put([cmds.GUI_TERMINATE])

    def _player_vs_player(self):
        turn = 0
        board = MoverBoard(self.args.c_data_folder)
        self.write_q.put([cmds.GAME_SCREEN])
        n_moves = 0

        movers, moves = board.generate_movers_and_moves()
        next_boards = board.generate_next()

        while n_moves < 100 and len(movers)>0:
            canon_b = board.get_canonical_perspective(turn)
            self.write_q.put([cmds.ACQUIRE_HUMAN_INPUT, canon_b, movers, moves])
            cmd = self.read_q.get()

            if cmd[0] == cmds.QUIT_GAME:
                print("received quit")
                return

            chosen_board = next_boards[cmd[1]]
            board.W, board.B, board.K = chosen_board.W, chosen_board.B, chosen_board.K

            board.reverse()
            turn = 0 if turn == 1 else 1

            movers, moves = board.generate_movers_and_moves()
            next_boards = board.generate_next()

            n_moves+=1
        
    
    def _cpu_vs_cpu(self):
        pass

    def _player_vs_cpu(self):
        pass