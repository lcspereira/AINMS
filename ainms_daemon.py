#!/usr/bin/python3
'''
Created on 20 de fev de 2018

@author: lucas
Neural network backend.
'''

from sklearn.neural_network import MLPClassifier
import matplotlib.pyplot as plt, mpld3
import pandas
import socket
import os
import pickle
import numpy as np
import _thread


def show_graphs (dataset, loss):
    """ Function to show the program graphs on other thread.
    dataset -- pandas dataset to graph
    loss -- neural network loss curve
    """
    try:
        plt.plot (loss)
        plt.ylabel ("Perda")
        plt.title ("Curva de Perda da Rede Neural")
        plt.xlabel ("Iteração")

        '''
        eighty_percent = np.full ((dataset.shape[0]), 80)
        ten_percent = np.full ((dataset.shape[0]), 10)

        #dataset.iloc[:,:-1].plot.bar(width=5)
        dataset.iloc[:,:-1].plot(figsize=(20,6))
        plt.plot (dataset.index, eighty_percent, 'r--')
        plt.plot (dataset.index, ten_percent, 'y--')
        plt.axes().get_xaxis().set_visible (False)
        plt.title ("Visualização de Dados de Treinamento")
        plt.ylabel ("%")
        
        with open("/tmp/train.html", 'w') as html_chart: 
            html_chart.write (mpld3.fig_to_html (plt.gcf()))
        '''
        plt.show()
        plt.close()
    except Exception as ex:
        raise (ex)

def train_device (train_file):
    """Instantiate and train the neural network using a CSV file. Returns the neural network.
    train_file -- Path to the CSV train file.
    """
    dataset = pandas.read_csv (train_file)
    X, y = dataset.iloc[:,:-1], dataset.iloc[:, -1]

    # Multilayer perceptron classifier
    # Model: Error Backpropagation
    # Activation function: Logistic sigmoid
    #clf = MLPClassifier(solver='sgd', activation='logistic', hidden_layer_sizes=(92,60), max_iter=10000, learning_rate='constant', tol=0.0001, verbose=True)
    clf = MLPClassifier(solver='sgd', activation='logistic', hidden_layer_sizes=(3200,), max_iter=10000, learning_rate='adaptive', tol=0.001, learning_rate_init=0.01, verbose=True, early_stopping=False)
    clf.fit (X, y)
    _thread.start_new_thread(show_graphs, tuple([dataset, clf.loss_curve_]))
    return clf

# Create Unix socket for frontend communication
server = socket.socket (socket.AF_UNIX, socket.SOCK_STREAM)
server.bind("/tmp/ainms.sock")
server.listen(1)

print ("Loading training data...")
if_clf = train_device('/etc/ainms/if_train.csv')
print ("[ OK ]")
print ("Waiting data input...")
while True:
    try:
        conn, client_addr = server.accept()
        while True:
            data = conn.recv (5192)
            if data:
                # Receive serialized management data gathered by frontend program
                mgmt_data = pickle.loads (data)
                print (str(mgmt_data[0]))
                # Process on neural network and sends the result to frontend.
                conn.sendall (pickle.dumps ([if_clf.predict(mgmt_data)]))
            else:
                break
        conn.close ()
    except (KeyboardInterrupt, SystemExit):
        server.close()
        os.unlink("/tmp/ainms.sock")