import os
import torch
import torchvision.transforms as transforms

from torch.utils.data import Dataset
import csv

MEAN = [0.5, 0.5, 0.5]
STD = [0.5, 0.5, 0.5]

class DATA(Dataset):
    def __init__(self, args, mode='train'):

        ''' set up basic parameters for dataset '''
        self.mode = mode
        self.data_dir = args.data_dir

        csv_path = os.path.join(self.data_dir, mode + '.csv')

        ''' read the data list '''
        with open(csv_path, mode='r') as pred:
            reader = csv.reader(pred)
            self.data = []
            for rows in reader:
                if rows[0] != 'data_name':
                    self.data.append([os.path.join(self.data_dir, rows[0]), rows[1]])

        self.transform = transforms.Compose([
            #transforms.ToPILImage(),
            #transforms.toTensor(),
            transforms.Normalize(MEAN, STD)

        ])

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):

        ''' get data '''
        movement = torch.load(self.data[idx][0])
        movement = torch.reshape(movement, (3, 7, 7))
        cls = int(self.data[idx][1])
        ''' read image '''

        return self.transform(movement), cls
