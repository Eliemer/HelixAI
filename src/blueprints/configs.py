from flask import Blueprint, flash, g, current_app, session, url_for, request
from flask import jsonify
from src.db import get_db
from werkzeug.utils import secure_filename
import json
import functools
import os
import tempfile

bp = Blueprint('configs', __name__, url_prefix='/configs')
# CONFIG_PATH = './pytorch_lightning_src/Configs'


# @bp.route('/', methods=('POST',))
# def create_new_config():
#     if request.method == 'POST':
#         config = request.form['parameters']
#         config_name = request.form['config_name']
#         path = current_app.config['CONFIG_PATH'] 
#         # validate config_name

#         config_name = path + secure_filename(config_name)

#         db = get_db()
#         error = None

#         try:
#             with tempfile.NamedTemporaryFile(dir=CONFIG_PATH, delete=False) as fp:
#                 json.dump(config, fp)

#             os.replace(fp.name, config_name)
#         except OSError:
#             print("Error: Writing Temporary File", config_name)


#         return 




@bp.route('/all', methods=('GET',))
def display_all_config_files():
    '''
    '''
    if request.method == 'GET':
        configs = []
        db = get_db()

        db_res = db.execute("SELECT * FROM ConfigFile").fetchall()


        for res in db_res:
            configs.append(dict(res))

        return jsonify(configs)

@bp.route('/user/<user_id>', methods=('GET',))
def display_user_config_files(user_id):
    if request.method == 'GET':
        configs = []

        ### make sql query for all config files associated with user_id ###
        db = get_db()
        db_res = db.execute(
            'SELECT Trains.config_id, config_path FROM Trains INNER JOIN ConfigFile ON ConfigFile.config_id = Trains.config_id WHERE user_id = ?', (user_id,)
        )

        for res in db_res:
            configs.append(dict(res))

        return jsonify(configs)

@bp.route('/by_config_id/<config_id>')
def search_by_config_id(config_id):
    db = get_db()

    db_res = db.execute("SELECT * FROM ConfigFile WHERE config_id=?", config_id).fetchone()

    return jsonify(dict(db_res))

@bp.route('/by_config_name/<config_path>')
def search_by_config_path(config_path):
    db = get_db()

    db_res = db.execute("SELECT * FROM ConfigFile WHERE config_path=(?)", [config_path]).fetchone()

    return jsonify(dict(db_res))

@bp.route('/order_by_dataset')
def all_configs_by_dataset():
    configs = []

    db = get_db()
    db_res = db.execute(
        ("SELECT ConfigFile.config_path, ConfigFile.config_id, Dataset.dataset_name, Dataset.dataset_id "
        "FROM ConfigFile INNER JOIN DatasetConfig ON ConfigFile.config_id=DatasetConfig.config_id "
        "INNER JOIN Dataset ON DatasetConfig.dataset_id=Dataset.dataset_id "
        "ORDER BY Dataset.dataset_id"
        )
    )

    for res in db_res:
        configs.append(dict(res))

    return jsonify(configs)



