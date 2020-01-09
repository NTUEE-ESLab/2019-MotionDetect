import socket
#import torch
import os
import csv
import numpy as np

if not os.path.exists('data_rdm'):
    os.makedirs('data_rdm')

csv_file = 'data_rdm/train.csv'


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
    label = 4
    while label != 0 | label != 1 | label != 2:
        label = input("Is it a pass (0) or a shoot(1)? ")
    if label == 2:
        print('error occurred. No valid input')
        conn.close()
        exit(1)

    #tensor = torch.tensor(np.asarray(movement))
    array = np.asarray(movement)

    if not os.path.exists(csv_file):
        with open(csv_file, mode='w') as csv_file:
            fieldnames = ['data_name', 'label']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({'data_name': 'data_000.pt', 'label': label})

        #file_name = os.path.join('data_rdm', 'data_000.pt')
        #print(file_name)
        file_name = os.path.join('data_rdm', 'data_000')
        np.save(array, file_name)
        #torch.save(tensor, file_name)

    else:
        with open(csv_file, mode='r') as pred:
            reader = csv.reader(pred)
            data = []
            for rows in reader:
                if rows[0] != 'data_name':
                    data.append([rows[0], rows[1]])


        last_file = data[-1][0]
        id = int(last_file[5:-4]) + 1
        file_number = '00' + str(id) if len(str(id))==1 else \
                ('0' + str(id) if len(str(id))==2 else str(id))
        file_name = 'data_' + file_number + '.pt'


        with open(csv_file, mode='a') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writerow({'data_name': file_name, 'label': label})

        #file_name = os.path.join('data_rdm', 'data_' + file_number + '.pt' )
        #print(file_name)
        file_name = os.path.join('data_rdm', 'data_' + file_number)
        print(file_name)
        np.save(array, file_name)
        #torch.save(tensor, file_name)


    conn.close()

