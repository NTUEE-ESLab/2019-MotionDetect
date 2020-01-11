import socket
import torch
import os
import csv
import numpy as np
import json
import time

def get_number(number, signal):
    if signal == 0:
        return number - 10000;
    elif signal == 1:
        return -(number - 10000);
    return -1


if not os.path.exists('data'):
    os.makedirs('data')

csv_file = 'data/train.csv'


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
    print(time.time() - time1)
    label = 4
    while label != 1 and label != 2 and label != 0:
        label = input("Is it a pass or a shoot?")
        label = int(label)
    if label == 2:
        print('error occurred. No valid input')
        conn.close()
        exit(1)
    print(movement)

    tensor = torch.tensor(np.asarray(movement))

    if not os.path.exists(csv_file):
        with open(csv_file, mode='w') as csv_file:
            fieldnames = ['data_name', 'label']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({'data_name': 'data_000.pt', 'label': label})

        # file_name = os.path.join('data_rdm', 'data_000.pt')
        # print(file_name)
        file_name = os.path.join('data', 'data_000.pt')
        # np.save(array, file_name)
        torch.save(tensor, file_name)

    else:
        with open(csv_file, mode='r') as pred:
            reader = csv.reader(pred)
            data = []
            for rows in reader:
                print(rows)
                if rows[0] != 'data_name':
                    data.append([rows[0], rows[1]])
                    print(data)

        #print(data)
        #print(data[-1][0])
        last_file = data[-1][0]
        #print(last_file[5:-3])
        id = int(last_file[5:-3]) + 1
        #print(id)
        file_number = '00' + str(id) if len(str(id)) == 1 else \
            ('0' + str(id) if len(str(id)) == 2 else str(id))
        file_name = 'data_' + file_number + '.pt'

        with open(csv_file, mode='a') as csv_file:
            fieldnames = ['data_name', 'label']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writerow({'data_name': file_name, 'label': label})

        # file_name = os.path.join('data_rdm', 'data_' + file_number + '.pt' )
        # print(file_name)
        file_name = os.path.join('data', file_name)
        print(file_name)
        # np.save(array, file_name)
        torch.save(tensor, file_name)

    conn.close()

