from argparse import Namespace
import tensorflow as tf
from checkers.logic.MoverBoard import MoverBoard
import numpy as np
from checkers.CheckersConstants import CheckersConstants as ccs
from checkers.logic.bb_utils import bb_to_np_compact
from tqdm import tqdm
import os
import matplotlib.pyplot as plot
from checkers.logging import GameLogger
from checkers.AI.MetricsModel import MetricsModel
from checkers.AI.BoardModel import BoardModel
from time import sleep

def revert_and_transform(arg):
    board = arg[0]
    turn = arg[1]
    canon_b = MoverBoard(board = board).get_canonical_perspective(turn)
    np_mat = bb_to_np_compact(canon_b.W, canon_b.B, canon_b.K)
    return np_mat.flatten()

def make_initial_q_value(args: Namespace):
    board_model = BoardModel()

    metrics_model = MetricsModel()
    metrics_path = os.path.join(args.c_model_folder, "metrics",  "metrics_model.ckpt")
    status = metrics_model.load_weights(metrics_path)
    status.expect_partial()

    
    start_board = MoverBoard(args.c_data_folder)
    boards_list, turns_list, metrics, winning = start_board.generate_games(10000)
    
    board_data = list(map(revert_and_transform, zip(boards_list, turns_list)))
    board_data = np.array(board_data)

    probabilistic = metrics_model.predict_on_batch(metrics)

    probabilistic = np.sign(probabilistic-0.5)
    winnings = np.sign(winning-0.1)

    print((probabilistic == -1).sum())
    print((probabilistic == 1).sum())
    
    print((probabilistic == winnings).sum())
    confidence = 1/(1+ np.absolute(winnings - probabilistic))

    board_model.compile(optimizer='nadam', loss='mean_squared_error')

    board_folder = os.path.join(args.c_model_folder, "board2")
    if os.path.exists(board_folder) == False:
        os.mkdir(board_folder)
    board_path = os.path.join(args.c_model_folder, "board", "board_model.ckpt")
    cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=board_path,
                                                 save_weights_only=True,
                                                 verbose=1)

    board_model.fit(board_data, probabilistic, epochs=32, batch_size=64, sample_weight=confidence, verbose=2, callbacks= [cp_callback])
    



def reinforce_board_model(args: Namespace):
    board_model = BoardModel()
    model_path = os.path.join(args.c_model_folder, "board",  "board_model.ckpt")
    status = board_model.load_weights(model_path)
    status.expect_partial()

    start_board = MoverBoard(args.c_data_folder)
    boards_list, turns_list, metrics, winning = start_board.generate_games(10000)

    board_data = list(map(revert_and_transform, zip(boards_list, turns_list)))
    board_data = np.array(board_data)

    preds = board_model.predict_on_batch(board_data)

    print("positive preds", (preds > 0).sum())
    print("positive preds", (preds > 1).sum())
    print("negative preds", (preds < 0).sum())
    print("negative preds", (preds < -1).sum())

    i=0
    for metric, winning, board, pred in zip(metrics, winning, board_data, preds):
        print("-----------")
        print(metric)
        print(board)
        print(winning)
        print(pred)
        print("-----------")
        i+=1
        if i == 2:
            break