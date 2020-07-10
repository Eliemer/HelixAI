from flask import Blueprint, flash, g, session, url_for
# from src.blueprints.auth import login_required
from src.db import get_db
import functools
import os

bp = Blueprint('configs', __name__, url_prefix='/config')

@bp.route('/by_config_id/<config_id>'):

@bp.route('/all')
def display_all_config_files():
    '''
    '''

    ### CORRECT ###
    configs = {}
    db = get_db()

    db_res = db.execute("SELECT * FROM ConfigFile").fetchall()

    for i, res in enumerate(db_res):
        configs[i] = tuple(res)[-1]

    return configs

@bp.route('/user/<user_id>')
def display_user_config_files(user_id):
    configs = {}

    ### make sql query for all config files associated with user_id ###
    db = get_db()
    db_res = db.execute(
        'SELECT * FROM Trains INNER JOIN ConfigFile ON ConfigFile.config_id = Trains.config_id WHERE user_id = ?', (user_id,)
    )

    for res in db_res:
        configs[len(configs)] = tuple(res)

    return configs
