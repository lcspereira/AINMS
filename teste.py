import numpy as np
import random
import pickle
import socket
from sklearn.metrics import classification_report

y = []
preds = []
print ("================================================================")
for i in range (0, 100):
    #speeds = [128000, 256000, 512000, 1024000, 2048000, 3072000, 4096000, 10000000, 100000000, 1000000000]
    #speed = random.choice(speeds)
    bit_rate = random.random() * 100
    in_error_rate = random.random() * 100
    out_error_rate = random.random() * 100
    in_discard_rate = random.random() * 100
    out_discard_rate = random.random() * 100
    data = np.array ([bit_rate, in_error_rate, out_error_rate, in_discard_rate, out_discard_rate])
    y.append ([float(data[0]), float(data[1]), float(data[2]), float(data[3]), float(data[4])])
    print (data)
    sock = socket.socket (socket.AF_UNIX, socket.SOCK_STREAM)
    sock.connect ("/tmp/ainms.sock")
    serialized_data = pickle.dumps (data)
    sock.sendall (serialized_data)
    res = sock.recv (5192)
    pred = pickle.loads(res)
    preds.append (int (pred[0]))
    print (pred)
    sock.close ()
print ("================================================================")
for i in range (0, 100):
    #speeds = [128000, 256000, 512000, 1024000, 2048000, 3072000, 4096000, 10000000, 100000000, 1000000000]
    #speed = random.choice(speeds)
    bit_rate = random.random() * 10
    in_error_rate = random.random() * 10
    out_error_rate = random.random() * 10
    in_discard_rate = random.random() * 10
    out_discard_rate = random.random() * 10
    data = np.array ([bit_rate, in_error_rate, out_error_rate, in_discard_rate, out_discard_rate])
    y.append ([float(data[0]), float(data[1]), float(data[2]), float(data[3]), float(data[4])])
    print (data)
    sock = socket.socket (socket.AF_UNIX, socket.SOCK_STREAM)
    sock.connect ("/tmp/ainms.sock")
    serialized_data = pickle.dumps (data)
    sock.sendall (serialized_data)
    res = sock.recv (5192)
    pred = pickle.loads(res)
    preds.append (int (pred[0]))
    print (pred)
    sock.close ()
print ("================================================================")
for i in range (0, 100):
    #speeds = [128000, 256000, 512000, 1024000, 2048000, 3072000, 4096000, 10000000, 100000000, 1000000000]
    #speed = random.choice(speeds)
    bit_rate = random.random() * 100
    in_error_rate = random.random() * 10
    out_error_rate = random.random() * 10
    in_discard_rate = random.random() * 10
    out_discard_rate = random.random() * 10
    data = np.array ([bit_rate, in_error_rate, out_error_rate, in_discard_rate, out_discard_rate])
    y.append ([float(data[0]), float(data[1]), float(data[2]), float(data[3]), float(data[4])])
    print (data)
    sock = socket.socket (socket.AF_UNIX, socket.SOCK_STREAM)
    sock.connect ("/tmp/ainms.sock")
    serialized_data = pickle.dumps (data)
    sock.sendall (serialized_data)
    res = sock.recv (5192)
    pred = pickle.loads(res)
    preds.append (int (pred[0]))
    print (pred)
    sock.close ()
print ("================================================================")
for i in range (0, 100):
    #speeds = [128000, 256000, 512000, 1024000, 2048000, 3072000, 4096000, 10000000, 100000000, 1000000000]
    #speed = random.choice(speeds)
    bit_rate = random.random() * 10
    in_error_rate = random.random() * 100
    out_error_rate = random.random() * 100
    in_discard_rate = random.random() * 10
    out_discard_rate = random.random() * 10
    data = np.array ([bit_rate, in_error_rate, out_error_rate, in_discard_rate, out_discard_rate])
    y.append ([float(data[0]), float(data[1]), float(data[2]), float(data[3]), float(data[4])])
    print (data)
    sock = socket.socket (socket.AF_UNIX, socket.SOCK_STREAM)
    sock.connect ("/tmp/ainms.sock")
    serialized_data = pickle.dumps (data)
    sock.sendall (serialized_data)
    res = sock.recv (5192)
    pred = pickle.loads(res)
    preds.append (int (pred[0]))
    print (pred)
    sock.close ()
print ("================================================================")
for i in range (0, 100):
    #speeds = [128000, 256000, 512000, 1024000, 2048000, 3072000, 4096000, 10000000, 100000000, 1000000000]
    #speed = random.choice(speeds)
    bit_rate = random.random() * 10
    in_error_rate = random.random() * 10
    out_error_rate = random.random() * 10
    in_discard_rate = random.random() * 100
    out_discard_rate = random.random() * 100
    data = np.array ([bit_rate, in_error_rate, out_error_rate, in_discard_rate, out_discard_rate])
    y.append ([float(data[0]), float(data[1]), float(data[2]), float(data[3]), float(data[4])])
    print (data)
    sock = socket.socket (socket.AF_UNIX, socket.SOCK_STREAM)
    sock.connect ("/tmp/ainms.sock")
    serialized_data = pickle.dumps (data)
    sock.sendall (serialized_data)
    res = sock.recv (5192)
    pred = pickle.loads(res)
    preds.append (int(pred[0]))
    print (pred)
    sock.close ()
y = np.array (y)
preds = np.array (preds)