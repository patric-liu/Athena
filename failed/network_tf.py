import random
import numpy as np 
import tensorflow as tf

# TWO HIDDEN LAYER NETWORK

RANDOM_SEED = 42
tf.set_random_seed(RANDOM_SEED)

def init_weights(shape):
	# Weight initialization
	weights = tf.truncated_normal(shape, stddev=0.1)
	return tf.Variable(weights)
def init_biases(shape):
	# Bias initialization
	biases = tf.constant(0.1, shape=shape)
	return tf.Variable(biases)

def forwardprop(X, w_1, w_2, w_3):
	h1 = tf.nn.relu(tf.matmul(X,w_1))
	h2 = tf.nn.relu(tf.matmul(h1,w_2))
	yhat = tf.matmul(h2, w_3)
	return yhat

h1_size = 50 # Number of hidden nodes in hidden layer 1
h2_size = 50 # Number of hidden nodes in hidden layer 2

x_size = 1000 # input size
y_size = 1 # output size

X = tf.placeholder(tf.float32, shape=[None, x_size])
y = tf.placeholder(tf.float32, shape=[None, y_size])

w_1 = init_weights([x_size,h1_size])
w_2 = init_weights([h1_size,h2_size])
w_3 = init_weights([h2_size,y_size]) 
b_1 = init_biases([h1_size])
b_2 = init_biases([h2_size])
b_3 = init_biases([y_size])

yhat = forwardprop(X, w_1, w_2, w_3)

sess = tf.InteractiveSession()
sess.run(tf.global_variables_initializer())

