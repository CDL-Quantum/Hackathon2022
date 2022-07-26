import pandas as pd
import numpy as np
from pennylane import numpy as np
from sklearn.preprocessing import normalize
from sklearn.preprocessing import StandardScaler

import pennylane as qml
#from pennylane_qiskit import IBMQDevice
#from pennylane_qiskit import BasicAerDevice
from pennylane.templates.embeddings import AngleEmbedding, AmplitudeEmbedding
from pennylane.optimize import AdamOptimizer
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA

import time

class QBC:
    def __init__(self, data, n_dim, n_layers, 
                 optimizer = AdamOptimizer(stepsize=0.1, beta1=0.9, beta2=0.99, eps=1e-08),
                 interface_type = "autograd",
                 loss_function = None,  backend = "default.qubit", shots = None):
        
        if loss_function == None:
            def square_loss(labels, predictions):
                loss = 0
                for l, p in zip(labels, predictions):
                    loss = loss + (l - p) ** 2

                loss = loss / len(labels)
                return loss
            self.loss_function = square_loss
        else: 
            self.loss_function = loss_function
        self.opt = optimizer
        self.data = data
        
        self.n_dim = n_dim
        
        dev = qml.device(backend, wires = self.n_dim, shots=shots)
        #dev = qml.device('default.qubit.tf', wires = num_qubits, shots=1024)
        #dev = qml.device('qiskit.ibmq', wires = num_qubits, backend='ibmq_manila', ibmqx_token="6cc75c58fc80fea56cb8dd391f8fbcfdb676a3dc7005493728bc9da7ea753e31a2110a01e3a0cc83f1a98f5ca79e32956fc66c11b5eea4cae163b3fa996be356", shots=256)
        #dev = qml.device('qiskit.basicaer', wires = num_qubits, shots = 256)

        @qml.qnode(dev)
        def circuit(parameters, data):
            for i in range(n_dim):
                qml.Hadamard(wires = i)

            AngleEmbedding(features = data, wires = range(self.n_dim), rotation = 'Y')

            qml.StronglyEntanglingLayers(weights = parameters, wires = range(self.n_dim))

            return qml.expval(qml.PauliZ(0))
        
        self.qlayer = qml.QNode(circuit, dev, interface=interface_type, diff_method='best')
        
        self.n_layers = n_layers
        self.weights = 0.01 * np.random.randn(self.n_layers, self.n_dim, 3, requires_grad=True)
        self.bias = np.array(0.0, requires_grad=True)

    def variational_classifier(self, weights, bias, x):
        return self.qlayer(weights, x) + bias
        
    def train(self, batch_size = 10, n_epochs = 50):
        wbest = 0
        bbest = 0
        abest = 0
        X, Y, _, _ = self.data.get_preprocessed()
        
        def cost(weights, bias, X, Y):
            predictions = [self.variational_classifier(weights, bias, x) for x in X]
            return self.loss_function(Y, predictions)

        def accuracy(labels, predictions):

            loss = 0
            for l, p in zip(labels, predictions):
                if abs(l - p) < 1e-5:
                    loss = loss + 1
            loss = loss / len(labels)

            return loss

        for it in range(n_epochs):

            # weights update by one optimizer step

            batch_index = np.random.randint(0, len(X), (batch_size,))
            X_batch = X[batch_index]
            Y_batch = Y[batch_index]
            self.weights, self.bias, _, _ = self.opt.step(cost, self.weights, self.bias, X_batch, Y_batch)

            # Compute the accuracy
            predictions = [np.sign(self.variational_classifier(self.weights, self.bias, x)) for x in X]

            if accuracy(Y, predictions) > abest:
                wbest = self.weights
                bbest = self.bias
                abest = accuracy(Y, predictions)
                print('New best')

            acc = accuracy(Y, predictions)

            print(
                "Iter: {:5d} | Cost: {:0.7f} | Accuracy: {:0.7f} ".format(
                    it + 1, cost(self.weights, self.bias, X, Y), acc
                )
            )
            
        self.weights = wbest
        self.bias = bbest
        
    def predict(self, test_data):
        predictions = [np.sign(self.variational_classifier(self.weights, self.bias, x)) for x in test_data]
        return predictions