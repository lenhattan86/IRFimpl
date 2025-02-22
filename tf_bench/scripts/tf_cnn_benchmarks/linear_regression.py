'''
A linear regression learning algorithm example using TensorFlow library.

Author: Aymeric Damien
Project: https://github.com/aymericdamien/TensorFlow-Examples/
'''

from __future__ import print_function

import tensorflow as tf
import argparse

import numpy
rng = numpy.random

#"python tf_cnn_benchmarks.py --device=cpu --data_format=NHWC --num_warmup_batches=0  --model=lenet --batch_size=32 --num_intra_threads=19 --num_batches=3750"

parser = argparse.ArgumentParser()
parser.add_argument('--batch_size', help='batch_size', required=False, default=32)
parser.add_argument('--data_size', help='data_size', required=False, default=1700)
parser.add_argument('--num_intra_threads', help='num_intra_threads', required=False, default=19)
parser.add_argument('--num_batches', help='num_batches', required=False, default=5000000)
parser.add_argument('--device', help='device', required=False, default='gpu')

args = vars(parser.parse_args())

batch_size = int(args['batch_size'])
data_size = int(args['data_size'])
num_intra_threads =int(args['num_intra_threads'])
num_batches =int(args['num_batches'])
device =args['device']

# Parameters
learning_rate = 0.01
training_epochs = num_batches
display_step = 50

# Training Data
#train_X = numpy.asarray([3.3,4.4,5.5,6.71,6.93,4.168,9.779,6.182,7.59,2.167, 7.042,10.791,5.313,7.997,5.654,9.27,3.1])                         
#train_Y = numpy.asarray([1.7,2.76,2.09,3.19,1.694,1.573,3.366,2.596,2.53,1.221, 2.827,3.465,1.65,2.904,2.42,2.94,1.3])
#n_samples = train_X.shape[0]

n_samples=data_size
train_X=rng.rand(1,n_samples)
train_Y=rng.rand(1,n_samples)


with tf.device('/'+device+':0'):
    # tf Graph Input
    X = tf.placeholder("float")
    Y = tf.placeholder("float")

    # Set model weights
    W = tf.Variable(rng.randn(), name="weight")
    b = tf.Variable(rng.randn(), name="bias")

    # Construct a linear model
    pred = tf.add(tf.multiply(X, W), b)

    # Mean squared error
    cost = tf.reduce_sum(tf.pow(pred-Y, 2))/(2*n_samples)
    # Gradient descent
    #  Note, minimize() knows to modify W and b because Variable objects are trainable=True by default
    optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(cost)

    # Initializing the variables
    init = tf.global_variables_initializer()

    # gpu share
#gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.2)

# Launch the graph
newConfig = tf.ConfigProto()
newConfig.intra_op_parallelism_threads = num_intra_threads
with tf.Session(config=newConfig) as sess:
# with tf.Session() as sess:
    sess.run(init)
    # Fit all training data
    for epoch in range(training_epochs):
        for (x, y) in zip(train_X, train_Y):
            sess.run(optimizer, feed_dict={X: x, Y: y})