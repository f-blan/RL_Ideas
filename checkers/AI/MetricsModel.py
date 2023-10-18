from argparse import Namespace
import tensorflow as tf
from checkers.logic.MoverBoard import MoverBoard
import numpy as np
from checkers.CheckersConstants import CheckersConstants as ccs
from checkers.logic.bb_utils import bb_to_np
from tqdm import tqdm
import os
import matplotlib.pyplot as plot


class MetricsModel(tf.keras.Model):
    def __init__(self):
        super().__init__()
        self.d1 = tf.keras.layers.Dense(32, activation='relu', input_dim=6)
        self.d2 = tf.keras.layers.Dense(16, activation='relu',  kernel_regularizer=tf.keras.regularizers.l2(0.1))
        self.out = tf.keras.layers.Dense(1, activation='relu',  kernel_regularizer=tf.keras.regularizers.l2(0.1))

    def call(self, inputs, training=None, mask=None):
        x = self.d1(inputs)
        x = self.d2(x)
        x = self.out(x)
        return x