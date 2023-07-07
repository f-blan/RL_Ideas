import tensorflow as tf
import numpy as np

print("TensorFlow version:", tf.__version__)

print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))