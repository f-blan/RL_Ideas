from argparse import Namespace
import tensorflow as tf
from checkers.CheckersConstants import CheckersConstants as ccs
from checkers.logic.bb_utils import bb_to_np

class BoardModel(tf.keras.Model):
    def __init__(self):
        super().__init__()
        self.d1 = tf.keras.layers.Dense(64, activation='relu', input_dim=32)

        # use regularizers, to prevent fitting noisy labels
        self.d2 = tf.keras.layers.Dense(32 , activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.01))
        self.d3 = tf.keras.layers.Dense(16 , activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.01)) # 16
        self.d4 = tf.keras.layers.Dense(8 , activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.01)) # 8

        self.out = tf.keras.layers.Dense(1 , activation='linear', kernel_regularizer=tf.keras.regularizers.l2(0.01)) 

    def call(self, x: tf.Tensor) -> tf.Tensor:
        x = self.d1(x)
        x = self.d2(x)
        x = self.d3(x)
        x = self.d4(x)
        x = self.out(x)

        return x