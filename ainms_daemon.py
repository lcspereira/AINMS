'''
Created on 20 de fev de 2018

@author: lucas
'''

from sklearn.neural_network import MLPClassifier
import matplotlib.pyplot as plt
import pandas
import socket
import os
import pickle
import numpy
import _thread


def show_loss_graph (loss):
    try:
        plt.plot (loss)
        plt.ylabel ("Loss")
        plt.xlabel ("Iteration")
        plt.show()
    except Exception as ex:
        print (str(ex))
        pass

def train_device (train_file):
    dataset = pandas.read_csv (train_file)
    X, y = dataset.iloc[:,:-1], dataset.iloc[:, -1]

    # Classificador perceptron multicamadas
    # Modelo: Retropropagação de erro
    # Função de ativação: Logistica sigmoidal
    clf = MLPClassifier(solver='sgd', activation='logistic', hidden_layer_sizes=(92,60), max_iter=10000, learning_rate='constant', verbose=True)
    clf.fit (X, y)
    _thread.start_new_thread(show_loss_graph, tuple([clf.loss_curve_]))
    return clf

server = socket.socket (socket.AF_UNIX, socket.SOCK_STREAM)
server.bind("/tmp/ainms.sock")
server.listen(1)

print ("Carregando dados de treinamento...")
if_clf = train_device('/etc/ainms/if_train.csv')
print ("[ OK ]")
print ("Aguardando dados de entrada...")
while True:
    try:
        conn, client_addr = server.accept()
        while True:
            data = conn.recv (5192)
            if data:
                mgmt_data = pickle.loads (data)
                print (mgmt_data)
                conn.sendall (pickle.dumps (if_clf.predict(mgmt_data)))
            else:
                break
        conn.close ()
    except (KeyboardInterrupt, SystemExit):
        server.close()
        os.unlink("/tmp/ainms.sock")