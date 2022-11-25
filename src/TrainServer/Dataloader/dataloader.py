from typing import TypedDict, Dict
import torch.utils.data
import torchvision.transforms as transforms
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
        answer = self.dataset.answer_list[index]
        return {"input": input, "answer": answer}


def _get_data_loader(
    dataset: Dataset,
    batch_size: int,
    num_workers: int,
) -> torch.utils.data.DataLoader:

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
    transform = transforms.Compose([
        transforms.ToTensor(),
        # normalize
    ])
    data = RawData(
        raw_data=raw_data,
        transform=transform,
    )
    total_dataset = Dataset(
        dataset=data,
        transform=transform,
    )

    train_dataset, valid_dataset = torch.utils.data.random_split(
        total_dataset,
        [0.8, 0.2],
        generator=torch.Generator().manual_seed(42)
    )

    train_dataloader = _get_data_loader(
        dataset=train_dataset,
        batch_size=batch_size,
        num_workers=num_workers,
    )
    valid_dataloader = _get_data_loader(
        dataset=valid_dataset,
        batch_size=batch_size,
        num_workers=num_workers,
    )

    return {
        "train": train_dataloader,
        "valid": valid_dataloader,
    }
