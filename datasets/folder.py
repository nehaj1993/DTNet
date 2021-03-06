#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
@author: rishabhbhardwaj
"""

import os

from PIL import Image
from torch.utils.data import Dataset


class FolderDataset(Dataset):

    def __init__(self, data_dir='./results/digits/evals',
                 split='train', transform=None, target_transform=None):
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
