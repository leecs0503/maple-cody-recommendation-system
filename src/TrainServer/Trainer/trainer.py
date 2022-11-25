from ..Model.model import Model
from ..Config.config import Config
from ..Dataloader.dataloader import load_DataLoader
import json
import logging

import torch.optim as optim
from torch.optim import lr_scheduler
import torch
import torch.nn as nn
from torch.utils.tensorboard import SummaryWriter

from typing import Literal

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
        # FIXME: 임시 코드
        with open('./json_data_result1.json', 'r') as f:
            raw_data: dict = json.load(f)
            self.load_data(raw_data)
        self.model = Model(
            num_result_classes=106,
        ).to(device)
        self.train(
            num_epochs=1000,
            learning_rate=0.001,
            step_size=20,
            gamma=0.1,
        )
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

    def log_batch(
        self,
        num_batch: int,
        loss: float,
        corr_exp: float,
        batch_size: int,
        phase: Literal["train", "valid"],
        num_epochs: int,
        epoch: int,
        batch_idx: int,
    ):
        self.writer.add_scalar(f"Step{epoch:02}/Loss/{phase.upper()}-{epoch:02}", loss, batch_idx)
        self.writer.add_scalar(f"Step{epoch:02}/ACC/{phase.upper()}-{epoch:02}", corr_exp / batch_size, batch_idx)
        self.writer.flush()
        msg = "| {} SET | Epoch [{:02d}/{:02d}], Step [{:04d}/{:04d}], Loss: {:.4f}, coor_exp: {:.4f}".format(
            phase.upper(),
            epoch + 1,
            num_epochs,
            batch_idx,
            num_batch,
            loss,
            corr_exp / batch_size
        )
        print(msg)
        self.logger.info(msg)

    def log_step(
        self,
        epoch_loss: float,
        epoch_acc_exp: float,
        phase: Literal["train", "valid"],
        epoch: int,
        num_epochs: int,
    ):
        self.writer.add_scalar(f"Epoch/Loss/{phase.upper()}", epoch_loss, epoch)
        self.writer.add_scalar(f"Epoch/ACC/{phase.upper()}", epoch_acc_exp, epoch)
        self.writer.flush()
        msg = f"| {phase.upper()} SET | Epoch [{epoch + 1:02}/{num_epochs:02}], Loss: {epoch_loss:.4}, Acc(Exp): {epoch_acc_exp:.4}"  # noqa: E501
        print(msg)
        self.logger.info(msg)
        pass

    def step(
        self,
        epoch: int,
        num_epochs: int,
        criterion,
        optimizer,
        scheduler,
    ) -> bool:
        for phase in self.data_loader:
            if phase == 'train':
                self.model.train()
            else:
                self.model.eval()

            running_loss = 0.0
            all_cnt = 0
            accept_cnt = 0

            for batch_idx, batch_sample in enumerate(self.data_loader[phase]):
                inputs = batch_sample["input"].to(device)
                answers = batch_sample["answer"].to(device)

                outputs = self.model(inputs)
                loss = criterion(outputs, answers)
                optimizer.zero_grad()
                running_loss += loss.item()
                _, o_v = torch.max(outputs, 1)
                for o, answer in zip(o_v, answers):
                    if answer.item() == o.item():
                        accept_cnt += 1
                    all_cnt += 1

                loss.backward()
                optimizer.step()
                self.log_batch(
                    num_batch=len(self.data_loader[phase]),
                    loss=running_loss / (batch_idx + 1),
                    corr_exp=accept_cnt / all_cnt,
                    batch_size=self.config.batch_size,
                    phase=phase,
                    num_epochs=num_epochs,
                    epoch=epoch,
                    batch_idx=batch_idx,
                )

            self.log_step(
                epoch_loss=running_loss,
                epoch_acc_exp=accept_cnt / all_cnt,
                phase=phase,
                epoch=epoch,
                num_epochs=num_epochs,
            )
            scheduler.step()
            print(f"EPOCH [{epoch:3d}]: loss: {running_loss :.5f} // acc: {accept_cnt / all_cnt:.5f}")

    def train(
        self,
        num_epochs: int,
        learning_rate: float,
        step_size: float,
        gamma: float,
    ):
        params = self.model.parameters()
        optimizer = optim.Adam(params, lr=learning_rate)
        scheduler = lr_scheduler.StepLR(optimizer, step_size=step_size, gamma=gamma)
        criterion = nn.CrossEntropyLoss().to(device)

        for epoch in range(num_epochs):
            early_stop = self.step(
                epoch=epoch,
                num_epochs=num_epochs,
                criterion=criterion,
                optimizer=optimizer,
                scheduler=scheduler,
            )
            if early_stop:
                break
