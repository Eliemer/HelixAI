from flask import Blueprint, flash, g, request, session, url_for
from flask import current_app, jsonify
from werkzeug.utils import secure_filename
from flask_jwt_extended import jwt_required, fresh_jwt_required, get_jwt_claims

from src.db import get_db

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
def upload_file(current_user):
	if request.method == 'POST':
		# check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return {"Error": "No file in form"}
		file = request.files['file']
		# if user does not select file, browser also
		# submit an empty part without filename

		if file.filename == '':
			flash('No selected file')
			return {"Error": "No selected file"}
		if file and allowed_file(file.filename):
				filename = secure_filename(file.filename)

				if not os.path.exists(os.path.join(current_app.config['CSV_PATH'], filename)) or request.form['replace']=="true":
					file.save(os.path.join(current_app.config['CSV_PATH'], filename))
				else:
					return {"Error": "input_csv already exists in filesystem", "filename": filename}

				return insert_dataset_to_db(filename, request.form['dataset_name'])

		else:
				return {"Error": "Invalid file or filename"}

	elif request.method == 'GET':
		return "This is /dashboad/::GET"


def insert_dataset_to_db(filename, dataset_name=None):
	db = get_db()

	if dataset_name is not None:
		exists = db.execute("SELECT dataset_id, dataset_name FROM Dataset WHERE input_csv=?", [filename]).fetchone()

		if exists is not None:


			flash("Dataset already exists")
			return jsonify({**dict(exists), **{"Error": "input_csv already exists in database", "filename": filename}})
		

		else:
			db.execute(
				"INSERT INTO Dataset (dataset_name, input_csv) VALUES (?,?)",
				[dataset_name, filename]
			)

			db.commit()

			return jsonify(dict(db.execute("SELECT dataset_id, dataset_name FROM Dataset WHERE input_csv=?", [filename]).fetchone()))



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

@bp.route('/count_classes/<dataset_name>', methods=('GET',))
def count_classes(dataset_name):

	counts = {}
	db = get_db()
	db_res = db.execute(
		'SELECT input_csv, error_csv FROM Dataset WHERE dataset_name=?', 
		[dataset_name]
	).fetchone()
	try:
		data_in = pd.read_csv(current_app.config['CSV_PATH'] + db_res[0])	
		class_counts_in = data_in.groupby(['CLASS_ID']).size()
		counts['Input'] = {f"class{i}": c for i, c in enumerate(class_counts_in)}
		counts['Error'] = {}

		try: 
			data_err = pd.read_csv(current_app.config['CSV_PATH'] + db_res[1])
			class_counts_out = data_err.groupby(['CLASS_ID']).size()		
			counts['Error'] = {f"class{i}": c for i, c in enumerate(class_counts_out)}

		except: 
			print("Warning: Error CSV does not exist", db_res[1])			

	except:
		return {"Error": "File does not exists", "Path": current_app.config['CSV_PATH'] + db_res[0]}

	
	return jsonify(counts)



