from argparse import Namespace
import tensorflow as tf
from checkers.logic.MoverBoard import MoverBoard
import numpy as np
from checkers.CheckersConstants import CheckersConstants as ccs
from checkers.logic.bb_utils import bb_to_np_compact
from tqdm import tqdm
import os
import matplotlib.pyplot as plot
from checkers.logging_utils import GameLogger
from checkers.AI.MetricsModel import MetricsModel
from checkers.AI.BoardModel import BoardModel
from time import sleep
import logging

from checkers.logging_utils import setup_logging
from keras.callbacks import CSVLogger


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
    boards_list, turns_list, metrics, winning = start_board.generate_games(1000)
    
    board_data = list(map(revert_and_transform, zip(boards_list, turns_list)))
    board_data = np.array(board_data)

    probabilistic = metrics_model.predict_on_batch(metrics)

    probabilistic = np.sign(probabilistic-0.5)
    winnings = np.sign(winning-0.1)

    confidence = 1/(1+ np.absolute(winnings - probabilistic))

    board_model.compile(optimizer='nadam', loss='mean_squared_error')

    board_folder = os.path.join(args.c_model_folder, "board")
    if os.path.exists(board_folder) == False:
        os.mkdir(board_folder)
    board_path = os.path.join(args.c_model_folder, "board", "board_model.ckpt")
    cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=board_path,
                                                 save_weights_only=True,
                                                 verbose=1)
    
    log_path = os.path.join(args.c_model_folder, "board", "tf_log.csv")
    csv_logger = CSVLogger(log_path, append=False, separator=';')

    board_model.fit(board_data, probabilistic, epochs=32, batch_size=64, sample_weight=confidence, verbose=2, callbacks= [cp_callback, csv_logger])
    



def reinforce_board_model(args: Namespace):

    board_model = BoardModel()
    model_path = os.path.join(args.c_model_folder, "board",  "board_model.ckpt")
    status = board_model.load_weights(model_path)
    status.expect_partial()
    board_model.compile(optimizer='nadam', loss='mean_squared_error')
    n_gens = 2
    n_games_per_gen = 2

    start_board = MoverBoard(args.c_data_folder)
    boards_list, turns_list, __, _ = start_board.generate_games(10000)

    winrates = []
    learning_rate = 0.5
    discount_factor = 0.95

    save_folder = os.path.join(args.c_model_folder, "reinforced")
    setup_logging(save_folder)

    if os.path.exists(save_folder) == False:
        os.mkdir(save_folder)
    board_path = os.path.join(args.c_model_folder, "reinforced", "board_model.ckpt")
    cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=board_path,
                                                 save_weights_only=True,
                                                 verbose=1)

    log_path = os.path.join(args.c_model_folder, "reinforced", "tf_log.csv")
    if os.path.exists(log_path):
        os.remove(log_path)
    csv_logger = CSVLogger(log_path, append=True, separator=';')

    for g in range(0, n_gens):
        reinforce_data = np.zeros((1, 32))
        reinforce_labels = np.zeros(1)
        logging.info(f"reinforcing generation: {g}")
        for game in range(0, n_games_per_gen):
            starting_pos = np.random.randint(0, len(boards_list))
            cur_board = MoverBoard(board=boards_list[starting_pos])
            cur_board.reverse()
            cur_player = ccs.WHITE_TURN if turns_list[starting_pos] == ccs.BLACK_TURN else ccs.BLACK_TURN
            turn_n = 0

            temp_reinforce_data = []
            n_w_wins = 0
            n_b_wins = 0
            n_draws = 0
            if game%20==0:
                logging.info(f">>>game number {game}")
            while True:
                boards = cur_board.generate_next()
                board_data = list(map(revert_and_transform, zip(boards, [cur_player for b in boards])))
                board_data = np.array(board_data)

                if len(boards)>0:                
                    scores = board_model.predict_on_batch(board_data)
                    choice = np.argmax(scores) if cur_player == ccs.WHITE_TURN else np.argmin(scores)

                    cur_board = MoverBoard(board=boards[choice])
                    cur_board.reverse()

                    temp_reinforce_data.append(board_data[choice])
                    cur_player = ccs.WHITE_TURN if cur_player == ccs.BLACK_TURN else ccs.BLACK_TURN
                    turn_n +=1

                if turn_n > 100 or len(boards) == 0 or cur_board.is_game_over():
                    if len(temp_reinforce_data) == 0:
                        break
                    canon_b = MoverBoard(board=cur_board.get_canonical_perspective(cur_player))
                    reward = -5
                    opt_pred = -1
                    if canon_b.W > 0 and canon_b.B == 0:
                        reward = 10
                        opt_pred = 1
                        n_w_wins+=1
                    elif canon_b.W == 0 and canon_b.B > 0:
                        reward = -10
                        opt_pred = -1
                        n_b_wins +=1
                    else:
                        reward = -3
                        opt_pred = 0
                        n_draws+=1
                    
                    temp_reinforce_data = np.array(temp_reinforce_data)
                    old_prediction = board_model.predict_on_batch(temp_reinforce_data)
                    optimal_futur_value = opt_pred*np.ones(old_prediction.shape)
                    temp_reinforce_labels = old_prediction + learning_rate * (reward + discount_factor * optimal_futur_value - old_prediction )
                    reinforce_data=np.vstack((reinforce_data, temp_reinforce_data))
                    reinforce_labels =np.vstack((reinforce_labels, temp_reinforce_labels))
                    break
        
        board_model.fit(reinforce_data[1:], reinforce_labels[1:], epochs=16, batch_size=64, verbose=1, callbacks= [cp_callback, csv_logger])
        winrate = int((n_w_wins+n_draws)/(n_w_wins+n_draws+n_b_wins)*100)
        winrates.append(winrate)
    
    generations = np.linspace(0, len(winrates), len(winrates))
    logging.info(f"Final win/draw rate : {winrates[-1]}%" )
    plot.plot(generations,winrates)
    plot.show()


