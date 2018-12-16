#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate

from project.json_encoder import AlchemySerializer

    
db = SQLAlchemy()
migrate = Migrate()

def create_app():

    # instantiate the app
    app = Flask(__name__)

    # custom json serializer
    app.json_encoder = AlchemySerializer

    # enable CORS
    CORS(app, resources={r"/*": {"origins": "*"}})

    # set config
    app_settings = os.environ.get('APP_SETTINGS')
    app.config.from_object(f'project.config.{app_settings}')

    # set up extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # register blueprints
    from project.api.replay import replay_blueprint
    app.register_blueprint(replay_blueprint)

    return app

app = create_app()

if __name__ == '__main__':
    app.run()