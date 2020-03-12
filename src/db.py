'''
This file will be in charge of all necessary CRUD operations and input validation
required by the app. Anything related to the Database goes here.
'''

import sqlite3
import click

from flask import current_app, g
from flask.cli import with_appcontext

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )

        g.db.row_factory = sqlite3.Row

    return g.db

def close_db():
    db = g.pop('db', None)

    if db is not None:
        db.close()
