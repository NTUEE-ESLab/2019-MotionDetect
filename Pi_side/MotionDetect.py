# -*- coding: utf-8 -*
from __future__ import absolute_import
import models

import argparse
#from parser import argparse


import time
import socket
import torch
import numpy as np
import json

def arg_parse():
    parser = argparse.ArgumentParser(description='DLCV TA\'s tutorial in image classification using pytorch')

    # Datasets parameters
    parser.add_argument('--data_dir', type=str, default='data',
                    help="root path to data directory")
    parser.add_argument('--workers', default=4, type=int,
                    help="number of data loading workers (default: 4)")
    
    # training parameters
    parser.add_argument('--gpu', default=0, type=int, 
                    help='gpu device ids for CUDA_VISIBLE_DEVICES')
    parser.add_argument('--epoch', default=100, type=int,
                    help="num of validation iterations")
    parser.add_argument('--val_epoch', default=1, type=int,
                    help="num of validation iterations")
    parser.add_argument('--train_batch', default=2, type=int,
                    help="train batch size")
    parser.add_argument('--test_batch', default=128, type=int,
                    help="test batch size")
    parser.add_argument('--lr', default=0.0002, type=float,
                    help="initial learning rate")
    parser.add_argument('--weight-decay', default=0.0005, type=float,
                    help="initial learning rate")
    
    # resume trained model
    parser.add_argument('--resume', type=str, default='log',
                    help="path to the trained model")
    # others
    parser.add_argument('--save_dir', type=str, default='log')
    parser.add_argument('--random_seed', type=int, default=999)

    args = parser.parse_args()

    return args

def prediction(mov):
    with torch.no_grad():  # do not need to caculate information for gradient during eval
        pred = model(mov)
        _, pred = torch.max(pred, dim=1)

    return pred

def get_number(number, signal):
    if signal == 0:
        return number - 10000
    elif signal == 1:
        return -(number - 10000)
    return -1



print("torch version:",torch.__version__)

args = arg_parse()
model = models.Net()
print(model)
model_std = torch.load('model_best.pth.tar',map_location=torch.device('cpu'))
model.load_state_dict(model_std)



while True:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('waiting for socket')
    server.bind(('192.168.137.1', 65431))  # YOU NEED EDIT HERE
    server.listen(5)  # possible sockets up to 5.
    conn, addr = server.accept()
    print(conn, addr)

    movement = []
    gx = []
    gy = []
    gz = []
    input("Press Enter to gather the data...")#insert 
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
            #print(gx, gz, gz)
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

