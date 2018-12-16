#!/usr/bin/python
# -*- coding: utf-8 -*-

import platform

from flask import Blueprint, jsonify, request
from ray import Reader

from project.api.models import Replay
from project.api.storage import Storage as db
from project.api.logging import logger


replay_blueprint = Blueprint('replay', __name__)


@replay_blueprint.route('/replay/upload/', methods=['POST'])
def parse_replay():
    logger.info('parse_replay()')
    response_object = {
        'status': 'success',
        'container_id': platform.uname()[1]
    }

    username = request.form.get('username', None)
    files = request.files.getlist('data_file')
    if not files or not username:
        response_object['message'] = 'Invalid request!'
        response_object['status'] = 'failed'
    else:
        for f in files:
            f.stream.seek(0)
            with Reader(f.stream.read()) as replay:
                db.insert_replay(
                    Replay(title="unknown", username=username, stats=replay.stats, team_stats=replay.team_stats, eliminations=[i for i in replay.eliminations if i.eliminator == username and not i.knocked]))
        response_object['message'] = 'Successfully uploaded replays!'
        response_object['uploaded'] = len(files)
    return jsonify(response_object)


@replay_blueprint.route('/replay/<username>/', methods=['GET'])
def all_replays_from(username):
    if not username:
        response_object['message'] = 'No username provided!'
        response_object['status'] = 'failed'
    else:
        logger.info(f'all_replays_from({username})')
        response_object = {
            'status': 'success',
            'container_id': platform.uname()[1]
        }

        replays = [replay for replay in db.get_all_replays_from(username)]

        response_object['replays'] = replays
    return jsonify(response_object)


@replay_blueprint.route('/replays/', methods=['GET'])
def all_replays():
    logger.info('all_replays()')
    response_object = {
        'status': 'success',
        'container_id': platform.uname()[1]
    }

    replays = [replay.to_json() for replay in db.get_all_replays()]

    response_object['replays'] = replays
    return jsonify(response_object)


@replay_blueprint.route('/ping/', methods=['GET'])
def ping():
    return jsonify({
        'status': 'success',
        'message': 'pong!',
        'container_id': platform.uname()[1]
    })
