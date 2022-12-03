from typing import TypedDict, Dict
import torch
import torch.utils.data
import torchvision.transforms as transforms
from PIL import Image
import base64
from io import BytesIO


class ComplementDataLoader:
    def __init__(
        self,
        train: torch.utils.data.DataLoader,
        valid: torch.utils.data.DataLoader,
        class_num: int
    ):
        self.train = train
        self.valid = valid
        self.class_num = class_num

class ComplementDataset(torch.utils.data.Dataset):
    def __init__(
        self,
        dataset: dict,
        transform: transforms.Compose,
    ):
        """ """
        self.dataset = dataset
        self.transform = transform

    def __len__(self):
        """dataset에 들어있는 데이터 개수"""
        return len(self.dataset["input_list"])

    def __getitem__(self, index: int):
        input = self.transform(self.dataset["input_list"][index])
        answer = torch.Tensor([self.dataset["answer_list"][index]]).type(torch.int64)
        return {"input": input, "answer": answer}


def _get_data_loader(
    dataset: ComplementDataset,
    batch_size: int,
    num_workers: int,
) -> torch.utils.data.DataLoader:

    return torch.utils.data.DataLoader(
        dataset=dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
    )

def preprocess_raw_data(raw_data: dict, parts):
    dataset = {
        "input_list": [],
        "answer_list": [],
    }
    answer_set = set()
    for crt_name, avatar_info_list in raw_data.items():
        for avatar_info in avatar_info_list:
            answer = avatar_info[parts]
            input_image_b64 = avatar_info[f"{parts}_image"]
            if input_image_b64 == "":
                continue
            input_image = Image.open(BytesIO(base64.b64decode(input_image_b64)))
            input_image = input_image.convert("RGB")
            input = input_image.resize((224, 224), Image.ANTIALIAS)
            dataset["input_list"].append(input)
            dataset["answer_list"].append(answer)
            answer_set.add(answer)

    answer_dict = {
        idx: answer
        for idx, answer in enumerate(answer_set)
    }
    answer_inv_dict = {
        answer: idx
        for idx, answer in enumerate(answer_set)
    }
    dataset["answer_list"] = [
        answer_inv_dict[answer]
        for answer in dataset["answer_list"]
    ]

    return dataset, len(answer_set), answer_dict

def load_DataLoader(
    data_set: Dict,
    batch_size: int,
    num_workers: int,
    class_num: int,
) -> ComplementDataLoader:
    transform = transforms.Compose([
        transforms.ToTensor(),
        # normalize
    ])
    total_dataset = ComplementDataset(
        dataset=data_set,
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

    return ComplementDataLoader(
        train=train_dataloader,
        valid=valid_dataloader,
        class_num=class_num,
    )
