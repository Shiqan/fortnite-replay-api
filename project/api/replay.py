#!/usr/bin/python
# -*- coding: utf-8 -*-

import platform

from flask import Blueprint, jsonify, request
from ray import Reader

from project.api.logging import logger
from project.api.models import Filter, Replay
from project.api.storage import Storage as db

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
                    Replay(title='unknown', username=username, stats=replay.stats, team_stats=replay.team_stats, eliminations=[i for i in replay.eliminations if i.eliminator == username and not i.knocked]))
        response_object['message'] = 'Successfully uploaded replays!'
        response_object['uploaded'] = len(files)
    return jsonify(response_object)


@replay_blueprint.route('/replay/<username>/', methods=['GET'])
def player_exists(username):
    logger.info(f'player_exists({username})')
    response_object = {
        'status': 'success',
        'container_id': platform.uname()[1]
    }

    if not username:
        response_object['message'] = 'No username provided!'
        response_object['status'] = 'failed'
        response_object['exists'] = False
    else:
        response_object['exists'] = db.player_exists(username)

    return jsonify(response_object)


@replay_blueprint.route('/replay/', methods=['POST'])
def all_replays_from():
    username = request.form.get('username', None)
    start = request.form.get('start', 1)
    length = request.form.get('length', 10)
    search = request.form.get('search', '')
    startdate = request.form.get('startdate', None)
    enddate = request.form.get('enddate', None)
    min_position, max_position = request.form.get(
        'position', '0,100').split(',')
    min_kills, max_kills = request.form.get('kills', '0,100').split(',')
    win = request.form.get('win', False)

    if not username:
        response_object['message'] = 'No username provided!'
        response_object['status'] = 'failed'
    else:
        search_filter = Filter(username=username, search=search, start=int(start), length=int(length), win=win,
                               startdate=startdate, enddate=enddate, min_position=int(float(min_position)), max_position=int(float(max_position)),
                               min_kills=int(float(min_kills)), max_kills=int(float(max_kills)))

        logger.info(f'all_replays_from() - {username}')
        response_object = {
            'status': 'success',
            'container_id': platform.uname()[1]
        }

        result = db.get_all_replays_from(search_filter)
        response_object['total'] = result.total
        response_object['pages'] = result.pages
        response_object['next'] = result.has_next
        response_object['prev'] = result.has_prev
        response_object['replays'] = result.items
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
