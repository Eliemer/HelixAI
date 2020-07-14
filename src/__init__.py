import os, sys
from flask_cors import CORS, cross_origin
from flask import Flask, jsonify


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'capstone.sqlite'),
        CONFIG_PATH=os.path.join(app.instance_path, 'configuration_files/'),
        PDB_PATH=os.path.join(app.instance_path, 'PDB/'),
        TENSOR_PATH=os.path.join(app.instance_path, 'Tensors/'),
        CSV_PATH=os.path.join(app.instance_path, 'CSV/')
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        print("Error: ", sys.exc_info()[0])

    try:
        os.makedirs(app.config['PDB_PATH'])
    except OSError:
        print("Error: ", sys.exc_info()[0])

    try:
        os.makedirs(app.config['TENSOR_PATH'])
    except OSError:
        print("Error: ", sys.exc_info()[0])

    try:
        os.makedirs(app.config['CSV_PATH'])
    except OSError:
        print("Error: ", sys.exc_info()[0])

        
    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    @app.route('/index')
    def index():
        return 'This is the index'

    # @app.route('/base_config')
    # def base_config():
    #     import json
    #     data = json.load(open('tests/configs/base_config.json', 'r'))
    #     return jsonify(data)

    from . import db
    db.init_app(app)

    from .blueprints import auth, dashboard, configs, deep_learn
    app.register_blueprint(auth.bp)
    app.register_blueprint(dashboard.bp)
    app.register_blueprint(configs.bp)
    app.register_blueprint(deep_learn.bp)

    return app
