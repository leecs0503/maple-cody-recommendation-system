from typing import TypedDict, List, Dict, Tuple
import torch.utils.data
import numpy as np
import torchvision.transforms as transforms
from PIL import Image
import os
from .raw_data import RawData

class DataLoader(TypedDict):
    train: torch.utils.data.DataLoader
    valid: torch.utils.data.DataLoader

class Dataset(torch.utils.data.Dataset):
    def __init__(
        self,
        dataset: RawData,
        transform: transforms.Compose,
    ):
        """ """
        self.dataset = dataset
        self.transform = transform

    def __len__(self):
        """dataset에 들어있는 데이터 개수"""
        return len(self.dataset.input_list)

    def __getitem__(self, index: int):
        input = self.dataset.input_list[index]
        output = self.dataset.output_list[index]
        return input, output

def _get_data_loader(
    raw_data: Dict,
    batch_size: int,
    num_workers: int,
) -> torch.utils.data.DataLoader:

    transform = transforms.Compose([
        transforms.ToTensor(),
        # normalize
    ])

    data = RawData(
        raw_data=raw_data,
        transform=transform,
    )

    
    dataset = Dataset(
        dataset=data,
        transform=transform,
    )
    return torch.utils.data.DataLoader(
        dataset=dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
    )


def load_DataLoader(
    raw_data: Dict,
    batch_size: int,
    num_workers: int,
):
    total_datalodaer = _get_data_loader(
        raw_data=raw_data,
        batch_size=batch_size,
        num_workers=num_workers,
    )
    train_dataloader, valid_dataloader = torch.utils.data.random_split(total_datalodaer, [0.8, 0.2], generator=torch.Generator().manual_seed(42))
    return {
        "train": train_dataloader,
        "valid": valid_dataloader,
    }