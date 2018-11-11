#!/usr/bin/python
# -*- coding: utf-8 -*-

import platform

from flask import Blueprint, jsonify, request
from ray import Reader

from project.api.models import Replay
from project.api.storage import PostgreStorage as db


replay_blueprint = Blueprint('replay', __name__)


@replay_blueprint.route('/replay/parse/', methods=['POST'])
def parse_replay():
    response_object = {
        'status': 'success',
        'container_id': platform.uname()[1]
    }
    if request.method == 'POST':
        f = request.files['data_file']
        username = request.files['username']
        if not f:
            return "No file"

        f.stream.seek(0)
        with Reader(f.stream.read()) as replay:
            response_object['stats'] = replay.stats
            response_object['team_stats'] = replay.team_stats

            db.insert_replay(
                Replay(title="unknown", username=username, stats=stats, team_stats=team_stats))
        response_object['message'] = 'Replay added!'
    return jsonify(response_object)


@replay_blueprint.route('/replays/<username>/', methods=['GET'])
def all_replays_from():
    response_object = {
        'status': 'success',
        'container_id': platform.uname()[1]
    }
    
    replays = [replay.to_json()
                   for replay in db.get_all_replays_from(username)]

    response_object['replays'] = replays
    return jsonify(response_object)

@replay_blueprint.route('/replays/', methods=['GET'])
def all_replays():
    response_object = {
        'status': 'success',
        'container_id': platform.uname()[1]
    }
    
    replays = [replay.to_json() for replay in db.get_all_replays()]

    response_object['replays'] = replays
    return jsonify(response_object)


@replay_blueprint.route('/replay/ping', methods=['GET'])
def ping():
    return jsonify({
        'status': 'success',
        'message': 'pong!',
        'container_id': platform.uname()[1]
    })
