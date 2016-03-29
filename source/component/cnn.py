#-*- encoding: utf-8 -*-
'''
A Theano-based program for convolutional neural network

Supports several layer types (fully connected, convolutional, max
pooling, softmax), and activation functions (sigmoid, tanh, and
rectified linear units, with more easily added).

'''

#### Libraries
# Standard library
import cPickle
import gzip

# Third-party libraries
import numpy as np
import theano
import theano.tensor as T 
from theano.tensor.nnet import conv # for convolutional layer
from theano.tensor.nnet import softmax # for softmax layer
from theano.tensor import shared_randomstreams # for random
from theano.tensor.signal import downsample # for pooling

# static variables
SAVE_PATH = "../config/result/"
OUTPUT_SIZE = 3

GPU = False
if GPU:
    print "Trying to run under a GPU.  If this is not desired, then modify "+\
        "cnn.py\nto set the GPU flag to False."
    try: theano.config.device = 'gpu'
    except: pass # it's already set
    theano.config.floatX = 'float32'
else:
    print "Running with a CPU.  If this is not desired, then the modify "+\
        "cnn.py\nto set the GPU flag to True."

# Activation functions for neurons
def linear(z): return z
def ReLU(z): return T.maximum(0.0, z)
from theano.tensor.nnet import sigmoid
from theano.tensor import tanh


#### Load the MNIST data
def load_data_shared(filename="../data/expanded/data.pkl"):
    f = open(DATA_DIR+"data.pkl", 'rb')
    training_data, validation_data, test_data = cPickle.load(f)
    f.close()
    def shared(data):
        '''
        Place the data into shared variables.  This allows Theano to copy
        the data to the GPU, if one is available.
        
        是用borrow属性让get_value的时候值更新的时候能够获取到 
        more detail： http://deeplearning.net/software/theano/tutorial/aliasing.html#borrowing-when-creating-shared-variables
        '''
        shared_x = theano.shared(np.asarray(data[0], dtype=theano.config.floatX), borrow=True)
        shared_y = theano.shared(np.asarray(data[1], dtype=theano.config.floatX), borrow=True)
        return shared_x, T.cast(shared_y, "int32")
    return [shared(training_data), shared(validation_data), shared(test_data)]

#### Main class used to construct and train networks
class Network(object):
    def __init__(self, layers, mini_batch_size):
        '''
        Takes a list of `layers`, describing the network architecture, and
        a value for the `mini_batch_size` to be used during training
        by stochastic gradient descent.
        '''
        self.layers = layers
        self.mini_batch_size = mini_batch_size
        self.params = [param for layer in self.layers for param in layer.params]
        self.x = T.matrix("x") # input
        self.y = T.ivector("y") # output
        init_layer = self.layers[0]
        init_layer.set_inpt(self.x, self.x, self.mini_batch_size)
        for i in xrange(1, len(len(layers))):
            prev_layer, layer = self.layers[i-1], self.layers[i]
            layer.set_inpt(prev_layer.output, prev_layer.output_dropout, self.mini_batch_size)
        self.output = self.layers[-1].output
        self.output_dropout = self.layers[-1].output_dropout

    def SGD(self, training_data, epochs, mini_batch_size, eta,
            validation_data, test_data, lmbda=0.0):
        

#### Define layer types

class ConvPoolLayer(object):
    '''
    Used to create a combination of a convolutional and a max-pooling
    layer.  A more sophisticated implementation would separate the
    two, but for our purposes we'll always use them together, and it
    simplifies the code, so it makes sense to combine them.
    '''

    def __init__(self, filter_shape, image_shape, poolsize=(2, 2),
                 activation_fn=ReLU):
        '''
        `filter_shape` is a tuple of length 4, whose entries are the number
        of filters, the number of input feature maps, the filter height, and the
        filter width.

        `image_shape` is a tuple of length 4, whose entries are the
        mini-batch size, the number of input feature maps, the image
        height, and the image width.

        `poolsize` is a tuple of length 2, whose entries are the y and
        x pooling sizes.
        '''
        self.filter_shape = filter_shape
        self.image_shape = image_shape
        self.poolsize = poolsize
        self.activation_fn=activation_fn
        # initialize weights and biases
        n_out = filter_shape[0] * np.prod(filter_shape[2:]) / np.prod(poolsize)
        self.w = theano.shared(
            np.asarray(
                np.random.normal(loc=0, scale=np.sqrt(1.0/n_out), size=filter_shape),
                dtype=theano.config.floatX),borrow=True)
        self.b = theano.shared(
            np.asarray(
                np.random.normal(loc=0, scale=1.0, size=(filter_shape[0],)),
                dtype=theano.config.floatX),borrow=True)
        self.params = [self.w, self.b]

    def set_inpt(self, inpt, inpt_dropout, mini_batch_size):
        # no dropout in the convolutional layers
        pass

class FullyConnectedLayer(object):

    def __init__(self, n_in, n_out, activation_fn=sigmoid, p_dropout=0.0):
        self.n_in = n_in
        self.n_out = n_out
        self.activation_fn = activation_fn
        self.p_dropout = p_dropout
        # Initialize weights and biases
        self.w = theano.shared(
                np.asarray(
                    np.random.normal(loc=0.0, scale=np.sqrt(1.0/n_out), size=(n_in, n_out)
                ), dtype=theano.config.floatX),name="w", borrow=True
            )
        self.b = theano.shared(
                np.asarray(
                    np.random.normal(loc=0.0, scale=np.sqrt(1.0/n_out), size=(n_out)
                ), dtype=theano.config.floatX),name="b", borrow=True
            )
        self.params=[self.w, self.b]

    def set_inpt(self, inpt, inpt_dropout, mini_batch_size):
        pass

    def accuracy(self, y):
        "Return the accuracy for the mini-batch."
        pass

# Softmax可以加快学习速度，主要是修改a和C
class SoftmaxLayer(object):

    def __init__(self, n_in, n_out, p_dropout=0.0):
        self.n_in = n_in
        self.n_out = n_out
        self.p_dropout = p_dropout
        # Initialize weights and biases
        self.w = theano.shared(
            np.zeros((n_in, n_out), dtype=theano.config.floatX),
            name='w', borrow=True)
        self.b = theano.shared(
            np.zeros((n_out,), dtype=theano.config.floatX),
            name='b', borrow=True)
        self.params = [self.w, self.b]

    def set_inpt(self, inpt, inpt_dropout, mini_batch_size):
        pass

    def cost(self, net):
        "Return the log-likelihood cost."
        pass

    def accuracy(self, y):
        "Return the accuracy for the mini-batch."
        pass

### other functions

def dropout_layer(layer, p_dropout):
    srng = shared_randomstreams.RandomStreams(
        np.random.RandomState(0).randint(999999))
    mask = srng.binomial(n=1, p=1-p_dropout, size=layer.shape)
    return layer*T.cast(mask, theano.config.floatX)

