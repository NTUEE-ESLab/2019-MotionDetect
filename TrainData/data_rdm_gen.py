import os
import numpy as np
import torch
import csv


'''create directory to save trained model and other info'''
if not os.path.exists('data_rdm'):
    os.makedirs('data_rdm')

csv_file = 'data_rdm/train.csv'

with open(csv_file, mode='w') as csv_file:
    fieldnames = ['data_name', 'label']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    for i in range(500):
        tensor = torch.rand((1, 484, 3))
        file_number = '00' + str(i) if len(str(i))==1 else \
                ('0' + str(i) if len(str(i))==2 else str(i))
        file_name = 'data_' + file_number + '.pt'

        label = np.random.randint(2)
        writer.writerow({'data_name': file_name, 'label': label})

        file_name = os.path.join('data_rdm', 'data_' + file_number + '.pt' )
        print(file_name)
        torch.save(tensor, file_name)


csv_file = 'data_rdm/valid.csv'

with open(csv_file, mode='w') as csv_file:
    fieldnames = ['data_name', 'label']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    for i in range(500, 550):
        tensor = torch.rand((1, 484, 3))
        file_number = '00' + str(i) if len(str(i))==1 else \
                ('0' + str(i) if len(str(i))==2 else str(i))
        file_name = 'data_' + file_number + '.pt'

        label = np.random.randint(2)
        writer.writerow({'data_name': file_name, 'label': label})

        file_name = os.path.join('data_rdm', 'data_' + file_number + '.pt' )
        print(file_name)
        torch.save(tensor, file_name)


