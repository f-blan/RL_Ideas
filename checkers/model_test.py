from argparse import Namespace
from checkers.AI.BoardModel import BoardModel
from checkers.AI.SimpleAI import SimpleAI
from checkers.AI.DeepQAI import DeepQAI
import numpy as np
from checkers.CheckersConstants import CheckersConstants as ccs
from checkers.logic.MoverBoard import MoverBoard
from typing import Tuple
import os

def test_reinforce(args: Namespace):
    print("TESTING THE AI")
    board_model = BoardModel()
    model_path = os.path.join(args.c_model_folder, "board",  "board_model.ckpt")
    _ = MoverBoard(args.c_data_folder)
    status = board_model.load_weights(model_path)
    status.expect_partial()
    board_model.compile(optimizer='nadam', loss='mean_squared_error')

    acc, w_acc, b_acc, draw_rate= model_validate(board_model)

    print("accuracy total: ", acc, "accuracy as white: ", w_acc, "accuracy as black", b_acc, "draw_rate", draw_rate)

def model_validate(model: BoardModel, ground_model_type: str = "SimpleAI", n_games: int = 100) -> Tuple[float, float, float, float]:
    games_as_white = n_games//2
    outcomes = np.array([ccs.DRAW_GAME for i in range(0, n_games)])

    opponentAI = SimpleAI

    for i in range(0, n_games):
        cur_color =  ccs.WHITE_TURN if i < games_as_white else ccs.BLACK_TURN
        opp_color =  ccs.BLACK_TURN if i < games_as_white else ccs.WHITE_TURN

        tested_model = DeepQAI(cur_color, model=model)
        opponent = opponentAI(opp_color)

        cur_board = MoverBoard()
        cur_turn = ccs.WHITE_TURN
        n_moves = 0

        while n_moves < 300 and cur_board.can_move():
            cur_ai = tested_model if cur_turn == cur_color else opponent
            cur_ai.copy_state(cur_board)
            cur_board = cur_ai.get_next_state()
            cur_board.reverse()
            cur_turn = ccs.BLACK_TURN if cur_turn == ccs.WHITE_TURN else ccs.WHITE_TURN
            n_moves +=1

        canon_b = cur_board.get_canonical_perspective(cur_turn)
        outcomes[i] = canon_b.get_winner()

    wins_as_white = (outcomes[:games_as_white] == ccs.WHITE_TURN).sum()
    wins_as_black = (outcomes[games_as_white:] == ccs.BLACK_TURN).sum()
    n_draws = (outcomes == ccs.DRAW_GAME).sum()

    return (wins_as_white+wins_as_black)/n_games, wins_as_white/games_as_white, wins_as_black/(n_games-games_as_white), n_draws/n_games

    