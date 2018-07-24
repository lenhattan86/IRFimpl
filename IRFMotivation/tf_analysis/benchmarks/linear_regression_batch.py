import numpy as np
import matplotlib.pyplot as plt
import time

import os
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

start = time.time()

# Define number of gradient descent loops
n_loops = 5000
# Define input data
nData = 10000000
X_data = np.arange(nData, step=0.1)
y_data = X_data + 20 * np.sin(X_data / 10)

# Plot input data
# plt.plot(X_data, y_data, c='r')
# plt.show()

import tensorflow as tf

# Define parameters
n_samples = len(X_data)
batch_size = 100000

# TensorFlow requires each sample to be an array
# even if the number of features is one
X_data = np.reshape(X_data, (n_samples, 1))
y_data = np.reshape(y_data, (n_samples, 1))

# Define placeholders for input
X = tf.placeholder(tf.float32, shape=(batch_size, 1))
y = tf.placeholder(tf.float32, shape=(batch_size, 1))

# Define variables to be learned
with tf.variable_scope("linear-regression"):
    # Define a tensor of size 1 x 1
    W = tf.get_variable("weights", (1, 1),
                        # initialize W randomly from normal
                        # distribution
                        initializer=tf.random_normal_initializer())
    # Define a tensor of size 1 (vector of size 1)
    b = tf.get_variable("bias", (1, ),
                        # initialized with 0
                        initializer=tf.constant_initializer(0.0))
    y_pred = tf.matmul(X, W) + b
    loss = tf.reduce_sum((y - y_pred) ** 2 / n_samples)

# Define optimizer operation
optimizer = tf.train.AdamOptimizer()
optimize = optimizer.minimize(loss)

with tf.Session() as sess:
    # Initialize Variables in graph
    sess.run(tf.global_variables_initializer())

    for step_idx in range(n_loops):
        # Select random mini-batch
        indices = np.random.choice(n_samples, batch_size)
        X_batch, y_batch = X_data[indices], y_data[indices]

        # Perform a single gradient descent step
        _, loss_val = sess.run([optimize, loss],
                               # feed_dict: placeholder -> data
                               feed_dict={X: X_batch, y: y_batch})

        # Print training status
        # print("[{}] loss: {}".format(step_idx + 1, loss_val))

    W_val, b_val = sess.run([W, b])

end = time.time()

print("End time "+str(end - start)+" seconds")