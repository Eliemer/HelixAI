from flask import Blueprint, flash, g, session, request
# from src.blueprints.auth import login_required
from src.db import get_db
import functools
import os

from pytorch_lightning_src.Model.GCNN import GCNN
import pytorch_lightning as pl
import json

bp = Blueprint('deep_learn', __name__, url_prefix='/deep_learn')

@bp.route('/train', methods=('GET', 'POST'))
def train_model():
    if request.method == 'POST':
        config = request.form

        model = GCNN(config)
        trainer = pl.Trainer()

        trainer.fit(model)
