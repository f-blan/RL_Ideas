from argparse import Namespace
import tensorflow as tf
from checkers.logic.MoverBoard import MoverBoard
import numpy as np
from checkers.CheckersConstants import CheckersConstants as ccs
from checkers.logic.bb_utils import bb_to_np
from tqdm import tqdm
import os
import matplotlib.pyplot as plot

def test_model(args: Namespace):
    # Metrics model, which only looks at heuristic scoring metrics used for labeling
    metrics_model = tf.keras.Sequential()
    metrics_model.add(tf.keras.layers.Dense(32, activation='relu', input_dim=6)) 
    metrics_model.add(tf.keras.layers.Dense(16, activation='relu',  kernel_regularizer=tf.keras.regularizers.l2(0.1)))

    # output is passed to relu() because labels are binary
    metrics_model.add(tf.keras.layers.Dense(1, activation='relu',  kernel_regularizer=tf.keras.regularizers.l2(0.1)))

    