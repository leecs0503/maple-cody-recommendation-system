from ..Model.model import Model
from ..Config.config import Config
from ..Dataloader.dataloader import load_DataLoader
import json
import random
import logging

import torch.optim as optim
from torch.optim import lr_scheduler
import torch
from torch.utils.tensorboard import SummaryWriter

from PIL import Image
import base64

import torchvision.transforms as transforms
from typing import List

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class Trainer:
    def __init__(
        self,
        config: Config,
        logger: logging.Logger,
    ) -> None:
        self.config = config
        self.logger = logger
        self.writer = SummaryWriter(config.tensorboard_path)
        self.data_loader = None
        self.load_model(
            config.model_path,
        )
            
    def load_data(
        self,
        raw_data: dict,
    ) -> None:
        
        if self.data_loader is not None:
            # TODO: online으로 데이터가 추가되는 것 처리
            pass
        else:
            self.data_loader = load_DataLoader(
                raw_data=raw_data,
                batch_size=self.config.batch_size,
                num_workers=self.config.num_workers,
            )

    def load_model(
        self,
        model_path: str,
    ):
        pass

    def save_model(
        self,
        model_path: str,
    ):
        pass

    def train(
        self,
    ):
        pass