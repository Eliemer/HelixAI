import functools

from flask import Blueprint, flash, g, redirect, render_template, request
from flask import session, url_for, current_app, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from src.db import get_db

import jwt
from datetime import datetime, timedelta

bp = Blueprint('auth', __name__, url_prefix='/auth')


# ../auth/register/
# Used to create new users
@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
            'SELECT login_id FROM Login WHERE user_name = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            db.execute(
                'INSERT INTO Login (user_name, password) VALUES (?, ?, ?)',
                (username, generate_password_hash(password), False)
            )
            db.commit()
            return jsonify(dict(db.execute('SELECT login_id, user_name FROM Login WHERE user_name=?', [username]).fetchone()))
        else:
            return jsonify({"Error": error})


    return 

@bp.route('/login', methods=('POST',))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']


        if not username:
            return jsonify({"Error": "Empty username field"}), 401

        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM Login WHERE user_name = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            token = jwt.encode({
                'sub': username,
                'iat': datetime.utcnow(),
                'exp': datetime.utcnow() + timedelta(minutes=30)},
                current_app.config['SECRET_KEY']
                )

            return jsonify({"access_token": token.decode('UTF-8')})
        else:
            return jsonify({"Error": error, "authenticated": False}), 401        


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None

    else:
        g.user = get_db().execute(
            	'SELECT * FROM User WHERE id = ?', (user_id, )
        ).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def _verify(*args, **kwargs):
        auth_headers = request.headers.get('Authorization', '').split()

        invalid = {
            'Error': 'invalid token.',
            'authenticated': False
        }

        expired = {
            'Error': 'expired token.',
            'authenticated': False
        }

        if len(auth_headers) != 2:
            return jsonify(invalid), 401

        try:
            db = get_db()

            token = auth_headers[1]
            data = jwt.decode(token, current_app.config['SECRET_KEY'])

            print(data['sub'], type(data['sub']))

            user = dict(db.execute(
                "SELECT login_id, user_name FROM Login WHERE user_name=(?)", [data['sub']]
                ).fetchone())

            if not user:
                raise RunTimeError("User not found")
            return view(user, *args, **kwargs)

        except jwt.ExpiredSignatureError:
            return jsonify(expired), 401

        except (jwt.InvalidTokenError):
            return jsonify(invalid), 401

    return _verify
