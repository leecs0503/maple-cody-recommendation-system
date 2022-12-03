import logging
import abc

from typing import Literal


class BaseTrainer(abc.ABC):
    def __init__(self, *args, **kwargs) -> None:
        self.logger = logging.getLogger("trainer")

    @abc.abstractmethod
    def get_dataloader(
        self,
        data_path: str,
    ) -> None:
        pass

    @abc.abstractmethod
    def step(self, *args, **kwargs):
        """ 학습 step을 진행하는 메소드 """
        pass

    @abc.abstractmethod
    def train(self, *args, **kwargs):
        """ criterion, optimizer, scheduler을 초기화하고, 학습 step을 진행"""
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
        self.writer.add_scalar(f"Step{epoch:02}/ACC/{phase.upper()}-{epoch:02}", corr_exp, batch_idx)
        self.writer.flush()
        msg = "| {} SET | Epoch [{:02d}/{:02d}], Step [{:04d}/{:04d}], Loss: {:.4f}, coor_exp: {:.4f}".format(
            phase.upper(),
            epoch + 1,
            num_epochs,
            batch_idx,
            num_batch,
            loss,
            corr_exp
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