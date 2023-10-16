from argparse import Namespace
import tensorflow as tf
from checkers.logic.MoverBoard import MoverBoard
import numpy as np
from checkers.CheckersConstants import CheckersConstants as ccs
from checkers.logic.bb_utils import bb_to_np
from tqdm import tqdm
import os
import matplotlib.pyplot as plot
from checkers.logging import GameLogger

def make_metrics_model(args: Namespace) -> None:
    # Metrics model, which only looks at heuristic scoring metrics used for labeling
    metrics_model = tf.keras.Sequential()
    metrics_model.add(tf.keras.layers.Dense(32, activation='relu', input_dim=6)) 
    metrics_model.add(tf.keras.layers.Dense(16, activation='relu',  kernel_regularizer=tf.keras.regularizers.l2(0.1)))

    logger = GameLogger(args.log_folder, "metrics_logs")

    # output is passed to relu() because labels are binary
    metrics_model.add(tf.keras.layers.Dense(1, activation='relu',  kernel_regularizer=tf.keras.regularizers.l2(0.1)))
    metrics_model.compile(optimizer='nadam', loss='binary_crossentropy', metrics=["acc"])

    start_board = MoverBoard(args.c_data_folder)
    boards_list = start_board.generate_next()
    turns_list = [ccs.WHITE_TURN for b in boards_list]
    branching_position = 0
    nmbr_generated_game = 10000
    cur_turn = ccs.WHITE_TURN
	
    print("generating games")
    pbar = tqdm(total=nmbr_generated_game)
    while len(boards_list) < nmbr_generated_game:
        temp = len(boards_list)-1
        for i in range(branching_position, len(boards_list)):
            cur_board = MoverBoard(board=boards_list[i])
            cur_board.reverse()
            if cur_board.can_move():
                next_gen = cur_board.generate_next()
                next_turns = [cur_turn for b in next_gen]
                boards_list += next_gen
                turns_list+=next_turns
                pbar.update(len(next_turns))
        branching_position = temp
        cur_turn = ccs.WHITE_TURN if cur_turn == ccs.BLACK_TURN else ccs.BLACK_TURN

    pbar.close()
    # calculate/save heuristic metrics for each game state
    metrics	= np.zeros((0, 6))
    winning = np.zeros((0, 1))

    print("processing games")
    for board, turn in tqdm(zip(boards_list[:nmbr_generated_game], turns_list[:nmbr_generated_game])):
        canon_b = MoverBoard(board = board).get_canonical_perspective(turn)
        np_b = bb_to_np(canon_b.W, canon_b.B, canon_b.K)
        temp = canon_b.get_metrics()

        metrics = np.vstack((metrics, temp[1:]))
        winning = np.vstack((winning, temp[0]))
    
    logger.save_game(boards_list)
    # fit the metrics model
    model_path = os.path.join(args.c_model_folder, "metrics_model.ckpt")
    cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=model_path,
                                                 save_weights_only=True,
                                                 verbose=1)
    history = metrics_model.fit(metrics , winning, epochs=4, batch_size=64, verbose=1, callbacks=[cp_callback])
    print(history.history)
    # History for accuracy
    plot.plot(history.history['acc'])
    #plot.plot(history.history['val_acc'])
    plot.title('model accuracy')
    plot.ylabel('accuracy')
    plot.xlabel('epoch')
    plot.legend(['train', 'validation'], loc='upper left')
    plot.show()

    # History for loss
    plot.plot(history.history['loss'])
    #plot.plot(history.history['val_loss'])
    plot.title('model loss')
    plot.ylabel('loss')
    plot.xlabel('epoch')
    plot.legend(['train', 'validation'], loc='upper left')
    plot.show()
