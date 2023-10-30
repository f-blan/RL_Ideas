from argparse import Namespace
import tensorflow as tf
from checkers.logic.MoverBoard import MoverBoard
import numpy as np
from checkers.CheckersConstants import CheckersConstants as ccs
from tqdm import tqdm
import os
import matplotlib.pyplot as plot
from checkers.logging_utils import GameLogger
from checkers.AI.MetricsModel import MetricsModel

def make_metrics_model(args: Namespace) -> None:
    # Metrics model, which only looks at heuristic scoring metrics used for labeling
    metrics_model = MetricsModel()
    metrics_model.compile(optimizer='nadam', loss= tf.keras.losses.BinaryCrossentropy(from_logits=True), metrics=["acc"])

    logger = GameLogger(args.log_folder, "metrics_logs")
    start_board = MoverBoard(args.c_data_folder)
    
    boards_list, turns_list, metrics, winning = start_board.generate_games(10000)

    log_list = list(map(lambda x: MoverBoard(board=x), boards_list))
    logger.save_game(log_list, turns_list)

    # fit the metrics model
    model_path = os.path.join(args.c_model_folder, "metrics")
    if os.path.exists(model_path) == False:
        os.mkdir(model_path)
        
    model_path = os.path.join(model_path, "metrics_model.ckpt")
    cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=model_path,
                                                 save_weights_only=True,
                                                 verbose=1)
    history = metrics_model.fit(metrics , winning, epochs=12, batch_size=64, verbose=1, callbacks=[cp_callback])
    preds = metrics_model.predict(metrics)

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

