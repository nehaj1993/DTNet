#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 22 13:05:26 2018
Source of the data: bitmoji/emoji_data.py


@author: nehaj1993
"""

import os
from torch.utils.data import Dataset, DataLoader
from PIL import Image
import numpy as np
import torch
from torch.autograd import Variable


class Cartoon(Dataset):

    def __init__(self, data_dir='./data/emojis',
                         split='train',transform=None, target_transform=None):
        self.data_dir = data_dir
        self.split = split
        self.transform = transform
        self.target_transform = target_transform
        self.len = len(os.listdir(data_dir))

    def __getitem__(self, index):
        """
        Args:
            index (int): Index
        """
        img_name = os.path.join(self.data_dir, '{}.png'.format(index))
        # print(img_name)
        img = Image.open(img_name)
        img = img.convert('RGB')

        if self.transform is not None:
            img = self.transform(img)

        return img

    def __len__(self):
        return self.len