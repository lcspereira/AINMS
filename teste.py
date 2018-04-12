import numpy as np
import random
import pickle

for i in range (0, 1000):
    speeds = [128000, 256000, 512000, 1024000, 2048000, 3072000, 4096000, 10000000, 100000000, 1000000000]
    speed = random.choice (speeds)
    bit_rate = random.uniform (0, speed)
    in_error_rate = random.uniform (0, 100)
    out_error_rate = random.uniform (0, 100)
    in_discard_rate = random.uniform (0, 100)
    out_discard_rate = random.uniform (0, 100)
    data = np.array ([speed, bit_rate, in_error_rate, out_error_rate, in_discard_rate, out_discard_rate])
    print (data)