import os
import csv
import numpy as np

csv_file = 'pr.csv'
label = 1

if not os.path.exists(csv_file):
    with open(csv_file, mode='w') as csv_file:
        fieldnames = ['data_name', 'label']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({'data_name': 'data_000.npy', 'label': label})

    # file_name = os.path.join('data_rdm', 'data_000.pt')
    # print(file_name)
    file_name = os.path.join('data_rdm', 'data_000')
    #np.save(array, file_name)
    # torch.save(tensor, file_name)

else:
    with open(csv_file, mode='r') as pred:
        reader = csv.reader(pred)
        data = []
        for rows in reader:
            print(rows)
            if rows[0] != 'data_name':
                data.append([rows[0], rows[1]])
                print(data)

    print(data)
    print(data[-1][0])
    last_file = data[-1][0]
    print(last_file[5:-4])
    id = int(last_file[5:-4]) + 1
    print(id)
    file_number = '00' + str(id) if len(str(id)) == 1 else \
        ('0' + str(id) if len(str(id)) == 2 else str(id))
    file_name = 'data_' + file_number + '.npy'

    with open(csv_file, mode='a') as csv_file:
        fieldnames = ['data_name', 'label']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writerow({'data_name': file_name, 'label': label})

    # file_name = os.path.join('data_rdm', 'data_' + file_number + '.pt' )
    # print(file_name)
    file_name = os.path.join('data_rdm', 'data_' + file_number)
    print(file_name)
    #np.save(array, file_name)
    # torch.save(tensor, file_name)
