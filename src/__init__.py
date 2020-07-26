import os, sys
from flask_cors import CORS, cross_origin
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    
    CORS(app)
    jwt = JWTManager(app)

    app.config.from_mapping(
        SECRET_KEY='dev', # replace with random_string(16)
        JWT=jwt,
        DATABASE=os.path.join(app.instance_path, 'capstone.sqlite'),
        CONFIG_PATH=os.path.join(app.instance_path, 'CONFIG/'),
        PDB_PATH=os.path.join(app.instance_path, 'PDB/'),
        TENSOR_PATH=os.path.join(app.instance_path, 'Tensors/'),
        CSV_PATH=os.path.join(app.instance_path, 'CSV/'),
        LOG_PATH=os.path.join(app.instance_path, 'LOG/'),
        MODEL_PATH=os.path.join(app.instance_path, 'MODEL/'),
        ATTR_PATH=os.path.join(app.instance_path, 'ATTRIBUTIONS/')
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
        print("Warning: ", sys.exc_info()[0])

    try:
        os.makedirs(app.config['CONFIG_PATH'])
    except OSError:
        print("Warning: ", sys.exc_info()[0])

    try:
        os.makedirs(app.config['PDB_PATH'])
    except OSError:
        print("Warning: ", sys.exc_info()[0])

    try:
        os.makedirs(app.config['TENSOR_PATH'])
    except OSError:
        print("Warning: ", sys.exc_info()[0])

    try:
        os.makedirs(app.config['CSV_PATH'])
    except OSError:
        print("Warning: ", sys.exc_info()[0])

    try:
        os.makedirs(app.config['LOG_PATH'])
    except OSError:
        print("Warning: ", sys.exc_info()[0])

    try:
        os.makedirs(app.config['MODEL_PATH'])
    except OSError:
        print("Warning: ", sys.exc_info()[0])
        
    try:
        os.makedirs(app.config['ATTR_PATH'])
    except OSError:
        print("Warning: ", sys.exc_info()[0])


    from . import db
    db.init_app(app)

    from .blueprints import auth,dashboard,configs,deep_learn,user
    app.register_blueprint(auth.bp)
    app.register_blueprint(dashboard.bp)
    app.register_blueprint(configs.bp)
    app.register_blueprint(deep_learn.bp)
    app.register_blueprint(user.bp)

    return app
