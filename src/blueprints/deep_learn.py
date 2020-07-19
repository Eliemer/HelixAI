from flask import Blueprint, flash, g, session, request
from flask import jsonify, current_app
from src.db import get_db
import functools
import os

from pytorch_lightning_src.Model.GCNN import GCNN
from pytorch_lightning_src.Logger.logger import JSONLogger
import pytorch_lightning as pl
import json

bp = Blueprint('deep_learn', __name__, url_prefix='/deep_learn')


def train(config):

	if os.path.exists(config['input_csv']):

		model = GCNN(config)
		logger = JSONLogger(
			path=current_app.config['LOG_PATH'],
			name=config['dataset']
		)

		trainer = pl.Trainer(
			logger=logger,
			max_epochs=config['epochs'],

			# Must provide configured checkpoint callback
			# to save them in custom location.
			# No checkpoints at all for now.
			checkpoint_callback=False
		)

		trainer.fit(model)

		metrics = json.load(open(logger.name + ".json", 'r'))

		return jsonify(metrics)

	else:
		return {"Error": "Input CSV not found"}


@bp.route('/train/raw', methods=('GET', 'POST'))
def train_with_raw():
	if request.method == 'POST':
		request.get_data()
		config = request.json

		# print(config)

		config = {**config}
		config['input_csv']   = os.path.join(current_app.config['CSV_PATH'], config['input_csv'])
		config['error_csv']   = os.path.join(current_app.config['CSV_PATH'], config['error_csv'])
		config['tensors']     = current_app.config['TENSOR_PATH']
		config['pdb']         = current_app.config['PDB_PATH']


		return train(config)

@bp.route('train/config/path/<config_path>', methods=("GET", "POST"))
def train_with_file(config_path):
	with open(os.path.join(current_app.config['CONFIG_PATH'], config_path), 'r') as fp:
		config = json.load(fp)

		config['input_csv']   = os.path.join(current_app.config['CSV_PATH'], config['input_csv'])
		config['error_csv']   = os.path.join(current_app.config['CSV_PATH'], config['error_csv'])
		config['tensors']     = current_app.config['TENSOR_PATH']
		config['pdb']         = current_app.config['PDB_PATH']

		return train(config)


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


# @bp.route('')