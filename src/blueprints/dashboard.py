from flask import Blueprint, flash, g, request, session, url_for
from flask import current_app, jsonify
from werkzeug.utils import secure_filename
from flask_jwt_extended import jwt_required, fresh_jwt_required, get_jwt_claims

from src.db import get_db

from itertools import zip_longest
import functools
import json
import os
import pandas as pd


ALLOWED_EXTENSIONS = {'csv'}

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

def allowed_file(filename):
	if '.' in filename:
		if filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
			return True
	return False

@bp.route('/', methods=['GET', 'POST'])
@fresh_jwt_required
def upload_file():
	if request.method == 'POST':
		if 'file' not in request.files:
			return {"Error": "No file in form"}

		file = request.files['file']

		if file.filename == '':
			return {"Error": "No selected file"}

		if file and allowed_file(file.filename):
				filename = secure_filename(file.filename)

				if not os.path.exists(os.path.join(current_app.config['CSV_PATH'], filename)):
					file.save(os.path.join(current_app.config['CSV_PATH'], filename))

				return insert_dataset_to_db(filename)

		else:
				return {"Error": "Invalid file or filename"}

	elif request.method == 'GET':
		return "This is /dashboad/::GET"


def insert_dataset_to_db(filename):
	db = get_db()

	exists = db.execute("SELECT dataset_id, dataset_name FROM Dataset WHERE input_csv=?", [filename]).fetchone()

	if exists is not None:
		return jsonify({**dict(exists), **{"Error": "input_csv already exists in database", "filename": filename}})
	
	else:
		count = count_classes(filename)
		print(count)
		in_count, err_count = count['Input'], count['Error']

		counts = [0] * 4
		for key in in_count:
			y = in_count[key]
			try:
				x = err_count[key]
			except KeyError:
				x = 0
			counts[key] = y - x



		print(counts)

		db.execute(
			"INSERT INTO Dataset (dataset_name, input_csv, num_pdbs_class1, num_pdbs_class2, num_pdbs_class3, num_pdbs_class4 ) VALUES (?,?,?,?,?,?)",
			[
				filename, filename, *counts
			]
		)

		db.commit()

		return jsonify(dict(db.execute("SELECT * FROM Dataset WHERE input_csv=?", [filename]).fetchone()))



@bp.route('/datasets', methods=('GET',))
def all_datasets():

	datasets = []
	db = get_db()

	db_res = db.execute(
		'SELECT * FROM Dataset'
	).fetchall()

	for res in db_res:
		datasets.append(dict(res))

	return jsonify(datasets)

# @bp.route('/count_classes/<dataset_name>', methods=('GET',))
def count_classes(dataset_name, error='dummy_error.csv'):

	# counts = {}
	# db = get_db()
	# db_res = db.execute(
	# 	'SELECT input_csv, error_csv FROM Dataset WHERE dataset_name=?', 
	# 	[dataset_name]
	# ).fetchone()

	counts = {}

	try:
		data_in = pd.read_csv(current_app.config['CSV_PATH'] + dataset_name)	
		class_counts_in = data_in.groupby(['CLASS_ID']).size()
		counts['Input'] = {i: c for i, c in enumerate(class_counts_in)}
		counts['Error'] = {}

		try: 
			data_err = pd.read_csv(current_app.config['CSV_PATH'] + error)
			class_counts_out = data_err.groupby(['CLASS_ID']).size()		
			counts['Error'] = {i: c for i, c in enumerate(class_counts_out)}

		except: 
			print("Warning: Error CSV does not exist", dataset_name)			

	except Exception as e:
		print(e)
		return {"Error": "File does not exists", "Path": current_app.config['CSV_PATH'] + dataset_name}

	
	return counts



