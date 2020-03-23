'''
Template for implementing models using Pytorch Lighting.
This code is not meant to be executed or imported, but
to serve as an example of code structure
'''
from typing import Callable, Dict
import torch
from torch import nn
from torch.nn import functional as F
from torch.utils.data import DataLoader
from torch.optim import Optimizer
import pytorch_lightning as pl

class LightningModel(pl.LightningModule):
    def __init__(self, *args, **kwargs) -> None:
        '''
        Layer inits
        '''
        raise NotImplementedError

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        '''
        Model definition and layer interconnectivity
        '''
        raise NotImplementedError

    def loss(self, logits: torch.Tensor, labels: torch.Tensor) -> Callable[[torch.Tensor, torch.Tensor], torch.Tensor]:
        '''
        Define and return loss function
        '''
        raise NotImplementedError

    def training_step(self, train_batch: torch.Tensor, batch_idx: int) -> Dict[str, torch.Tensor]:
        '''
        Forward the batch through the model
        Calculate loss
        return loss
        '''
        raise NotImplementedError

    def validation_step(self, val_batch: torch.Tensor, batch_idx: int) -> Dict[str, torch.Tensor]:
        '''
        Forward the batch through the model
        Calculate loss
        return loss
        '''
        raise NotImplementedError

    def test_step(self, test_batch: torch.Tensor, batch_idx: int) -> Dict[str, torch.Tensor]:
        '''
        Forward the batch through the model
        Calculate loss
        return loss
        '''
        raise NotImplementedError

    def prepare_data(self) -> None:
        '''
        This code is executely only once.
        Include here all the preprocessing that needs to happen only once,
        such as downloads and transforms
        '''
        raise NotImplementedError

    def train_dataloader(self) -> DataLoader:
        '''
        Define dataloader.
        DO NOT PROVIDE SAMPLER!
        '''
        raise NotImplementedError

    def val_dataloader(self) -> DataLoader:
        '''
        Define dataloader.
        DO NOT PROVIDE SAMPLER!
        '''
        raise NotImplementedError

    def test_dataloader(self) -> DataLoader:
        '''
        Define dataloader.
        DO NOT PROVIDE SAMPLER!
        '''
        raise NotImplementedError

    def configure_optimizers(self) -> Optimizer:
        '''
        Initialize and return optimizer
        '''
        raise NotImplementedError

'''
model = LightningModel()
trainer = pl.Trainer()

trainer.fit(model)
'''
