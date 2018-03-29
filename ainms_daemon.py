'''
Created on 20 de fev de 2018

@author: lucas
'''

from sklearn.neural_network import MLPClassifier
import pandas
import socket
import os
import pickle

def train_device (train_file):
    dataset = pandas.read_csv (train_file)
    X, y = dataset.iloc[:,:-1], dataset.iloc[:, -1]
    clf = MLPClassifier(solver='sgd', hidden_layer_sizes=(50,10))
    clf.fit (X, y)
    return clf

server = socket.socket (socket.AF_UNIX, socket.SOCK_STREAM)
server.bind("/tmp/ainms.sock")
server.listen(1)


if_clf = train_device('/etc/ainms/if_train.csv')

while True:
    try:
        conn, client_addr = server.accept()
        while True:
            data = conn.recv (5192)
            if data:
                mgmt_data = pickle.loads (data)
                print (if_clf.predict(mgmt_data))
            else:
                break
        conn.close ()
    except (KeyboardInterrupt, SystemExit):
        conn.close ()
        server.close()
        os.unlink("/tmp/ainms.sock")