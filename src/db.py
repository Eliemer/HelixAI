'''
This file is in charge of defining the db object and config.
Queries are in /blueprints
This file defines init, close, and get functions
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

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    print("Initializing")

    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

    ### Populate DB
    # comment out for production

    print("Populating")

    import random, string

    def random_string(length):
        letters_and_digits = string.ascii_letters + string.digits
        return ''.join((random.choice(letters_and_digits) for i in range(length)))


    # Login Table
    data = [(i, random_string(10), random_string(10)) for i in range(25)]
    db.executemany('INSERT INTO Login VALUES (?,?,?)', data)

    # Users Table
    data = [(i, random_string(10), random_string(10), random_string(10), random_string(10), random_string(10), random_string(10), random_string(10), i) for i in range(25)]
    db.executemany('INSERT INTO User VALUES (?,?,?,?,?,?,?,?,?)', data)

    # ConfigFile
    data = [(i, random_string(10)+'.json') for i in range(25)]
    db.executemany('INSERT INTO ConfigFile VALUES (?,?)', data)

    # Dataset
    data = [(i, random_string(10), random.randint(1,1000), random.randint(1,1000), random.randint(1,1000), random.randint(1,1000), random_string(10)+'.csv', random_string(10)+'.csv') for i in range(35)]
    data.append([len(data), 'my_dataset', 0, 0, 0, 0, 'test_input.csv', 'test_error.csv'])
    db.executemany('INSERT INTO Dataset VALUES (?,?,?,?,?,?,?,?)', data)

    # Model
    data = [(i, random_string(10), random.random(), random.uniform(0,0.010)) for i in range(40)]
    db.executemany('INSERT INTO Model VALUES (?,?,?,?)', data)

    # Pdbs
    # Attributions

    # Trains
    data = [(random.randint(0, 24), random.randint(0,24)) for _ in range(75)]
    data = list(set(data)) # removes duplicates
    db.executemany('INSERT INTO Trains VALUES (?,?)', data)

    # Interpret
    data = [(random.randint(0, 24), random.randint(0,39)) for _ in range(75)]
    data = list(set(data))
    db.executemany('INSERT INTO Interpret VALUES (?,?)', data)

    # DatasetConfig
    data = [(random.randint(0,24), random.randint(0,35)) for _ in range(45)]
    data = list(set(data))
    db.executemany('INSERT INTO DatasetConfig VALUES (?,?)', data)

    db.commit()
    print("Finished")

@click.command('init_db')
@with_appcontext
def init_db_command():
    '''Clear the existing data and create new tables.'''
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
