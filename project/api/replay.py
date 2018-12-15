#!/usr/bin/python
# -*- coding: utf-8 -*-

import platform

from flask import Blueprint, jsonify, request
from ray import Reader

from project.api.models import Replay
from project.api.storage import Storage as db
from project.api.logging import logger


replay_blueprint = Blueprint('replay', __name__)


@replay_blueprint.route('/upload/', methods=['POST'])
def parse_replay():
    logger.info('parse_replay()')
    response_object = {
        'status': 'success',
        'container_id': platform.uname()[1]
    }
    
    f = request.files['data_file']
    username = request.form.get('username', None)
    if not f:
        response_object['message'] = 'No file found!'
        response_object['status'] = 'failed'
    else:
        f.stream.seek(0)
        with Reader(f.stream.read()) as replay:
            response_object['stats'] = replay.stats
            response_object['team_stats'] = replay.team_stats

            db.insert_replay(
                Replay(title="unknown", username=username, stats=replay.stats, team_stats=replay.team_stats, eliminations=[i for i in replay.eliminations if i.eliminator == username and not i.knocked]))
        response_object['message'] = 'Replay added!'
    logger.debug(response_object)
    return jsonify(response_object)


@replay_blueprint.route('/replay/<username>/', methods=['GET'])
def all_replays_from(username):
    logger.info(f'all_replays_from({username})')
    response_object = {
        'status': 'success',
        'container_id': platform.uname()[1]
    }
    
    replays = [replay for replay in db.get_all_replays_from(username)]

    response_object['replays'] = replays
    return jsonify(response_object)

@replay_blueprint.route('/replays/all/', methods=['GET'])
def all_replays():
    logger.info('all_replays()')
    response_object = {
        'status': 'success',
        'container_id': platform.uname()[1]
    }
    
    replays = [replay.to_json() for replay in db.get_all_replays()]

    response_object['replays'] = replays
    return jsonify(response_object)


@replay_blueprint.route('/replays/ping/', methods=['GET'])
def ping():
    return jsonify({
        'status': 'success',
        'message': 'pong!',
        'container_id': platform.uname()[1]
    })
