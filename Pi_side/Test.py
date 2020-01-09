import models
from parser import arg_parse

import socket
import torch
import numpy as np

def prediction(mov):
    with torch.no_grad():  # do not need to caculate information for gradient during eval
        pred = model(mov)
        _, pred = torch.max(pred, dim=1)

    return pred


args = arg_parse()
model = models.Net(args)
model_std = torch.load('model_best.pth.tar')
model.load_state_dict(model_std)


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('192.168.1.238', 65431))  # YOU NEED EDIT HERE
server.listen(5)  # possible sockets up to 5.
while True:
    conn, addr = server.accept()
    print(conn, addr)

    movement = []
    input("Press Enter to gather the data...")
    while len(movement) <= 484:
        try:
            data = conn.recv(1024)
            print('recive:', data.decode())
            movement.append(data.decode())

        except ConnectionResetError as e:
            print('Connect is shut down！')
            break

    tensor = torch.tensor(np.asarray(movement))

    pred = prediction(tensor)
    pred = pred.numpy().squeeze()
    print(pred)

    if pred == 0:
        print('Its a pass!')
    else:
        print('Its a shoot!')

    conn.close()

