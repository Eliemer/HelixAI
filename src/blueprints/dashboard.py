from flask import Blueprint, flash, g, redirect, render_template, session, url_for
# from src.blueprints.auth import login_required
from src.db import get_db
import functools
import json
import pandas as pd


ALLOWED_EXTENSIONS = {'csv'}

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

# def allowed_file(filename):


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)
    return wrapped_view


@bp.route('/index')
@login_required
def index():
    return 

@bp.route('/new', methods=('GET', 'POST'))
def new_dataset():


@bp.route('/datasets', methods=('GET',))
def all_datasets():

	datasets = {}
	db = get_db()

	db_res = db.execute(
		'SELECT * FROM Dataset'
	).fetchall()

	for i, res in enumerate(db_res):
		datasets[i] = tuple(res)

	return datasets

@bp.route('/count_classes/<dataset_name>', methods=('GET',))
def count_classes(dataset_name):

	db = get_db()
	db_res = db.execute(
		'SELECT input_csv, error_csv FROM Dataset WHERE dataset_name=?', 
		[dataset_name]
	).fetchone()

	data_in = pd.read_csv(db_res[0])
	data_err = pd.read_csv(db_res[1])

	class_counts_in = data_in.groupby(['CLASS_ID']).size()
	class_counts_out = data_err.groupby(['CLASS_ID']).size()


	return json.dumps({'Input': {i: c for i, c in enumerate(class_counts_in)}, 'Error': {i: c for i, c in enumerate(class_counts_out)}})