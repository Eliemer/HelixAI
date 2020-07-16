from flask import Blueprint, flash, g, session, request
from flask import jsonify
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

@bp.route('get_models/<user_id>', methods=['GET'])
def get_models_from_user(user_id):
	models = []

	db = get_db()
	db_res = db.execute(
		("SELECT User.user_id, Model.* "
		"FROM User INNER JOIN Interpret USING(user_id) "
		"INNER JOIN Model USING(model_id)"
		"WHERE User.user_id=?"),
		(user_id,)
	).fetchall()

	for res in db_res:
		models.append(dict(res))

	return jsonify(models)
