'''
A linear regression learning algorithm example using TensorFlow library.

Author: Aymeric Damien
Project: https://github.com/aymericdamien/TensorFlow-Examples/
'''

from __future__ import print_function

from tensorflow.python.client import timeline
import tensorflow as tf
import numpy
import matplotlib.pyplot as plt

import timeline as tl

rng = numpy.random

# Parameters
learning_rate = 0.01
training_epochs = 1
display_step = 50

# Training Data
train_X = numpy.asarray([3.3,4.4,5.5,6.71,6.93,4.168,9.779,6.182,7.59,2.167,
                         7.042,10.791,5.313,7.997,5.654,9.27,3.1])
train_Y = numpy.asarray([1.7,2.76,2.09,3.19,1.694,1.573,3.366,2.596,2.53,1.221,
                         2.827,3.465,1.65,2.904,2.42,2.94,1.3])
n_samples = train_X.shape[0]

with tf.device('/cpu:0'):
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

#config = tf.ConfigProto()
#config.gpu_options.allow_growth = True
#config.gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.333)
#    gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.05)

# Launch the graph
#with tf.Session(config=tf.ConfigProto(gpu_options=gpu_options)) as sess:
with tf.Session(config=tf.ConfigProto(log_device_placement=True)) as sess:
    # create run_metadata for timeline
    run_options = tf.RunOptions(trace_level=tf.RunOptions.FULL_TRACE)
    run_metadata = tf.RunMetadata()
    many_runs_timeline = tl.TimeLiner()

    sess.run(init)

    # Fit all training data
    for epoch in range(training_epochs):
        for (x, y) in zip(train_X, train_Y):
            sess.run(optimizer, feed_dict={X: x, Y: y}, options=run_options, run_metadata=run_metadata)

        # if epoch % display_step == 0 && i % :
#        if epoch <= 1:
            # Create the Timeline object, and write it to a json
            fetched_timeline = timeline.Timeline(run_metadata.step_stats)
            chrome_trace = fetched_timeline.generate_chrome_trace_format()
            many_runs_timeline.update_timeline(chrome_trace)

    many_runs_timeline.save('linear_regression_cpu.json')
