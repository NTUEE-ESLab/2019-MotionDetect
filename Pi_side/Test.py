import models
from parser import arg_parse

import time
import socket
import torch
import numpy as np
import json

def prediction(mov):
    with torch.no_grad():  # do not need to caculate information for gradient during eval
        pred = model(mov)
        _, pred = torch.max(pred, dim=1)

    return pred

def get_number(number, signal):
    if signal == 0:
        return number - 10000;
    elif signal == 1:
        return -(number - 10000);
    return -1



args = arg_parse()
model = models.Net()
model_std = torch.load('model_best.pth.tar')
model.load_state_dict(model_std)


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('waiting for socket')
server.bind(('192.168.1.238', 65431))  # YOU NEED EDIT HERE
server.listen(5)  # possible sockets up to 5.
while True:
    conn, addr = server.accept()
    print(conn, addr)

    movement = []
    gx = []
    gy = []
    gz = []
    input("Press Enter to gather the data...")
    i=0
    time1= time.time()
    while len(gx) <= 48:

        try:

            data = conn.recv(76)
            #print('recive:', data.decode())
            rec = data.decode()
            print(i)
            #print('recieve before:' + str(i), rec)
            rec = rec[0:rec.find('}')+1]
            #print(len(rec))
            #print('recieve:' + str(i), rec)
            i +=1
            rec = json.loads(rec)
            gx.append(get_number(rec['gx'], rec['sx']))
            gy.append(get_number(rec['gy'], rec['sy']))
            gz.append(get_number(rec['gz'], rec['sz']))
            print(gx, gz, gz)
            time.sleep(0.05)

        except ConnectionResetError as e:
            print('Connect is shut down！')
            break
    movement = [gx, gy, gz]
    #print(time.time() - time1)

    tensor = torch.tensor(np.asarray(movement))

    tensor = torch.reshape(tensor, (1, 3, 7, 7))
    pred = prediction(tensor.float())
    pred = pred.numpy().squeeze()
    #print(pred)

    if pred == 0:
        print('Its a pass!')
    else:
        print('Its a shoot!')

    conn.close()

