from flask import Blueprint, flash, g, current_app, session, url_for, request
from flask import jsonify
from src.db import get_db
from werkzeug.utils import secure_filename

from flask_jwt_extended import jwt_required, fresh_jwt_required, get_jwt_identity

import json
import functools
import os
import tempfile

bp = Blueprint('configs', __name__, url_prefix='/configs')
ALLOWED_EXTENSIONS = {'json'}

# CONFIG_PATH = './pytorch_lightning_src/Configs'

def allowed_file(filename):
    if '.' in filename:
        if filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
            return True
    return False


@bp.route('/', methods=('POST',))
@fresh_jwt_required
def create_new_config():
    if request.method == 'POST':
        if 'file' not in request.files:
            return new_conf_from_json(request)

        file = request.files['file']

        if file.filename == '':
            return {"Error": "No selected file"}

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            if not os.path.exists(os.path.join(current_app.config['CONFIG_PATH'], filename)):
                file.save(os.path.join(current_app.config['CONFIG_PATH'], filename))

            return insert_conf_to_db(filename)

        else:
            return {"Error": "Invalid file or filename"}

    elif request.method == 'GET':
        return "This is /configs/::GET"

def new_conf_from_json(request):
    config = request.get_json()
    filename = config['name'] + '.json'
    with open(os.path.join(current_app.config['CONFIG_PATH'],filename), 'w') as fp:
        json.dump(config, fp)

    return insert_conf_to_db(filename)


def insert_conf_to_db(filename):
    db = get_db()

    exists = db.execute("SELECT config_id, config_path FROM ConfigFile WHERE config_path=?", [filename]).fetchone()

    if exists is not None:
        return jsonify({**dict(exists), **{"Error": "Config file already exists in database", "filename": filename}})

    else:
        db.execute(
            "INSERT INTO ConfigFile (config_path) VALUES (?)",
            [filename]

        )

        db.commit()

        ### Missing insert in all relations



        return jsonify(dict(
            db.execute(
                    "SELECT * FROM ConfigFile WHERE config_path=?",
                    [filename]
                ).fetchone()))


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

@bp.route('/user', methods=('GET',))
@jwt_required
def display_user_config_files():
    if request.method == 'GET':

        user_id = get_jwt_identity()

        configs = []

        ### make sql query for all config files associated with user_id ###
        db = get_db()
        db_res = db.execute(
            'SELECT Trains.config_id, config_path FROM Trains INNER JOIN ConfigFile ON ConfigFile.config_id = Trains.config_id WHERE user_id = ?', [user_id]
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



