from test import evaluate
import models
import torch
import data
import os
from parser import arg_parse

if __name__ == '__main__':
    args = arg_parse()

    model = models.Net()
    model_std = torch.load(os.path.join(args.save_dir, 'model_best.pth.tar'))
    model.load_state_dict(model_std)
    model.cuda()

    test_loader = torch.utils.data.DataLoader(data.DATA(args, mode='val'),
                                                 batch_size=args.train_batch,
                                                 num_workers=args.workers,
                                                 shuffle=False)

    acc = evaluate(model, test_loader)
    print(acc)





