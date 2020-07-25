from flask import Blueprint, flash, g, current_app, session, url_for, request
from flask import jsonify
from src.db import get_db
from flask_jwt_extended import jwt_required, fresh_jwt_required, get_jwt_identity

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

# @bp.route('/update')
# @fresh_jwt_required
# def update_profile():
# 	db = get_db()
# 	user_id = get_jwt_identity()
# 	exists = db.execute("SELECT * FROM User WHERE user_id=?",[user_id]).fetchone()

# 	if exists is not None:
# 		db.execute(
# 			"",
			
# 		)