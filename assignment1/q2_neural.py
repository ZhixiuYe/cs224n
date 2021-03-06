#!/usr/bin/env python

import numpy as np
import random

from q1_softmax import softmax
from q2_sigmoid import sigmoid, sigmoid_grad
from q2_gradcheck import gradcheck_naive


def forward_backward_prop(data, labels, params, dimensions):
    """
    Forward and backward propagation for a two-layer sigmoidal network

    Compute the forward propagation and for the cross entropy cost,
    and backward propagation for the gradients for all parameters.

    Arguments:
    data -- M x Dx matrix, where each row is a training example.
    labels -- M x Dy matrix, where each row is a one-hot vector.
    params -- Model parameters, these are unpacked for you.
    dimensions -- A tuple of input dimension, number of hidden units
                  and output dimension
    """

    ### Unpack network parameters (do not modify)
    ofs = 0
    Dx, H, Dy = (dimensions[0], dimensions[1], dimensions[2])

    W1 = np.reshape(params[ofs:ofs+ Dx * H], (Dx, H))
    ofs += Dx * H
    b1 = np.reshape(params[ofs:ofs + H], (1, H))
    ofs += H
    W2 = np.reshape(params[ofs:ofs + H * Dy], (H, Dy))
    ofs += H * Dy
    b2 = np.reshape(params[ofs:ofs + Dy], (1, Dy))

    ### YOUR CODE HERE: forward propagation
    # 20 * 10 * 10 * 5 = 20 * 5
    h1 = np.dot(data, W1) + b1
    s1 = sigmoid(h1)
    # 20 * 5 * 5 * 10 = 20 * 10
    h2 = np.dot(s1, W2) + b2
    s2 = softmax(h2)

    # raise NotImplementedError
    ### END YOUR CODE

    ### YOUR CODE HERE: backward propagation
    # 20 * 10
    gradh2 = (s2 - labels) / data.shape[0]
    # 20 * 10 * 10 * 5 .* 20 * 5= 20 * 5
    gradh1 = np.dot(gradh2, W2.T) * sigmoid_grad(s1)
    # 10 * 20 * 20 * 5 = 10 * 5
    gradW1 = np.dot(data.T, gradh1)
    # 1 * 20 * 20 * 5 = 1 * 5
    #gradb1 = np.dot(np.ones((1,20)), gradh1)
    gradb1 = np.sum(gradh1, axis=0, keepdims=True)
    # 5 * 20 * 20 * 10 = 5 * 10
    gradW2 = np.dot(s1.T, gradh2)
    # 1 * 20 * 20 * 10 = 1 * 10
    # gradb2 = np.dot(np.ones((1, 20)), gradh2)
    gradb2 = np.sum(gradh2, axis=0, keepdims=True)

    cost = -1 * np.sum(np.log(s2[labels == 1])) / data.shape[0]


    # raise NotImplementedError
    ### END YOUR CODE

    ### Stack gradients (do not modify)

    grad = np.concatenate((gradW1.flatten(), gradb1.flatten(),
        gradW2.flatten(), gradb2.flatten()))

    return cost, grad


def sanity_check():
    """
    Set up fake data and parameters for the neural network, and test using
    gradcheck.
    """
    print "Running sanity check..."

    N = 20
    dimensions = [10, 5, 10]
    data = np.random.randn(N, dimensions[0])   # each row will be a datum
    labels = np.zeros((N, dimensions[2]))
    for i in xrange(N):
        labels[i, random.randint(0,dimensions[2]-1)] = 1

    params = np.random.randn((dimensions[0] + 1) * dimensions[1] + (
        dimensions[1] + 1) * dimensions[2], )

    gradcheck_naive(lambda params:
        forward_backward_prop(data, labels, params, dimensions), params)


def your_sanity_checks():
    """
    Use this space add any additional sanity checks by running:
        python q2_neural.py
    This function will not be called by the autograder, nor will
    your additional tests be graded.
    """
    print "Running your sanity checks..."
    ### YOUR CODE HERE
    raise NotImplementedError
    ### END YOUR CODE


if __name__ == "__main__":
    sanity_check()
    # your_sanity_checks()
