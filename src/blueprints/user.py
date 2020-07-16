from flask import Blueprint, flash, g, current_app, session, url_for, request
from flask import jsonify
from src.db import get_db
import json


bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/all')
def all_users():
	users = []
	db = get_db()

	db_res = db.execute(
		("SELECT * FROM User")
	).fetchall()

	for res in db_res:
		users.append(dict(res))

	return jsonify(users)