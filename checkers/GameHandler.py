from argparse import Namespace
from checkers.GUI import CheckersGUI, SimpleGUI, TerminalGUI
from checkers.logic.MoverBoard import MoverBoard
from queue import Queue
from checkers.GUI.Commands import Commands as cmds
from checkers.logic.bb_utils import print_bb, bb_to_np
from checkers.CheckersConstants import CheckersConstants as ccs
from checkers.logic.CheckersBoard import CheckersBoard
from checkers.AI.SimpleAI import SimpleAI
from checkers.AI.DeepQAI import DeepQAI
from checkers.logging import GameLogger
import numpy as np

class GameHandler:
    def __init__(self, args: Namespace) -> None:
        self.args = args
        self.read_q = Queue()
        self.write_q = Queue()
        self.log_folder = args.log_folder
        self.helper_board = MoverBoard(args.c_data_folder)
        self.gui = SimpleGUI(args, self.write_q, self.read_q) if args.c_GUI_type == "simple" else TerminalGUI(args, self.write_q, self.read_q)

        self.model_folder = args.c_model_folder
        self.ai_class = DeepQAI if args.c_AI_type == "rl" else SimpleAI
        

    def run_game(self) -> None:
        self.gui.start()
        while True:
            print("handler sends menu screen")
            self.write_q.put([cmds.MENU_SCREEN])
            request = self.read_q.get()
            logger = None
            if len(request) > 1:
                logger = GameLogger(self.log_folder, request[1])
            print("handler received", request)
            match request[0]:
                case cmds.START_PVP_MODE:
                    self._player_vs_player(logger)
                case cmds.START_CVC_MODE:
                    self._cpu_vs_cpu(logger)
                case cmds.START_PVC_MODE:
                    self._player_vs_cpu(logger)
                case cmds.START_VIEW_MODE:
                    self._view_game()
                case cmds.EXIT_APP:
                    break
        self.write_q.put([cmds.GUI_TERMINATE])

    def _view_game(self):
        self.write_q.put([cmds.BROWSE_SCREEN])
        cmd, filename = self.read_q.get()
        if cmd == cmds.QUIT_GAME:
            return
        
        boards = np.load(filename)

        self.write_q.put([cmds.VIEW_SCREEN])
        self.write_q.put([cmds.VIEW_SCREEN, boards])

        self.read_q.get()

    def _player_vs_player(self, logger: GameLogger = None):
        turn = ccs.WHITE_TURN
        board = MoverBoard(self.args.c_data_folder)
        self.write_q.put([cmds.GAME_SCREEN])
        n_moves = 0

        movers, moves = board.generate_movers_and_moves()
        next_boards = board.generate_next()
        boards = []
        canon_b = CheckersBoard()

        while n_moves < 100 and len(movers)>0 and board.W != 0 and board.B != 0:
            canon_b = board.get_canonical_perspective(turn)
            self.write_q.put([cmds.ACQUIRE_HUMAN_INPUT, turn, canon_b, movers, moves])
            
            cmd = self.read_q.get()
            if cmd[0] == cmds.QUIT_GAME:
                return
            
            if cmd[0] == cmds.UNDO_MOVE and len(boards) > 0:
                board = boards.pop()
                movers, moves = board.generate_movers_and_moves()

                next_boards = board.generate_next()
                n_moves-=1
                turn = ccs.WHITE_TURN if turn == ccs.BLACK_TURN else ccs.BLACK_TURN
                continue
            
            boards.append(MoverBoard(board=board))
            chosen_board = next_boards[cmd[1]]
            board.W, board.B, board.K = chosen_board.W, chosen_board.B, chosen_board.K

            board.reverse()
            turn = ccs.WHITE_TURN if turn == ccs.BLACK_TURN else ccs.BLACK_TURN

            movers, moves = board.generate_movers_and_moves()

            next_boards = board.generate_next()

            n_moves+=1
            canon_b = board.get_canonical_perspective(turn)
            
        if board.B == 0 or board.W == 0:
            self.write_q.put([cmds.WHITE_WINS if canon_b.B == 0 else cmds.BLACK_WINS, -1, canon_b, np.array([]), np.array([])])
        else:
            print(n_moves)
            print(movers)
            print(moves)
            self.write_q.put([cmds.DRAW_GAME, -1, canon_b, np.array([]), np.array([])])
        if logger is not None:
            logger.save_game(boards)
        cmd = self.read_q.get()
        
            
    
    def _cpu_vs_cpu(self, logger: GameLogger = None):
        turn = ccs.WHITE_TURN
        board = MoverBoard(self.args.c_data_folder)
        self.write_q.put([cmds.GAME_SCREEN])
        n_moves = 0

        movers, moves = board.generate_movers_and_moves()
        boards = []
        canon_b = CheckersBoard()

        ai_w = self.ai_class(ccs.WHITE_TURN, self.model_folder)
        ai_b = self.ai_class(ccs.BLACK_TURN, self.model_folder)
        

        while n_moves < 100 and len(movers)>0 and board.W != 0 and board.B != 0:
            canon_b = board.get_canonical_perspective(turn)
            cur_ai = ai_w if turn == ccs.WHITE_TURN else ai_b
            cur_ai.copy_state(board)
            next_state = cur_ai.get_next_state()
            self.write_q.put([cmds.PROCESS_CPU_INPUT, turn, canon_b, next_state])
            cmd = self.read_q.get()
            
            if cmd[0] == cmds.QUIT_GAME:
                return
            
            boards.append(MoverBoard(board=board))
            board.W, board.B, board.K = next_state.W, next_state.B, next_state.K

            board.reverse()
            turn = ccs.WHITE_TURN if turn == ccs.BLACK_TURN else ccs.BLACK_TURN

            movers, moves = board.generate_movers_and_moves()
            n_moves+=1
            canon_b = board.get_canonical_perspective(turn)
            
        if board.B == 0 or board.W == 0:
            self.write_q.put([cmds.WHITE_WINS if canon_b.B == 0 else cmds.BLACK_WINS, -1, canon_b, np.array([]), np.array([])])
        else:
            print(n_moves)
            print(movers)
            print(moves)
            self.write_q.put([cmds.DRAW_GAME, -1, canon_b, np.array([]), np.array([])])
        
        if logger is not None:
            logger.save_game(boards)

        cmd = self.read_q.get()
        

    def _player_vs_cpu(self, logger: GameLogger):
        self.write_q.put([cmds.SELECTION_SCREEN])

        cmd = self.read_q.get()[0]
        if cmd == cmds.EXIT_APP:
            return
        player_color = cmd

        turn = ccs.WHITE_TURN
        board = MoverBoard(self.args.c_data_folder)

        self.write_q.put([cmds.GAME_SCREEN])
        n_moves = 0

        movers, moves = board.generate_movers_and_moves()
        next_boards = board.generate_next()
        boards = []
        canon_b = CheckersBoard()
        next_state = MoverBoard()

        ai = self.ai_class(ccs.WHITE_TURN if player_color == ccs.BLACK_TURN else ccs.BLACK_TURN, self.model_folder)
        
        while n_moves < 100 and len(movers)>0 and board.W != 0 and board.B != 0:
            canon_b = board.get_canonical_perspective(turn)

            if turn == player_color:
                self.write_q.put([cmds.ACQUIRE_HUMAN_INPUT, turn, canon_b, movers, moves])
            else:
                ai.copy_state(board)
                next_state = ai.get_next_state()
                self.write_q.put([cmds.PROCESS_CPU_INPUT, turn, canon_b, next_state])
            cmd = self.read_q.get()

            if cmd[0] == cmds.QUIT_GAME:
                return
            
            if cmd[0] == cmds.UNDO_MOVE and len(boards) > 0:
                board = boards.pop()
                board = boards.pop()
                movers, moves = board.generate_movers_and_moves()

                next_boards = board.generate_next()
                n_moves-=2
                continue
            
            boards.append(MoverBoard(board=board))
            
            if player_color == turn:
                chosen_board = next_boards[cmd[1]]
                board.W, board.B, board.K = chosen_board.W, chosen_board.B, chosen_board.K
            else:
                board.W, board.B, board.K = next_state.W, next_state.B, next_state.K

            board.reverse()
            turn = ccs.WHITE_TURN if turn == ccs.BLACK_TURN else ccs.BLACK_TURN

            movers, moves = board.generate_movers_and_moves()

            next_boards = board.generate_next()

            n_moves+=1
            canon_b = board.get_canonical_perspective(turn)
            
        if board.B == 0 or board.W == 0:
            self.write_q.put([cmds.WHITE_WINS if canon_b.B == 0 else cmds.BLACK_WINS, -1, canon_b, np.array([]), np.array([])])
        else:
            print(n_moves)
            print(movers)
            print(moves)
            self.write_q.put([cmds.DRAW_GAME, -1, canon_b, np.array([]), np.array([])])
        
        if logger is not None:
            logger.save_game(boards)

        cmd = self.read_q.get()