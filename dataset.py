import os
import torch
import pandas as pd
from torch.utils.data import Dataset, DataLoader
from math import log2
from PIL import Image
import config
import torchvision.transforms as transforms


class CelebA_dataset(Dataset):
    def __init__(self, root_dir, csv_file, transform=None):
        self.root_dir = root_dir
        self.csv_annotations = pd.read_csv(csv_file)
        self.transform = transform
        
    def __len__(self):
        return len(self.csv_annotations)
    
    def __getitem__(self, index):
        img_path = os.path.join(self.root_dir, self.csv_annotations.iloc[index,1])
        img = Image.open(img_path)
        label = torch.tensor(self.csv_annotations.iloc[index, 2:])
        # label = torch.tensor(float(self.csv_annotations.iloc[index, 1]))
        if self.transform:
            img = self.transform(img)
        return img, label.to(torch.float32)
        
