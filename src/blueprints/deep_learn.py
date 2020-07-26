from flask import Blueprint, flash, g, session, request
from flask import jsonify, current_app
from flask_jwt_extended import jwt_required, fresh_jwt_required, get_jwt_identity

from src.db import get_db
import functools
import os

import torch
from pytorch_lightning_src.Model.interpret_v2 import Interpreter
from pytorch_lightning_src.Model.GCNN import GCNN
from pytorch_lightning_src.Logger.logger import JSONLogger
import pytorch_lightning as pl
import json

bp = Blueprint('deep_learn', __name__, url_prefix='/deep_learn')


def train(config):

	if os.path.exists(config['input_csv']):

		i = 0
		save_path = os.path.join(current_app.config['MODEL_PATH'], config['dataset'] + f"__version_{i}_.pt")
		while(os.path.exists(save_path)):
			save_path = os.path.join(current_app.config['MODEL_PATH'], config['dataset'] + f"__version_{i+1}_.pt")
			i+=1

		model = GCNN(config)
		logger = JSONLogger(
			path=current_app.config['LOG_PATH'],
			name=save_path.split('/')[-1].split('.')[0]
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
		trainer.test(model)

		torch.save(model.state_dict(), save_path)
		metrics = json.load(open(logger.name + ".json", 'r'))
		model_class = str(type(model))

		res = insert_model_to_db(save_path.split('/')[-1], metrics, model_class)

		return {"metrics": metrics, "model_details": res}

	else:
		return {"Error": "Input CSV not found"}


def interpret(config, model_path):
	if os.path.exists(config['input_csv']):

		save_path = model_path.split('.')[0] + '.npz'
		save_path = os.path.join(current_app.config['ATTR_PATH'], save_path)

		model = GCNN(config)
		model.prepare_data()
		model.setup(0)
		model_path = os.path.join(current_app.config['MODEL_PATH'], model_path)
		model.load_state_dict(torch.load(model_path))

		for params in model.parameters():
			params = torch.autograd.Variable(params, requires_grad=True)

		interpreter = Interpreter(
			model = model,
			loss_fn = torch.nn.CrossEntropyLoss(),
			protein_type = config['dataset']
		)

		losses, attributions = interpreter.interpret_test(
			dataset = model.train_dataloader()
		)

		pdbs, output_path = interpreter.generate_attributions(
			losses, 
			attributions, 
			output_path=save_path
		)

		return jsonify({"pdb": pdbs, "path": output_path}), 200

def insert_model_to_db(name, metrics, model_class):
	db = get_db()

	test_acc = metrics[-1]['test_acc_mean']
	test_loss = metrics[-1]['test_loss_mean']
	exists = db.execute(
		"SELECT * FROM Model WHERE model_path=?",
		[name]
	).fetchone()

	if exists is not None:
		pass

		# exists = dict(exists)
		# if exists['model_accuracy'] < test_acc and exists['model_loss'] > test_loss:
		# 	db.execute('UPDATE Model SET model_accuracy=?, model_loss=? WHERE model_id=?',
		# 		[test_acc, test_loss, exists['model_id']])

	else:
		db.execute(
			"INSERT INTO Model(model_python_class, model_path, model_metrics, model_accuracy, model_loss) VALUES (?,?,?,?,?)",
			[model_class, 
			name,
			name.split('.')[0] + '.json',
			test_acc,
			test_loss])


	db.commit()
	res = db.execute("SELECT * FROM Model WHERE model_path=?",
		[name]).fetchone()

	return dict(res)

@bp.route('/interpret/config/path/<config_path>/model/<model_path>', methods=('GET', 'POST'))
@fresh_jwt_required
def interpret_with_file(config_path, model_path):
	if request.method == 'POST':
		with open(os.path.join(current_app.config['CONFIG_PATH'], config_path), 'r') as fp:
			config = json.load(fp)

			# print(config)

			config = {**config}
			config['input_csv']   = os.path.join(current_app.config['CSV_PATH'], config['input_csv'])
			config['error_csv']   = os.path.join(current_app.config['CSV_PATH'], config['error_csv'])
			config['tensors']     = current_app.config['TENSOR_PATH']
			config['pdb']         = current_app.config['PDB_PATH']

			return interpret(config, model_path)

@bp.route('/train/raw', methods=('GET', 'POST'))
#@fresh_jwt_required
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

@bp.route('/train/config/path/<config_path>', methods=("GET", "POST"))
#@fresh_jwt_required
def train_with_file(config_path):
	with open(os.path.join(current_app.config['CONFIG_PATH'], config_path), 'r') as fp:
		config = json.load(fp)

		config['input_csv']   = os.path.join(current_app.config['CSV_PATH'], config['input_csv'])
		config['error_csv']   = os.path.join(current_app.config['CSV_PATH'], config['error_csv'])
		config['tensors']     = current_app.config['TENSOR_PATH']
		config['pdb']         = current_app.config['PDB_PATH']


		train_res = train(config)
		user_trained = insert_to_db_user_trains(
			config_path, 
			get_jwt_identity(),
			train_res['model_details']['model_path']
		)
		is_trained_res = insert_to_db_is_trained(
			config_path, 
			train_res['model_details']['model_path']
		)

		return jsonify({**{"model_path": train_res['model_details']['model_path']}, 
			**train_res,	
			**user_trained, 
			**is_trained_res}), 200

def insert_to_db_user_trains(config_path, user_id, model_path):
	db = get_db()
	config_id = db.execute("SELECT * FROM ConfigFile WHERE config_path=?", [config_path]).fetchone()
	model_id = db.execute("SELECT * FROM Model WHERE model_path=?", [model_path]).fetchone()

	if config_id is not None and model_id is not None:

		config_id = dict(config_id)
		model_id = dict(model_id)

		db.execute(
			"INSERT OR IGNORE INTO Trains VALUES (?,?,?)",
			[user_id, config_id['config_id'], model_id['model_id']]
		)

		db.commit()

		return {"msg": 200}

	else:
		return {"Error": "config is not in database"}

def insert_to_db_is_trained(config_path, model_path):
	db = get_db()

	model_id = db.execute("SELECT model_id FROM Model WHERE model_path=?", [model_path]).fetchone()
	config_id= db.execute("SELECT config_id FROM ConfigFile WHERE config_path=?", [config_path]).fetchone()

	if model_id is not None and config_id is not None:
		model_id = dict(model_id)
		config_id = dict(config_id)

		db.execute('INSERT OR IGNORE INTO is_Trained VALUES (?,?)', [model_id['model_id'], config_id['config_id']])

		db.commit()

		config_row = db.execute("SELECT config_id, config_path FROM is_Trained INNER JOIN ConfigFile USING(config_id) WHERE config_id=?",
			[config_id['config_id']]).fetchone()

		if config_row is not None:
			config_id = {**config_id, **dict(config_row)}

		return {**model_id, **config_id}

	else:
		return {"Error": "model or config file does not exists in DB"}

@bp.route('/get_models', methods=['GET'])
@jwt_required
def get_models_from_user():
	models = []

	user_id = get_jwt_identity()

	db = get_db()
	db_res = db.execute(
		("SELECT Model.* "
		"FROM Trains "
		"INNER JOIN Model ON Model.model_id=Trains.model_id "
		"WHERE Trains.user_id=?"),
		(user_id,)
	).fetchall()

	for res in db_res:
		models.append(dict(res))

	return jsonify(models)


@bp.route('/get_train_results', methods=['GET'])
def get_all_train_results():
	results = []

	db = get_db()

	db_res = db.execute(
		("SELECT config_id, model_id, model_metrics "
		"FROM Trains "
		"INNER JOIN Model "
		"Using(model_id) ")).fetchall()

	for res in db_res:
		res = dict(res)

		res['metrics'] = json.load(open(
			os.path.join(
				current_app.config['LOG_PATH'],
				res['model_metrics'])))[-1] 
				# the last metrics are the test epoch
		results.append(res)

	return jsonify(results), 200
